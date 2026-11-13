"""How far a hair tool's strands sit from the head's skin, from its USD curves and the head OBJ (both in the tool's frame).

    python tools/strand_skin_check.py <hair_strands.usda> <head.obj>

WHY, 13 November 2026 (advisor 127): Loomwright's hair looked buried on Darren in Unreal; this measures the tool's own
output before blaming the tool. Signed distance to the nearest head vertex along its normal; negative is inside.
"""
import re, sys, numpy as np
from scipy.spatial import cKDTree
usda, head = sys.argv[1], sys.argv[2]
txt=open(usda).read()
counts=np.array([int(x) for x in re.search(r'int\[\] curveVertexCounts = \[([^\]]*)\]',txt).group(1).split(',')])
pts=np.array(re.findall(r'\(([-\d.e]+), ([-\d.e]+), ([-\d.e]+)\)',re.search(r'point3f\[\] points = \[(.*?)\]\s*\n',txt,re.S).group(1)),dtype=float)
V=[];F=[]
for l in open(head):
    if l.startswith('v '): V.append([float(x) for x in l.split()[1:4]])
    elif l.startswith('f '): F.append([int(x.split('/')[0])-1 for x in l.split()[1:]])
V=np.array(V); N=np.zeros_like(V)
for f in F:
    for i in range(1,len(f)-1):
        n=np.cross(V[f[i]]-V[f[0]],V[f[i+1]]-V[f[0]])
        for k in (f[0],f[i],f[i+1]): N[k]+=n
N/=np.linalg.norm(N,axis=1,keepdims=True)+1e-12
d,i=cKDTree(V).query(pts); s=np.einsum('ij,ij->i',pts-V[i],N[i])
st=np.concatenate([[0],np.cumsum(counts)[:-1]]); tips=st+counts-1
lift=np.array([s[a:a+c].max() for a,c in zip(st,counts)])*1000
print('curves %d points %d; bounds %s to %s'%(len(counts),len(pts),pts.min(0).round(3),pts.max(0).round(3)))
print('all points: median %.1f mm off skin, inside %.0f%%; roots inside %.0f%%; tips median %.1f mm, inside %.0f%%; strand peak lift p50 %.1f p95 %.1f mm'%(np.median(s)*1000,100*(s<0).mean(),100*(s[st]<0).mean(),np.median(s[tips])*1000,100*(s[tips]<0).mean(),*np.percentile(lift,[50,95])))
