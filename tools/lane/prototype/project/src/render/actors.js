// One door for the figures: the rigged Quaternius people when their files have loaded, the drawn-in-code ones if not.
import { buildChar as buildOld, poseChar as poseOld, holdProp as holdOld } from './figures.js';
import { peopleReady, buildCharR, poseCharR, holdPropR, realiseChar } from './rig.js';
export { realiseChar };
export function buildChar(look, o) {
  if (peopleReady()) {
    try {
      const c = buildCharR(look, o);
      c.rigged = true;
      return c;
    } catch (e) {
      console.warn('rigged figure failed, using the simple one:', e.message);
    }
  }
  return buildOld(look, o);
}
export const poseChar = (c, a, dt) => (c.rigged ? poseCharR(c, a, dt) : poseOld(c, a, dt));
export const holdProp = (c, n) => (c.rigged ? holdPropR(c, n) : holdOld(c, n));
