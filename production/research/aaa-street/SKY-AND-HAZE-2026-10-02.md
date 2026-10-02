# Sky and haze: clouds that show, light and haze that stay

2 October 2026, research helper, 25 minutes. D: a source says it; I: inference. Epic's pages are labelled UE 5.8, undated.

**The setup today (from the code):** a 2 km unlit dome with Is Sky on, at 15 times brightness. The sky light is Captured Scene with real-time capture, which photographs Is Sky meshes, the Sky Atmosphere and the height fog [D2]: the dome is the light. The day fog is four times the base density from 15 m, with its opacity cap tripled, up to 1.

## 1. Why the clouds vanish

- **The fog covers the dome.** Is Sky turns off aerial perspective "but does apply height and volumetric fog" [D3]. At 1 km the dome is far past the point where the fog reaches its cap, so the sky turns flat fog grey; dimming the dome only dims what shows through [I].
- **Epic's fix is Fog Cutoff Distance:** past it "will not have fog applied. This is useful for excluding skyboxes" [D1]. Set it inside the dome and beyond the farthest hill.
- **Other fog settings.**
  - Start Distance does nothing at 1 km [I].
  - Max Opacity below 1 still veils the sky [I].
  - Volumetric fog ignores all three [D4]: keep it off by day.
  - Directional Inscattering glows over the sky too; black for overcast [D1, I].
- **Is Sky already keeps the Sky Atmosphere's haze off** [D3, D8]. A translucent sky with "Apply Fogging" off also works, but is messier [D7, I].
- **The horizon.** Inscattering Color Cubemap colours fog from a cubemap [D1]; given the same photo, far roofs fade into the sky [I].

## 2. Separating the seen sky from the light

- **A, cheapest, keeps the code's design.** A sky light's light is "the pixel intensity multiplied by the light intensity" [D9]. Dim the dome by a factor and raise the sky light by the same factor: the street stays as it is [I].
- **B.** The sky light uses a Specified Cubemap of the same photo; the dome is set on its own [D5, D6]. No real-time capture needed.
- **Not these.** The HDRI Backdrop's one Intensity drives both light and backdrop [D10]. Volumetric clouds are built for time of day, overkill for a fixed overcast [D11, I].
- **Lumen's screen traces** sample the frame [D12], so the dome may add some bounce light [I].

## 3. Making clouds read in a bright sky

- Overcast clouds differ by about a stop; this photo is "low-contrast" [D13]. High on the tone curve's shoulder, that stop squeezes to white [I].
- Under fixed exposure, set the brightest cloud below the shoulder, measured with Pixel Inspector [D14]. Real clouds run 400 to about 10,000 cd/m² [D14].
- Leave the tone mapper alone, as "film stock" [D14].
- **Local Exposure** (Post Process, Lens): Highlight Contrast 0.6 to 1 lowers bright areas and keeps their detail [D15].
- At 1440p the dome needs about an 8K panorama [I]; a Max Texture Size cap makes it soft [D6].

## 4. Cost on an RX 6700 at 60 fps

- **Dome:** almost nothing [I]. **Fog:** a far start cuts its cost to "50% or less" [D1].
- **Real-time capture:** 0.20 ms a frame at most on PS4, spread over nine frames [D2]; a fixed overcast does not need it [I].
- **Volumetric clouds:** no Epic figure [D11]; one artist reports 1 to 2 ms on an RTX 3080 Ti at 1440p [D16]. An RX 6700 is slower [I].
- **Texture memory (arithmetic) [I]:** an 8K panorama in 16-bit float is about 256 MB plus a third for mips; HDR Compressed (BC6H) [D6] about 32 MB; 16K four times either.
- **Seam:** mips can draw a line where the panorama wraps; use no mips or the Skybox texture group [D17].

## What to try first

1. **Test, minutes:** the hook frame with Fog Cutoff at 900 m. Clouds appear: fog was the cause; if not, exposure or texture.
2. **Fog:** Cutoff inside the dome and past the hill; inscattering black; volumetric fog off by day.
3. **Option A:** dim the dome until clouds read; raise the sky light by the same factor.
4. **Local Exposure:** Highlight Contrast about 0.8.
5. **Fog colour:** from the photo's horizon, or the Inscattering Color Cubemap.
6. **Option B:** Specified Cubemap; capture off, about 0.2 ms saved.
7. **Texture:** 8K, HDR Compressed, not capped.

Only after these: volumetric clouds, at 1 to 2 ms or more.

## Sources

- D1 Epic, Exponential Height Fog. https://dev.epicgames.com/documentation/en-us/unreal-engine/exponential-height-fog-in-unreal-engine
- D2 Epic, Sky Lights. https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-lights-in-unreal-engine
- D3 Epic, Sky Atmosphere Component. https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-atmosphere-component-in-unreal-engine
- D4 Epic, Volumetric Fog; forum, 25 June 2020. Summary only. https://dev.epicgames.com/documentation/unreal-engine/volumetric-fog-in-unreal-engine
- D5 World of Level Design, 15 February 2025. https://www.worldofleveldesign.com/categories/ue5/hdri-lighting-guide.php
- D6 HDRI Skybox, undated. https://www.hdriskybox.com/guides/hdri-in-unreal-engine
- D7 Epic forum, answer 30 January 2024. https://forums.unrealengine.com/t/how-to-make-exponential-height-fog-ignore-the-skysphere/146398
- D8 Epic forum, March to October 2025. https://forums.unrealengine.com/t/skysphere-gets-washed-out-by-sky-atmosphere-whats-the-intended-workflow/2409104
- D9 Epic, Physical Lighting Units. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine
- D10 Epic, HDRI Backdrop. https://dev.epicgames.com/documentation/en-us/unreal-engine/hdri-backdrop-visualization-tool-in-unreal-engine
- D11 Epic, Volumetric Cloud. https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-cloud-component-in-unreal-engine
- D12 Epic, Lumen GI and Reflections. https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- D13 Poly Haven, belfast_open_field (CC0). https://polyhaven.com/a/belfast_open_field
- D14 B. Leleux, 80.lv, 13 July 2018, older than asked. https://80.lv/articles/setting-lighting-in-unreal-engine-4-20
- D15 Epic, Auto Exposure. https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-exposure-in-unreal-engine
- D16 ArtStation, undated; summary only. https://www.artstation.com/artwork/4NGvNn
- D17 S. Streeting, 6 April 2021; summary only. https://www.stevestreeting.com/2021/04/06/skyboxes-in-ue4/
