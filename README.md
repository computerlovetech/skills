# Agent Skills by computerlove.tech

The agent skills we use every day at [computerlove.tech](https://computerlove.tech), shared with the world.

These aren't demos. Each skill here earns its place by being part of how we actually work with coding agents. When we stop using a skill, we remove it.

Skills are small, plain-markdown folders that follow the [Agent Skills open standard](https://agentskills.io). They work with Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and any other agent that supports the standard. Read them, fork them, and change them to fit how you work.

## Install

Install with [`skills`](https://github.com/vercel-labs/skills), the open agent skills CLI from Vercel:

```bash
# Pick from all skills in this repo
npx skills@latest add computerlovetech/skills

# Install a specific skill
npx skills@latest add computerlovetech/skills --skill <skill-name>

# List available skills without installing
npx skills@latest add computerlovetech/skills --list
```

The CLI detects your agent and puts each skill in the right place.

## Browse the skills

Skills live in `skills/`, with drafts under `skills/in-progress/`. Open a skill's `SKILL.md` to see what it does. The frontmatter `name` and `description` explain the workflow and when the agent should use it.

## License

MIT
