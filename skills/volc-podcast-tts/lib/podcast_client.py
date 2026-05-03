"""同步 WebSocket 客户端：播客 TTS v3 → 拼接 PCM / 可选写 WAV。"""

from __future__ import annotations

import re
import time
import uuid
import wave
from typing import Any

_DIALOGUE_LINE_RE = re.compile(r"^(女|男)[:：]\s*(.+)$")

from podcast_protocol import (
    EVT_CONNECTION_FINISHED,
    EVT_CONNECTION_STARTED,
    EVT_PODCAST_END,
    EVT_PODCAST_ROUND_END,
    EVT_PODCAST_ROUND_RESPONSE,
    EVT_PODCAST_ROUND_START,
    EVT_SESSION_FINISHED,
    EVT_SESSION_STARTED,
    EVT_USAGE,
    MSG_ERROR,
    pack_finish_connection,
    pack_finish_session,
    pack_start_connection,
    pack_start_session,
    parse_one_message,
)

try:
    import websocket  # websocket-client
    from websocket._exceptions import (
        WebSocketConnectionClosedException,
        WebSocketTimeoutException,
    )
except ImportError as e:
    raise ImportError(
        "需要 websocket-client：pip install -r requirements.txt"
    ) from e


WS_URL = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"
DEFAULT_APP_KEY = "aGjiRDfUWi"
DEFAULT_RESOURCE_ID = "volc.service_type.10050"

_OK_STATUS = 20000000


def _recv_deadline_timeout(recv_idle_sec: float, deadline: float) -> float:
    """单次 recv 超时：同时满足空闲阈值与全局 deadline（避免永久卡在 recv）。"""
    rem = deadline - time.monotonic()
    if rem <= 0:
        return 0.001
    if recv_idle_sec <= 0:
        return rem
    return float(min(recv_idle_sec, rem))


def _meta_audio_url(meta: dict[str, Any]) -> str | None:
    pe = meta.get("podcast_end")
    if not isinstance(pe, dict):
        return None
    mi = pe.get("meta_info")
    if not isinstance(mi, dict):
        return None
    url = mi.get("audio_url")
    return url if isinstance(url, str) and url.strip() else None


def _payload_api_error(payload: Any) -> str | None:
    """JSON 业务错误（非 ERROR 帧）常见字段。"""
    if not isinstance(payload, dict):
        return None
    if "status_code" not in payload:
        return None
    try:
        code = int(payload["status_code"])
    except (TypeError, ValueError):
        return None
    if code == _OK_STATUS:
        return None
    msg = payload.get("message", payload.get("msg", ""))
    return f"status_code={code} message={msg!r}"


def _headers_legacy(app_id: str, access_key: str, resource_id: str, app_key: str) -> list[str]:
    rid = str(uuid.uuid4())
    return [
        f"X-Api-App-Id: {app_id}",
        f"X-Api-Access-Key: {access_key}",
        f"X-Api-Resource-Id: {resource_id}",
        f"X-Api-App-Key: {app_key}",
        f"X-Api-Request-Id: {rid}",
    ]


def _headers_api_key(api_key: str, resource_id: str, app_key: str) -> list[str]:
    """新版控制台：仅需 API Key（见豆包语音 V3 文档 X-Api-Key）。"""
    rid = str(uuid.uuid4())
    return [
        f"X-Api-Key: {api_key}",
        f"X-Api-Resource-Id: {resource_id}",
        f"X-Api-App-Key: {app_key}",
        f"X-Api-Request-Id: {rid}",
    ]


