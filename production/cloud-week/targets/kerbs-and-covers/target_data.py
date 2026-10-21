"""Data blocks for target.json (sources, photograph measurements, decisions, variants, wear, checks, probes).
Imported by make_target.py.  Millimetres.  Dates are 2026-10-09 (read) and 2019 (taken)."""

READ = '2026-10-09'

PH_NOTE = ('Poly Haven (polyhaven.com), asset licence CC0 (read at https://polyhaven.com/license on 9 October 2026: "All assets ... licensed as CC0"). '
           'Photographs for measuring only; not placed in the game, not traced into a texture, not fed to an image model.')


def sources():
    s = []

    def ph(id_, url, author, taken, coords, shows, used, period, same):
        s.append({'id': id_, 'url': url, 'date_read': READ, 'author': author, 'licence': 'CC0 1.0 (Poly Haven)', 'date_taken': taken,
                  'coords': coords, 'shows': shows, 'used': used, 'period_or_replacement': period, 'same_in_1990': same})

    ph('S1', 'https://polyhaven.com/a/urban_street_03 ; files via https://api.polyhaven.com/files/urban_street_03 (8k tone-mapped JPG)',
       'Andreas Mischok', '2019-09-07 07:46 UTC (published 2019-09-26)', [51.481339, 0.006877],
       'An overcast Victorian terrace street in south-east London (south-east London, near the Greenwich meridian): granite kerbs with a granite-sett channel, a vehicle crossing with a concrete ramp, granite flank strips and a row of setts as the lip, rust-brown cast-iron gully grates, a large recessed utility cover in the footway, patched flags. THE MAIN PHOTOGRAPH.',
       'yes (main)',
       'Mixed. The granite kerbs, setts and cast-iron grates are period-type objects (Victorian to 1970s, laid long before 1990); the concrete ramp looks 1970s-80s (weathered exposed aggregate); the yellow lines and the car are 2019.',
       'Granite kerbs and sett channels were laid in the 19th and early 20th century and kept; cast-iron gratings to BS 497 (1976) were the 1990 norm; vehicle crossings with a concrete ramp and granite or concrete flanks were common in the 1970s-80s. Differences in 1990: the stone would be sootier and the channel dirtier; no 2000s dropper-block crossing with tactile blisters; no ductile-iron hinged grates.')
    ph('S2', 'https://polyhaven.com/a/urban_street_01 ; files via api.polyhaven.com', 'Andreas Mischok', '2019-08-18 07:09 UTC', [51.528295, -0.053879],
       'A resurfaced Bethnal Green street with a new granite build-out: granite kerb blocks, a mitred corner (about 133 degrees), a planter kerb.',
       'yes (corner)', 'REPLACEMENT: the kerbs are new (2010s sawn-top granite, cleaner than 1990); the form (mitred corner, joint width, block length) is period.',
       'Granite kerb corners were mitred or cut to radius in the same way for a century; in 1990 they would be older, chipped and dirtier.')
    ph('S3', 'https://polyhaven.com/a/urban_street_02', 'Andreas Mischok', '2019-08-18 06:45 UTC', [51.526655, -0.056465],
       'An estate road: a square cover filled with tarmac (hairline outline, grass at the corners).', 'yes (tarmac-filled recessed cover)',
       'Period-type object, old tarmac.', 'Recessed covers re-surfaced with tarmac are 1970s-1990s practice; it looks the same.')
    ph('S4', 'https://polyhaven.com/a/urban_street_04', 'Andreas Mischok', '2019-09-14 12:58 UTC (sunlit)', [51.511786, -0.201884],
       'A Notting Hill / Bayswater street: a large-radius granite kerb corner, a long two-leaf studded cover in the carriageway, a small recessed footway cover.',
       'yes (corner radius, road cover, small cover)',
       'Granite kerb is Victorian; the road cover is utility ironwork of unknown age (a reinstatement patch around it).',
       'Studded steel or iron utility covers in a pale mortar surround are 1960s-90s; a London-smart street, so the wear is cleaner than a port town\'s.')
    ph('S5', 'https://polyhaven.com/a/bethnal_green_entrance', 'Andreas Mischok', '2019-08-18 07:01 UTC', [51.526915, -0.054044],
       'A block-paved estate entrance with a double-triangular square stud-pattern cover (two leaves split on a diagonal, 10 x 10 studs; the cover is 0.9 m from the nadir, so its size is +-8 %).',
       'yes (stud cover)', 'The block paving is 1990s-2000s; the cover is older ironwork re-set in it.',
       'Cast square-stud treads are 1960s-80s; same.')
    ph('S6', 'https://polyhaven.com/a/birbeck_street_underpass', 'Andreas Mischok', '2019-08-18 06:53 UTC', [51.525806, -0.056277],
       'A tarmac street under a railway arch: a pale concrete bullnosed kerb with a worn aggregate top, kerb-face yellow marks, a cast-iron gully grate with oval-trimmed slots.',
       'yes (concrete kerb, second grate)', 'Concrete kerb probably 1970s-90s; grate probably 1980s or later (rust-brown cast iron).',
       'Concrete bullnosed kerbs were laid from the 1960s; the grate type is BS 497 (1976) style; same in 1990, newer-looking.')
    ph('S7', 'https://polyhaven.com/a/metal_grate_rusty ; https://api.polyhaven.com/files/metal_grate_rusty (2k diffuse)',
       'Photography Dimitrios Savva, processing Rob Tuytel', 'published 2022-07-07 (taken date not given)', None,
       'A 500 mm tile of a rusty cast tread plate (raised alternate horizontal and vertical lugs).', 'yes (lug pattern, measured by autocorrelation)',
       'A scan of real ironwork of unknown age.', 'Lug treads of this type are 20th-century iron.')
    ph('S8', 'https://polyhaven.com/a/water_manhole_cover ; https://api.polyhaven.com/files/water_manhole_cover (glTF 1k and .bin)',
       'Raunox', 'published 2023-11-08 (a modelled asset, not a photograph)', None,
       'A weathered round cast-iron manhole cover model: 690.76 x 690.76 x 67.62 mm, lid radius about 294 mm. Its texture atlas is not used.',
       'yes (frame and lid sizes only)', 'Modelled asset.', 'A 600 class round cover with a 690 frame is 20th-century standard.')
    s.append({'id': 'S9', 'url': 'repository: production/cloud-week/targets/SCENE-SLOTS.md; production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md; '
              'production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/research/street-wear/WET-ROAD-2026-10-08.md; '
              'production/cloud-week/targets/wear/TARGET.md and target.json', 'date_read': READ, 'author': 'the project', 'licence': 'the project\'s own',
              'date_taken': '2026-09-29 to 2026-10-08', 'shows': 'the street\'s present kerb, channel, gully and crossover; the asset plan\'s kerb and cover rows; the wear target\'s channel and grate numbers',
              'used': 'yes (Read numbers)', 'period_or_replacement': 'n/a', 'same_in_1990': 'n/a'})
    s.append({'id': 'S10', 'url': 'WebSearch result summaries (9 October 2026): BS 7263 Part 1 (1990) kerb types HB2, BN2, BN3 and dropper kerbs; BS 497 Part 1 (1976) manhole covers, road gully gratings and frames, superseded 1994 by BS EN 124; tactile blister paving first laid in Parliament Square in 1983, the Department\'s guidance dated 1998',
              'date_read': READ, 'author': 'search summaries of third-party pages (NBS Source, a kerb supplier, Southwark and Edinburgh councils, BSI shop pages, CIHT and Euroblind articles, trid.trb.org)',
              'licence': 'n/a (leads only)', 'date_taken': 'n/a', 'shows': 'leads', 'used': 'NO numbers taken except where a line says "lead"; none changed a photograph-based number',
              'period_or_replacement': 'n/a', 'same_in_1990': 'n/a'})
    s.append({'id': 'S11', 'url': 'https://polyhaven.com/a/docklands_01 and docklands_02 ; limehouse', 'date_read': READ, 'author': 'Savva Zakharov (docklands); Andreas Mischok (limehouse)',
              'licence': 'CC0 1.0 (Poly Haven)', 'date_taken': '2025-03-11 and 2025-03-20 (docklands); 2019-05-19 (limehouse)',
              'coords': [53.346038, -6.237996], 'shows': 'Docklands: granite setts and recessed covers on a quay; the coordinates 53.346, -6.238 are DUBLIN, not Britain. Limehouse: block paving, cast bollards, chain.',
              'used': 'NO. Looked at and left out: Dublin is not a British street (its covers and setts carry Irish ironwork); Limehouse is a clean 1980s-90s development.',
              'period_or_replacement': 'n/a', 'same_in_1990': 'n/a'})
    return s


