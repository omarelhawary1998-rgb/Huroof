# Song Review & Master — "Show Me All The Signs"

**Source:** `Show Me All The Signs (2).wav` (Google Drive) — 16-bit / 44.1 kHz stereo WAV, 3:12
**Reviewed & remastered:** 2026-07-16
**Estimated tempo:** ~107 BPM

---

## Fine-tuned masters (download links)

| File | Link |
|---|---|
| Mastered WAV (24→16-bit dithered, distribution-ready) | https://www.adobe.com/files/id/urn:aaid:sc:EU:20989514-01f5-459a-910a-267686a9b4b2 |
| Mastered MP3 (320 kbps, for sharing/demo) | https://www.adobe.com/files/id/urn:aaid:sc:EU:208318d9-241d-44aa-afa3-1ba652be67cf |
| 30-second hook clip (0:28–0:58, for TikTok/Reels/Shorts) | https://www.adobe.com/files/id/urn:aaid:sc:EU:073e2eb0-d559-4f31-b613-6e502c17a13a |

---

## Technical review of the original

Measured with EBU R128 loudness analysis and octave-band spectral analysis:

| Metric | Original | Issue |
|---|---|---|
| Integrated loudness | −12.9 LUFS | Slightly quiet vs. modern pop masters (−9 to −11 LUFS) |
| True peak | **−0.16 dBTP** | Too hot — lossy encoding (Spotify/YouTube Ogg/AAC) can push inter-sample peaks above 0 and cause audible distortion. Target is ≤ −1.0 dBTP |
| Loudness range (LRA) | 10.0 LU | Healthy dynamics — good |
| Digital clipping | None | Good |
| Stereo correlation | **0.98 (side −19.8 dB below mid)** | Mix is nearly mono. Modern pop/electronic records have a much wider image; narrow width makes a track feel small on headphones |
| 2–4 kHz (presence) | −19.3 dB rel. | Noticeably scooped — this band carries vocal intelligibility and "forwardness"; the dip makes vocals sit behind the instrumental |
| 8–16 kHz (air) | −17.3 dB rel. | Slightly dark top end |
| Low end (20–250 Hz) | Strongest region | Full, warm low end — kept as-is (genre-appropriate) |

### Structure / arrangement notes (energy map)

- **0:00–0:25 — intro is long and quiet** (−27 → −23 dB RMS). On streaming this risks skips; on short-form it's dead air. Consider an "intro edit" that reaches the first hook within ~10 seconds, or use the hook clip for all social content.
- **0:28–0:52 — first big section** (−14 dB RMS): strongest early moment; this is the hook-clip source.
- **1:00–1:30 — mid section dips slightly** and stays flat for ~30 s; a drum drop-out or riser around 1:15 would add contour.
- **1:35–1:58 and 2:35–3:00 — choruses land well**; final chorus is the loudest moment of the song (good).
- **3:00–3:12 — quick fade-out ending.** Fine for streaming; a hard ending would loop better on TikTok.

## What was changed in the new master

Conservative mastering moves only (no destructive processing, original dynamics preserved):

1. **Presence lift:** +3 dB bell @ 2.9 kHz (wide Q) — brings the vocal forward.
2. **Mud control:** −1.2 dB bell @ 200 Hz — cleans the low-mids slightly.
3. **Air:** +1.5 dB high shelf @ 9.5 kHz — opens the top end.
4. **Stereo width:** side level raised ~+4 dB (side/mid −19.8 → −14.8 dB). Mono compatibility preserved (correlation still 0.94).
5. **Loudness:** +2.2 dB gain into a 4×-oversampled true-peak limiter.

| Metric | Original | New master |
|---|---|---|
| Integrated loudness | −12.9 LUFS | **−11.3 LUFS** |
| True peak | −0.16 dBTP | **−1.03 dBTP** (streaming-safe) |
| LRA | 10.0 LU | 7.7 LU (still dynamic) |
| Presence (2–4 kHz) | −19.3 dB rel. | −16.8 dB rel. |
| Air (8–16 kHz) | −17.3 dB rel. | −16.8 dB rel. |
| Side/mid width | −19.8 dB | −14.8 dB |

## Recommendations that need the session files (can't be done from the stereo master)

- Re-balance the lead vocal +1 dB in the mix rather than relying on master-bus EQ.
- Pan/widen doubles, pads and hats in the mix for real stereo width.
- Tighten the intro to ≤10 s or record a cold-open vocal version.
- Consider a hard ending (or both versions: streaming fade + looping edit for social).

## Music video (Neon Multiverse visualizer)

An audio-reactive music video was produced from the mastered track, following the
"Neon Multiverse" storyboard's palette (hot pink / electric purple / neon cyan / gold),
pacing, and sync points — portal opening on the intro build, radial spectrum montage,
heart-shaped shockwaves on the final chorus, and a spray-on glitter title card at the end.
The storyboard's Marvel/Barbie character shots were deliberately **not** used: trademarked
characters in a promotional video would risk takedowns and rights issues; the visualizer is
100% original content, safe to publish on all platforms.

| File | Link |
|---|---|
| Full visualizer, 1280×720 (3:12) | https://www.adobe.com/files/id/urn:aaid:sc:EU:4ab2505b-b7f6-42af-9732-0fd957dd3c06 |

A vertical 9:16 hook-clip video (0:28–0:58) was also produced for TikTok/Reels/Shorts.
Both can be regenerated or restyled with `tools/render_music_video.py`
(requires: numpy, scipy, Pillow, ffmpeg; place the mastered WAV next to the script):

```
python3 render_music_video.py wide      # full 16:9 video
python3 render_music_video.py vertical  # 30s 9:16 hook clip
```

See `SONG_PROMOTION_PLAN.md` for the release and growth strategy.