def synthesize_podcast(
    *,
    app_id: str = "",
    access_key: str = "",
    api_key: str = "",
    podcast_body: dict[str, Any],
    resource_id: str = DEFAULT_RESOURCE_ID,
    app_key: str = DEFAULT_APP_KEY,
    timeout_sec: int = 600,
    verbose: bool = False,
    recv_idle_sec: float = 75.0,
    max_stream_sec: float | None = None,
    finish_phase_sec: float = 90.0,
    connect_handshake_sec: float = 45.0,
    inter_speaker_silence_ms: int = 0,
) -> tuple[bytes, dict[str, Any]]:
    """建立连接 → StartSession → 收流 → FinishSession → FinishConnection。

    鉴权二选一：`api_key`（新版控制台复制的 API Key）或 `app_id` + `access_key`（旧版）。
    返回 (pcm_bytes, meta)，meta 含 usage、podcast_end、round_end、completed_via 等。

    健壮性：`max_stream_sec` 为整段合成 recv 阶段墙钟上限（默认等于 timeout_sec）；
    每次 recv 超时取 min(recv_idle_sec, 剩余墙钟)，避免单独依赖服务端 363（文档写明可不返回）。
    """
    session_id = str(uuid.uuid4())
    stream_limit = float(max_stream_sec if max_stream_sec is not None else timeout_sec)
    meta: dict[str, Any] = {
        "session_id": session_id,
        "usage_events": [],
        "podcast_end": None,
        "round_starts": [],
        "round_ends": [],
        "errors": [],
        "warnings": [],
        "completed_via": None,
    }

    # action=3：每句对白一轮；363 可不返回，以 RoundEnd 条数对齐 nlp_texts。
    nlp = podcast_body.get("nlp_texts")
    expected_round_ends: int | None = None
    if isinstance(nlp, list) and len(nlp) > 0:
        expected_round_ends = len(nlp)

    aparam = podcast_body.get("audio_params") or {}
    sample_rate_i = int(aparam.get("sample_rate") or 24000)
    meta["sample_rate"] = sample_rate_i
    meta["inter_speaker_silence_ms"] = max(0, int(inter_speaker_silence_ms))
    si = podcast_body.get("speaker_info") or {}
    if isinstance(si, dict):
        meta["speaker_random_order"] = si.get("random_order")

    ak = (api_key or "").strip()
    if ak:
        if verbose:
            print("auth=api_key (X-Api-Key + Resource-Id + App-Key)")
        hdr = _headers_api_key(ak, resource_id, app_key)
    else:
        if not (app_id or "").strip() or not (access_key or "").strip():
            raise ValueError("需要 api_key，或同时提供 app_id 与 access_key")
        if verbose:
            print("auth=legacy (X-Api-App-Id + X-Api-Access-Key + …)")
        hdr = _headers_legacy(app_id.strip(), access_key.strip(), resource_id, app_key)

    ws = websocket.WebSocket()
    ws.connect(
        WS_URL,
        header=hdr,
        timeout=timeout_sec,
    )

    pcm_parts: list[bytes] = []
    _recv_timeout_prev = ws.gettimeout()
    prev_round_speaker: str | None = None
    current_round_speaker: str | None = None
    inter_ms = max(0, int(inter_speaker_silence_ms))

    def send_raw(msg: bytes) -> None:
        ws.send_binary(msg)

    def drain_phase(
        *,
        phase: str,
        deadline: float,
        stop_events: set[int],
        stop_on_conn_finished: bool = False,
        soft_close: bool = False,
    ) -> None:
        while True:
            ws.settimeout(max(0.001, deadline - time.monotonic()))
            if ws.gettimeout() <= 0.002:
                meta["warnings"].append(f"{phase}_wall_timeout")
                if verbose:
                    print(f"<< {phase}: deadline exceeded")
                break
            try:
                raw = ws.recv()
            except WebSocketTimeoutException:
                meta["warnings"].append(f"{phase}_recv_timeout")
                if verbose:
                    print(f"<< {phase}: recv timeout")
                break
            except WebSocketConnectionClosedException as e:
                if soft_close:
                    meta["warnings"].append(f"{phase}_ws_closed:{e!s}")
                    if verbose:
                        print(f"<< {phase}: connection closed (ignored)")
                    break
                meta["errors"].append({"phase": phase, "type": "closed", "msg": str(e)})
                raise RuntimeError(f"WebSocket 在 {phase} 阶段被关闭") from e
            if not isinstance(raw, bytes):
                continue
            try:
                ev, _sid, payload, msg_type = parse_one_message(raw)
            except ValueError as e:
                meta["warnings"].append(f"{phase}_bad_frame:{e!s}")
                continue
            if msg_type == MSG_ERROR:
                meta["errors"].append({"phase": phase, "payload": payload})
                raise RuntimeError(f"服务端 ERROR 帧: {payload!r}")
            if verbose:
                print(f"<< {phase} event={ev}")
            if ev in stop_events:
                break
            if stop_on_conn_finished and ev == EVT_CONNECTION_FINISHED:
                break

    try:
        send_raw(pack_start_connection())
        hs_deadline = time.monotonic() + min(float(connect_handshake_sec), float(timeout_sec))
        while True:
            ws.settimeout(_recv_deadline_timeout(12.0, hs_deadline))
            try:
                raw = ws.recv()
            except WebSocketTimeoutException:
                raise RuntimeError(
                    f"连接握手超时（>{connect_handshake_sec}s 未收到 ConnectionStarted）"
                ) from None
            except WebSocketConnectionClosedException as e:
                raise RuntimeError(f"连接握手阶段 WebSocket 已关闭: {e}") from e
            if not isinstance(raw, bytes):
                raise RuntimeError(f"unexpected websocket frame type: {type(raw)}")
            try:
                ev, sid, payload, msg_type = parse_one_message(raw)
            except ValueError as e:
                raise RuntimeError(f"握手帧解析失败: {e}") from e
            if msg_type == MSG_ERROR:
                raise RuntimeError(f"握手 ERROR 帧: {payload!r}")
            if verbose:
                print(f"<< event={ev} session={sid[:8]}… payload_type={type(payload).__name__}")
            err = _payload_api_error(payload)
            if err and ev != EVT_USAGE:
                raise RuntimeError(f"握手业务错误: {err}")
            if ev == EVT_CONNECTION_STARTED:
                break
            if ev == EVT_CONNECTION_FINISHED:
                raise RuntimeError("connection finished before start")

        send_raw(pack_start_session(session_id, podcast_body))

        stream_deadline = time.monotonic() + stream_limit

        while True:
            ws.settimeout(_recv_deadline_timeout(recv_idle_sec, stream_deadline))
            if ws.gettimeout() <= 0.002:
                meta["completed_via"] = "wall_clock"
                if verbose:
                    print(f"<< stream wall_clock limit {stream_limit}s, finishing session")
                break
            try:
                raw = ws.recv()
            except WebSocketTimeoutException:
                if pcm_parts:
                    meta["completed_via"] = "recv_idle"
                    if verbose:
                        print(
                            f"<< recv idle (bounded), closing session with "
                            f"{len(pcm_parts)} pcm chunks"
                        )
                    break
                meta["completed_via"] = "recv_idle_empty"
                raise RuntimeError(
                    "recv 超时且尚无音频：检查鉴权、action、资源开通或增大 "
                    "--recv-idle-sec / --max-stream-sec"
                ) from None
            except WebSocketConnectionClosedException as e:
                meta["errors"].append({"phase": "stream", "type": "closed", "msg": str(e)})
                raise RuntimeError("合成中途 WebSocket 连接关闭（未完成收尾）") from e

            if not isinstance(raw, bytes):
                continue
            try:
                ev, _sid, payload, msg_type = parse_one_message(raw)
            except ValueError as e:
                meta.setdefault("unknown_events", []).append({"parse_error": str(e)})
                continue

            if msg_type == MSG_ERROR:
                meta["errors"].append({"phase": "stream", "payload": payload})
                raise RuntimeError(f"合成 ERROR 帧: {payload!r}")

            if verbose:
                pt = len(payload) if isinstance(payload, bytes) else payload
                print(f"<< event={ev} payload={pt}")

            if ev == EVT_SESSION_STARTED:
                continue
            if ev == EVT_USAGE:
                if isinstance(payload, dict):
                    meta["usage_events"].append(payload)
                continue
            if ev == EVT_PODCAST_ROUND_START:
                if isinstance(payload, dict):
                    meta["round_starts"].append(payload)
                    sp = payload.get("speaker")
                    if (
                        isinstance(sp, str)
                        and inter_ms > 0
                        and prev_round_speaker is not None
                        and sp != prev_round_speaker
                    ):
                        nbytes = int(sample_rate_i * 2 * (inter_ms / 1000.0))
                        if nbytes > 0:
                            pcm_parts.append(b"\x00" * nbytes)
                            meta["inter_speaker_padding_bytes"] = (
                                meta.get("inter_speaker_padding_bytes", 0) + nbytes
                            )
                            if verbose:
                                print(
                                    f"<< inter-speaker silence {inter_ms}ms "
                                    f"({nbytes} pcm bytes)"
                                )
                    current_round_speaker = sp if isinstance(sp, str) else None
                continue
            if ev == EVT_PODCAST_ROUND_RESPONSE:
                if isinstance(payload, (bytes, bytearray)):
                    pcm_parts.append(bytes(payload))
                continue
            if ev == EVT_PODCAST_ROUND_END:
                if isinstance(payload, dict):
                    meta["round_ends"].append(payload)
                    if current_round_speaker is not None:
                        prev_round_speaker = current_round_speaker
                    if (
                        expected_round_ends is not None
                        and len(meta["round_ends"]) >= expected_round_ends
                    ):
                        meta["completed_via"] = "nlp_round_ends"
                        if verbose:
                            print(
                                f"<< nlp_texts done ({len(meta['round_ends'])} round_end), "
                                "finishing session"
                            )
                        break
                continue
            if ev == EVT_PODCAST_END:
                if isinstance(payload, dict):
                    meta["podcast_end"] = payload
                meta["completed_via"] = "podcast_end"
                break
            if ev == EVT_SESSION_FINISHED:
                meta["completed_via"] = "session_finished_downlink"
                break

            api_err = _payload_api_error(payload)
            if api_err:
                raise RuntimeError(f"下行业务错误 (event={ev}): {api_err}")

            meta.setdefault("unknown_events", []).append(
                {"event": ev, "payload_type": str(type(payload))}
            )

        if expected_round_ends is not None:
            got = len(meta["round_ends"])
            if got < expected_round_ends:
                via = meta.get("completed_via") or ""
                if via in ("wall_clock", "recv_idle", "recv_idle_empty"):
                    raise RuntimeError(
                        f"对白未完成：收到 {got}/{expected_round_ends} 次 RoundEnd"
                        f"（completed_via={via}）。增大 --max-stream-sec 或检查网络。"
                    )
                meta["warnings"].append(
                    f"partial_round_ends:{got}/{expected_round_ends}:via={via}"
                )

        fs_deadline = time.monotonic() + finish_phase_sec
        send_raw(pack_finish_session(session_id))
        drain_phase(
            phase="finish_session",
            deadline=fs_deadline,
            stop_events={EVT_SESSION_FINISHED},
        )

        fc_deadline = time.monotonic() + finish_phase_sec
        send_raw(pack_finish_connection())
        drain_phase(
            phase="finish_connection",
            deadline=fc_deadline,
            stop_events=set(),
            stop_on_conn_finished=True,
            soft_close=True,
        )

    finally:
        ws.settimeout(_recv_timeout_prev)
        ws.close()

    out_pcm = b"".join(pcm_parts)
    if not out_pcm and _meta_audio_url(meta) is None:
        raise RuntimeError(
            "未收到 PCM 音频且 podcast_end 中无 audio_url；"
            "若使用 --return-audio-url 请检查 meta JSON"
        )

    return out_pcm, meta


