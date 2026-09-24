---
name: ai-intensity
description: >-
  A standalone opencode skill that conducts an interactive self-assessment of the user's AI usage intensity according to the RSQKit spectrum (0-10). It does NOT detect or infer AI usage from repository files. It asks the user questions and helps them determine their own level.

  Triggers when the user asks to determine, assess, or figure out their AI usage intensity:

  - "What AI intensity level should I use?"
  - "Determine my AI intensity"
  - "What level of AI is appropriate for my project?"
  - "Am I using too much AI?"
  - "ai-intensity"
  - "assess my AI usage"
  - "help me figure out my AI spectrum level"
---

## Key principle

The RSQKit spectrum is **not a maturity scale**. Higher intensity does not mean better practice, higher skill, or better quality. The right level depends on the task, review capacity, material sensitivity, and safe access.

> *"Use the lowest intensity you can justify."* — RSQKit

The questions the RSQKit poses — *"Where do you sit? Where do you want to be? Where should you be?"* — can only be answered by the user, not by scanning repository files.

## Workflow

The skill walks the user through **four dimensions**, one question at a time. Each question presents the relevant RSQKit spectrum descriptions to help the user self-assess. The skill **never assigns a level** — it helps the user **determine their own**.

### Dimension 1: Current Usage ("Where do you sit?")

Ask: "What AI tools do you currently use in your research software work?"

Present the full RSQKit spectrum (0-10) with descriptions as reference. Let the user pick the level that matches their current practice.

**Spectrum reference (show to user):**

| Level | Name | RSQKit description |
|---|---|---|
| 0 | No Gen-AI usage | Work undertaken without generative AI assistance |
| 1 | Conversational interaction | Conversations asking for explanations, design trade-offs, unfamiliar errors and conceptual help |
| 2 | Conversational artefact creation | Chat-based creation of small, reviewable outputs (helper function, test skeleton, README paragraph) |
| 3 | Conversational creation with zip files | Providing selected files, snippets, logs or zip files so the tool can reason about the content |
| 4 | IDE autocomplete and inline suggestions | AI suggestions appear while editing (boilerplate, repetitive test cases, docstrings) |
| 5 | Editor-integrated local assistant | The assistant can make bounded edits inside the editor (refactor a function, add type hints, generate tests) |
| 6 | Repository-aware assistance | The tool can search and reason across the repository (trace where a setting is used, identify tests for a feature) |
| 7 | Constrained local tool-using agents | An agent can edit files, run commands and iterate locally under supervision |
| 8 | Managed or cloud coding agents | A hosted or managed agent works in a configured environment, often asynchronously |
| 9 | CI/PR/repository agents | Agents are integrated into shared project workflows (review PRs, suggest CI fixes, triage issues) |
| 10 | Open-ended autonomous agents | Broad tool-using systems with persistence, scheduling or external integrations |

Source: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

Ask follow-up questions to understand context:
- "What specific tools do you use? (ChatGPT, Copilot, Claude Code, Cursor, etc.)"
- "How often do you use AI in your development work?"

Record the user's chosen level and notes.

### Dimension 2: Desired Intensity ("Where do you want to be?")

Ask: "What level of AI autonomy do you want to work toward?"

Present the same spectrum. Ask follow-up questions:
- "What tasks would benefit from more AI?"
- "What's holding you back from higher intensity?"
- "What would need to change for you to be comfortable at a higher level?"

Record the user's chosen level and notes.

### Dimension 3: Authorized Intensity ("Where should you be?")

Ask: "What level of AI is allowed or authorized in your context?"

Explore external constraints:
- "Does your project have an AI usage policy?"
- "Does your institution or funder have restrictions?"
- "Is there sensitive data that limits what can be shared with AI tools?"
- "Are there ethical or environmental considerations?"

Present the RSQKit's AI Intensity Considerations content:
- Level 0 is valid when: learning/assessment, data cannot be shared, limited review capacity, ethical/environmental concerns, no AI policy agreed
- Moving up: only when greater intensity solves a real problem
- Moving down: when a simpler practice provides the same benefit, or review cannot keep pace
- Source: https://everse.software/RSQKit/ai_intensity_considerations

Record the user's chosen level and notes.

### Dimension 4: Review Capacity (sustainability)

Ask: "How much review capacity do you have? What are you comfortable reviewing?"

Explore the sustainability of the chosen intensity:
- "Are you solo or on a team?"
- "How much time can you dedicate to reviewing AI-generated work?"
- "What types of changes are you comfortable reviewing?"
- "What would overwhelm your review capacity?"

Present the RSQKit's guidance on review:
- "Keep generated artefacts small enough to review"
- "If you cannot understand the code, documentation or output, you cannot rely on it"
- "Ownership of generated code is not the same as understanding generated code"
- Source: https://everse.software/RSQKit/how_do_you_use_AI_to_develop_quality_research_software

Record the user's notes.

## Output: `ai-intensity.yaml`

After the Q&A, generate the profile file. **Preview** it to the user, ask for **explicit confirmation**, then **write** it.

```yaml
# AI Intensity Profile
# Generated by the AI Intensity Q&A skill
# This is NOT an evaluation — it is a self-determination by the project's users.
# See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

schema_version: "1.0.0"

project:
  name: <project name from repo>
  repository: <repo URL if available>

# Self-determined intensity levels (0-10, RSQKit spectrum)
intensity:
  current: <level>          # Where the user currently sits
  desired: <level>           # Where the user wants to be
  authorized: <level>        # What is allowed/authorized in their context
  sustainable: <level>       # What is sustainable given review capacity

# The determining factors (free text, from the Q&A)
determination:
  current_usage: >-
    <user's answer about current tools and usage>
  desired_intensity: >-
    <user's answer about what they want>
  authorized_intensity: >-
    <user's answer about constraints>
  review_capacity: >-
    <user's answer about review capacity>

# RSQKit spectrum reference (embedded for the scan to display)
spectrum_reference:
  url: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
  considerations_url: https://everse.software/RSQKit/ai_intensity_considerations
  note: >-
    It is not a maturity scale. Higher intensity does not mean better practice.
    Use the lowest intensity you can justify.

declaration:
  date: "<today's date>"
  determined_by: <user name>
  next_review: "<6 months from now>"
  notes: >-
    Initial self-assessment via AI Intensity Q&A skill.
```

### File location

Write `ai-intensity.yaml` to the repository root (the current working directory or the repo being scanned).

### After writing

1. Display what was created
2. Inform the user that `everse-scan` will read this profile in future scans
3. Remind the user to commit the file so collaborators and agents can respect it
4. Link to the RSQKit spectrum page for further reading

## Principles

1. **Self-determination** — the user decides, the skill facilitates
2. **Neutrality** — no level is presented as better than another
3. **RSQKit fidelity** — use RSQKit's own descriptions, don't paraphrase
4. **No detection** — never infer AI usage from repository files
5. **Persistence** — the profile is committed to the repo so collaborators and agents can respect it

## Relationship with everse-scan

- This skill is **separate** from `everse-scan`
- `everse-scan` reads `ai-intensity.yaml` if present and includes it **neutrally** in the report
- If `ai-intensity.yaml` is absent, `everse-scan` notes "No AI intensity profile found" with a link to the RSQKit AI spectrum page
- `everse-scan` does **not** conduct the Q&A — it only reads the profile

## Relationship with aidecl.yaml

- `ai-intensity.yaml` records **preferences** — what AI level is desired/authorized
- `aidecl.yaml` records **provenance** — what AI was actually used, what it did, who reviewed it
- Both files follow AI Declaration Format conventions but serve different purposes
- See: https://ai-declaration.org
