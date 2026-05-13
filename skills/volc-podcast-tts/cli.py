#!/usr/bin/env python3
"""火山播客 TTS WebSocket v3：长文本/对白剧本 → PCM 或 WAV（PCM 封装）。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parent / "lib"
sys.path.insert(0, str(_LIB))

from podcast_client import (  # noqa: E402
    DEFAULT_RESOURCE_ID,
    dialogue_input_looks_prefixed,
    load_nlp_texts_from_markdown,
    load_nlp_texts_from_prefixed_dialogue,
    merge_adjacent_same_speaker_rounds,
    synthesize_podcast,
    write_pcm_as_wav,
)


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key.startswith("$env:"):
            key = key.removeprefix("$env:")
        if key and key not in os.environ:
            os.environ[key] = val


def build_podcast_body(
    *,
    action: int,
    input_id: str,
    input_text: str | None,
    prompt_text: str | None,
    nlp_texts: list[dict[str, str]] | None,
    input_url: str | None,
    audio_format: str,
    sample_rate: int,
    speech_rate: int,
    use_head_music: bool,
    use_tail_music: bool,
    speakers: tuple[str, str] | None,
    random_speaker_order: bool | None,
    retry_task_id: str | None,
    last_finished_round_id: int | None,
    input_text_max_length: int | None,
    return_audio_url: bool,
) -> dict:
    body: dict = {
        "input_id": input_id,
        "scene": "deep_research",
        "action": action,
        "use_head_music": use_head_music,
        "use_tail_music": use_tail_music,
        "audio_params": {
            "format": audio_format,
            "sample_rate": sample_rate,
            "speech_rate": speech_rate,
        },
    }
    if speakers:
        # action=3 为固定对白，random_order 应与稿子一致（否则更像「拼盘」）；0/4 保持文档默认 true
        if random_speaker_order is None:
            ro = action != 3
        else:
            ro = random_speaker_order
        body["speaker_info"] = {
            "random_order": ro,
            "speakers": [speakers[0], speakers[1]],
        }
    if action == 0:
        if input_url:
            body["input_info"] = {"input_url": input_url}
            if input_text_max_length is not None:
                body["input_info"]["input_text_max_length"] = input_text_max_length
            if return_audio_url:
                body["input_info"]["return_audio_url"] = True
        elif input_text:
            body["input_text"] = input_text
            if input_text_max_length is not None:
                body.setdefault("input_info", {})[
                    "input_text_max_length"
                ] = input_text_max_length
            if return_audio_url:
                body.setdefault("input_info", {})["return_audio_url"] = True
    elif action == 3:
        body["nlp_texts"] = nlp_texts or []
    elif action == 4:
        body["prompt_text"] = prompt_text or ""
    if retry_task_id:
        body["retry_info"] = {
            "retry_task_id": retry_task_id,
            "last_finished_round_id": int(last_finished_round_id or 0),
        }
    return body


def main() -> int:
    skill_dir = Path(__file__).resolve().parent
    load_env_file(skill_dir / "local.env")

    p = argparse.ArgumentParser(description="火山播客 WebSocket v3 → 音频文件")
    p.add_argument(
        "--action",
        type=int,
        choices=(0, 3, 4),
        default=0,
        help="0=长文本/URL 总结播客，3=nlp_texts 对白直出，4=prompt 联网总结",
    )
    p.add_argument("--input", "-i", help="输入 UTF-8 文本（action 0）或对白 Markdown（action 3）")
    p.add_argument("--prompt", help="action 4 的 prompt 文本")
    p.add_argument("--input-url", help="action 0：网页或可下载文件链接")
    p.add_argument("--nlp-json", help="action 3：nlp_texts JSON 文件路径（含 [{speaker,text},…]）")
    p.add_argument(
        "--dialogue-format",
        choices=("auto", "prefixed", "paragraph"),
        default="auto",
        help=(
            "action 3 且使用 --input 时：prefixed=每行「女：/男：」；"
            "paragraph=空行分段且奇偶轮轮换发音人；auto=首行判断"
        ),
    )
    ro_g = p.add_mutually_exclusive_group()
    ro_g.add_argument(
        "--fixed-speaker-order",
        action="store_true",
        help="speaker_info.random_order=false（action=3 默认已固定；也可强制用于其它 action）",
    )
    ro_g.add_argument(
        "--random-speaker-order",
        action="store_true",
        help="speaker_info.random_order=true（覆盖 action=3 默认）",
    )
    p.add_argument(
        "--merge-same-speaker-lines",
        action="store_true",
        help=(
            "action=3：合并相邻同一发音人的轮次（≤300 字），减少服务端硬切次数"
        ),
    )
    p.add_argument(
        "--inter-speaker-silence-ms",
        type=int,
        default=0,
        metavar="MS",
        help=(
            "男女（不同发音人）轮次之间插入静音毫秒数，减轻「蹦」一下的拼接感；"
            "可试 60–120（默认 0 不改时长）"
        ),
    )
    p.add_argument("--output", "-o", required=True, help="输出文件 .wav / .pcm / .mp3（由 format 决定）")
    p.add_argument("--input-id", default="volc_podcast_skill", help="业务侧 input_id")
    p.add_argument("--format", default="pcm", choices=("pcm", "mp3", "aac", "ogg_opus"))
    p.add_argument("--sample-rate", type=int, default=24000, choices=(16000, 24000, 48000))
    p.add_argument("--speech-rate", type=int, default=0)
    p.add_argument("--head-music", action="store_true", help="开头音效（默认关）")
    p.add_argument("--tail-music", action="store_true", help="结尾音效")
    p.add_argument(
        "--speakers",
        help="两个发音人 id，逗号分隔；默认文档示例 dayi+mizai",
        default="zh_male_dayixiansheng_v2_saturn_bigtts,zh_female_mizaitongxue_v2_saturn_bigtts",
    )
    p.add_argument(
        "--api-key",
        default=os.environ.get("VOLCENGINE_PODCAST_API_KEY", ""),
        help="新版控制台「复制」的 API Key；设置后可不配 APP_ID/Access Token",
    )
    p.add_argument("--app-id", default=os.environ.get("VOLCENGINE_PODCAST_APP_ID", ""))
    p.add_argument("--access-key", default=os.environ.get("VOLCENGINE_PODCAST_ACCESS_KEY", ""))
    p.add_argument("--resource-id", default=os.environ.get("VOLCENGINE_PODCAST_RESOURCE_ID", DEFAULT_RESOURCE_ID))
    p.add_argument("--app-key", default=os.environ.get("VOLCENGINE_PODCAST_APP_KEY", "aGjiRDfUWi"))
    p.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="WebSocket connect 超时秒数；亦作为 max-stream-sec 默认值",
    )
    p.add_argument("--retry-task-id", default=os.environ.get("VOLCENGINE_PODCAST_RETRY_TASK_ID", ""))
    p.add_argument("--last-finished-round-id", type=int, default=None)
    p.add_argument("--input-text-max-length", type=int, default=None)
    p.add_argument("--return-audio-url", action="store_true")
    p.add_argument("--meta-out", help="调试：写出服务端 meta JSON")
    p.add_argument(
        "--max-stream-sec",
        type=float,
        default=None,
        help="合成下行阶段最大等待秒数（默认与连接 timeout 相同）；防止 action 0/4 长时间无 363 时挂死",
    )
    p.add_argument(
        "--recv-idle-sec",
        type=float,
        default=75.0,
        help="相邻下行帧最长间隔（与 max-stream 取更小作为单次 recv 超时）；≤0 表示仅用 max-stream 剩余墙钟",
    )
    p.add_argument(
        "--finish-phase-sec",
        type=float,
        default=90.0,
        help="FinishSession / FinishConnection 阶段 recv 墙钟上限",
    )
    p.add_argument(
        "--connect-handshake-sec",
        type=float,
        default=45.0,
        help="ConnectionStarted 握手最长等待",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    app_id = (args.app_id or "").strip()
    access_key = (args.access_key or "").strip()
    api_key = (args.api_key or "").strip()
    if not api_key and (not app_id or not access_key):
        print(
            "ERROR: 二选一 — (1) 新版控制台：VOLCENGINE_PODCAST_API_KEY=快速接入里「复制」的长密钥；"
            "勿把密钥名的 api-key-xxxx 当成 APP_ID。"
            " (2) 旧版：VOLCENGINE_PODCAST_APP_ID + VOLCENGINE_PODCAST_ACCESS_KEY",
            file=sys.stderr,
        )
        return 2

    sp_parts = [s.strip() for s in args.speakers.split(",") if s.strip()]
    speakers_t: tuple[str, str] | None = None
    if len(sp_parts) >= 2:
        speakers_t = (sp_parts[0], sp_parts[1])

    input_text: str | None = None
    nlp_texts: list[dict[str, str]] | None = None
    prompt_text: str | None = (args.prompt or "").strip() or None

    if args.action == 0:
        if args.input_url:
            pass
        elif args.input:
            input_text = Path(args.input).read_text(encoding="utf-8")
        else:
            print("ERROR: action 0 需要 --input 文本文件或 --input-url", file=sys.stderr)
            return 2
    elif args.action == 3:
        if args.nlp_json:
            nlp_texts = json.loads(Path(args.nlp_json).read_text(encoding="utf-8"))
        elif args.input:
            if not speakers_t:
                print("ERROR: action 3 需要 --speakers 指定两名发音人", file=sys.stderr)
                return 2
            raw_in = Path(args.input).read_text(encoding="utf-8")
            fmt = args.dialogue_format
            if fmt == "prefixed":
                nlp_texts = load_nlp_texts_from_prefixed_dialogue(
                    args.input, speakers_t[0], speakers_t[1]
                )
            elif fmt == "paragraph":
                nlp_texts = load_nlp_texts_from_markdown(
                    args.input, speakers_t[0], speakers_t[1]
                )
            elif dialogue_input_looks_prefixed(raw_in):
                nlp_texts = load_nlp_texts_from_prefixed_dialogue(
                    args.input, speakers_t[0], speakers_t[1]
                )
            else:
                nlp_texts = load_nlp_texts_from_markdown(
                    args.input, speakers_t[0], speakers_t[1]
                )
        else:
            print("ERROR: action 3 需要 --input 对白 Markdown 或 --nlp-json", file=sys.stderr)
            return 2
        if nlp_texts and args.merge_same_speaker_lines:
            nlp_texts = merge_adjacent_same_speaker_rounds(nlp_texts)
    elif args.action == 4:
        if not prompt_text:
            print("ERROR: action 4 需要 --prompt", file=sys.stderr)
            return 2

    retry_tid = (args.retry_task_id or "").strip() or None

    rs_order: bool | None = None
    if args.fixed_speaker_order:
        rs_order = False
    elif args.random_speaker_order:
        rs_order = True

    body = build_podcast_body(
        action=args.action,
        input_id=args.input_id,
        input_text=input_text,
        prompt_text=prompt_text,
        nlp_texts=nlp_texts,
        input_url=(args.input_url or "").strip() or None,
        audio_format=args.format,
        sample_rate=args.sample_rate,
        speech_rate=args.speech_rate,
        use_head_music=args.head_music,
        use_tail_music=args.tail_music,
        speakers=speakers_t,
        random_speaker_order=rs_order,
        retry_task_id=retry_tid,
        last_finished_round_id=args.last_finished_round_id,
        input_text_max_length=args.input_text_max_length,
        return_audio_url=args.return_audio_url,
    )

    pcm, meta = synthesize_podcast(
        app_id=app_id,
        access_key=access_key,
        api_key=api_key,
        podcast_body=body,
        resource_id=args.resource_id,
        app_key=args.app_key,
        timeout_sec=args.timeout,
        verbose=args.verbose,
        recv_idle_sec=args.recv_idle_sec,
        max_stream_sec=args.max_stream_sec,
        finish_phase_sec=args.finish_phase_sec,
        connect_handshake_sec=args.connect_handshake_sec,
        inter_speaker_silence_ms=max(0, int(args.inter_speaker_silence_ms)),
    )

    if args.meta_out:
        Path(args.meta_out).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    out = Path(args.output)
    if args.format == "pcm":
        if out.suffix.lower() == ".wav":
            write_pcm_as_wav(pcm, str(out), args.sample_rate, channels=1)
        else:
            out.write_bytes(pcm)
    else:
        out.write_bytes(pcm)

    print(str(out.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
