// New kinds of act of the system "shops".
const n = (e) => e.name || 'a shopkeeper';
export const KINDS_ADD = {
  bought_coat: { sev: 0.25, val: 0.05, crime: 0, town: 'open', truth: (e) => `Tom bought ${e.what || 'a coat'} at ${e.shop || 'a shop'}`, mine: (e) => `Bought ${e.what || 'a coat'} at ${e.shop || 'a shop'}` },
  bought_tool: { sev: 0.3, val: -0.1, crime: 0, town: 'open', truth: (e) => `Tom bought ${e.what || 'a tool'} at the ironmonger's`, mine: (e) => `Bought ${e.what || 'a tool'} at the ironmonger's` },
  fenced: { sev: 0.55, val: -0.45, crime: 1, town: 'saw', truth: (e) => `Tom sold ${e.what || 'goods'} to ${n(e)} with no questions asked`, mine: (e) => `Sold ${e.what || 'goods'} to ${n(e)}, no questions` },
  walked_off: { sev: 0.2, val: -0.05, crime: 0, town: null, priv: 1, truth: (e) => `Tom walked away from ${n(e)}'s price`, mine: (e) => `Walked away from ${n(e)}'s price` },
  stitched: { sev: 0.5, val: -0.2, crime: 0, town: null, priv: 1, truth: () => 'Tom had a cut stitched by Dr Calvert, who asked nothing', mine: () => "Stitched at Dr Calvert's. He asked nothing and will remember" },
  haircut: { sev: 0.15, val: 0.05, crime: 0, town: 'open', truth: () => 'Tom had his hair cut on Copper Row', mine: () => 'Had a haircut on Copper Row' },
  washed_coat: { sev: 0.3, val: -0.1, crime: 0, town: 'open', truth: () => 'Tom put a coat through a service wash at the Washeteria', mine: () => 'Put the coat through a service wash. The attendant saw what was on it' },
  hired_brief: { sev: 0.4, val: 0, crime: 0, town: 'open', truth: () => 'Tom put a solicitor on call at the Corn Exchange', mine: () => 'A solicitor on call, Pym and Tasker at the Corn Exchange' },
};
