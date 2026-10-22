# LLM and agent applications

## Metrics

Input, output and cached tokens per task, cache hit rate, time to first token, end-to-end latency, model calls and tool calls per task, cost per task, context size at each call.

## Levers

- **Prompt caching**: stable prefix first (system prompt, tools, documents), variable content last, no timestamps or random IDs in the prefix, cache breakpoints at the boundaries.
- **Fewer tokens**: trim context to what the step needs, summarize or drop stale tool results, compact tool definitions, structured outputs instead of prose to parse.
- **Fewer and parallel calls**: parallel tool calls, merging steps that do not need a model in between, deterministic code for work that does not need a model.
- **Latency**: streaming, lower effort or reasoning budget where quality holds, prefetching likely next context.
- **Throughput and cost**: batch APIs for non-interactive work, concurrency limits from measured rate limits.

Switching to a smaller or different model, lowering effort, and dropping context change output quality and need the user, with an evaluation set measuring the quality change.

## Tools

Provider usage fields (tokens, cache reads and writes), token counting endpoints, request tracing, an evaluation set run before and after.

## With bench.py

`--before` and `--after` are the two pipeline versions. A locked `bench/measure-llm.sh {cmd} {out}` runs a fixed task set, prints `{"input_tokens": …, "cached_tokens": …, "output_tokens": …, "latency_ms": …, "cost_usd": …}` from the provider's usage fields, and writes the answers to `{out}`; `--check` scores them against the evaluation set and fails below the agreed threshold. Pass `--higher-better cached_tokens`.
