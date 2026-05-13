"""共享 remote 协议定义。"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal


@lru_cache(maxsize=1)
def load_remote_protocol_spec() -> dict[str, Any]:
    """加载共享 remote 协议 spec。"""

    spec_path = Path(__file__).with_name("remote_protocol.json")
    return json.loads(spec_path.read_text(encoding="utf-8"))


_REMOTE_PROTOCOL_SPEC = load_remote_protocol_spec()
PROTOCOL_VERSION = str(_REMOTE_PROTOCOL_SPEC["version"])
HTTP_ROUTES = tuple(str(item) for item in _REMOTE_PROTOCOL_SPEC["httpRoutes"])
SSE_EVENT_TYPES = tuple(str(item) for item in _REMOTE_PROTOCOL_SPEC["sseEventTypes"])
REMOTE_COMMAND_TYPES = tuple(
    str(item) for item in _REMOTE_PROTOCOL_SPEC.get("remoteCommandTypes", [])
)
REMOTE_EVENT_TYPES = tuple(str(item) for item in _REMOTE_PROTOCOL_SPEC.get("remoteEventTypes", []))

HttpRoute = Literal[*HTTP_ROUTES]
SseEventType = Literal[*SSE_EVENT_TYPES]
