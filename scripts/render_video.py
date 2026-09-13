#!/usr/bin/env python3
"""Render ArmorCodex demo video: terminal-style slides + edge-tts voiceover."""
import asyncio, os, subprocess, glob

W, H, OUT = 1280, 720, os.path.expanduser("~/lab/armor-bounty/video")
os.makedirs(OUT, exist_ok=True)
from PIL import Image, ImageDraw, ImageFont
F = lambda s, b=False: ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf" % ("-Bold" if b else ""), s)

BG, FG, DIM, GREEN, RED, CYAN, YELLOW = (13,17,23), (230,237,243), (110,120,135), (63,185,80), (248,81,73), (88,166,255), (210,153,34)

# (title, [ (color, text) lines ], voiceover)
SCENES = [
 ("armorcodex — intent-based security for openai codex", [
   (CYAN, "$ curl -fsSL https://armoriq.ai/install_armorcodex.sh | bash"),
   (GREEN, "✔ hooks enabled   ✔ MCP server wired   ✔ global hooks installed"),
   (GREEN, "✔ armorcodex is wired up correctly"),
   (DIM, "   policy rules · intent verification · audit logging"),
 ], "ArmorCodex from ArmorIQ. One command to install. It adds intent-based security to OpenAI Codex: every shell command gets checked against a declared plan and policy rules before it runs."),
 ("step 1 · codex must declare its plan", [
   (CYAN, "$ codex exec \"run: echo planned-ok, then whoami\""),
   (DIM, "tool armorcodex-policy.register_intent_plan("),
   (DIM, '  {"goal":"Run two shell commands","steps":['),
   (FG, '    {"tool":"Bash","reason":"echo planned-ok"},'),
   (FG, '    {"tool":"Bash","reason":"whoami"}]}'),
   (GREEN, 'success: "Intent registered: 2 steps"'),
 ], "Before touching the terminal, Codex is asked to register an intent plan. This is the contract: exactly what it says it will do."),
 ("step 2 · planned commands run fine", [
   (DIM, "hook PreToolUse → check against plan + policy"),
   (CYAN, "$ echo planned-ok"),
   (GREEN, "planned-ok            exit 0 · allowed ✓"),
   (DIM, "  (in registered plan: match on tool + args)"),
 ], "Planned commands pass through untouched. The echo was in the plan, so it ran."),
 ("step 3 · intent drift gets DENIED", [
   (CYAN, "$ whoami   # deliberately OFF-plan"),
   (RED, '{"hookEventName":"PreToolUse",'),
   (RED, ' "permissionDecision":"deny",'),
   (RED, ' "permissionDecisionReason":"ArmorCodex intent'),
   (RED, '  mismatch: parameters not allowed for Bash"}'),
   (DIM, "agent report: \"whoami was blocked by ArmorCodex\""),
 ], "Now the drift. I ask for a second command that was never declared. Enforce mode: denied at the hook layer, before execution. The agent sees the deny reason and reports it honestly."),
 ("step 4 · enforce vs monitor mode", [
   (GREEN, "ARMORCODEX_MODE=enforce  → off-plan call DENIED"),
   (YELLOW, "ARMORCODEX_MODE=monitor  → off-plan call passes"),
   (DIM, "  whoami → 'onar' (logged only, no block)"),
   (CYAN, "$ armor policy template lockdown && armor yes"),
   (DIM, "  staged proposal needs HUMAN confirm in terminal"),
 ], "Flip a mode variable: enforce blocks, monitor only logs. Great for rolling out gradually. Policies can also be set from chat — armor policy commands stage a diff, and applying is human-only by design."),
 ("verdict", [
   (FG, "+ one-line install, works fully LOCAL, no API key"),
   (FG, "+ real hook-layer enforcement, fail-closed on bad payloads"),
   (FG, "+ human-only policy apply gate"),
   (FG, "- Bash-only today: MCP/file edits not intercepted yet"),
   (DIM, "  (their docs are upfront about this harness limit)"),
   (GREEN, "ships the guardrail it advertises. demo verified."),
 ], "Honest take: it is a Bash guardrail, not a full sandbox — their own docs say MCP and file edits aren't hooked yet. But what it does, it does at the hook layer with fail-closed defaults, and it runs entirely locally. Worth trying if your agents execute shell."),
]

def render(title, lines, path):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,56], fill=(22,27,34))
    for i,c in enumerate([(248,81,73),(210,153,34),(63,185,80)]):
        d.ellipse([24+i*26,20,38+i*26,34], fill=c)
    d.text((W/2,28), "onz@vps: ~/project — codex + armorcodex", font=F(16), fill=DIM, anchor="mm")
    y = 90
    d.text((48, y), title, font=F(26, True), fill=CYAN); y += 64
    for c, t in lines:
        for chunk in [t[i:i+72] for i in range(0, max(len(t),1), 72)] or [""]:
            d.text((48, y), chunk, font=F(21), fill=c); y += 34
    d.text((48, H-40), "armorcodex · intent-based enforcement", font=F(14), fill=DIM)
    img.save(path)

async def tts(text, path):
    import edge_tts
    await edge_tts.Communicate(text, "en-US-GuyNeural", rate="+8%").save(path)

def main():
    for i,(t,l,v) in enumerate(SCENES):
        render(t, l, f"{OUT}/s{i}.png")
        asyncio.run(tts(v, f"{OUT}/s{i}.mp3"))
        dur = float(subprocess.run(["ffprobe","-v","0","-show_entries","format=duration","-of","csv=p=0",f"{OUT}/s{i}.mp3"],capture_output=True,text=True).stdout.strip())+0.7
        subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-framerate","30","-t",str(dur),"-i",f"{OUT}/s{i}.png",
                        "-i",f"{OUT}/s{i}.mp3","-c:v","libx264","-preset","fast","-pix_fmt","yuv420p",
                        "-c:a","aac","-shortest",f"{OUT}/clip{i}.mp4"], check=True)
    open(f"{OUT}/list.txt","w").write("".join(f"file 'clip{i}.mp4'\n" for i in range(len(SCENES))))
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{OUT}/list.txt",
                    "-c","copy",f"{OUT}/armorcodex_demo.mp4"], check=True)
    print("done:", subprocess.run(["ffprobe","-v","0","-show_entries","format=duration","-of","csv=p=0",f"{OUT}/armorcodex_demo.mp3".replace("mp3","mp4")],capture_output=True,text=True).stdout.strip(),"sec")

if __name__ == "__main__":
    main()
