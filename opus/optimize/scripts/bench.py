#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import random
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

LOCK = Path("bench/.lock")


def fill(template, **values):
    for k, v in values.items():
        template = template.replace("{" + k + "}", str(v))
    return template


def shell(cmd, replace=False):
    return ["cmd", "/c", cmd] if os.name == "nt" else ["/bin/sh", "-c", ("exec " if replace else "") + cmd]


def spawn(cmd, out_path, timeout, writes_out):
    with open(os.devnull if writes_out else out_path, "wb") as out:
        start = time.perf_counter()
        proc = subprocess.Popen(shell(cmd, replace=not writes_out), stdout=out, stderr=subprocess.DEVNULL)
        timer = threading.Timer(timeout, proc.kill)
        timer.start()
        if hasattr(os, "wait4"):
            _, status, usage = os.wait4(proc.pid, 0)
            code = os.waitstatus_to_exitcode(status)
            rss = usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024) / 2**20
        else:
            code = proc.wait()
            rss = None
        wall = time.perf_counter() - start
        timer.cancel()
    if code < 0:
        return None, code
    metrics = {"wall_s": wall}
    if rss is not None:
        metrics["max_rss_mib"] = rss
    return metrics, code


def external(measure, timeout):
    try:
        r = subprocess.run(shell(measure), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, -1
    lines = [l for l in r.stdout.decode(errors="replace").splitlines() if l.strip()]
    if r.returncode != 0 or not lines:
        return None, r.returncode or 1
    try:
        metrics = {k: float(v) for k, v in json.loads(lines[-1]).items()}
    except (ValueError, AttributeError, TypeError):
        sys.exit(f"--measure must print a JSON object of numbers on its last line, got: {lines[-1][:200]}")
    return metrics, 0


def same(check, expected, actual, inp):
    if check:
        return subprocess.run(shell(fill(check, expected=expected, actual=actual, input=inp)), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    return Path(actual).exists() and Path(expected).exists() and digest(expected) == digest(actual)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mann_whitney(a, b):
    pooled = sorted([(x, 0) for x in a] + [(x, 1) for x in b])
    ranks, ties, i = [0.0] * len(pooled), 0.0, 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks[k] = (i + j) / 2 + 1
        ties += (j - i + 1) ** 3 - (j - i + 1)
        i = j + 1
    n1, n2 = len(a), len(b)
    n = n1 + n2
    if n1 == 0 or n2 == 0 or n < 3:
        return 1.0
    u = sum(r for r, (_, g) in zip(ranks, pooled) if g == 0) - n1 * (n1 + 1) / 2
    sigma = math.sqrt(n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1))))
    if sigma == 0:
        return 1.0
    return math.erfc(max(abs(u - n1 * n2 / 2) - 0.5, 0) / sigma / math.sqrt(2))


def cmd_run(a):
    variants = {"before": a.before, "after": a.after}
    higher = set(a.higher_better.split(",")) if a.higher_better else set()
    rows, failures = [], []
    with tempfile.TemporaryDirectory() as work:
        inputs = list(a.input)
        if a.gen:
            seed = random.SystemRandom().randrange(1, 2**31)
            path = str(Path(work) / f"gen-{seed}.input")
            subprocess.run(shell(fill(a.gen, seed=seed, out=path)), check=True)
            inputs.append(path)
            print(f"generated input with seed {seed}")
        if not inputs:
            if not a.measure:
                sys.exit("no inputs: pass --input and/or --gen")
            inputs = ["-"]
        if a.measure and not a.check:
            print("warning: --measure without --check, output correctness is not verified")

        def once(name, inp, out_path):
            if a.measure:
                return external(fill(a.measure, cmd=variants[name], input=inp, out=out_path, variant=name), a.timeout)
            return spawn(fill(variants[name], input=inp, out=out_path), out_path, a.timeout, "{out}" in variants[name])

        expected = {}
        for idx, inp in enumerate(inputs):
            expected[inp] = str(Path(work) / f"expected-{idx}")
            metrics, code = once("before", inp, expected[inp])
            if metrics is None or code != 0:
                sys.exit(f"before failed on {inp} (exit {code})")
        for rnd in range(a.rounds):
            for i in range(a.runs):
                order = list(variants)
                random.shuffle(order)
                for name in order:
                    for idx, inp in enumerate(inputs):
                        out_path = str(Path(work) / f"out-{name}-{idx}")
                        if os.path.exists(out_path):
                            os.remove(out_path)
                        metrics, code = once(name, inp, out_path)
                        ok = metrics is not None and code == 0
                        if ok and (not a.measure or a.check):
                            ok = same(a.check, expected[inp], out_path, inp)
                        if not ok:
                            failures.append(f"{name} failed or differs on {os.path.basename(inp)}")
                        rows.append({"variant": name, "input": os.path.basename(inp), "round": rnd, "run": i, "ok": ok, "metrics": metrics or {}})
        names = [os.path.basename(i) for i in inputs]
    out = Path("bench/runs")
    out.mkdir(parents=True, exist_ok=True)
    raw = out / f"{time.strftime('%Y%m%d-%H%M%S')}-{a.name}.jsonl"
    meta = {k: v for k, v in vars(a).items() if k != "func"}
    meta.update(inputs=names, lock=json.loads(LOCK.read_text()) if LOCK.exists() else None)
    with raw.open("w") as f:
        f.write(json.dumps({"meta": meta}) + "\n")
        for r in rows:
            f.write(json.dumps(r) + "\n")
    report(rows, raw, a.primary, higher)
    if failures:
        print("OUTPUT MISMATCH OR FAILURE, this candidate does not count:")
        for m in sorted(set(failures))[:20]:
            print("  " + m)
        sys.exit(2)