def unreached():
    return [
        {'what': 'Wikimedia Commons, Geograph, Flickr, archive.org, Historic England, Hathitrust, National Archives', 'result': 'refused (connection 403/000) from this cloud on 9 October 2026', 'used': 'nothing'},
        {'what': 'gov.uk and assets.publishing.service.gov.uk (the Department\'s tactile paving guidance of 1998, Inclusive Mobility)', 'result': 'refused; only search summaries seen', 'used': 'nothing (a lead for "no tactile paving in 1990")'},
        {'what': 'BSI knowledge and shop pages (BS 7263, BS 340, BS 435, BS 497)', 'result': 'refused; only search summaries seen', 'used': 'nothing (leads)'},
        {'what': 'ambientCG manhole-cover and grate scans (ManholeCover001 to 011, Grate001, Grate002; CC0)', 'result': 'the catalogue API answered but every download (ambientcg.com/get?file=...) was refused with 403', 'used': 'nothing'},
        {'what': 'Sketchfab, Pexels, Unsplash', 'result': 'refused', 'used': 'nothing'},
    ]


def photo_measurements():
    ASS = 'urban_street_03'
    pms = []
    pms.append({
        'id': 'PM01', 'what': 'granite kerb section, block at the crossing\'s right end', 'photo': ASS, 'taken': '2019-09-07', 'method': 'pano_depression',
        'raw': {'view': {'yaw': 281, 'pitch': -21, 'fov': 16, 'w': 1600, 'h': 1000}, 'rows': {'foot': 640, 'arris_mid': 490, 'rear': 405}, 'assumed_upstand_mm': 115},
        'reading': 'rows read on a gridded view (ph-urban_street_03-kerb-end-flank-view.jpg); foot = bottom of the dark face, arris_mid = middle of the light-to-dark rounding, rear = the dark joint behind the top',
        'error': 'rows +-8 (about +-0.08 degree): upstand +-12 mm, top width +-20 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM02', 'what': 'granite kerb section, straight run', 'photo': ASS, 'taken': '2019-09-07', 'method': 'pano_depression',
        'raw': {'view': {'yaw': 100, 'pitch': -22, 'fov': 18, 'w': 1600, 'h': 1000}, 'rows': {'foot': 530, 'arris_mid': 403, 'rear': 326}, 'assumed_upstand_mm': 115},
        'reading': 'luminance profile over columns 850 to 1050: top 125 to 145 grey levels, drop to 54 at rows 396 to 410, face 47 to 57, rear joint 90 at rows 316 to 322',
        'error': 'foot row +-15 (the shaded foot is soft): upstand +-15 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM03', 'what': 'concrete bullnosed kerb section (Birbeck Street)', 'photo': 'birbeck_street_underpass', 'taken': '2019-08-18', 'method': 'pano_depression',
        'raw': {'view': {'yaw': 150, 'pitch': -22, 'fov': 18, 'w': 1600, 'h': 1000}, 'rows': {'foot': 810, 'arris_mid': 690, 'rear': 600}, 'assumed_upstand_mm': 95},
        'reading': 'rounded top, no sharp arris; foot lost in a dark band', 'error': 'upstand +-15 mm, width +-25 mm (a worn, re-surfaced kerb)', 'kind': 'Photo'})
    pms.append({
        'id': 'PM04', 'what': 'granite block lengths along the straight run (three whole blocks)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [337, 279, 381], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'kerb top, camera 1.5 m, run rotated 5 degrees (x1.004 ignored)'},
        'reading': 'joint to joint along the kerb top', 'error': '+-30 mm each', 'kind': 'Photo'})
    pms.append({
        'id': 'PM05', 'what': 'kerb joint width', 'photo': ASS, 'taken': '2019-09-07', 'method': 'angular_width',
        'raw': {'px': 12, 'fov_deg': 18, 'w_px': 1600, 'distance_mm': 3900}, 'reading': 'dark open joint in the kerb top, view yaw 100 pitch -22 fov 18', 'error': '+-3 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM06', 'what': 'channel width, kerb foot to asphalt edge (granite sett channel)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'rows_height_corrected',
        'raw': {'foot_row': 403, 'edge_row': 474, 'edge_z_mm': 6},
        'reading': 'foot row 403 (the base of the lip row; the soft shadow under the kerb starts to rise there); asphalt edge row 474 = the steepest brightness change, over columns 330 to 1100; the asphalt edge stands about 6 mm up so it is smeared outward 1600/1594',
        'error': '+-15 mm; the asphalt overlay may have narrowed the channel', 'kind': 'Photo'})
    pms.append({
        'id': 'PM07', 'what': 'lip setts along the kerb (seven whole setts)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [65, 55, 55, 65, 65, 50, 45], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'ground'}, 'reading': 'joint to joint, blue-grey and pale setts', 'error': '+-9 mm each', 'kind': 'Photo'})
    pms.append({
        'id': 'PM08', 'what': 'lip row depth across the kerb (front top edge to the back joint centre)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [42], 'mm_per_px': 3.0, 'plane_factor': 0.9906, 'plane': 'ground; the lip top is 15 mm up, so lengths read 1.0094 too long'},
        'reading': 'rows 351 (dark joint centre) to 393 (front top edge) on the main frame: 42 px', 'error': '+-9 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM09', 'what': 'lip upstand from the dark band under it', 'photo': ASS, 'taken': '2019-09-07', 'method': 'smear_height',
        'raw': {'smear_mm': 30, 'distance_mm': 3900}, 'reading': 'a vertical face of height h at distance d smears d*h/(1.6 m - h) outward in the ground ortho; the dark band under the lip row is 10 px = 30 mm',
        'error': '+-8 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM10', 'what': 'crossing: gap between the two kerb block ends', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_two_edges',
        'raw': {'px0': 185, 'px1': 900, 'mm_per_px': 3.0, 'plane': 'kerb top, camera 1.475 m'}, 'reading': 'end faces at columns 185 and 900 of the top frame', 'error': '+-30 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM11', 'what': 'crossing: ramp back edge, distance behind the kerb foot', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_rows_to_distance',
        'raw': {'rows': [403, 95], 'edge_z_mm': 120, 'plane_z_mm': 125, 'note': 'row 403 = foot line in the ground frame; row 95 = ramp back edge in the top frame (horizontal distances, both true; the edge at the flag level is drawn 0.3 % too near on the kerb-top plane, corrected)'},
        'reading': 'distance from camera = 5000 - 3 * row (mm); the difference is the ramp back edge behind the foot line', 'error': '+-40 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM12', 'what': 'flank strip width and length (left and right)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [57, 47, 250, 235], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'footway level, camera 1.475 m'},
        'reading': 'stone widths between the joints on the top frame: left 57 px (171 mm: cols 78 to 135), right 47 px (140 mm: cols 900 to 947); lengths 250 and 235 px (left, right)', 'error': '+-12 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM13', 'what': 'gully grate A overall (along the kerb, across)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [163, 108], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'ground'}, 'reading': 'columns 205 to 368, rows 437 to 545 of the main ground frame', 'error': '+-9 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM14', 'what': 'gully grate A slot field and slot pitch', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [289, 190, 38], 'mm_per_px': 1.5, 'plane_factor': 1.0, 'plane': 'ground'},
        'reading': 'CORRECTED after the review: slot field 289 px on the 1.5 mm preview (columns 170 to 459, first slot left edge to last slot right edge: 433 mm; the first reading, 278 px, took the first slot\'s left edge 6 px too far in), slot length 190 px, mean slot pitch 38 px (slot centres at 182, 218, 258, 297, [335 hidden under a leaf], 372, 410, 448); 8 slots. Slot widths at half level 25.5 to 34.5 (median 28.5) and bars 24 to 28.5 (PM28)', 'error': '+-3 mm on pitch; +-8 on lengths', 'kind': 'Photo'})
    pms.append({
        'id': 'PM15', 'what': 'grate B slot pitch (Birbeck Street) from the perspective view', 'photo': 'birbeck_street_underpass', 'taken': '2019-08-18', 'method': 'angular_width',
        'raw': {'px': 108, 'fov_deg': 12, 'w_px': 1400, 'distance_mm': 3550}, 'reading': 'seven slots at columns 330, 430, 530, 650, 760, 880, 990 of a 1400 px wide, 12 degree view (yaw 0.96, pitch -23; the preview is the same view reduced to 1200 px); pitch about 108 px; the slots stand about square to the view, so no foreshortening is applied', 'error': '+-6 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM16', 'what': 'corner radius, circle fit to the yellow line of the corner', 'photo': 'urban_street_04', 'taken': '2019-09-14', 'method': 'circle_fit_px',
        'raw': {'points_px': [[650, 470.5], [700, 471.0], [740, 471.0], [780, 465.0], [820, 457.5], [860, 445.5], [900, 429.5], [940, 412.0], [980, 387.5],
                              [1030, 361.5], [1070, 336.5], [1110, 305.0], [1150, 266.5], [1190, 222.5]],
                'mm_per_px': 10.0, 'line_offset_mm': 200, 'plane': 'ground, yaw 135, 10 mm a pixel'},
        'reading': 'yellow line centre line found per column by colour, circle fitted by least squares; the line stands about 0.2 m off the kerb', 'error': '+-0.6 m', 'kind': 'Photo'})
    pms.append({
        'id': 'PM17', 'what': 'stud cover: lattice pitch', 'photo': 'bethnal_green_entrance', 'taken': '2019-08-18', 'method': 'lattice_vectors_px',
        'raw': {'a_px': [62, 20], 'b_px': [-18, 58], 'mm_per_px': 1.5}, 'reading': 'neighbouring studs on the rectified ortho (1.5 mm a pixel); the two vectors are at right angles (a square lattice)', 'error': '+-8 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM18', 'what': 'stud cover: outer edges', 'photo': 'bethnal_green_entrance', 'taken': '2019-08-18', 'method': 'edge_lengths_px',
        'raw': {'edges_px': [[630, 175], [-165, 570]], 'mm_per_px': 1.5}, 'reading': 'top edge and right edge of the cover on the 1.5 mm ortho, 0.9 m from the nadir; CORRECTED after the review: the top edge runs about 650 px along (the first reading, 515, was short), giving about 980 x 920 mm', 'error': '+-70 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM19', 'what': 'recessed utility cover in the footway: outer and infill', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [394, 223, 320, 140, 42], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'footway, camera 1.48 m'},
        'reading': 'outer 394 x 223 px, infill 320 x 140 px, left rim 42 px; 7 m from the camera, so across-the-kerb sizes are +-100 mm', 'error': '+-50 mm along, +-100 mm across', 'kind': 'Photo'})
    pms.append({
        'id': 'PM20', 'what': 'tarmac-filled recessed cover', 'photo': 'urban_street_02', 'taken': '2019-08-18', 'method': 'ortho_px_list',
        'raw': {'px': [340, 355], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'ground'}, 'reading': 'hairline outline columns 300 to 640, rows 440 to 795', 'error': '+-40 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM21', 'what': 'two-leaf studded road cover', 'photo': 'urban_street_04', 'taken': '2019-09-14', 'method': 'ortho_px_list',
        'raw': {'px': [456, 150], 'mm_per_px': 4.0, 'plane_factor': 1.0, 'plane': 'ground, 7.3 m away'}, 'reading': 'long axis and width on a 4 mm ortho 7 m away', 'error': '+-150 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM22', 'what': 'yellow line width on the 1.6 m picture (NOT a calibration: see calibration_data.py; 64 to 82 mm by the way it is read)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [24], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'ground'}, 'reading': 'rows 548 to 572 at column 900 of the 1.6 m picture; read by area over length the line is 64 mm, by the review\'s edges 76 to 82: a ragged painted line cannot fix a camera height (for a 75 mm line it gives 1.46 to 1.87 m); the bricks and a tyre decide it', 'error': '+-5 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM23', 'what': 'tread pattern cell (Poly Haven metal_grate_rusty, 500 mm tile)', 'photo': 'metal_grate_rusty', 'taken': 'n/a', 'method': 'listed',
        'raw': {'results': {'period_x_mm': 71.4, 'period_y_mm': 83.5, 'row_spacing_mm': 41.75, 'row_shift_mm': 35.7, 'lug_mm': [36, 10.5]}, 'how': 'autocorrelation of the 2k diffuse (axis peaks 71.3 and 83.5 mm) and, after the review, lug centres read off the 1k displacement map: rows 41.75 apart, a horizontal and a vertical lug alternating every 35.7 along a row, each row shifted 35.7'},
        'reading': 'FFT autocorrelation peaks at 292 px (71.3 mm) and 342 px (83.5 mm) took only the axis peaks and missed the centred lattice; the lug centres on the displacement map give 2 horizontal and 2 vertical lugs per 71.4 x 83.5 cell', 'error': '+-2 mm', 'kind': 'Photo (a texture scan of real ironwork)'})
    pms.append({
        'id': 'PM24', 'what': 'round cover model: outer diameter, depth, lid radius', 'photo': 'water_manhole_cover', 'taken': 'n/a', 'method': 'listed',
        'raw': {'results': {'outer_diameter_mm': 690.76, 'depth_mm': 67.62, 'lid_radius_mm': 294.1, 'ring_inner_radius_mm': 313.4}, 'how': 'glTF 1k, positions in metres read from the .bin'},
        'reading': 'vertex rings at radius 294.1, 313.4, 345.4 mm', 'error': 'exact (a model)', 'kind': 'Read (a model\'s geometry, not a photograph)'})
    pms.append({
        'id': 'PM25', 'what': 'granite kerb, face line to the rear joint, on the kerb-top plane', 'photo': ASS, 'taken': '2019-09-07', 'method': 'ortho_px_list',
        'raw': {'px': [63], 'mm_per_px': 3.0, 'plane_factor': 1.0, 'plane': 'kerb top, camera 1.475 m'},
        'reading': 'top frame, right block: the dark fall of the arris is centred at row 400 and the face line is row 403; the rear joint\'s front edge is row 340: 63 px; the light top alone is rows 340 to 397 (171 mm)',
        'error': '+-9 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM26', 'what': 'granite kerb: how far the middle of the arris stands behind the foot line (a battered face)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'setback_from_rows',
        'raw': {'foot_row': 403, 'edge_row': 399.5, 'edge_z_mm': 117.7, 'plane_z_mm': 125},
        'reading': 'top frame: the middle of the light-to-dark fall over the right block is row 399.5 (rows 394 to 406 over columns 959 to 1109); on the kerb-top plane a point 7 mm lower is drawn 0.5 % nearer, which is corrected; foot row 403 on the ground frame',
        'error': '+-9 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM27', 'what': 'mitred granite corner: interior angle (urban_street_01)', 'photo': 'urban_street_01', 'taken': '2019-08-18', 'method': 'corner_angle',
        'raw': {'dirs_deg': [57, 11], 'dirs2_deg': [61, 14.5], 'note': 'on the 3.5 mm ground ortho ph-urban_street_01-kerb-mitred-corner-ortho.jpg: the kerb\'s road edges run at 57 and 11 degrees, the yellow lines at 61 and 13 to 16 (the review\'s readings)'},
        'reading': 'interior angle = 180 minus the difference of the two runs\' directions: 134 from the kerb edges, 133.5 from the yellow lines', 'error': '+-5 degrees', 'kind': 'Photo'})
    pms.append({
        'id': 'PM28', 'what': 'grate A: slot and bar widths on the 1.5 mm preview (the review)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'listed',
        'raw': {'scale_with_height': True, 'results': {'slot_width_median_mm': 28.5, 'slot_width_min_mm': 25.5, 'slot_width_max_mm': 34.5, 'bar_width_min_mm': 24.0, 'bar_width_max_mm': 28.5, 'black_fraction': 0.41},
                'how': 'at half level across the slots on ph-urban_street_03-gully-grate-ortho.jpg; on a second ortho the slots read 25.5 to 31.5 (median 30) and the bars 25.5 to 28.5; the black fraction of the grate is about 0.41'},
        'reading': 'the slots are about as wide as the bars, not two-thirds iron', 'error': '+-3 mm', 'kind': 'Photo'})
    pms.append({
        'id': 'PM29', 'what': 'grate B (Birbeck Street): slot width, bars, lifting holes (the review, rough)', 'photo': 'birbeck_street_underpass', 'taken': '2019-08-18', 'method': 'listed',
        'raw': {'scale_with_height': True, 'results': {'slot_width_mm': 28.0, 'bar_width_mm': 30.0, 'lifting_hole_diameter_mm': 25.0}, 'how': 'on the preview the slots are about half the pitch; two round lifting holes sit on the long axis beyond the two end slots'},
        'reading': 'rough: perspective view', 'error': '+-15 %', 'kind': 'Photo'})
    pms.append({
        'id': 'PM30', 'what': 'grate A: centre and pitch of the slot field (centroids of the seven visible slots on the main ground frame)', 'photo': ASS, 'taken': '2019-09-07', 'method': 'listed',
        'raw': {'scale_with_height': True, 'results': {'x_centre_mm': -751.3, 'pitch_mm': 56.97, 'residual_std_mm': 1.0, 'slot_width_half_level_mm_mean': 28.6},
                'how': 'brightness minima of the slots over rows 462 to 520 of the 3 mm main ground frame (columns 225.7, 244.4, 263.7, 283.3, [the fifth is under a leaf], 321.1, 339.7, 358.3); centre = mean of (3 x column - 1628 - the nominal slot centre); half-level widths 30, 27, 30, 27, 27, 24, 33 mm'},
        'reading': 'the slot field is centred at x -751 in the crossing\'s plan frame; the pitch is 57.0; the slots are 28.6 wide at half level', 'error': '+-2 mm on the centre and pitch; +-3 on widths', 'kind': 'Photo'})
    return pms


def photographs_win():
    from corrected_numbers import N, REF
    return [
        {'item': 'camera height of every panorama', 'scene_or_book': 'the first draft assumed 1.6 m for all six panoramas', 'photograph': 'measured for each on its own (calibration_data.py): urban_street_03 1.44, 01 1.23, 02 1.01, bethnal_green_entrance 1.00, birbeck_street_underpass 1.165, urban_street_04 1.50 m, all at the ground the measurement sits on',
         'chose': 'every size read off a picture scaled by h / 1.6 (0.90, 0.77, 0.63, 0.625, 0.73, 0.94); angles unchanged', 'why': 'the bollards\' writer and reviewer showed none was taken at 1.6 m; bricks (horizon method) and car wheels agree where both exist (urban_street_03: 1.43 and 1.46)'},
        {'item': 'kerb top width', 'scene_or_book': '125 (Read: scene; BS 7263 HB2/BN2 125 x 255, a lead)', 'photograph': '163, 167 on two granite blocks at the measured upstand and 170 on the kerb-top ortho (face line to the rear joint), at the corrected height; 122 on the concrete kerb at its measured upstand',
         'chose': f"granite {N['TOPW']}, concrete {N['CW']}", 'why': 'three readings of granite agree within 8 mm; the visible top runs from the face line to the dark joint under the flag; the concrete kerb now agrees with the 125 section'},
        {'item': 'kerb face profile', 'scene_or_book': 'no profile stated in the scene; a search lead names BS 7263 HB2 half-battered and BN2 bullnosed', 'photograph': 'the middle of the arris stands 26 +-9 mm behind the foot line on the granite kerb at the corrected height (a battered upper face); the concrete kerb is fully rounded',
         'chose': f"granite half-battered (vertical to {N['VERT_Z']}, back {N['BATTER']} by {N['U'] - N['ARRIS_R']}, arris R {N['ARRIS_R']}); concrete bullnosed (R {N['CR']})", 'why': 'photographs win'},
        {'item': 'kerb upstand', 'scene_or_book': '125 (Read)', 'photograph': '107 and 102 to the middle of the arris rounding on granite at the corrected height (a vertical-face equivalent 104 to 116; the top is about 8 above the arris middle); 70 on the concrete kerb',
         'chose': f"granite {N['U']} (the 125 is outside the error), concrete {N['CU']}", 'why': 'photographs win: at 0.90 the arris-middle readings no longer reach 125; the concrete kerb sits between PM03 (about 85 to 88) and the bollards\' footway step (0.105)'},
        {'item': 'kerb block length', 'scene_or_book': '915 uniform (Read; BS block 3 ft)', 'photograph': 'whole granite blocks 0.75, 0.91, 1.03 m at the corrected height',
         'chose': f"granite random {N['LEN_MIN']} to {N['LEN_MAX']} (mean {N['LEN_MEAN']}); concrete 915", 'why': 'old granite kerb came in random lengths about a metre; the 915 block is the concrete one'},
        {'item': 'channel material', 'scene_or_book': 'concrete ("the kerb\'s own concrete"; wear target channel_concrete)', 'photograph': 'two courses of granite setts, 10 mm mortar joints, pale and worn',
         'chose': 'granite setts beside granite kerb; concrete channel block only beside the concrete kerb', 'why': 'the photograph shows setts; their brightness (1.35 to 1.7 times the road, Read from the wear target) is unchanged'},
        {'item': 'channel width', 'scene_or_book': '255 (Read; also the width of a BS concrete channel block)', 'photograph': f"226 +-15 (two courses of setts, foot to asphalt edge) at the corrected height",
         'chose': f"{N['CH_W']} for the granite sett channel (courses {N['CH_A']} and {N['CH_B']}); 255 kept for the concrete channel block", 'why': 'photographs win; the scene\'s 255 is the width of a BS concrete channel block'},
        {'item': 'gully grate', 'scene_or_book': '400 mm square, recess 50, dish 30 (Read)', 'photograph': f"440 x 292 rectangle, 8 slots 26 wide (23 to 31) x 256 at pitch 51, bars 25 (22 to 26), slots across the channel, black fraction about 0.41, dish about 15 mm, kink in the yellow line (all at the corrected height)",
         'chose': f"{N['GA_L']} x {N['GA_W']}, 8 slots {N['GA_SLOT_W']} x {N['GA_SLOT_L']}, bars {N['GA_BAR']}; dish 15; recess and dish of the scene dropped", 'why': 'photographs win; the 400 square is a trade guess'},
        {'item': 'dropped crossover upstand and taper block', 'scene_or_book': '6 mm upstand, one taper block (Read)', 'photograph': f"a row of granite setts stands about {N['LIP_Z']} proud as the lip; a ramp 0.83 m deep at 1 in {N['RAMP_RUN'] / N['RAMP_RISE']:.1f}; granite flank strips; no taper block",
         'chose': f"lip {N['LIP_Z']} mm, ramp and flank strips; the taper block kept as a precast variant (Judgement, a lead)", 'why': 'the photographed crossing is the period form; 6 mm is the modern flush figure'},
        {'item': 'corner', 'scene_or_book': 'asset plan: "kerb blocks ... drop kerb, corner" (no figures)', 'photograph': f"a mitred corner of about 133 degrees (build-out; PM27, unchanged by scale) and a radius corner of about {N['CORNER_R'] / 1000:.1f} m (granite blocks cut to the curve; PM16 at the corrected height)",
         'chose': 'both, as two pieces', 'why': 'both seen'},
        {'item': 'tactile paving', 'scene_or_book': 'asset plan: "leave the cone off"', 'photograph': 'no tactile surface on any dropped kerb in the photographs (the crossing in urban_street_03 is plain concrete); they are 2019 and say nothing about 1990',
         'chose': 'none', 'why': 'leads: first trial 1983, guidance 1998; a minor street in 1990 has none'},
        {'item': 'grate slot and bar widths', 'scene_or_book': 'none printed (the first draft of this target: slot 18, bar 39; after the review 29 and 28 at 1.6 m)', 'photograph': 'slots 23 to 31 (median 26), bars 22 to 26; the black fraction is about 0.41 (PM28; PM14 corrected to a 289 px field; both at the corrected height)',
         'chose': f"slot {N['GA_SLOT_W']}, bar {N['GA_BAR']}, slot span {N['GA_SPAN']}, end walls {N['GA_END_ALONG']}, open fraction {N['GA_OPEN']}", 'why': 'the review re-measured the grate; the camera height then scaled it'},
        {'item': 'stud cover construction and size', 'scene_or_book': 'none printed (the first draft: one lid, 8 x 8 studs, 860; after the review 960 and 10 x 10)', 'photograph': f"two triangular leaves on one diagonal joint with half-studs along it, 10 x 10 studs, outer about 612 x 575 at the corrected height, a round keyhole about 12, a blank raised oblong boss about 50 x 25; no oblong lifting pockets",
         'chose': f"two triangular leaves, 10 x 10 studs, outer {N['STUD_OUT']}, keyholes and a blank boss", 'why': 'photographs win; a 600 square cover is the usual size'},
        {'item': 'round cover tread lattice', 'scene_or_book': 'none printed (the first draft: one horizontal and one vertical lug per 71.3 x 83.5 cell)', 'photograph': 'a centred lattice: 2 horizontal and 2 vertical lugs per 71.4 x 83.5 cell, rows 41.75 apart, 36 x 10.5 lugs (PM23: the texture\'s own 500 mm tile, no camera)',
         'chose': 'lugs_in_cell with four lug centres', 'why': 'the autocorrelation had taken only the axis peaks'},
        {'item': 'footway cover frame top', 'scene_or_book': 'none printed (the first draft: a flat outer flange)', 'photograph': 'the cast frame carries rows of small raised oblong lugs over its whole top (a 7 m telephoto: pattern yes, lug size no)',
         'chose': 'a lugged frame (P2 lug 36 x 10.5 x 2.5, rows 41.75 apart)', 'why': 'photographs win; the lug size is Judgement'},
        {'item': 'channel setts colour shares', 'scene_or_book': 'wear target M24: the channel reads 1.35 to 1.7 times the road', 'photograph': 'pale and dull setts mixed with some blue-grey (the lip row and channel boxes of PM sample set)',
         'chose': 'sett_pale_worn 0.35, sett_dull 0.50, granite_blue_grey 0.15', 'why': 'without shares the clean setts could not land the channel inside 1.35 to 1.7; at these shares about 1.51 after the grime'},
        {'item': 'asphalt laps the outer sett course', 'scene_or_book': f"channel course 255 (Read)", 'photograph': f"beyond the crossing\'s right end block the asphalt covers the outer 30 to 50 mm of course B (27 to 45 at the corrected height), so the visible channel is about 150 to 175; in front of the crossing course B shows to {N['CH_W']}",
         'chose': f"{N['CH_W']} modelled underneath; the asphalt laps 30 to 50 over about a third of a run", 'why': 'photographs win'},
        {'item': 'cover and grate lettering', 'scene_or_book': 'the brief: blank or generic words if photographed', 'photograph': 'no lettering legible on any cover or grate in the photographs',
         'chose': 'none', 'why': 'nothing photographed; "SV" "WATER" "GAS" allowed only if a photograph shows them'},
    ]


def variants():
    from corrected_numbers import N
    return {
        'kerb_granite': {'count': 3, 'what': 'three colour variants (grey 75 %, blue-grey 20 %, pink-grey 5 %) x random length x laying scatter; wear states: clean top / chipped arris / tyre-polished front / weed at the foot'},
        'kerb_concrete': {'count': 1, 'what': 'one section; 3 wear states (pointing cracked, arris spalled, paint blip); three runs of 4 to 8 blocks on the street, about 20 m of the 96 m of kerb, away from the crossing and the gully'},
        'crossover': {'count': 2, 'what': 'A the photographed form (ramp + flank strips + sett lip) at 3.0 m on the west side at x 22.5; B the precast dropper variant (not used unless the builder wants a second crossing)'},
        'channel': {'count': 2, 'what': 'granite setts (2 courses) beside granite; concrete channel block beside concrete'},
        'corner': {'count': 2, 'what': f"mitred (angle 133 +-5, 90 allowed) and radius {N['CORNER_R']}; neither is in today's street: place at a build-out or at the cross-street end if the town adds one"},
        'gully_grate': {'count': 2, 'what': f"A (8 slots {N['GA_SLOT_W']} x {N['GA_SLOT_L']}, {N['GA_L']} x {N['GA_W']}, on the street at x 12, east) and B (7 slots {N['GB_SLOT_W']} wide oval-trimmed, {N['GB_L']} x {N['GB_W']}, two lifting holes, optional second at the quay end); 3 wear states each; mirror along the kerb allowed"},
        'covers': {'count': 4, 'what': f"four cast patterns (asset plan): P1 double-triangular square-stud cover ({N['STUD_OUT']} square, two leaves, 10 x 10 studs), P2 round 600 class with lug tread, P3 recessed infill cover (footway telecom-style {N['FW_OUT'][0]} x {N['FW_OUT'][1]}; carriageway tarmac-filled {N['RD_OUT'][0]} x {N['RD_OUT'][1]}), P4 two-leaf fine-stud road cover {N['DL_OUT'][0]} x {N['DL_OUT'][1]}; plus small service lids (stopcock, gas, telecom blank)"},
        'street_counts_judgement': 'covers 10 to 14: P1 x2, P2 x2, P3 footway x2 and road x1, P4 x1, small lids x6 (3 stopcock, 2 gas, 1 telecom blank); grates 1 (the scene) to 3',
    }


def wear():
    return {
        'note': 'what the photographs show; the numbers and masks belong to the wear family (gutter_grime, grate_wear, iron_wear, footway_infill): this lists the SHAPE-level wear the models carry.',
        'kerb_granite': ['top polished lighter at the front half (tyres, feet)', 'face dark with traffic film; the foot has a darker tide line',
                         '1 block in 6 has an arris chip 20 to 60 mm long, 5 to 15 mm deep, or a chipped end', 'joints open and dark, 3 to 15 mm; a weed clump (100 to 150 mm) in a joint or at the foot about every 3 to 6 m of kerb (Photo: two in 4 m); leaf litter caught at the foot',
                         'blocks tilt up to 1.5 degrees and step 3 mm between neighbours'],
        'kerb_concrete': ['pointing cracked and lost', 'arris spalled 10 to 30 mm, aggregate showing', 'paint blips across the top (lines family)'],
        'channel_setts': ['mortar lost in 1 joint in 4, to 20 mm', 'setts polished pale on top, silt and leaf mulch in the joints, a sett missing or loose about 1 in 40',
                          'grit and mulch pile where the channel meets the grate (wear: gully piles)', 'a weed or two in the joints'],
        'crossover': ['ramp: exposed aggregate, speckled, a hairline crack across it, bitumen joint black and cracked, dried needles and leaf mould in the joint at the left flank (a brown stain 150 wide)',
                      'flank strips: polished top, one chipped end, one splayed inner face dark', 'lip setts: blue-grey and pale setts with dark mortar, 1 in 8 pinkish'],
        'gully_grate': ['bars rust-brown, tops polished by wheels, slots full of black silt', 'a leaf or two across the slots; litter caught; the asphalt around dished and cracked',
                        'the yellow line kinks around it (lines family)'],
        'covers': ['stud and lug tops lighter where worn, sides and crevices rust-brown and black', 'leaf litter and grit in pockets and gaps', 'recessed infill cracked or chipped at the corner; a gap of 10 to 15 mm to the surround, grass or moss at the corners of the tarmac-filled one',
                   'pale mortar surround patched'],
        'what_is_not_here': ['no gum, no cigarette ends, no oil: the wear family places them', 'no bright orange rust'],
    }


def checks():
    from corrected_numbers import N
    C = []
    U, TW, AR = N['U'], N['TOPW'], N['ARRIS_R']

    def add(name, applies, measure, expected, tol, kind):
        C.append({'name': name, 'applies_to': applies, 'measure': measure, 'expected': expected, 'tolerance': tol, 'kind': kind})

    add('kerb_upstand_granite', 'kerb_granite', 'height of the top above the channel top (z of the flat top minus z = 0)', U, 10, 'Photo: arris middle 102 to 107 (+8 to the top) at the corrected height; the scene\'s Read 125 is outside the error')
    add('kerb_top_width_granite', 'kerb_granite', 'y extent of the flat top plus arris, face line to back', TW, 15, 'Photo PM01, PM02, PM25 (163, 167, 170 at the corrected height)')
    add('kerb_depth', 'kerb_granite, kerb_concrete', 'z from the top to the underside', 255, 4, 'Read')
    add('kerb_arris_radius_granite', 'kerb_granite', 'radius of a circle fitted to the top-front edge in section', AR, 8, 'Judgement; Photo (a worn rounding of about 25 mm)')
    add('kerb_face_batter', 'kerb_granite', f"face vertical from z = 0 to {N['VERT_Z']}, then set back {N['BATTER']} mm by z = {U - AR} (measured at the arris middle: 26 +-9)", {'vertical_to_z': N['VERT_Z'], 'set_back': N['BATTER']}, {'vertical_to_z': 15, 'set_back': 8}, 'Photo PM26')
    add('kerb_block_length_granite', 'a run of 10 or more granite blocks', f"every length between {N['LEN_MIN']} and {N['LEN_MAX']}, mean {N['LEN_MEAN']}, no two neighbours within 20 mm", {'min': N['LEN_MIN'], 'max': N['LEN_MAX'], 'mean': N['LEN_MEAN']}, 100, 'Photo PM04 (0.75, 0.91, 1.03)')
    add('kerb_joint_width', 'kerb_granite', 'gap between neighbouring blocks at the top', N['JOINT'], 3, 'Photo PM05')
    add('kerb_concrete_section', 'kerb_concrete', 'upstand, top width, arris radius', {'upstand': N['CU'], 'top_width': N['CW'], 'arris_radius': N['CR']}, {'upstand': 12, 'top_width': 12, 'arris_radius': 10}, 'Photo PM03; the scene\'s 125; Judgement for the radius')
    add('kerb_concrete_length', 'kerb_concrete', 'block length', 915, 5, 'Read')
    add('channel_width', 'channel_setts', 'face line to the asphalt edge', N['CH_W'], 12, 'Photo PM06 (204 +-15 at the corrected height)')
    add('channel_width_concrete', 'channel_concrete', 'face line to the far edge of the block', 255, 5, 'Read')
    add('channel_courses', 'channel_setts', 'number of courses; across-widths A and B', {'courses': 2, 'A': N['CH_A'], 'B': N['CH_B']}, {'courses': 0, 'A': 10, 'B': 10}, 'Photo, Judgement')
    add('sett_length', 'channel_setts', 'sett length along the kerb, all', {'min': N['SETT_MIN'], 'max': N['SETT_MAX']}, 15, 'Photo')
    add('sett_top_level', 'channel_setts, lip_row', 'z of every channel sett top', {'min': -5, 'max': 4}, 1, 'Judgement; Photo')
    add('channel_over_road_brightness', 'channel_setts material after the wear family', 'luminance of the channel over the road beside it', {'min': 1.35, 'max': 1.7}, 0.0, 'Read: wear target M24 (Photo 1.35 to 1.7)')
    add('crossover_width', 'crossover', 'gap between the two end-block faces', 3000, 20, 'Read: SCENE-SLOTS 3.0 m')
    add('crossover_lip', 'crossover', 'z of the lip setts top; count of setts', {'z': N['LIP_Z'], 'count': N['LIP_N']}, {'z': 6, 'count': 1}, 'Photo PM09 (11 +-8 at the corrected height); Derived')
    add('crossover_ramp', 'crossover', 'ramp rise and run from the lip back edge to the back edge; back edge y', {'rise': N['RAMP_RISE'], 'run': N['RAMP_RUN'], 'back_y': -N['RAMP_BACK']}, {'rise': 8, 'run': 40, 'back_y': 40}, 'Photo PM11 (832 +-40 at the corrected height)')
    add('crossover_flank', 'crossover', 'flank strip width, length, top z', {'width': N['FLANK_W'], 'length': N['RAMP_BACK'] - N['FLANK_Y1'], 'top_z': N['FLAGS_Z']}, {'width': 20, 'length': 30, 'top_z': 8}, 'Photo PM12')
    add('crossover_watertight', 'crossover', 'largest gap between ramp, lip, flank strips and end blocks', 15, 0, 'Judgement (bitumen joint 12 mm)')
    add('gully_grate_overall', 'gully_grate_A', 'overall size along the kerb x across', [N['GA_L'], N['GA_W']], [10, 10], 'Photo PM13 (440 x 292 at the corrected height)')
    add('gully_grate_slots', 'gully_grate_A', 'slot count; slot width x length; bar width; slot span; end wall along; pitch; slots perpendicular to the kerb', {'count': N['GA_N'], 'width': N['GA_SLOT_W'], 'length': N['GA_SLOT_L'], 'bar': N['GA_BAR'], 'span': N['GA_SPAN'], 'end_wall_along': N['GA_END_ALONG'], 'pitch': N['GA_PITCH']}, {'count': 0, 'width': 4, 'length': 8, 'bar': 4, 'span': 6, 'end_wall_along': 4, 'pitch': 2}, 'Photo PM14 (field 289 px = 390 at the corrected height), PM28 (slots 23 to 31, bars 22 to 26), PM30')
    add('gully_grate_open_fraction', 'gully_grate_A', f"slot area over the grate\'s plan area, {N['GA_N']} x {N['GA_SLOT_W']} x {N['GA_SLOT_L']} / ({N['GA_L']} x {N['GA_W']})", 0.42, 0.04, 'Derived; Photo (the photograph\'s black fraction is about 0.41; a ratio, unchanged by the camera height)')
    add('gully_grate_B', 'gully_grate_B', 'slot count, slot width, bar width, pitch; lifting holes (count, diameter, on the long axis beyond the end slot centres); raised marks on the centre bar blank', {'slots': 7, 'width': N['GB_SLOT_W'], 'bar': N['GB_BAR'], 'pitch': N['GB_PITCH'], 'holes': 2, 'hole_diameter': N['GB_HOLE'], 'beyond_end_slot_mm': N['GB_HOLE_OFF']}, {'slots': 0, 'width': 4, 'bar': 4, 'pitch': 3, 'holes': 0, 'hole_diameter': 3, 'beyond_end_slot_mm': 12}, 'Photo, rough (PM29, PM15 at the corrected height)')
    add('cast_iron_grate_base_colour', 'materials.cast_iron_grate', 'the base colour of the grate iron is the wear target\'s iron_grate; the rust comes from grate_wear (expected composite on the bars 92/74/66)', [58, 54, 52], 0, 'Read: wear target surfaces.iron_grate')
    add('gully_grate_place', 'gully_grate_A', 'y of the kerb-side edge', N['GA_Y0'], 15, 'Photo (92 at the corrected height)')
    add('gully_flush', 'gully_grate_A, covers', 'z of the top surface against the surface it is set in', 0, 3, 'Judgement (cover infill in the footway stands 8 below the flags, +-3)')
    add('cover_stud_square', 'cover_stud_square', 'outer; frame rim; lid; studs per row and column; pitch; stud size; stud height; leaves (2, triangular, one diagonal joint with the studs on it cut to half-studs); keyhole per leaf; blank raised boss', {'outer': N['STUD_OUT'], 'rim': N['STUD_RIM'], 'lid': N['STUD_OUT'] - 2 * N['STUD_RIM'], 'studs': 10, 'pitch': N['STUD_PITCH'], 'stud': N['STUD'], 'height': N['STUD_H'], 'leaves': 2, 'joint': N['STUD_JOINT'], 'keyhole': N['STUD_KEYHOLE'], 'boss': N['STUD_BOSS']}, {'outer': 40, 'rim': 4, 'lid': 15, 'studs': 0, 'pitch': 3, 'stud': 3, 'height': 1, 'leaves': 0, 'joint': 2, 'keyhole': 3, 'boss': [8, 6, 1]}, 'Photo PM17, PM18 (612 x 575 +-45 at the corrected height 1.00 m) and the review of bethnal_green_entrance')
    add('cover_round', 'cover_round_600', 'frame diameter; lid diameter; depth', {'frame': 690, 'lid': 590, 'depth': 68}, {'frame': 5, 'lid': 5, 'depth': 3}, 'Read from a Poly Haven model (PM24)')
    add('cover_round_tread', 'cover_round_600', 'lug lattice: cell; lugs per cell (2 horizontal, 2 vertical) at (0,0) and (35.7,41.75) horizontal, (35.7,6) and (0,47.75) vertical; lug size and height', {'cell': [71.4, 83.5], 'lugs': 4, 'lug': [36, 10.5], 'height': 2.5}, {'cell': [1, 1], 'lugs': 0, 'lug': [3, 2], 'height': 1}, 'Photo PM23 (the review: the centred lattice; the texture\'s own 500 mm)')
    add('cover_recessed_footway_frame_lugs', 'cover_recessed_footway', 'raised oblong lugs 36 x 10.5 x 2.5 on the whole frame top, two staggered rows along the long sides, more across the wider left end (3 columns against 2)', {'lug': [36, 10.5], 'height': 2.5, 'row_pitch': 41.75}, {'lug': [4, 3], 'height': 1, 'row_pitch': 4}, 'Photo for the pattern; Judgement for the size')
    add('cover_recessed_footway', 'cover_recessed_footway', 'outer; infill', {'outer': N['FW_OUT'], 'infill': N['FW_IN']}, {'outer': [40, 60], 'infill': [30, 40]}, 'Photo PM19 (at the corrected height 1.44 m)')
    add('cover_recessed_road', 'cover_recessed_road', 'outer', N['RD_OUT'], [40, 40], 'Photo PM20 (at the corrected height 1.01 m)')
    add('cover_road_double_leaf', 'cover_road_double_leaf', 'outer; the leaf split is Judgement, not Photo', N['DL_OUT'], [100, 80], 'Photo PM21 (rough; at the corrected height 1.50 m); the split: Judgement')
    add('kerb_corner', 'kerb_corner_mitre, kerb_corner_radius', 'mitre interior angle (or 90); radius corner radius on the face', {'mitre_deg': 133, 'or_deg': 90, 'radius': N['CORNER_R']}, {'mitre_deg': 5, 'or_deg': 2, 'radius': 600}, 'Photo PM27 (133 +-5); PM16 (6.4 m to the line at the corrected height, less 0.2, +-0.6)')
    add('channel_setts_colour_share', 'channel_setts', 'colour shares of sett_pale_worn, sett_dull, granite_blue_grey; their linear mean over asphalt_dry after the channel body x 0.85', {'shares': [0.35, 0.50, 0.15], 'after_grime_over_road': [1.35, 1.7]}, {'shares': 0.0, 'after_grime_over_road': 0.0}, 'the review (point 6); Read: wear target M24')
    add('camera_heights_measured', 'every photograph measurement', 'each panorama\'s camera height is recomputed from its own anchors (bricks by the horizon method, car wheels), none is assumed; the mean of the anchors lies within the stated error of the stated height', {'urban_street_03': 1.44, 'urban_street_01': 1.23, 'urban_street_02': 1.01, 'bethnal_green_entrance': 1.00, 'birbeck_street_underpass': 1.165, 'urban_street_04': 1.50}, 0.1, 'calibration_data.py, calibrate.py')
    add('no_lettering', 'every cover and grate, mesh and textures', 'glyphs, crests, maker marks, council names, crowns', 0, 0, 'Brief')
    add('no_tactile_paving', 'the crossing and the street', 'blister or corduroy meshes or textures', 0, 0, 'Judgement; leads')
    add('pivot_and_units', 'every exported piece', 'pivot as in frame.pivot; metres; z up; scale 1', 'as stated', 5, 'Brief')
    add('colour_of_granite_top', 'kerb_granite material (clean albedo)', 'mean sRGB of the top texture', None, 10, 'Photo (see materials.granite_grey.srgb)')
    add('drawing_match', 'each piece', 'silhouette of the built piece in plan and section at 1 mm a pixel against target_drawing.py polygons', 0.9, 0.0, 'min intersection over union; 0.95 for the kerb sections')
    return C


def could_not_settle():
    return [
        'The camera heights are the largest remaining uncertainty: bricks by the horizon method (gauge 75 mm, 73 to 79 for Victorian courses: +-4 %) and car wheels (a tyre D known to +-4 %) give 1.44 +-0.07 (urban_street_03), 1.23 +-0.08 (01), 1.01 +-0.06 (02), 1.00 +-0.06 (bethnal_green_entrance), 1.165 +-0.07 (birbeck), 1.50 +-0.10 (04); every size read off a picture carries that error on top of its own (5 to 8 %). The 75 mm yellow line could not settle urban_street_03 (64 to 82 mm by how it is read). The footway-to-road steps (0.10 to 0.15 m) are Judgement or the bollards\' measurement. A photograph with a measured object in it (a kerb against a ruler, a standard slab) would settle every size.',
        'urban_street_04 has no brick wall standing on the ground (stucco and stone), so its height rests on three car wheels only; the method agrees with the bricks on urban_street_03 (1.46 against 1.43), but 04\'s corner radius, road cover and small cover are +-9 % in size.',
        'The kerb top width (170 granite, 125 concrete), upstand (115, 95), face batter (20 mm back by z 90, PM26: 26 +-9) and arris radius (25, 50) rest on three views at 3.5 m with errors of 9 to 25 mm; the batter and the arris radius are read off one block each. At the corrected height the granite upstand falls from the scene\'s 125 to 115 (the arris-middle readings no longer reach 125). A close photograph of a kerb end (Geograph, once reachable) would settle the profile.',
        'Whether Quay Street\'s old kerb is granite is Judgement: a port town\'s old quarter had granite kerbs and sett channels (the photographs show them in a Victorian street), but no photograph of a 1990 port-town street was reached.',
        'The channel width: 204 +-15 in one street (the scene\'s 255 is a concrete channel block\'s width); a second street with setts would show whether 205 or a wider sett course was usual.',
        'The round 600 cover\'s own pattern was not photographed: the lug tread comes from a CC0 scan of a real tread plate (a 500 mm tile, so no camera) and the frame size from a CC0 model. A photographed British round cover is still owed.',
        'The stopcock and gas lids are Judgement (no photograph); BS 5834 (surface boxes) and the water and gas companies\' drawings should be read once the network opens.',
        'Grate B (Birbeck Street) is measured only from a perspective view at 3.5 m: its slot lengths and frame are +-15 % before the height error.',
        'Gully grate dishing (15 mm) and the pot depth are Judgement.',
        'Whether a taper (dropper) block was used for house crossings in a 1990 port town: the photographed crossing used a concrete ramp with flank strips; the precast dropper (BS 7263, search lead) is kept as a variant.',
        'Tactile paving: leads say the first blister trial was 1983 and the guidance 1998; no 1985 to 1995 photograph of a minor-street dropped kerb was reached.',
        'Colours are ratios against the road on tone-mapped copies, not calibrated albedo; the wet-street look is the wear family\'s.',
        'No photograph from 1975 to 2000 was reached (Wikimedia, Geograph, Flickr, archive.org all refused): every photograph is 2019 and its 1990 sameness is argued, not shown.',
    ]


def to_read_later():
    return [
        'BS 7263 Part 1 (1990) Precast concrete flags, kerbs, channels, edgings and quadrants: kerb sections (HB2, BN2, BN3), droppers, channels; and BS 340 (1979) it replaced.',
        'BS 435 (1975) Dressed natural stone kerbs, channels, quadrants and setts: the granite kerb and sett sizes (title and year from memory, to be checked).',
        'BS 497 Part 1 (1976) Manhole covers, road gully gratings and frames for drainage purposes (superseded 1994 by BS EN 124): grating sizes and slot patterns.',
        'BS 5834 (surface boxes for underground stop valves) and the gas and telecom operators\' cover drawings, for the small lids.',
        'TRRL reports on road gully capacity (the search lead: "The drainage capacity of BS road gullies and a procedure for estimating their spacing"): grate sizes in use.',
        'The Department of Transport and DETR guidance on tactile paving (1998), the 1983 Parliament Square trial (Cranfield, Department of Transport research), and any 1985-92 local trial at a minor-street crossing.',
        'Highway authorities\' standard details for vehicle crossings (1970s and 1980s drawings: ramp gradient, flank strips, dropper kerbs).',
        'Dated photographs 1975 to 2000: Geograph (CC BY-SA) searches for "dropped kerb", "granite sett channel", "gully grating", "stop tap cover"; Wikimedia Commons categories for cast-iron covers and gratings in England; Historic England Archive and a port town\'s local archive (Hull, Grimsby, Whitby, North Shields) for street scenes of the 1980s.',
        'IHT "Roads and Traffic in Urban Areas" (1987) and the Department\'s "Design Bulletin 32" for urban kerb and drainage details.',
    ]


def edge_probes():
    """Edges of the drawn photographed crossing that self_check.py looks for on the two main photographs (drawn at the measured camera height, 1.44 m).
    image: 'ground' (the channel plane) or 'top' (the kerb-top plane); kind 'h' (constant y, along x) or 'v' (constant x, along y);
    fixed = predicted y (h) or x (v) in plan mm; span = the other coordinate's range; z_mm = height of the edge (things off the plane
    are smeared outward by (camera - plane) / (camera - z); the check applies that); type: 'step' (largest brightness change), 'line' (darkest
    line, a joint), 'step_low' (the start of a soft shadow ramp, 20 % of the rise; this one DEFINES the foot anchor) or 'half_level' (a soft edge read where the
    profile crosses the middle of the levels either side, 'outside' = -1 or +1 the side of the outer level; for the grate's slot edges the outer level is the bar level common to all slots, 'level': 'bar_median', so a lighter end wall does not move the edge); tol_mm = stated error.
    Every position is computed from the corrected numbers (the first draft's x 0.90)."""
    from corrected_numbers import N, REF
    g = REF['gully']
    xc = g['x_centre']
    p = N['GA_PITCH']
    hw = N['GA_SLOT_W'] / 2.0
    s1, s4, s8 = -3.5 * p, -0.5 * p, 3.5 * p
    half = REF['gap'] / 2.0
    U, TW = N['U'], N['TOPW']
    arr_mid_z = U - N['ARRIS_R'] + N['ARRIS_R'] * 0.7071
    arr_mid_y = -(N['BATTER'] + N['ARRIS_R'] * (1 - 0.7071))
    rj = -(TW + 5)
    lx, rx = REF['flank_left_x'], REF['flank_right_x']
    P = []

    def add(**k):
        P.append(k)
    add(id='foot_line_right_block', image='ground', kind='h', fixed=0, z_mm=0, type='step_low', span=[1330, 1580], tol_mm=15, what='kerb face foot (the anchor of y = 0): the dark face, then the shadow ramp up to the setts, clear of the weed')
    add(id='lip_front_top_edge', image='ground', kind='h', fixed=0, z_mm=N['LIP_Z'], type='step', span=[-765, 765], tol_mm=12, what='light lip setts above, the dark band of their front face below')
    add(id='lip_back_joint', image='ground', kind='h', fixed=-(N['LIP_W'] + N['RAMP_JOINT'] / 2.0), z_mm=N['LIP_Z'], type='line', span=[-765, 765], tol_mm=12, what='the dark joint between the lip row and the ramp (centre)')
    add(id='channel_asphalt_edge', image='ground', kind='h', fixed=REF['channel_width'], z_mm=6, type='step', span=[-225, 810], tol_mm=15, what='pale setts above, asphalt below')
    add(id='grate_left_edge', image='ground', kind='v', fixed=xc - g['along'] / 2.0, z_mm=0, type='half_level', outside=-1, span=[160, 360], tol_mm=20, what='setts left of the grate against its left end wall (the end walls are soft: +-20; the right edge is not visible against the setts, both 100 to 120 grey levels, so it has no probe; the slot edges below carry the grate\'s width)')
    add(id='grate_slot_tops', image='ground', kind='h', fixed=g['y0'] + N['GA_END_ACROSS'], z_mm=0, type='step', span=[xc - 160, xc + 160], tol_mm=12, what='the upper ends of the black slots (frame y0 + end wall)')
    add(id='grate_slot_bottoms', image='ground', kind='h', fixed=g['y1'] - N['GA_END_ACROSS'], z_mm=0, type='step', span=[xc - 160, xc + 160], tol_mm=15, what='the lower ends of the black slots (frame y1 - end wall)')
    for nm, sc, lab in (('slot1', s1, 'first'), ('slot4', s4, 'fourth'), ('slot8', s8, 'eighth')):
        add(id=f'{nm}_left_edge', image='ground', kind='v', fixed=round(xc + sc - hw, 1), z_mm=0, type='half_level', outside=-1, level='bar_median', span=[135, 340], tol_mm=6, what=f'{lab} slot, left side edge (slot {N["GA_SLOT_W"]} wide: centre {sc:+.1f} from the grate centre, edge at -{hw:g})')
        add(id=f'{nm}_right_edge', image='ground', kind='v', fixed=round(xc + sc + hw, 1), z_mm=0, type='half_level', outside=1, level='bar_median', span=[135, 340], tol_mm=6, what=f'{lab} slot, right side edge')
    add(id='kerb_front_arris_right_block', image='top', kind='h', fixed=round(arr_mid_y, 1), z_mm=round(arr_mid_z, 1), type='step', span=[1125, 1530], tol_mm=15, what='light top to dark face (the middle of the arris rounding)')
    add(id='kerb_top_rear_joint_right_block', image='top', kind='h', fixed=rj, z_mm=U, type='line', span=[1125, 1530], tol_mm=15, what='dark joint between the kerb top and the flag behind it (centre)')
    add(id='ramp_back_joint', image='top', kind='h', fixed=-(N['RAMP_BACK'] + 6), z_mm=N['FLAGS_Z'], type='line', span=[-720, 720], tol_mm=18, what='the dark joint between the concrete ramp and the flags (centre: 6 mm behind the ramp\'s back edge, the joint being 10 to 20 wide)')
    add(id='flank_right_inner_joint', image='top', kind='v', fixed=rx[0] - 6, z_mm=N['FLAGS_Z'], type='line', span=[-790, -225], tol_mm=15, what='dark joint between the ramp and the right flank strip')
    add(id='flank_right_outer_joint', image='top', kind='v', fixed=rx[1] + 6, z_mm=N['FLAGS_Z'], type='line', span=[-790, -225], tol_mm=15, what='dark joint between the right flank strip and the dark flag')
    add(id='flank_left_outer_joint', image='top', kind='v', fixed=lx[0] - 6, z_mm=N['FLAGS_Z'], type='line', span=[-790, -225], tol_mm=15, what='dark joint between the pale flag and the left flank strip')
    return P


def scale_fit():
    from corrected_numbers import REF
    mm = (REF['flank_right_x'][1] + 6) - (REF['flank_left_x'][0] - 6)
    return {'left': 'flank_left_outer_joint', 'right': 'flank_right_outer_joint', 'mm_between': mm,
            'note': f'the scale is fitted on one dimension only (the distance between the two flank strips\' outer joints, {mm:g} mm in the drawing); the ortho is 3 mm a pixel by construction at the stated camera height, so the fitted scale should be about 1.00. This fit tests the drawing against the picture, not the camera height: that is tested in part B against the anchors.'}


def handover():
    from corrected_numbers import N
    return {
        'note': 'what this target hands to other targets and to NOW.md (review point 7; numbers corrected for the camera heights, 9 October)',
        'to_wear_target': [
            {'item': 'gutter_grime channel band', 'was': '0.255 m wide, in the kerb\'s own concrete', 'now': f"{N['CH_W'] / 1000:.3f} m on granite stretches (granite setts, two courses {N['CH_A']} and {N['CH_B']}; the first draft said 0.225); 0.255 m beside the concrete kerb (concrete channel block)"},
            {'item': 'places gully entry and grate_wear grate size', 'was': '0.40 m square', 'now': f"{N['GA_L'] / 1000:.3f} m x {N['GA_W'] / 1000:.3f} m (8 slots {N['GA_SLOT_W']} x {N['GA_SLOT_L']}, bars {N['GA_BAR']}; the first draft said 0.485 x 0.325)"},
            {'item': 'iron base colour', 'was': 'this target\'s clean rust-brown 92/74/66 against the wear target\'s iron_grate 58/54/52 with grate_wear rust 100/72/56', 'now': 'ONE base: the wear target\'s iron_grate 58/54/52; the rust comes from grate_wear; 92/74/66 is the expected composite on the bars, for checking the result'},
            {'item': 'camera heights', 'was': 'the wear target\'s photograph measurements (M01 to M25) assumed 1.6 m for urban_street_02 and 03', 'now': 'urban_street_03 was 1.44 m and urban_street_02 1.01 m: every size the wear target read off them (the 75 mm yellow line as a scale, the flags, litter, kerb scuffs, the oil dots) is 0.90 and 0.63 of what it printed; the wear writer should re-check them'},
        ],
        'for_NOW_md': f"Kerbs and covers target (unit 3.7), camera heights corrected 9 Oct: granite kerb {N['U']} x {N['TOPW']} half-battered, setts channel {N['CH_W']} (concrete 255), crossover 3.0 m with ramp, flank strips and a {N['LIP_Z']} mm lip, gully grate {N['GA_L']} x {N['GA_W']} (8 slots {N['GA_SLOT_W']} x {N['GA_SLOT_L']}), four cast covers; wear target: channel band 0.204 granite / 0.255 concrete, grate 0.440 x 0.290, iron base 58/54/52, and its urban_street_02/03 sizes x 0.63/0.90.",
    }
