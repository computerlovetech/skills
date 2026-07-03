#!/usr/bin/env python3
"""Speak a short agent reply through ElevenLabs and local audio playback."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

API = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL_ID = "eleven_flash_v2_5"
DEFAULT_EXPRESSIVE_MODEL_ID = "eleven_v3"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set.")
    return key


def default_model() -> str:
    if os.environ.get("ELEVENLABS_MODEL_ID"):
        return os.environ["ELEVENLABS_MODEL_ID"]
    expressive = os.environ.get("ELEVENLABS_EXPRESSIVE", "").lower()
    if expressive in {"1", "true", "yes"}:
        return DEFAULT_EXPRESSIVE_MODEL_ID
    return DEFAULT_MODEL_ID


def resolve_player(player: str | None) -> list[str] | None:
    configured = player or os.environ.get("ELEVENLABS_AUDIO_PLAYER")
    if configured:
        return configured.split()
    if sys.platform == "darwin" and shutil.which("afplay"):
        return ["afplay"]
    if shutil.which("ffplay"):
        return ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error"]
    if shutil.which("mpg123"):
        return ["mpg123", "-q"]
    return None


def synthesize(text: str, voice_id: str, model_id: str, output_format: str, out: str) -> None:
    body = {
        "text": text,
        "model_id": model_id,
    }
    req = urllib.request.Request(
        f"{API}/text-to-speech/{voice_id}/stream?output_format={output_format}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "xi-api-key": api_key(),
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            audio = response.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:1000]
        raise SystemExit(f"ElevenLabs HTTP {e.code}: {detail}") from e
    with open(out, "wb") as fh:
        fh.write(audio)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="Text to speak. If omitted, stdin is used.")
    parser.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID))
    parser.add_argument("--model", default=default_model())
    parser.add_argument("--output-format", default=os.environ.get("ELEVENLABS_OUTPUT_FORMAT", DEFAULT_OUTPUT_FORMAT))
    parser.add_argument("--out", help="Write the MP3 here instead of a temporary file.")
    parser.add_argument("--player", help="Playback command. Defaults to afplay, ffplay, or mpg123.")
    parser.add_argument("--no-play", action="store_true", help="Generate audio without playing it.")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    text = text.strip()
    if not text:
        raise SystemExit("No text provided.")

    out = args.out
    if not out:
        handle = tempfile.NamedTemporaryFile(prefix="lets-talk-", suffix=".mp3", delete=False)
        out = handle.name
        handle.close()

    synthesize(text, args.voice, args.model, args.output_format, out)

    if not args.no_play:
        player = resolve_player(args.player)
        if not player:
            raise SystemExit(f"No audio player found. MP3 written to {out}")
        subprocess.run([*player, out], check=True)

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
