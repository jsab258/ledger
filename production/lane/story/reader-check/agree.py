import sys,itertools
from scipy.stats import spearmanr
tier={'RDR2':1,'GTAV':2,'G4':2,'KCD2':2,'SD':3,'HIT':3,'WDL':4,'LAN':4}
lab={'K':'RDR2','B':'GTAV','R':'G4','M':'KCD2','T':'SD','F':'HIT','N':'WDL','W':'LAN'}
def check(name,ranks):
    games=list(tier)
    pooled={g:sum(r.index(g) for r in ranks.values())/len(ranks) for g in games}
    out=[]
    for k,r in list(ranks.items())+[('pooled',None)]:
        pos={g:(r.index(g) if r else pooled[g]) for g in games}
        rho=spearmanr([tier[g] for g in games],[pos[g] for g in games]).correlation
        conc=tot=0
        for a,b in itertools.combinations(games,2):
            if tier[a]==tier[b]: continue
            tot+=1
            if (tier[a]-tier[b])*(pos[a]-pos[b])>0: conc+=1
        out.append(f"{name} {k}: Spearman {rho:.2f}, pairs {conc} of {tot}, RDR2 place {pos['RDR2']+1:g}")
    return out
if __name__=='__main__':
    R={'reader1':'KRMWTBFN','reader2':'KWRTMBFN','reader3':'KWTRBMFN'}
    ranks={k:[lab[c] for c in v] for k,v in R.items()}
    print("\n".join(check('round 1',ranks)))
    pooled={g:sum(r.index(g) for r in ranks.values())/3 for g in tier}
    print(sorted(pooled,key=pooled.get))
