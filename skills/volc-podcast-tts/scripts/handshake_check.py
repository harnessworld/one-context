#!/usr/bin/env python3
"""仅检测 WebSocket 鉴权握手（不发合成任务）。依赖 local.env 或已导出的 VOLCENGINE_PODCAST_*。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SKILL / "lib"))

def _load_local_env() -> None:
    p = _SKILL / "local.env"
    if not p.is_file():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key.startswith("$env:"):
            key = key.removeprefix("$env:")
        if key and key not in os.environ:
            os.environ[key] = val


def main() -> int:
    _load_local_env()
    import websocket  # noqa: E402
    from podcast_client import (  # noqa: E402
        DEFAULT_APP_KEY,
        DEFAULT_RESOURCE_ID,
        WS_URL,
        _headers_api_key,
        _headers_legacy,
    )

    api_key = (os.environ.get("VOLCENGINE_PODCAST_API_KEY") or "").strip()
    app_id = (os.environ.get("VOLCENGINE_PODCAST_APP_ID") or "").strip()
    access_key = (os.environ.get("VOLCENGINE_PODCAST_ACCESS_KEY") or "").strip()
    resource_id = (os.environ.get("VOLCENGINE_PODCAST_RESOURCE_ID") or DEFAULT_RESOURCE_ID).strip()
    app_key = (os.environ.get("VOLCENGINE_PODCAST_APP_KEY") or DEFAULT_APP_KEY).strip()

    if api_key:
        hdr = _headers_api_key(api_key, resource_id, app_key)
        mode = "api_key"
    elif app_id and access_key:
        hdr = _headers_legacy(app_id, access_key, resource_id, app_key)
        mode = "legacy"
    else:
        print("ERROR: need VOLCENGINE_PODCAST_API_KEY or APP_ID+ACCESS_KEY", file=sys.stderr)
        return 2

    ws = websocket.WebSocket()
    ws.connect(WS_URL, header=hdr, timeout=20)
    print(f"OK handshake mode={mode}")
    ws.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
