import json, os
D = r"F:\LedgerTools\tmp\clothes\md\ron1"
res = []
for k in ["%02d" % i for i in range(26)] + ["half1", "half2"]:
    utility_api.NewProject()
    ok = pattern_api.ImportPatternJSON(os.path.join(D, "t-%s.json" % k))
    res.append((k, pattern_api.GetSeamlinePairGroupCount()))
print("TRY", res)
