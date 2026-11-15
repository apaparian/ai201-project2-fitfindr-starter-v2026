"""The request log: one JSON object per line, one line per /ask request."""

import json
import threading
from datetime import datetime, timezone

import config

_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def log_request(
    request_id: str,
    query: str,
    output: str | None = None,
    duration_ms: float | None = None,
    status: str = "ok",          # TODO: your labels, e.g. ok / agent_error / crashed
    # TODO: your extra fields here, e.g. selected_item_id, model_calls, tokens
    **extra,
) -> dict:
    entry = {
        "timestamp": _now(),
        "request_id": request_id,
        "input": query,
        "output": output,
        "duration_ms": duration_ms,
        "status": status,
    }
    entry.update(extra)
    return _append(entry)


def log_rejection(request_id: str, reason: str, query: str = "",
                  duration_ms: float | None = None, **extra) -> dict:
    # TODO: mirror Project 4: event="rejected", status="rejected", reason=reason.
    # Which of the standard fields should still appear so the shapes match?

    return _append({
        "timestamp": _now(),
        "request_id": request_id,
        "input": query,
        "output": None,
        "duration_ms": duration_ms,
        "status": "rejected",
        "event": "rejected",
        "reason": reason,
        **extra,
    })


def _append(entry: dict) -> dict:
    # TODO: copy the pattern from Project 4's audit.py _append:
    # mkdir LOG_DIR, dump to one line, write under the lock.
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    print(line, flush=True)                     # Render's log viewer reads stdout
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    return entry


def read_entries(limit: int | None = None) -> list[dict]:
    # TODO: Project 4 skips malformed lines instead of raising. Why is that right?
    if not config.REQUEST_LOG.exists():
        return []
    entries = []
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue        # one half-written line shouldn't hide the rest of the log
    return entries[-limit:] if limit else entries


def clear() -> int:
    count = len(read_entries())
    if config.REQUEST_LOG.exists():
        config.REQUEST_LOG.unlink()
    return count
