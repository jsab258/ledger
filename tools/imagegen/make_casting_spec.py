"""Write the casting portraits' batch spec for the image lane (Z-Image-Turbo).

    python tools/imagegen/make_casting_spec.py      # writes tools/imagegen/casting-2026-09-24.json

WHY, 24 September. Jafar: a sheet for each principal, starting with Sheila
Dunn, Ron Kirby and Darren Milner, with "concept portraits from the image
lane, in period clothes in the street's light": a front, a profile and a
full-length figure each. The looks are the casting research's (DELIVERY.md,
section 7.3). Each person is ONE long description used word for word in all
three shots with one seed, so the three read as the same invented person.

The content clause is the library's, less "no recognisable faces", which a
portrait cannot keep; "no real person" and "no celebrity likeness" stay, and
the build refuses a prompt without "no trade marks".
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "casting-2026-09-24.json")

CLAUSE = ("an invented fictional person not based on anyone, no real person, no celebrity likeness, "
          "no real company names, no real brand logos, no trade marks, no alcohol and no gambling anywhere "
          "in frame, nobody under eighteen in frame, nothing sexual")

STREET = ("standing on the pavement of a grey northern English port-town street in 1990, old brick shopfronts "
          "and a wet pavement softly out of focus behind, soft flat overcast daylight from a pale grey sky, "
          "the street empty behind")
FILM = ("a candid documentary photograph on 35mm colour negative film, natural unretouched skin with pores "
        "and lines, true-to-life colour, sharp focus on the person")

PEOPLE = {
    "sheila-dunn": (20261001,
        "Sheila Dunn, an invented fictional Englishwoman of fifty-three, bookkeeper at a small minicab office: "
        "a pale, lined, tired face with smoker's lines round her mouth and faint crow's feet, a thin mouth in a "
        "plain rose lipstick on an otherwise bare face, grey-blue eyes, greying brown hair in a short set perm, "
        "large square tinted spectacles on a thin gold chain, a beige hand-knitted cardigan buttoned over a "
        "cream blouse with a small round collar",
        "a brown knee-length pleated skirt, flesh-coloured tights, flat brown lace-up shoes, a brown leather "
        "handbag over her forearm"),
    "ron-kirby": (20261002,
        "Ron Kirby, an invented fictional Englishman of fifty-eight, a retired docker who now works the door "
        "of a minicab office: big and heavy-set with a thick neck, bald on top with a short fringe of grey hair "
        "at the sides, a full grey-brown moustache, a broad weathered ruddy face, a nose broken long ago, "
        "heavy-lidded patient eyes, a navy blue donkey jacket with a black shoulder panel across the back over "
        "a grey knitted jumper",
        "dark grey work trousers, scuffed black leather boots, big hands with faded blue tattoos on the backs"),
    "darren-milner": (20261003,
        "Darren Milner, an invented fictional Englishman of twenty-five, a thin, restless street hustler, "
        "clearly a grown man with light stubble on his jaw: a narrow pale face, quick amused eyes, a cocky "
        "half-smile, a grown-out perm with bleached tips, a shiny purple and teal nylon tracksuit jacket of "
        "the rustling 1990 kind, zipped half up over a white T-shirt",
        "stonewashed blue jeans, scuffed white trainers, a black pager clipped to his belt"),
}

SHOTS = {
    "front": (768, 1024, "a head-and-shoulders portrait photograph, the person facing the camera at eye level, of"),
    "profile": (768, 1024, "a head-and-shoulders portrait photograph in exact side profile, the person facing "
                           "the left edge of the frame, of"),
    "full": (768, 1344, "a full-length standing photograph from head to shoes, the whole figure in frame, the "
                        "person facing the camera, of"),
}


def items():
    out = []
    for slug, (seed, face, below) in PEOPLE.items():
        for shot, (w, h, lead) in SHOTS.items():
            body = face + (", " + below if shot == "full" else "")
            out.append({
                "id": "%s-%s" % (slug, shot),
                "kind": "portrait",
                "binds_to": "production/casting/%s/SHEET.md (%s)" % (slug, shot),
                "width": w, "height": h, "seed": seed,
                "prompt": "Use case: casting reference. One photoreal photograph: %s %s, %s. %s." % (lead, body, STREET, FILM),
                # No age words here: the guard refuses them in any field, and
                # at cfg 1.0 the negative is inert anyway; "clearly a grown"
                # adult is in every prompt instead.
                "negative": "cartoon, illustration, painting, 3d render, plastic skin, airbrushed, "
                            "beauty filter, heavy make-up, modern clothes, logo, text, watermark",
            })
    return out


def main():
    with open(os.path.join(HERE, "interiors-2026-09-23.json"), encoding="utf-8") as fh:
        base = json.load(fh)
    spec = {
        "schema": 2,
        "batch_name": "casting-2026-09-24",
        "content_rules": {
            "_comment": ["The library's clause less 'no recognisable faces', which a portrait cannot keep; "
                         "see make_casting_spec.py."],
            "rules_clause": CLAUSE,
            "why": base["content_rules"]["why"],
            "forbidden_tokens": base["content_rules"]["forbidden_tokens"],
        },
        "style": {
            "_comment": ["framing_required is the check build_prompt runs; a portrait fills its frame."],
            "framing_required": "filling the frame edge to edge",
            "by_kind": {"portrait": {"prefix": "the photograph filling the frame edge to edge,", "suffix": ""}},
        },
        "defaults": base["defaults"],
        "items": items(),
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print("make_casting_spec: wrote %s, %d items" % (os.path.relpath(OUT), len(spec["items"])))


if __name__ == "__main__":
    main()
