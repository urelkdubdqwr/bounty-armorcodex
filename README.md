<img src="assets/header.svg" alt="ARMORCODEX DEMO — bounty shipped" width="100%">

# armorcodex-demo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

End-to-end demo of [ArmorCodex](https://github.com/armoriq/armorCodex) — intent-based Bash security for OpenAI Codex — built for the ArmorIQ content contest (First Dollar, Sep 2026).

Two submissions, two angles:

| # | Video | Angle |
|---|-------|-------|
| 1 | `armorcodex_demo.mp4` (60s) | Install → enforce → monitor → policy walkthrough |
| 2 | `armorcodex_intent_guardrail.mp4` (69s) | Outcome-first: plan passes, drift denied, human-only policy gate |

## Contents

- `REPORT.md` — written report: setup steps, enforcement evidence (enforce vs monitor), challenges faced & fixes
- `SUBMISSION-PACK.md` — contest submission answers (tweet captions + form Q&A for both submissions)
- `armorcodex_demo.mp4` — submission #1 video (60s, voiceover, 6 scenes)
- `armorcodex_intent_guardrail.mp4` — submission #2 video (69s, outcome-first narrative)
- `scripts/render_video.py` — PIL + edge-tts + ffmpeg renderer for submission #1
- `scripts/render_video_v2.py` — renderer for submission #2

## TL;DR findings

- One-line installer wires hooks + MCP into `~/.codex`; self-verifies
- On-plan Bash passes; off-plan gets `permissionDecision: deny` at the hook layer, before execution
- `ARMORCODEX_MODE=monitor` = log-only A/B of the same drift
- Policy changes stage as diffs; applying is human-only (`armor yes`) — agents can't lift their own guard
- Works fully local, no API key needed (backend = optional signed tokens + audit)
- Gotchas: needs Codex CLI ≥0.125 (0.80 silently skips hooks); headless install needs `ARMORIQ_API_KEY=*** ARMORCODEX_AUDIT_ENABLED=false`; bwrap sandbox failures can mask enforcement in test results

## Submission #2 — outcome-first angle

Video #2 frames the demo as a security story:

1. **Agents should not get to change their own guardrails** — thesis
2. **Install** — one command, local enforcement ready
3. **Declare the intent** — `register_intent_plan` with one Bash step
4. **Planned command passes** — `echo planned-ok` allowed
5. **Undeclared command gets denied** — `whoami` blocked before execution
6. **Policy changes require a human** — `armor policy template lockdown` staged, `armor yes` applied by human
7. **Verdict** — practical shell guardrail, honest about current limits

## Run the renderer

```bash
python3 scripts/render_video_v2.py
# → ~/lab/armor-bounty/video-v2/armorcodex_intent_guardrail.mp4
```

By ONAR-77. Receipts > vibes. ��
