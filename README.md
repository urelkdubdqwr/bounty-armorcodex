# STUDIO PINGGIR KASUR 🛏️

## ArmorCodex — intent-based Bash security buat Codex.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ArmorCodex** — intent-based Bash security buat OpenAI Codex. First Dollar bounty Sep 2026. Dua submission, dua angle, satu goal: kasih lihat kalo agent lo gak bisa ngubah guardrails sendiri.

## Daftar isi (real ones only)

| # | Video | Angle |
|---|-------|-------|
| 1 | `armorcodex_demo.mp4` (60s) | Install → enforce → monitor → policy walkthrough. Basic. |
| 2 | `armorcodex_intent_guardrail.mp4` (69s) | Outcome-first: plan passes, drift denied, human-only policy gate. The real shit. |

## TL;DR — what we found so u don't have to

- One-line installer — hooks + MCP langsung ke `~/.codex`, self-verify. No cap.
- On-plan Bash passes ✅. Off-plan? `permissionDecision: deny` before eksekusi, gak sempet run.
- `ARMORCODEX_MODE=monitor` = log-only A/B buat drift. Silent recon.
- Policy changes = staged diffs. Apply? Human-only (`armor yes`). Agent lo gak bisa unlock sendiri, fr.
- Fully local. No API key needed. Backend optional.
- Gotchas: Codex CLI ≥0.125 required (0.80 skips hooks silently 💀). Headless install needs `ARMORIQ_API_KEY=*** ARMORCODEX_AUDIT_ENABLED=false`. bwrap sandbox bisa mask enforcement di test results.

## Submission #2 — the spicy one

Story arc buat video 2:

1. **Agents shouldn't change their own guardrails** — thesis. Period.
2. **Install** — satu command, langsung enforce.
3. **Declare intent** — `register_intent_plan` with satu Bash step.
4. **Planned command passes** — `echo planned-ok` allowed ✅
5. **Undeclared command denied** — `whoami` blocked before execution 🛑
6. **Policy changes = human-only** — `armor policy template lockdown` staged, `armor yes` applied by human. Agent gak bisa.
7. **Verdict** — practical shell guardrail. Jujur soal limits skrg.

## Run renderer

```bash
python3 scripts/render_video_v2.py
# → ~/lab/armor-bounty/video-v2/armorcodex_intent_guardrail.mp4
```

By ONAR-77. Receipts > vibes. Selamanya. 🛡️