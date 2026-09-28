# The conversation light, 28 September

Each of the three in the game where the encounter stands them, photographed three ways at ONE held exposure (fixed bias 0.2, matched to the street's own automatic exposure: F:/LedgerTools/tmp/sweep-0928), the same framing, face LOD 0, material quality High, shading Epic, subsurface scattering on:
front = the street's daylight as it is; talk = with the conversation light (ue-probe LedgerTalkLight.h); studio = with the portrait tool's key and fill.

Face brightness (mean luma of the face region, 0-255): Sheila 42 / 115 / 112; Ron 46 / 137 / 119; Darren 84 / 152 / 163.
Cost of the conversation light on the card: 0.33 ms (GPU time per frame, median of 120 frames off and 120 on; budget 0.5).
Sheila C1 and Darren C5 are the faces approved on 25 September, before the rebuild; Ron is P2.
Made with: -PortraitInGame -PortraitPair -PortraitHoldBias=0.2 [-PortraitCost].

## Made gentler, same day, evening

The blind reviewer failed the first pair: the two pictures differed in camera and background (the person turned between shots), and the lit face was about 3.4 times as bright as the brick behind it, where skin against red brick in the same daylight is about 1.5 to 2. Now each person's pair keeps its first camera and facing, and the key is 3 cd, or a quarter of that when the sun reaches the face (a line traced toward the sun). Face against the wall right behind (mean luma): Ron in shade 0.59 without the light and 1.95 with it (2 cd gave 1.68); Sheila in sun 1.45 without and 2.27 with (2 cd without the sun rule gave 2.95). rocco-front-3cd.jpg and rocco-talk-3cd.jpg are the new pair. Made with -PortraitInGame -PortraitPair -PortraitHoldBias=0.2 -TalkKeyCd=3.

## Settled from measurement, same evening

The reviewer failed the 3 cd pair too: measured in linear light (sRGB decoded), not screen values, the face was 3.9 times the wall, and flat (forehead against chin 1.2 to 1). Two tries spent, so the strength comes from measurement: a sweep from 45 degrees up (steeper, so the chin and neck stay darker than the forehead, as under the street's own light from above) at 1.0, 1.4 and 1.8 cd gave Ron 1.35, 1.61 and 1.85 times the wall in linear light on my patches, which read about 1.3 times lower than the reviewer's. Settled at a 1.2 cd key and a 1 cd eye light (the eye light's shine had lifted a sunlit face by a third at 2 cd), and no key at all on a face the sun reaches: Ron in shade 1.18 on my patches (about 1.5 on the reviewer's); Sheila in sun 2.17 unlit, 2.54 with the eye light alone. rocco-front-settled.jpg and rocco-talk-settled.jpg are the pair.

## Shadowed, same night

A third reviewer failed the 1.2 cd pair on hair: the key cast no shadow, so Ron's moustache went from near-black to sandy grey (14 times brighter in linear light) while the skin brightened far less; and the face was 2.0 to 2.6 times the wall on its patches. The key now casts shadows, deep shadows for hair included (only the person spoken to is on its channel, so only they cast into it), at 1 cd: Ron 0.94 on my patches, where the reviewer's larger patches read about twice mine. rocco-front-shadowed.jpg and rocco-talk-shadowed.jpg are the pair.

## Hair left out, unshadowed, 0.6 cd: same night

A fourth reviewer failed the shadowed pair: the moustache still brightened 8.5 times against 2.4 for the skin, and the face was 2.17 times the wall on its patches. And shadows cost 1.99 ms a frame on this card (budget 0.5). So the hair, brows, moustache and lashes are taken off the light's channel (they stay in the street's light only), the shadows are off again, and the key is 0.6 cd. Cost 0.20 ms (median of 120 frames off and on, key forced on). Ron 0.79 times the wall on my patches (the reviewers' larger patches read about twice mine); the moustache stays dark brown. rocco-front-final.jpg and rocco-talk-final.jpg are the pair.
