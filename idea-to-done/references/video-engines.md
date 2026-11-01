# Video render engines (how to make a video, by quality)

When the deliverable is a video and the tier is A (composed, not generated — see `media-capability.md`), *how* you render the frames decides whether it looks amateur or professional. There is a ladder of engines inside Tier A; prefer the highest one the environment supports.

## The engine ladder (all Tier A — composed, no generative model)

1. **Drawing library (PIL/Pillow, ffmpeg drawtext).** Shapes and text drawn per frame in Python. Works anywhere, needs nothing. Fine for simple cards and basic motion, but gradients are banded, type is flat, easing is hand-rolled — it reads "made by a script".
2. **Web render (HTML/CSS/Canvas/SVG/WebGL via a headless browser).** Design each scene as a web page — real CSS gradients, blur, web fonts, SVG/Canvas particles, even WebGL 3D — then capture frames with a headless browser (Chromium via Playwright/Puppeteer is often pre-installed) and encode with ffmpeg. A large visual jump over PIL, and borrows the craft of `frontend-design`. Drive animation deterministically: a `frame(p)` function the capture loop calls at each `p = i/N`, not wall-clock, so frames are reproducible.
3. **Remotion (preferred for real motion graphics).** A React framework purpose-built for video: compositions with a fixed `width/height/fps/durationInFrames`, animation via `useCurrentFrame()` + `interpolate()`/`spring()`, timing via `<Sequence>`/`<Series>`, audio via `<Audio>`, a live-preview Studio (`npx remotion studio`), and deterministic render (`npx remotion render`, Chromium under the hood). This is the professional "code → video" path that gives interpolation, sequencing, and audio for free. Needs Node + an npm install of `remotion`.

Above this ladder sit Tier B (local generative models) and Tier C (hosted generative connectors) in `media-capability.md` — those *generate* footage; everything here *composes* it.

## Choosing the engine (Tech Lead, during capability provisioning)

- Detect, do not assume: is Node present (`node -v`)? Is Remotion installed or installable (does `npm` reach the registry here)? Is a headless browser present (a Playwright/Chromium install)?
- **Prefer Remotion** when Node + Remotion are available — it is the best motion-graphics quality without a model.
- **Else prefer the web render** when a headless browser is available — still far better than PIL.
- **Else fall back to PIL** — always works.
- Record the chosen engine in `DECISIONS.md`, and if a better engine is only a short install away, name it as the "one thing to enable" (per `media-capability.md`): e.g. *"this ran on PIL; installing Remotion (`npm i remotion`) on a machine with npm access would make it motion-graphics quality."*

## Remotion workflow (when chosen)

The storyboard maps cleanly onto Remotion, so the Video Editor writes React, not frames by hand:

- One **composition** at the deliverable's spec: `width`, `height`, `fps`, `durationInFrames = round(target_seconds * fps)`.
- Each **storyboard scene → a `<Sequence from={startFrame} durationInFrames={sceneFrames}>`**; the scene durations must still sum to the target length (the storyboard's sum-check carries over).
- Animate from `useCurrentFrame()` with `interpolate()`/`spring()` and easing — never from wall-clock, so the render is deterministic.
- Preview in `npx remotion studio`; render with `npx remotion render <CompId> out.mp4`.
- Edit by changing the React code (the "edit via prompt" pattern): change a color token, a timing, a transition — re-render only what changed.

The install/scaffold is `npx create-video@latest`; this runs on the user's own machine (where npm works) even when a cloud sandbox's npm registry is blocked. If Remotion cannot be reached here, that is a capability gap with an actionable fix (install it where npm works), not a dead end.

## Verification does not change

Whatever engine rendered it, the result is still verified by the video branch of `references/verification-checklist.md`: probe the container (ffprobe), prove real motion (consecutive-frame delta, localized to the animated region — a slideshow of static cards must not pass), sample one frame per scene for beats-present-and-in-order, and watch it for craft. A fancier engine does not excuse skipping the motion proof.
