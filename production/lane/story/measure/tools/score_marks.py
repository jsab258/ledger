import re,sys
P=dict(A1=9,A2=9,A3=9,A4=9,B1=6,B2=6,C1=8,D1=7,E1=5,F1=3,G1=3)
N=dict(N1=3,N2=3,N3=3,N4=8,N5=7,N6=6,N7=4,N8=2,N9=2)
if len(sys.argv)>2 and sys.argv[2]=='v2':
    exec(open(sys.argv[3]).read())
for f in sys.argv[1].split(','):
    t=open(f).read()
    print(f.split('/')[-1])
    for m in re.finditer(r'MARKS\s+(\w+):\s*(.*)',t):
        lab=m.group(1); kv=dict(x.split('=') for x in m.group(2).replace('`','').split())
        pr=sum(v for k,v in P.items() if kv.get(k)=='P'); lost=sum(v for k,v in N.items() if kv.get(k)=='F')
        print(f"  {lab}: praise {pr}/{sum(P.values())} lost {lost}/{sum(N.values())} net {pr-lost} overall {kv.get('OVERALL')}  fails: {' '.join(k for k in list(P)+list(N) if kv.get(k)=='F')}")
