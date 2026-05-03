"""火山「播客语音合成」WebSocket v3 二进制帧打包/解析。

帧格式对齐官方文档「播客API-websocket-v3协议」与 volcengine_audio 中
VolcengineTTSFunctions.calculate_payload / extract_response_payload 的常见布局。
"""

from __future__ import annotations

import gzip
import json
import struct
from typing import Any

# --- 与 volcengine_audio.protocol 对齐 ---
PROTOCOL_VERSION_V1 = 0b0001
HEADER_SIZE_4 = 0b0001
MSG_FULL_CLIENT_REQUEST = 0b0001
MSG_FULL_SERVER_RESPONSE = 0b1001
MSG_AUDIO_ONLY_RESPONSE = 0b1011
MSG_ERROR = 0b1111
FLAG_EVENT_ID = 0b0100
SER_JSON = 0b0001
SER_RAW = 0b0000
COMP_NONE = 0b0000
COMP_GZIP = 0b0001

# EventSend（上行）
EVT_START_CONNECTION = 1
EVT_FINISH_CONNECTION = 2
EVT_START_SESSION = 100
EVT_FINISH_SESSION = 102

# EventReceive（下行，播客扩展）
EVT_CONNECTION_STARTED = 50
EVT_CONNECTION_FINISHED = 52
EVT_SESSION_STARTED = 150
EVT_SESSION_FINISHED = 152
EVT_USAGE = 154
EVT_PODCAST_ROUND_START = 360
EVT_PODCAST_ROUND_RESPONSE = 361
EVT_PODCAST_ROUND_END = 362
EVT_PODCAST_END = 363


def pack_message(
    *,
    message_type: int,
    event: int,
    session_id: str | None,
    payload_obj: dict[str, Any] | None = None,
    payload_raw: bytes | None = None,
    serialization: int = SER_JSON,
    compression: int = COMP_NONE,
) -> bytes:
    """打包一条上行消息。"""
    header = bytearray(
        [
            (PROTOCOL_VERSION_V1 << 4) | HEADER_SIZE_4,
            (message_type << 4) | FLAG_EVENT_ID,
            (serialization << 4) | compression,
            0x00,
        ]
    )
    out = bytes(header)
    out += struct.pack(">I", event)
    if session_id is not None:
        sid = session_id.encode("utf-8")
        out += struct.pack(">I", len(sid))
        out += sid
    if payload_raw is not None:
        body = payload_raw
    else:
        body = json.dumps(payload_obj or {}, ensure_ascii=False).encode("utf-8")
    if compression == COMP_GZIP:
        body = gzip.compress(body)
    out += struct.pack(">I", len(body))
    out += body
    return out


def pack_start_connection() -> bytes:
    return pack_message(
        message_type=MSG_FULL_CLIENT_REQUEST,
        event=EVT_START_CONNECTION,
        session_id=None,
        payload_obj={},
    )


def pack_finish_connection() -> bytes:
    return pack_message(
        message_type=MSG_FULL_CLIENT_REQUEST,
        event=EVT_FINISH_CONNECTION,
        session_id=None,
        payload_obj={},
    )


def pack_start_session(session_id: str, podcast_body: dict[str, Any]) -> bytes:
    """播客 StartSession：payload 为业务 JSON（不要 BidirectionalTTS 的 namespace 包裹）。"""
    return pack_message(
        message_type=MSG_FULL_CLIENT_REQUEST,
        event=EVT_START_SESSION,
        session_id=session_id,
        payload_obj=podcast_body,
    )


def pack_finish_session(session_id: str) -> bytes:
    return pack_message(
        message_type=MSG_FULL_CLIENT_REQUEST,
        event=EVT_FINISH_SESSION,
        session_id=session_id,
        payload_obj={},
    )


def parse_one_message(data: bytes) -> tuple[int, str, Any, int]:
    """解析一条下行消息 → (event_code, session_id, payload, message_type)。

    payload: dict（JSON）或 bytes（RAW 音频 / 未解码）
    message_type: 帧头消息类型（含 MSG_ERROR=0b1111）
    """
    if len(data) < 12:
        raise ValueError("frame too short")
    b1 = data[1]
    msg_type = (b1 >> 4) & 0xF
    flags = b1 & 0xF
    ser = (data[2] >> 4) & 0xF
    comp = data[2] & 0xF
    off = 4
    if flags == FLAG_EVENT_ID:
        event = struct.unpack(">I", data[off : off + 4])[0]
        off += 4
    else:
        event = -1
    sid_len = struct.unpack(">I", data[off : off + 4])[0]
    off += 4
    session_id = data[off : off + sid_len].decode("utf-8") if sid_len else ""
    off += sid_len
    plen = struct.unpack(">I", data[off : off + 4])[0]
    off += 4
    payload = data[off : off + plen]

    if comp == COMP_GZIP:
        payload = gzip.decompress(payload)

    if msg_type == MSG_ERROR:
        try:
            return event, session_id, json.loads(payload.decode("utf-8")), msg_type
        except Exception:
            return event, session_id, payload, msg_type

    if ser == SER_RAW:
        return event, session_id, payload, msg_type

    # JSON
    try:
        return event, session_id, json.loads(payload.decode("utf-8")), msg_type
    except json.JSONDecodeError:
        return event, session_id, payload, msg_type
