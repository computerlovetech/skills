---
name: lets-talk
description: Speak replies aloud through the ElevenLabs API during a conversational voice session. Use this skill whenever the user's prompt starts with "Let's talk" or "Okay, let's talk", or when the user says they want a speech session, voice session, spoken session, wants you to talk out loud, mentions using Wispr Flow for dictation, or asks you to answer with ElevenLabs audio instead of normal chat. In this mode, speak first and keep visible text minimal unless the user needs to read, copy, inspect, or confirm something.
---

# Let's Talk

Use this skill when the user wants an interactive spoken conversation. The user
handles speech-to-text with Wispr Flow, so your job is text-to-speech output.

## Core behavior

- Answer primarily by running `scripts/speak_response.py` with the text that
  should be spoken aloud.
- Keep the visible chat quiet. Only type visible text when the user needs to
  read exact details, copy commands, see paths, review code, approve a costly or
  risky action, or understand that voice playback failed.
- Write spoken replies for the ear, not the screen: short sentences, natural
  phrasing, one or two ideas at a time, and no dense lists.
- Do not narrate markdown, bullet structure, code, terminal output, JSON, stack
  traces, URLs, file paths, or exact identifiers unless there is a good spoken
  reason. Put exact details in visible text instead.
- For ordinary conversation, aim for 10-45 spoken words. For technical work,
  speak a concise summary and show exact artifacts visibly.

## Speaking

Run the bundled helper script from this skill's installed directory:

```bash
python3 <path-to-installed-lets-talk>/scripts/speak_response.py --text "Spoken reply here."
```

In Codex workspaces this is usually
`.agents/skills/lets-talk/scripts/speak_response.py`; in Claude Code workspaces
it is usually `.claude/skills/lets-talk/scripts/speak_response.py`.

The script reads:

- `ELEVENLABS_API_KEY` or `ELEVEN_API_KEY`
- `ELEVENLABS_VOICE_ID`, defaulting to the same voice used by
  `Code/kraenhansen/private/elevenlabs-claude-voice`
- `ELEVENLABS_MODEL_ID`, defaulting to `eleven_flash_v2_5`
- `ELEVENLABS_EXPRESSIVE=true`, which switches the default model to `eleven_v3`
- `ELEVENLABS_AUDIO_PLAYER`, if a specific local player command is needed

If the script fails because no API key is present, say that visibly and do not
pretend the user heard the answer.

## Response pattern

1. Compose a spoken answer that sounds natural when heard aloud.
2. Run the script to speak it.
3. Add visible text only when it adds utility beyond the audio.

For a simple voice-chat answer, there may be no visible response beyond a brief
status such as `Spoken.` if the interface requires a final message.

For a coding or workspace task:

- Speak what you are doing or what changed in a sentence or two.
- Show exact file paths, commands, diffs, test results, or next actions visibly.
- When work takes time, keep spoken progress updates short and sparse.

## Spoken style

Prefer:

- "I found the existing ElevenLabs wrapper. It already has the voice and model defaults we need."
- "I need to show you the exact command, because it is something you may want to copy."
- "The tests passed. There is one visible path below so you can inspect the change."

Avoid:

- "Here is a comprehensive summary with five bullets."
- "Backtick python space dash m pytest colon ..."
- Long explanations that would be tiring to listen to.

## Relationship to the existing project

The workspace also contains
`Code/kraenhansen/private/elevenlabs-claude-voice`, a fuller Claude Code wrapper
that uses `<speak>` tags. This skill does not require that wrapper to be active.
It calls ElevenLabs directly so it can be invoked from a normal agent session.
