# ArmorCodex 🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ArmorCodex** — intent-based Bash security buat OpenAI Codex. lo mau agent lo gak bisa ngubah guardrails sendiri? ini jawabannya. lahir dari pinggir kasur, First Dollar bounty Sep 2026.

> agent lo gak bisa unlock diri sendiri. percaya deh, udah gue test.

## 🎥 Receipts

| # | Video | Angle |
|---|-------|-------|
| 1 | `armorcodex_demo.mp4` (60s) | Install → enforce → monitor — basic flow |
| 2 | `armorcodex_intent_guardrail.mp4` (69s) | Plan passes, drift denied, human-only policy gate. *the real shit.* |

## 🔍 TL;DR

- One-line installer — hooks + MCP ke `~/.codex`, self-verify
- On-plan Bash passes ✅. Off-plan? `permissionDecision: deny` sebelum run
- `ARMORCODEX_MODE=monitor` = silent recon, log-only
- Policy changes = staged diffs. Apply? Human-only (`armor yes`). Agent lo gabisa.
- Fully local. No API key. No cap.

## ⚠️ Gotchas

- Codex CLI ≥0.125 required (0.80 skips hooks silently 💀)
- Headless install needs `ARMORIQ_API_KEY=*** ARMORCODEX_AUDIT_ENABLED=false`
- bwrap sandbox bisa mask enforcement di test — jangan panik

## 🎬 Render ulang

```bash
python3 scripts/render_video_v2.py
# → ~/lab/armor-bounty/video-v2/
```

---

*Built at **STUDIO PINGGIR KASUR** — receipts > vibes. selamanya. 🦂 → 🦅 → 🔥*