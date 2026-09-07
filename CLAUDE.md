# CLAUDE.md

@AGENTS.md

Claude Code specifics, all public-safe:

- The canonical shared instructions are in `AGENTS.md` (imported above). Do not duplicate them here.
- If `CLAUDE.local.md` exists (gitignored), Claude Code loads it automatically; it points at the private
  local context described in AGENTS.md under "Local Private Agent Context".
- The user's plan, notes, and session logs for this project live in a separate private repository, not
  here. Never copy content from there into this repo.
