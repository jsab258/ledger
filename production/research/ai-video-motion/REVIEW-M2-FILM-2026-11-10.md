# Review: m2 solve film beside its source (n09-8), 10 Nov 2026

A fresh reviewer read every 4th composed frame (1 to 80), full-size front and side views at frames 1, 40 and 80, enlarged heads at 14 frames and feet every 8th frame, and tracked head, feet and shoulder pixels on all 81 frames (about 3.2 mm a pixel at the body; figure 1.69 m over about 530 px).

## Findings

1. **Foot slide: none.** Toe tips and feet stay within 1 to 6 px (under 2 cm) over all 81 frames in both views. **But the feet are wrong**: in every frame both feet point toes-down by roughly 30 to 45 degrees (side view, frames 1 to 81), so the heels sit several cm off the floor. The source stands flat-footed throughout. (The grid is drawn at the lowest point, so "touching" here means only the toe tips.)
2. **Jitter: very low.** Frame-to-frame second differences average under 1 px for head and feet; worst single step 4 to 9 px at one toe tip (front, near frames 1 and 73), which looks like a mask edge. The motion reads as smooth.
3. **Legs and posture do not match.** The source stands with both legs straight. The solve bends the right knee with the shin angled out (front, all frames) and the left knee about 25 degrees forward (side, all frames). This holds over the whole clip, so it is a fixed pose offset, not drift.
4. **Arms**: they hang at hip height like the source's, but with elbows a little bent and held out (front, frames 1 to 81). In the side view the near (right) arm and clavicle swing back about 6 cm during the turn (frames 17 to 65, back by 73). The source's arms barely move.
5. **Head timing matches**: the head moves from frame 2, holds from about 15 to 60, and is back by about 75. The source turns from about frame 5 to 13 and returns by 73 to 77. **Direction probably wrong**: the source turns to his left. In the solve the back-of-head marker swings to the viewer's right in the front view (frames 12 to 60), and the right arm going back fits a turn to his right. Both point to a mirrored turn. Confidence is moderate, because the head is a plain ball with no face mark; a nose marker would settle it.
6. **Slow drift**: in the side view the head moves steadily backward by about 5 cm from frame 1 to 81 (307 to 290 px) and never comes back. Over a looped idle this would show as a jump.
7. **Shoulders**: the torso does not turn with the head (as the numbers already say). Only the right arm moves.

## Verdict

**USABLE AFTER CLEAN-UP, head and neck only.** The clean-up: keep the head and neck curves; check the turn's direction and mirror it if confirmed; take out the backward drift; put the legs, feet and torso on a clean idle base (or lock the feet flat with IK and straighten the knees); add a small share of the turn to the shoulders by hand.

The method is worth pursuing for head turns and small upper-body gestures, since the timing is right and the motion is smooth. It is not worth pursuing for the legs or feet from a single front camera.
