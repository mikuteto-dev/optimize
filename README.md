# optimize

Agent skill that pushes runtime, memory, binary size and startup time toward the theoretical limit, with benchmarks that prove each gain.

Two variants follow each vendor's prompting guide:

| Variant | For | Guide |
|---------|-----|-------|
| `opus/optimize` | Claude Opus 5.5 (Claude Code) | [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) |
| `astra/optimize` | GPT-6 Astra (Codex) | [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) |

Copy the variant's `optimize` directory into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex).
