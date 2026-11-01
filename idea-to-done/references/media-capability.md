# Media capability provisioning

A media deliverable often needs a capability the current environment may or may not have — generating imagery, animating a character, synthesizing a voice, scoring music. The honest rule (`scope-guard.md` capability honesty) says never imply output you cannot produce. This file makes that rule **actionable instead of a dead end**: find what the deliverable needs, use whatever is actually available, and when there is a gap, tell the user the one thing to enable to close it — while delivering the best honest fallback meanwhile. Never pretend; never silently cap.

## The capability ladder

Three tiers, by what each needs. The Media/Visual Producer names the **target tier** from the request ("smooth like a real cartoon" = Tier C); the Tech Lead checks what the environment can actually reach.

- **Tier A — local rendering.** `ffmpeg`, image libraries, drawing/compositing, cut-out ("puppet") animation, frame interpolation, higher fps, transitions, overlays. Real motion, but composed — not generated. Needs nothing beyond the usual tools. Almost always available.
- **Tier B — local models.** Open image/video models (image-to-video, text-to-video), local TTS, local music generation. True generated animation and audio, run on this machine. Needs a GPU, large model downloads, and network reach to fetch them — often absent in a sandbox. Verify before promising.
- **Tier C — hosted APIs / connectors.** External generation services for video, voice, and music. Highest quality and genuinely smooth generative output; the heavy compute is theirs. Needs a configured connector or API key, network access to that service, and usually budget. This is the realistic path to "no limits, smooth".

## Provisioning procedure (Tech Lead, with the Media/Visual Producer)

1. **Set the target tier** from the request. "Make it move / smooth / like a real animation" is Tier B/C, not Tier A.
2. **Detect what is actually available**, do not assume:
   - local tools (is `ffmpeg` present? image libs?),
   - local models (is a model actually installed and runnable here? a GPU?),
   - **configured connectors / API tools** — look at the session's own tools and connectors for a media-generation, text-to-speech, or music service, and for any keys the environment exposes. A connector that is present *is* capability; use it.
3. **If the target tier is reachable with what is available, use it** — route to that connector or skill, follow its rules, and record the routing in `DECISIONS.md`. (A hosted call is an external, often paid action: see the guardrail below.)
4. **If there is a gap, close it in the open — never stop at "can't":**
   - Record the **Capability ladder** in `DESIGN.md` (its media variant): target tier, what is available here, the gap, and how to close it.
   - Tell the user the **one thing to enable** to reach the target tier — which connector, key, or tool, in a single clear sentence (see format below).
   - Meanwhile, produce the **best achievable tier as a provisional fallback** (usually Tier A), flagged per the capability `blocked assumption` in `scope-guard.md` — which must always carry the "how to close the gap" line.

## The "one thing to enable" message

When the target tier needs something not present, say it as one actionable sentence, naming the capability class (not a brand you cannot verify is available):

> "A smooth, generated animation of your character needs a video-generation service this environment doesn't have connected. Connect a video-generation connector (or provide an API key for one) and I'll produce it; meanwhile here is the cut-out animated version, which is as far as the local tools reach."

State the capability class plainly; name specific services only as examples, and only route to one that is actually configured.

## Guardrails (these do not lift, ever)

- **Honesty is not a quality cap.** Removing the no-fabrication / honest-output rules would not make a video smoother — it would only make the skill claim smoothness it did not deliver. Lift capability by adding tools; keep integrity.
- **Verify generated output like any other.** A clip a connector returned is still checked by the video/audio verification branch (probe it, watch it); a connector's confident output is data, not proof.
- **A hosted call is an external action.** It leaves the environment and usually costs money, so it falls under the irreversible/external stop-and-ask: do not spend the user's budget on a connector call while they are unreachable without their standing authorization for it. Prepare the call, and wait.
- **Source inputs stay read-only** whatever the tier (hard rule).
- **No silent downscoping.** If you delivered Tier A when the user asked for Tier C, that is a provisional deliverable led with at gate 2, not a quiet substitution.
