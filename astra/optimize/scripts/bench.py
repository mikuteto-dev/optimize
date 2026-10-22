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


def run_once(cmd, inp, timeout):
    full = cmd.replace("{input}", inp)
    start = time.perf_counter()
    proc = subprocess.Popen(["/bin/sh", "-c", "exec " + full], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    timer = threading.Timer(timeout, proc.kill)
    timer.start()
    digest = hashlib.sha256()
    for chunk in iter(lambda: proc.stdout.read(1 << 20), b""):
        digest.update(chunk)
    _, status, usage = os.wait4(proc.pid, 0)
    wall = time.perf_counter() - start
    timer.cancel()
    proc.returncode = os.waitstatus_to_exitcode(status)
    if proc.returncode < 0:
        return None
    rss = usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024)
    return {"wall": wall, "rss": rss, "code": proc.returncode, "sha": digest.hexdigest()}


def mann_whitney(a, b):
    pooled = sorted([(x, 0) for x in a] + [(x, 1) for x in b])
    ranks = [0.0] * len(pooled)
    i = 0
    ties = 0.0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        t = j - i + 1
        ties += t ** 3 - t
        i = j + 1
    n1, n2 = len(a), len(b)
    r1 = sum(r for r, (_, g) in zip(ranks, pooled) if g == 0)
    u = r1 - n1 * (n1 + 1) / 2
    n = n1 + n2
    sigma = math.sqrt(n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1))))
    if sigma == 0:
        return 1.0
    z = (abs(u - n1 * n2 / 2) - 0.5) / sigma
    return math.erfc(z / math.sqrt(2))


def generate(gen, seed, workdir):
    out = str(Path(workdir) / f"gen-{seed}.input")
    subprocess.run(["/bin/sh", "-c", gen.replace("{seed}", str(seed)).replace("{out}", out)], check=True)
    return out


def cmd_run(a):
    variants = {"before": a.before, "after": a.after}
    inputs = list(a.input)
    with tempfile.TemporaryDirectory() as workdir:
        if a.gen:
            seed = random.SystemRandom().randrange(1, 2**31)
            inputs.append(generate(a.gen, seed, workdir))
            print(f"generated input with seed {seed}")
        if not inputs:
            sys.exit("no inputs: pass --input and/or --gen")
        rows = []
        mismatch = []
        reference = {}
        for inp in inputs:
            r = run_once(a.before, inp, a.timeout)
            if r is None or r["code"] != 0:
                sys.exit(f"before failed on {inp}")
            reference[inp] = r["sha"]
        for rnd in range(a.rounds):
            for i in range(a.runs):
                order = list(variants)
                random.shuffle(order)
                for name in order:
                    for inp in inputs:
                        r = run_once(variants[name], inp, a.timeout)
                        if r is None:
                            mismatch.append(f"{name} timed out on {inp}")
                            continue
                        if r["sha"] != reference[inp] or r["code"] != 0:
                            mismatch.append(f"{name} output differs on {inp}")
                        rows.append({"variant": name, "input": os.path.basename(inp), "round": rnd, "run": i, **r})
    out = Path("bench/runs")
    out.mkdir(parents=True, exist_ok=True)
    raw = out / f"{time.strftime('%Y%m%d-%H%M%S')}-{a.name}.jsonl"
    meta = {"name": a.name, "before": a.before, "after": a.after, "inputs": [os.path.basename(i) for i in inputs], "rounds": a.rounds, "runs": a.runs, "lock": LOCK.read_text() if LOCK.exists() else None}
    with raw.open("w") as f:
        f.write(json.dumps({"meta": meta}) + "\n")
        for r in rows:
            f.write(json.dumps(r) + "\n")
    report(rows, raw)
    if mismatch:
        print("OUTPUT MISMATCH, this candidate does not count:")
        for m in sorted(set(mismatch))[:20]:
            print("  " + m)
        sys.exit(2)


def report(rows, raw):
    by = {}
    rss = {}
    for r in rows:
        by.setdefault((r["input"], r["variant"]), []).append(r["wall"])
        rss.setdefault((r["input"], r["variant"]), []).append(r["rss"])
    print(f"raw: {raw}")
    for inp in sorted({k[0] for k in by}):
        b, f = by.get((inp, "before"), []), by.get((inp, "after"), [])
        if not b or not f:
            continue
        mb, mf = statistics.median(b), statistics.median(f)
        p = mann_whitney(b, f)
        first = [r["wall"] for r in rows if r["input"] == inp and r["variant"] == "after" and r["round"] == 0 and r["run"] == 0]
        rb, rf = statistics.median(rss[(inp, "before")]) / 2**20, statistics.median(rss[(inp, "after")]) / 2**20
        print(f"{inp}: before {mb:.4f}s  after {mf:.4f}s  ratio {mb / mf:.3f}x  p={p:.2g}  n={len(b)}/{len(f)}  maxRSS {rb:.0f} -> {rf:.0f} MiB")
        if first and mf > 0 and first[0] / mf > 3:
            print(f"  first run {first[0]:.4f}s is {first[0] / mf:.1f}x the median: check for state carried across runs")


def cmd_lock(a):
    files = sorted({str(p) for pattern in a.files for p in Path().glob(pattern) if p.is_file()})
    if not files:
        sys.exit("no files matched")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(json.dumps({f: hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files}, indent=1))
    print(f"locked {len(files)} files in {LOCK}")


def main():
    p = argparse.ArgumentParser(description="Interleaved, fresh-process benchmark with output checks")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    r.add_argument("--before", required=True, help="command for the old implementation, {input} is replaced")
    r.add_argument("--after", required=True, help="command for the new implementation, {input} is replaced")
    r.add_argument("--input", action="append", default=[])
    r.add_argument("--gen", help="input generator command with {seed} and {out}; a fresh random seed is used every invocation")
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
