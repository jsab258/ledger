# THE FIRST JOB (26 October): what this Marvelous offers, read from itself before anything is built on
# the documented list (production/research/game-clothing-pipeline/MD-SCRIPTING-2026-10-26.md): every
# public function of each CLO module, and the ImportExportOption fields, so later jobs call only what
# is really there.
import inspect

for name in ("utility_api", "import_api", "pattern_api", "fabric_api", "export_api", "ApiTypes"):
    mod = globals().get(name)
    if mod is None:
        result[name] = "missing"
        continue
    result[name] = sorted(n for n in dir(mod) if not n.startswith("_"))
try:
    opt = ApiTypes.ImportExportOption()
    result["ImportExportOption"] = {n: repr(getattr(opt, n)) for n in dir(opt) if not n.startswith("_") and not callable(getattr(opt, n))}
except Exception as e:
    result["ImportExportOption"] = "error: %s" % e
for fn in ("GetMajorVersion", "GetMinorVersion", "GetPatchVersion", "GetVersion"):
    f = getattr(globals().get("utility_api"), fn, None)
    if f is not None:
        try:
            result[fn] = f()
        except Exception as e:
            result[fn] = "error: %s" % e
log("probe done")