def write_pcm_as_wav(pcm: bytes, path: str, sample_rate: int, channels: int = 1) -> None:
    with wave.open(path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm)


def load_nlp_texts_from_markdown(path: str, male: str, female: str) -> list[dict[str, str]]:
    """极简对白格式：奇数段 → male，偶数段 → female（段落用空行分隔）。"""
    text = open(path, encoding="utf-8").read().strip()
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    out: list[dict[str, str]] = []
    for i, b in enumerate(blocks):
        sp = male if i % 2 == 0 else female
        out.append({"speaker": sp, "text": b[:300]})
    return out


def load_nlp_texts_from_prefixed_dialogue(path: str, male: str, female: str) -> list[dict[str, str]]:
    """口播稿常见格式：每行「女：…」「男：…」（中英文冒号均可），空行忽略。

    与段落轮换格式不同：说话人以行首标记为准，不要求空行分段。
    """
    out: list[dict[str, str]] = []
    for line in open(path, encoding="utf-8").read().splitlines():
        line = line.strip()
        if not line:
            continue
        m = _DIALOGUE_LINE_RE.match(line)
        if not m:
            raise ValueError(
                "对白行须以 女： 或 男： 开头（当前行: "
                + repr(line[:100] + ("…" if len(line) > 100 else ""))
                + "）"
            )
        sp = female if m.group(1) == "女" else male
        t = m.group(2).strip()
        if len(t) > 300:
            t = t[:300]
        out.append({"speaker": sp, "text": t})
    return out


