import unreal, math
L=[]
CLIPS=["M_Neutral_Walk_Stop_F_Lfoot","M_Neutral_Walk_Stop_F_Rfoot"]
reg=unreal.AssetRegistryHelpers.get_asset_registry()
assets=reg.get_assets_by_path("/Game/Characters/UEFN_Mannequin/Animations", recursive=True)
paths={str(a.asset_name):str(a.package_name) for a in assets if str(a.asset_class_path.asset_name)=="AnimSequence"}
def curve_at(keys, t):
    times, vals = keys
    if not times: return None
    if t<=times[0]: return vals[0]
    for i in range(1,len(times)):
        if t<=times[i]:
            a=(t-times[i-1])/max(1e-6,times[i]-times[i-1]); return vals[i-1]+(vals[i]-vals[i-1])*a
    return vals[-1]
for name in CLIPS:
    if name not in paths: L.append("MISSING "+name); continue
    seq=unreal.load_asset(paths[name])
    length=seq.get_play_length()
    ck={}
    for c in ("contact_l","contact_r"):
        try:
            t,v=unreal.AnimationLibrary.get_float_keys(seq, unreal.Name(c))
            t=list(t); v=list(v)
            L.append("keys %s %s: %d keys, times %.2f..%.2f, values %.1f..%.1f"%(name,c,len(t),min(t) if t else -1,max(t) if t else -1,min(v) if v else -1,max(v) if v else -1))
            if t and max(t) > length*1.5: t=[x*length/max(t) for x in t]
            ck[c]=(t,v)
        except Exception as e:
            ck[c]=([],[]); L.append("curve? %s %s"%(c,str(e)[:60]))
    opts=unreal.AnimPoseEvaluationOptions()
    try: opts.set_editor_property("should_retarget", False)
    except Exception: pass
    try: opts.set_editor_property("extract_root_motion", False)
    except Exception: pass
    rows=[]
    n=int(length*60)+1
    for k in range(n):
        t=min(length,k/60.0)
        pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts)
        P={}
        for b in ("root","ball_l","ball_r"):
            tr=unreal.AnimPoseExtensions.get_bone_pose(pose, b, unreal.AnimPoseSpaces.WORLD)
            P[b]=tr.translation
        rows.append((t,P,curve_at(ck["contact_l"],t),curve_at(ck["contact_r"],t)))
    rest={f:min(r[1]["ball_"+f].z for r in rows) for f in ("l","r")}
    L.append("== %s length %.2f s, frames %d, root travel %.1f cm"%(name,length,n,math.hypot(rows[-1][1]["root"].x-rows[0][1]["root"].x, rows[-1][1]["root"].y-rows[0][1]["root"].y)))
    for f in ("l","r"):
        # by height alone in the clip's own frame: the ball within 1 cm of its lowest for 4 frames or more, its travel
        best=0.0; bspan=None; start=None; cnt=0
        for r in rows:
            p=r[1]["ball_"+f]
            if p.z < rest[f]+1.0:
                if start is None: start=(p.x,p.y,r[0]); cnt=0
                cnt+=1
                d=math.hypot(p.x-start[0],p.y-start[1])
                if cnt>=4 and d>best: best=d; bspan=(start[2],r[0])
            else: start=None
        L.append("   ball_%s flat on the ground (within 1 cm of lowest): worst travel %.1f cm %s"%(f,best,("%.2f-%.2f s"%bspan) if bspan else ""))
        # episodes: marked planted (contact<1) and low-but-marked-moving (contact>=1 and height < rest+2.5)
        for label, test in (("marked planted", lambda r: (r[2] if f=="l" else r[3]) is not None and (r[2] if f=="l" else r[3]) < 1.0),
                            ("low, marked moving", lambda r: (r[2] if f=="l" else r[3]) is not None and (r[2] if f=="l" else r[3]) >= 1.0 and r[1]["ball_"+f].z < rest[f]+2.5)):
            start=None; worst=0.0; span=None
            for r in rows:
                p=r[1]["ball_"+f]
                if test(r):
                    if start is None: start=(p.x,p.y,r[0])
                    d=math.hypot(p.x-start[0],p.y-start[1])
                    if d>worst: worst=d; span=(start[2],r[0])
                else: start=None
            L.append("   ball_%s %s: worst travel %.1f cm %s"%(f,label,worst,("%.2f-%.2f s"%span) if span else ""))
open("F:/LedgerTools/scratch/gasp-export/clip_feet.txt","w").write("\n".join(L))