def report(rows, raw, primary, higher):
    print(f"raw: {raw}")
    keys = sorted({k for r in rows for k in r["metrics"]})
    primary = primary or ("wall_s" if "wall_s" in keys else (keys[0] if keys else None))
    for inp in sorted({r["input"] for r in rows}):
        print(inp)
        for key in sorted(keys, key=lambda k: k != primary):
            b = [r["metrics"][key] for r in rows if r["input"] == inp and r["variant"] == "before" and key in r["metrics"]]
            f = [r["metrics"][key] for r in rows if r["input"] == inp and r["variant"] == "after" and key in r["metrics"]]
            if not b or not f:
                continue
            mb, mf = statistics.median(b), statistics.median(f)
            gain = (mf / mb if key in higher else mb / mf) if mb and mf else float("nan")
            mark = "*" if key == primary else " "
            print(f" {mark}{key}: before {mb:.6g}  after {mf:.6g}  gain {gain:.3f}x  p={mann_whitney(b, f):.2g}  n={len(b)}/{len(f)}")
            if key == primary:
                first = [r["metrics"][key] for r in rows if r["input"] == inp and r["variant"] == "after" and r["round"] == 0 and r["run"] == 0 and key in r["metrics"]]
                if first and mf and (first[0] / mf if key not in higher else mf / first[0]) > 3:
                    print("   first run is >3x worse than the median: check for state carried across runs")


def cmd_lock(a):
    files = sorted({str(p) for pattern in a.files for p in Path().glob(pattern) if p.is_file()})
    if not files:
        sys.exit("no files matched")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(json.dumps({f: digest(f) for f in files}, indent=1))
    print(f"locked {len(files)} files in {LOCK}")


def main():
    p = argparse.ArgumentParser(description="Interleaved benchmark with fresh seeds, output checks, raw logs and significance")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    r.add_argument("--before", required=True, help="old variant: a command with {input} and optional {out}, or any string --measure understands")
    r.add_argument("--after", required=True, help="new variant, same form as --before")
    r.add_argument("--input", action="append", default=[])
    r.add_argument("--gen", help="input generator with {seed} and {out}; a new random seed every invocation")
    r.add_argument("--measure", help="command printing a JSON object of numeric metrics on its last line; {cmd} {input} {out} {variant}")
    r.add_argument("--check", help="command exiting 0 when outputs match; {expected} {actual} {input}. Default: byte-identical output")
    r.add_argument("--primary", help="metric to lead with (default wall_s, else the first metric)")
    r.add_argument("--higher-better", default="", help="comma-separated metrics where larger is better")
    r.add_argument("--rounds", type=int, default=3)
    r.add_argument("--runs", type=int, default=5)
    r.add_argument("--timeout", type=float, default=600)
    r.set_defaults(func=cmd_run)
    l = sub.add_parser("lock")
    l.add_argument("files", nargs="+", help="glob patterns for the benchmark, tests, generators and reference")
    l.set_defaults(func=cmd_lock)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
