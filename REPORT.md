# ArmorCodex Demo Report — ONAR-77

## Setup process (what I ran)

1. Prereqs: Node 26, Codex CLI 0.125, on an Ubuntu VPS (headless).
2. Install from checkout:
   ```bash
   git clone https://github.com/armoriq/armorCodex.git
   cd armorCodex && npm install
   ARMORIQ_API_KEY=*** bash install_armorcodex.sh --force-hooks
   ```
   The installer wired four things and self-verified: `[features] hooks = true` in
   `~/.codex/config.toml`, the `armorcodex-policy` MCP server, global
   `~/.codex/hooks.json` (UserPromptSubmit / PreToolUse / PermissionRequest /
   PostToolUse), and plugin deps. Verification printed
   `✔ armorcodex is wired up correctly`.
3. Started `codex exec` from a project dir. No ArmorIQ backend key →
   full local enforcement mode ("Plan stored locally"), which is fine for
   a guardrail demo.

## Demo: intent plan blocking off-plan Bash

- **On-plan**: registered a 1-step plan (`Bash: echo planned-ok`) via
  `mcp__armorcodex-policy__register_intent_plan`, then ran it → `planned-ok`,
  exit 0.
- **Drift**: without touching the plan, asked Codex to run `whoami`.
  Enforce mode (default) returned at the hook layer:
  ```json
  {"hookEventName":"PreToolUse","permissionDecision":"deny",
   "permissionDecisionReason":"ArmorCodex intent mismatch: parameters not allowed for Bash"}
  ```
  The command never executed; Codex reported the block honestly.
- **Policy drift**: registering a plan that covers only the policy tools made
  an unplanned `echo should-be-denied` fail with
  `intent drift: tool not in plan (Bash)` — two independent deny paths
  (tool-level and parameter-level) both observed.

## Enforce vs monitor

- `ARMORCODEX_MODE=enforce` (default): failures block the tool call.
  Missing/malformed hook payloads fail closed.
- `ARMORCODEX_MODE=monitor` (re-ran the exact same drift session): the
  off-plan `whoami` **ran and printed `onar`** — logged, never blocked.
  Clean A/B in ~15 seconds, ideal for gradual rollout on a team.

## Policies from chat + human-only apply gate

- `armor policy list` works as a plain chat prompt (intercepted at
  UserPromptSubmit) — no config files touched.
- `armor policy template lockdown` **staged** a proposal (`pol_3e808f86`) with
  a diff; Codex explicitly refused to self-apply: applying requires a human
  typing `armor yes` in the terminal. That gate is a nice anti-prompt-injection
  property: the agent under guard cannot lift its own guard.

## Challenges faced & how I overcame them

1. **Interactive login gate in CI/headless**: installer aborts without a TTY
   unless credentials exist. Pass `ARMORIQ_API_KEY=*** +
   `ARMORCODEX_AUDIT_ENABLED=false` → local-only mode, everything else identical.
2. **Old Codex CLI silently skips hooks**: Codex 0.80 showed `mcp ready` but
   never fired PreToolUse. Hook support needs newer CLI (0.125). Upgrading fixed
   the "plan registered but drift allowed" confusion — it wasn't ArmorCodex,
   it was the harness.
3. **Sandbox collision**: Codex's own bwrap sandbox fails on some VPS kernels
   (`RTM_NEWADDR: Operation not permitted`) *before* hooks see the command,
   producing a false "no enforcement" reading. Running with the sandbox
   bypass flag isolated this; ArmorCodex then denied correctly.
4. **Plan step tool naming**: steps must use the harness's normalized tool name
   (`Bash`/`bash`); a `local_shell` step name registered fine but never matched,
   so drift denial came from "not in plan" rather than param mismatch — worth
   knowing when authoring strict plans.

## Honest verdict

ArmorCodex is a Bash guardrail, not a full boundary — their README is upfront
that MCP/file-edit/web tools aren't intercepted by Codex hooks yet. Within that
scope it does exactly what it advertises: hook-layer enforcement, fail-closed
defaults, enforce/monitor flip via one env var, chat-driven policy with a
human-only apply gate, and it runs 100% local with no backend account required.
The audit trail (runtime.json session/plan state) is inspectable on disk.
Worth installing if your agents execute shell.
