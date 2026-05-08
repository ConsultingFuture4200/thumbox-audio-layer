<!-- GSD:project-start source:PROJECT.md -->
## Project

**thUMBox Audio Layer**

Platform-layer infrastructure that lets thUMBox voice-bearing personality packs (receptionBOX first) consume audio as an LLM-native token stream rather than as text transcripts produced by ASR.

It is **not** a personality pack. Customers don't buy it. It enables receptionBOX (and future voice packs) to achieve latency, expressiveness, and cost characteristics a conventional ASR → text → LLM cascade cannot reach.

**Core Value:** Three-phase decomposition with binary go/no-go gates between each phase, each delivering a measurable latency win that compounds:

1. **Predictive-delta ASR** (achievable with existing tools, 6-10 weeks)
2. **LLM-targeted neural audio codec** (research-grade architectural bet, 3-4 months)
3. **Per-firm codec fine-tuning** (the differentiator: "appliance gets faster the more your firm uses it")

The asymmetry argument: a single-tenant on-prem appliance can do per-firm codec fine-tuning that multi-tenant cloud cannot safely do. Same structural argument as receptionBOX Path B, generalized to the codec layer.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
