import re,sys
P1=dict(A1=9,A2=9,A3=9,A4=9,B1=6,B2=6,C1=8,D1=7,E1=5,F1=3,G1=3)
N1=dict(N1=3,N2=3,N3=3,N4=8,N5=7,N6=6,N7=4,N8=2,N9=2)
P=dict(C1=12,C2=12,C3=11,C4=11,W1=9,H1=9,U1=6,E1=5,T1=5)
N=dict(X1=7,X2=7,X3=6,X4=8,X5=6)
S=['S1','S2','S3','S4','S5']
if len(sys.argv)>2 and sys.argv[2]=='v1': P,N,S=P1,N1,[]
for f in sys.argv[1].split(','):
    t=open(f).read()
    print(f.split('/')[-1])
    for m in re.finditer(r'MARKS\s+(\w+):\s*(.*)',t):
        lab=m.group(1); kv=dict(x.split('=') for x in m.group(2).replace('`','').split())
        pr=sum(v for k,v in P.items() if kv.get(k)=='P'); lost=sum(v for k,v in N.items() if kv.get(k)=='F')
        print(f"  {lab}: praise {pr}/{sum(P.values())} lost {lost}/{sum(N.values())} net {pr-lost} overall {kv.get('OVERALL')}  fails: {' '.join(k for k in list(P)+list(N)+S if kv.get(k)=='F')}")
