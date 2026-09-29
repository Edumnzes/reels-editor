# Visual references — looks, text, SFX, colour, angles, asset banks

Distilled from reference reels the user picked (Brazilian editors, 2024–2026) plus asset-bank
research. Use it to choose a *direction* per video and to brief the user; the engine hooks are
noted as `→ engine`. Don't copy these creators' work — borrow the principles.

## Contents
1. The five reference reels (what each teaches)
2. Pick a direction (preset table)
3. Text / typography
4. Sound effects (SFX)
5. Colour grading
6. Camera angles & shot grammar
7. Asset banks (Motion Array & co.) + licensing
8. What the engine can't do (and the workaround)

## 1. Reference reels

**@douglxsmov — "fontes que uso no CapCut"** (instagram.com/p/DWT9aOIjWvt)
- Font pairing is the look: heavy geometric sans (Cocogoose) + elegant serif italic (Libre Baskerville) *in the same line* — "Um **problema** de saúde"; condensed display (Fixture Ultra Bold) for loud titles; thin "Cinematográfica"; decorative (Alice in Wonderland / Callisya Signature) only for themed content.
- Small hand-drawn accents (arrows, underline scribbles) next to labels.
→ engine: `family="serif"` accent words (caption style `minimal`), `family="cond"` for titles.

**@oraulcharles — makeover of a doctor's video ("foco na mensagem e autoridade")** (…/DbtbPymRO1g)
- "Peguei as referências, cravei a paleta de cores e limpei a poluição visual": one palette (cream/beige + desaturated green that matches wardrobe and plants), nothing extra on screen.
- Captions: small, lowercase, clean sans; keyword swapped to bold caps or serif/script in the palette colour ("Então você **começou** a usar *molinja*").
- Layouts: split screen (B-roll top, speaker bottom) with a **soft blurred seam**; rounded picture-in-picture with a coloured border for before/after; circular vignette mask with words scattered around it; title card on cream with a blue chromatic glow.
- Angles: medium seated → tight close-up punch → extreme close-up (eyes/nose) on emotional words.
→ engine: `look="clean_warm"`, `caption_style="minimal"`, accent = palette colour; PiP/split via motions (see §8).

**@obiel.mov — "Flash Cut" (Premiere)** (…/DcJUcb0uJhT)
- Subject masked/tracked, tinted white + glow ("Wonder Glow"), hard cuts on the beat — **always sold with a camera-flash SFX**.
- Look: monochrome warm-orange background, orange/teal skin grade.
- Captions: small white lowercase with soft shadow; keyword large bold in orange with glow, surrounded by the small words ("que vocês **aprender** queiram").
- Angles: dutch tilt close-up alternating with straight medium shot.
→ engine: `flashes=[t]` + `sfx=[(t, "flash", -6)]`, `look="teal_orange"`, `caption_style="minimal"` with orange accent.

**@raele.videomaker — "3 habilidades além da edição"** (…/DZVqlxAqL1i)
- Low-key moody grade: dark, warm practical lights and bokeh behind; wide lens close to the face (intimate, slightly distorted).
- Keyword in glowing handwritten script under spaced small caps ("VOCÊ VAI SE / *dar mal*").
- Conceptual B-roll cutaways from stock (3D objects, money rain, clock) duotoned purple/black to match the grade.
- Comment-bait CTA: giant translucent word behind the speaker ("comenta aqui **NÃO**").
→ engine: `look="moody"`, `family="hand"` + `glow=` for accent titles, big translucent `T()` behind captions for the CTA.

**@rick_miura — "textos imersivos"** (…/C5mTkBYvGO6) — 59k likes, 33.6k comments
- 3D-tracked text living in the scene: painted on the ground, on walls, behind the subject; tall condensed caps (Bebas-like), white + yellow.
- Wide establishing shots, low angle, whip pans with motion blur, light-leak transitions, series framing ("EPISÓDIO DE HOJE / E NO PRÓXIMO EPISÓDIO" over a grid background).
- CTA "comenta #texto que te explico no direct" drove the comment count.
→ engine: `caption_style="cinematic"`, `look="vivid_day"`; true 3D tracking is out of scope (§8).

