#!/usr/bin/env python3
"""ArmorCodex bounty v2 — outcome-led terminal demo, under 2 min."""
import asyncio
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = Path.home() / "lab/armor-bounty/video-v2"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf"
def f(size, bold=False): return ImageFont.truetype(FONT % ("-Bold" if bold else ""), size)

BG = (12, 15, 20); PANEL = (20, 25, 34); FG = (232, 238, 244)
DIM = (133, 146, 163); GREEN = (84, 210, 125); RED = (255, 105, 105)
CYAN = (95, 206, 255); GOLD = (245, 195, 78); PURPLE = (174, 127, 255)

SCENES = [
("AGENTS SHOULD NOT GET TO CHANGE THEIR OWN GUARDRAILS", [
 (PURPLE, "ArmorCodex / ArmorIQ  •  OpenAI Codex CLI"),
 (DIM, "A 60-second real-world guardrail test"),
 (GOLD, "PLAN  →  EXECUTE  →  DRIFT  →  DENY"),
 (DIM, "Intent-based enforcement at the hook layer"),
], "Most agent guardrails live in the prompt. This one sits before shell execution. I tested whether ArmorCodex actually stops an agent when it drifts from its declared plan."),
("01  INSTALL: ONE COMMAND", [
 (CYAN, "$ curl -fsSL https://armoriq.ai/install_armorcodex.sh | bash"),
 (GREEN, "✓ Codex hooks installed"),
 (GREEN, "✓ policy MCP server wired"),
 (GREEN, "✓ local enforcement ready — no API key required"),
], "Install is one command. ArmorCodex wires hooks into the Codex CLI, plus a policy server. The local enforcement path works without an API key."),
("02  DECLARE THE INTENT FIRST", [
 (CYAN, "$ codex exec \"run echo planned-ok\""),
 (DIM, "register_intent_plan"),
 (FG, "  goal: Run one planned bash command"),
 (FG, "  tool: Bash"),
 (FG, "  command: echo planned-ok"),
 (GREEN, "✓ intent registered"),
], "Before using Bash, Codex registers a specific intent: one command, echo planned-ok. That becomes the allowed execution contract."),
("03  THE PLANNED COMMAND PASSES", [
 (DIM, "PreToolUse hook → intent + policy check"),
 (CYAN, "$ echo planned-ok"),
 (GREEN, "planned-ok"),
 (GREEN, "✓ allowed — exact plan match"),
], "The planned command passes exactly as expected. No friction when the action matches the declared intent."),
("04  ONE EXTRA COMMAND. HARD DENY.", [
 (CYAN, "$ whoami     # not declared"),
 (RED, "permissionDecision: deny"),
 (RED, "ArmorCodex intent mismatch:"),
 (RED, "parameters not allowed for Bash"),
 (DIM, "execution never reaches the shell"),
], "Then I try whoami without updating the plan. ArmorCodex denies it before execution. That is the distinction: the agent cannot quietly extend its own scope."),
("05  POLICY CHANGES REQUIRE A HUMAN", [
 (CYAN, "$ armor policy template lockdown"),
 (GOLD, "staged: deny Bash by default"),
 (DIM, "agent can propose policy changes"),
 (CYAN, "$ armor yes"),
 (PURPLE, "human terminal confirmation required"),
 (GREEN, "✓ policy applied by human, not agent"),
], "There is a second guardrail. An agent can stage a policy change, but only a human typing armor yes in the terminal can apply it. That closes the obvious self-approval loop."),
("VERDICT: A PRACTICAL SHELL GUARDRAIL", [
 (GREEN, "+ installs fast / local mode works"),
 (GREEN, "+ plans enforced before Bash executes"),
 (GREEN, "+ human-only policy apply gate"),
 (GOLD, "monitor mode logs first; enforce mode blocks"),
 (RED, "- current limitation: Bash hooks, not full file/MCP coverage"),
 (DIM, "ArmorCodex is honest about that boundary."),
], "My take: this is a practical Bash guardrail, not a magic sandbox. It is most useful where agents can run shell commands and you need a hard boundary between a declared plan and an unexpected action."),
]

def wrap(text, width=72):
    return [text[i:i+width] for i in range(0, len(text), width)] or [""]

def render(title, lines, path):
    im = Image.new("RGB", (W,H), BG); d = ImageDraw.Draw(im)
    d.rectangle((0,0,W,60), fill=PANEL)
    for i, color in enumerate((RED,GOLD,GREEN)): d.ellipse((25+i*27,21,39+i*27,35), fill=color)
    d.text((W-38,30), "ONAR-77 / terminal proof", font=f(15), fill=DIM, anchor="rm")
    d.rectangle((38,92, W-38, H-74), outline=(57,72,92), width=2)
    d.rectangle((39,93, W-39, 151), fill=(16,23,31))
    d.text((64,122), title, font=f(25,True), fill=CYAN, anchor="lm")
    y = 188
    for color, text in lines:
        for part in wrap(text):
            d.text((74,y),part,font=f(23),fill=color)
            y += 44
        y += 8
    d.line((38,H-48,W-38,H-48), fill=(57,72,92), width=1)
    d.text((54,H-29),"ARMORIQ  ×  ARMORCODEX",font=f(14,True),fill=PURPLE)
    d.text((W-54,H-29),"intent-based enforcement",font=f(14),fill=DIM,anchor="rm")
    im.save(path)

async def speak(text, out):
    import edge_tts
    await edge_tts.Communicate(text, "en-US-GuyNeural", rate="+10%").save(out)

def duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(path)],capture_output=True,text=True,check=True)
    return float(r.stdout.strip())

def main():
    clips=[]
    for i,(title,lines,voice) in enumerate(SCENES):
        png, mp3, clip = OUT/f"s{i}.png", OUT/f"s{i}.mp3", OUT/f"clip{i}.mp4"
        render(title,lines,png)
        asyncio.run(speak(voice,mp3))
        subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-framerate","30","-t",str(duration(mp3)+0.65),"-i",str(png),"-i",str(mp3),"-c:v","libx264","-preset","medium","-crf","22","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(clip)],check=True)
        clips.append(clip)
    (OUT/"list.txt").write_text("".join(f"file '{x}'\n" for x in clips))
    target = OUT/"armorcodex_intent_guardrail.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(OUT/"list.txt"),"-c","copy",str(target)],check=True)
    d=duration(target)
    assert 25 < d < 120, d
    print(f"done: {target} ({d:.2f}s, {target.stat().st_size} bytes)")

if __name__ == "__main__": main()