def dialogue_input_looks_prefixed(text: str) -> bool:
    """若首个非空行匹配「女：/男：」，则视为前缀对白格式。"""
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        return bool(_DIALOGUE_LINE_RE.match(s))
    return False


def merge_adjacent_same_speaker_rounds(
    nlp: list[dict[str, str]],
    *,
    max_chars: int = 300,
) -> list[dict[str, str]]:
    """合并相邻且发音人相同的轮次，减少服务端轮次硬切（仍受单轮 max_chars 限制）。"""
    if not nlp:
        return []
    out: list[dict[str, str]] = []
    ft = str(nlp[0].get("text", "")).strip()
    if ft:
        out.append({"speaker": str(nlp[0]["speaker"]), "text": ft[:max_chars]})
    for item in nlp[1:]:
        sp = str(item["speaker"])
        tx = str(item.get("text", "")).strip()
        if not tx:
            continue
        if not out:
            out.append({"speaker": sp, "text": tx[:max_chars]})
            continue
        if sp == out[-1]["speaker"]:
            a = out[-1]["text"]
            sep = ""
            if a and a[-1] not in "。！？，、；：\"\"''（）…":
                sep = "，"
            merged = (a + sep + tx).strip()
            if len(merged) <= max_chars:
                out[-1]["text"] = merged
                continue
        out.append({"speaker": sp, "text": tx[:max_chars]})
    return out