## 2. Pick a direction
| Content | caption_style | look | accent | typical extras |
|---|---|---|---|---|
| Trade show / product / B2B sales | hormozi | none or vivid_day | #FFD400 | cards, counters, explainer chart |
| Authority / doctor / consultant | minimal | clean_warm | palette colour (e.g. #7FA37A green, #C8A46A gold) | PiP, split screen, few graphics |
| Energetic personal brand / tutorial | minimal (orange accent) | teal_orange | #FF8A1F | flash cuts + flash SFX, dutch angles |
| Storytelling / reflective | minimal with hand/serif accents | moody | warm white / #B18CFF | duotone stock cutaways, comment CTA |
| Outdoor / travel / cinematic | cinematic | vivid_day | #FFD400 | wide shots, whip pans, series titles |
Show the user `python project.py looks <t>` (same frame in every grade) and one preview per caption
style when the direction isn't obvious — it's a 1-minute decision that changes the whole video.

## 3. Text / typography
- Max two families per video (+ one accent). Sans for body, accent = serif italic OR handwritten OR condensed — never all three.
- Hierarchy inside one caption: small connective words, big keyword ("que vocês **APRENDER** queiram").
- Minimal captions: ~58 px sentence case, no stroke, soft shadow — needs a calm background; switch to `hormozi` on busy scenes.
- Series/episode framing and "comenta PALAVRA" CTAs lift comments; put the word on screen big.
- Fonts bundled (OFL, commercial OK): Montserrat, Libre Baskerville Italic, Bebas Neue, Caveat. Cocogoose/Neulis/Fixture are commercial/trial fonts — only if the user owns a licence.

## 4. Sound effects
Sounds are **selective** (manual §5): only the key events — hook entrance, main card, proof/result, CTA — about
2 per 10 s at most, never on plain cuts (one sound per cut causes fatigue). ~−8 to −14 dB under the voice.
Which sound for which event:
| Event | SFX category (file prefix) | gain |
|---|---|---|
| Card / pill pops in | `pop` or `click` | −10 |
| Slide-in, whip, scene change | `whoosh` / `swoosh` | −8 |
| Flash cut | `flash` (camera shutter + flash) | −6 |
| Counter running | `tick` / `typing` | −14 |
| Big reveal / title | `riser` → `impact` | −8 |
| Positive result ("conta menor") | `ding` / `success` | −10 |
| Error / problem | `error` / `buzz` | −12 |
Keep a library in `~/reels-sfx/` named by category (`whoosh_01.wav`, `pop_soft.wav` …); the engine resolves
`sfx=[(t, "whoosh", -8)]` to the first match. Never download SFX without the user's OK — tell them what
to grab (below) and where to put it.

## 5. Colour grading
| Look | Recipe (engine GRADES) | Matches |
|---|---|---|
| clean_warm | lifted blacks, warm cream tint, contrast .9, sat .86 | authority, clinics, interiors |
| teal_orange | warm highlights / teal shadows, contrast 1.12 | personal brand, skin-forward |
| moody | darker mids, contrast 1.18, sat .82, strong vignette | reflective, night, practical lights |
| vivid_day | contrast 1.1, sat 1.15, slight warm | outdoor, events, product in daylight |
Rules: grade before graphics (engine does); keep skin natural (check faces in `looks.jpg`); match
graphic accent to the grade (cream look → gold/green accents, not neon yellow). For pro LUTs from
Motion Array/Artlist, the user can export .cube — not wired into the engine yet; approximate with a GRADES entry.

## 6. Camera angles & shot grammar
- Eye-level medium = authority/explanation. Low angle = confidence/scale (products, buildings). High angle = vulnerability/overview.
- Close-up on emotional or key words; extreme close-up (eyes) for 0.5–1 s max as punctuation.
- Dutch tilt (5–10°) = energy/unease, use on hooks and flash cuts only.
- Wide establishing shot first when location matters (trade show floor, plant, rooftop).
- Wide lens close to the face = intimate/vlog; long lens = premium/interview.
- When recording advice to the user: 2 framings of the same take (medium + close) make jump cuts feel multi-cam.
- Engine: punch-ins simulate close-ups; `ZOOM` + `RANGES` can't create real angle changes — note in the summary when a reshoot/B-roll would help.

## 7. Asset banks
| Bank | What for | Price (2026, annual) | Licence notes |
|---|---|---|---|
| Motion Array | video-first: templates (Premiere/AE/Resolve/FCP), motion graphics, SFX, music, LUTs, presets, stock footage up to 8K | ~US$24.99/mo | subscription; download while subscribed, licence per project |
| Envato Elements | biggest catalogue (26M+): templates, footage, music, SFX, **fonts**, graphics | ~US$16.50/mo | register each project to the licence |
| Artlist | premium music/SFX/footage/templates/LUTs, "Clearlist" for channel claims | ~US$39.99/mo | lifetime use of what you downloaded while subscribed |
| Mixkit (free) | SFX (whoosh, pop, transitions), music, footage | free | Mixkit SFX Free License: commercial OK, no attribution |
| Pixabay (free) | 110k+ SFX, music, stock video | free | Pixabay Content License: commercial OK, no attribution |
| Freesound (free) | huge SFX archive | free | per-file CC0 / CC-BY / CC-BY-NC — filter to CC0 or credit; avoid NC for business |
| Google Fonts (free) | OFL fonts (the bundled ones come from here) | free | OFL: commercial OK |
Suggested starter pack to ask the user for: Mixkit/Pixabay "whoosh", "pop", "click", "camera flash",
"riser", "impact", "ding" → `~/reels-sfx/`. Duotone stock cutaways (raele style): Motion Array / Envato "3D object loop", "money rain", "clock".

## 8. Out of scope for the engine (workarounds)
- Text behind the subject / 3D-tracked "immersive" text, subject-masked flash cut: need segmentation/tracking (CapCut "Remove background", Premiere Object Mask, After Effects 3D Camera Tracker). The engine's `flashes` is a full-frame approximation.
- Split screen with blurred seam, circular mask, PiP with border: doable in a project motion with PIL masks over `frame` — build only if the user asks; otherwise suggest them.
- LUT .cube files, templates (.mogrt/.aep): edited in the user's NLE; the skill can list which to use and where.
