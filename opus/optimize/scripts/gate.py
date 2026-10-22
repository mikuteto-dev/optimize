#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

OPEN = "untested"
STATUSES = {"untested", "kept", "reverted", "needs user"}


def last_user_text(transcript):
    try:
        lines = Path(transcript).read_text(errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") != "user":
            continue
        c = e.get("message", {}).get("content")
        if isinstance(c, str):
            return c
        if isinstance(c, list):
            texts = [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text"]
            if texts:
                return " ".join(texts)
    return ""


def table(path):
    rows, header = [], None
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(dict(zip(header, cells)))
    return header or [], rows


def changed_files(root):
    try:
        out = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [l[3:] for l in out.splitlines() if l[3:] and not l[3:].startswith("bench/")]


def problems(root):
    ledger = root / "bench/candidates.md"
    if not ledger.exists():
        if changed_files(root):
            return ["Code changed but bench/candidates.md does not exist. Create the ledger and work it, or state in your reply why optimization does not apply to this change."]
        return []
    header, rows = table(ledger)
    out = []
    if "status" not in header:
        return ["bench/candidates.md has no table with a 'status' column."]
    if not rows:
        out.append("The ledger has no candidates. List candidates from references/any-system.md and the checklists.")
    for r in rows:
        st = r.get("status", "").lower()
        if st not in STATUSES:
            out.append(f"Unknown status '{r.get('status')}' in row: {r}")
        if st == OPEN:
            out.append(f"Untested candidate: {next(iter(r.values()), '')}")
        if st == "kept":
            raw = r.get("raw", "")
            if not raw or not (root / raw).exists():
                out.append(f"Kept candidate without an existing raw-data file: {next(iter(r.values()), '')}")
    lock = root / "bench/.lock"
    if lock.exists():
        for f, h in json.loads(lock.read_text()).items():
            p = root / f
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
                out.append(f"Locked benchmark file changed or missing: {f}. Restore it, or re-lock and re-measure every kept candidate after the new lock.")
        for r in rows:
            raw = root / r.get("raw", "")
            if r.get("status", "").lower() == "kept" and raw.is_file() and raw.stat().st_mtime < lock.stat().st_mtime:
                out.append(f"Kept candidate measured before the current lock: {next(iter(r.values()), '')}")
    else:
        out.append("bench/.lock is missing. Lock the benchmark, tests, generators and reference with scripts/bench.py lock before measuring.")
    measured = [r for r in rows if r.get("kind", "").lower() == "structural" and r.get("status", "").lower() != OPEN and (root / r.get("raw", "")).is_file()]
    if len({r.get("area", "").lower() for r in measured}) < 3:
        out.append("Fewer than 3 structural candidates in different areas measured with bench.py. Prototype and measure structurally different strategies (algorithm, data layout, language or library, architecture, lower layer) before converging.")
    pdir = root / "bench/profiles"
    profiles = [p.stat().st_mtime for p in pdir.rglob("*") if p.is_file()] if pdir.is_dir() else []
    kept = [(root / r["raw"]).stat().st_mtime for r in rows if r.get("status", "").lower() == "kept" and (root / r.get("raw", "")).is_file()]
    if not profiles:
        out.append("bench/profiles/ is empty. Profile the workload with the field's profiler, save the output there, and add the candidates it points to.")
    elif kept and max(profiles) < max(kept):
        out.append("No profile of the current version in bench/profiles/. Profile the latest kept version, save it there, and add the candidates it points to.")
    text = ledger.read_text(errors="replace").lower()
    if rows and not any(l.startswith("verified:") for l in text.splitlines()):
        out.append("No 'Verified:' line. Have a fresh context rerun the benchmark and output comparison from the ledger alone, then record the result as 'Verified: <who> <date> <result>'.")
    return out


def main():
    hook = "--hook" in sys.argv
    data = {}
    if hook:
        try:
            data = json.load(sys.stdin)
        except ValueError:
            data = {}
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
    if hook and "stop optimize" in last_user_text(data.get("transcript_path", "")).lower():
        return 0
    found = problems(root)
    if not found:
        if not hook:
            print("ok")
        return 0
    reason = "optimize: not done yet.\n- " + "\n- ".join(found[:15])
    if hook:
        if not (root / "bench/candidates.md").exists():
            marker = Path(os.environ.get("TMPDIR", "/tmp")) / f"optimize-gate-{data.get('session_id', 'none')}"
            if data.get("stop_hook_active") or marker.exists():
                return 0
            marker.touch()
        print(json.dumps({"decision": "block", "reason": reason}))
        return 0
    print(reason)
    return 1


if __name__ == "__main__":
    sys.exit(main())
