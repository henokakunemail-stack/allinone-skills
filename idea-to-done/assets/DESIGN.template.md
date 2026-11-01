# Design: <project name>

Status: draft | approved · Updated: <date>

> Pick the variant that fits the deliverable (see `references/document-set.md` §DESIGN.md).
> Keep only the sections that apply; delete the rest.
> - **UI** → the Screens / Flows / Components / States sections below.
> - **Visual system** (image set, poster, brand) → the "Visual system" section below.
> - **Storyboard** (video, animation, audio) → the "Storyboard" section below.

<!-- ========== UI VARIANT ========== -->

## Screens / views

Only screens that trace to a requirement.

| Screen | Purpose | Requirement |
|---|---|---|
| <name> | <one line> | R<n> |

## User flows

### Flow 1: <main task from the PRD, e.g. "first user, first day">
1. <step> (screen: <name>)
2. <step>
3. <outcome>

## Visual direction

- Tone: <...>
- Typography: <...>
- Color: <...>
- Density / layout: <...>
- Reference material from the user: <...>

## Shared components

- <component>: used in <screens>

## Required states

For each screen: empty, loading, error, success as applicable.

| Screen | Empty | Loading | Error |
|---|---|---|---|
| <name> | <what shows> | <what shows> | <what shows> |

<!-- ========== VISUAL-SYSTEM VARIANT (image set / poster / brand) ========== -->

## Visual system

- Palette: <hex values, roles — bg / text / accent>
- Type scale: <font, sizes, weights>
- Grid / margins: <canvas size, safe margins>
- Fixed elements shared by every piece: <logo, handle, badge, frame…>
- Visual references from the user: <...>

### Identical vs varies (the consistency contract)

| Property | Must be identical across the set | May vary per item |
|---|---|---|
| <e.g. canvas size> | ✓ | |
| <e.g. quote text> | | ✓ |

<!-- ========== STORYBOARD VARIANT (video / animation / audio) ========== -->

## Storyboard

Target length: <e.g. 60s>. Scene durations must sum to it (state the sum below).

| Scene | t_start–t_end (dur) | On-screen text | Visual | Audio / VO | Transition |
|---|---|---|---|---|---|
| 1 | 0–3s (3s) | <hook> | <...> | <...> | cut |
| … | | | | | |

Sum of durations: <...> = target length ✓

### Visual / pacing direction

- Tone, palette, typography, motion, energy: <...>
- References from the user: <...>

<!-- ========== CAPABILITY LADDER (media where quality needs a generation capability) ========== -->

## Capability ladder

See `references/media-capability.md`. Fill when the deliverable's quality depends on generating imagery, animation, voice, or music.

- **Target tier (what the request really asks for):** <A composed / B local model / C hosted generative>
- **Available here:** <local tools only / local model / configured connector X>
- **Gap:** <none, or: target needs a capability not present>
- **How to close it:** <the one thing to enable — which video-gen / voice / music connector or key — or "none needed">
- **Fallback delivered meanwhile:** <e.g. Tier A cut-out animation> — <provisional? yes/no>
