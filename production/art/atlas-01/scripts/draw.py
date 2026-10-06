"""Deterministic authored drawings of the adopted atlas. Python standard library; no procedural layout.

Adopted 2026-10-06 (ADOPTED-2026-10-06.md): the drawings of the earlier Mickey's fit-out (plan,
elevations, yard) are gone with their data; the Hook detail is redrawn to the built street (48 m,
the climb, the bend). Pictures never go into git: SVGs are written to --out (default
F:/LedgerTools/atlas-01-<today>).
"""
from pathlib import Path
import json, html, math, sys, datetime
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
def _out():
    a=sys.argv[1:]
    if '--out' in a: return Path(a[a.index('--out')+1])
    return Path('F:/LedgerTools/atlas-01-'+datetime.date.today().isoformat())
OUT=_out()
A=json.loads((ROOT/'data/atlas.json').read_text())
S=json.loads((REPO/'production/specs/vignette-scene.json').read_text(encoding='utf-8'))
INK='#253a3d'; BG='#f5f0e5'; MUTED='#607073'
def esc(s): return html.escape(str(s))
def text(x,y,s,size=20,fill=INK,anchor='start',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>'
def line(x1,y1,x2,y2,stroke=INK,w=2,dash=''):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{stroke}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def rect(x,y,w,h,fill,stroke='none',sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(pts,fill='none',stroke=INK,w=2,close=False,dash=''):
    p='M'+' L'.join(f'{x},{y}' for x,y in pts)+(' Z' if close else '')
    return f'<path d="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def circle(x,y,r,fill,stroke='none',sw=1): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def save(name,w,h,body,title,subtitle='ADOPTED 2026-10-05 / UPDATED TO THE BUILT STREET 2026-10-06'):
    OUT.mkdir(parents=True,exist_ok=True)
    head=rect(0,0,w,h,BG)+text(38,43,'LEDGER  /  ATLAS 01',17,MUTED,weight=700)+text(38,94,title,40,weight=700)+text(38,125,subtitle,16,MUTED)+line(38,147,w-38,147,'#b9beb3')
    foot=line(38,h-52,w-38,h-52,'#b9beb3')+text(38,h-22,'MERIDIAN  /  1988-1992',15,MUTED)+text(w-38,h-22,'AUTHORED DESIGN',15,MUTED,'end')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>text{{font-family:Arial,Helvetica,sans-serif}}</style>{head}{body}{foot}</svg>'
    (OUT/(name+'.svg')).write_text(svg,encoding='utf-8')
def town(overlay=False):
    def t(p): return (50+p[0]*.8,190+(1020-p[1])*.8)
    b=rect(38,174,904,710,'#dedbcb')
    coast=A['land'][:A['land'].index([1040,1000])+1]
    b+=path([t(p) for p in coast]+[(942,884),(38,884),(38,t(coast[0])[1])],'#b9d3d2','none',0,True)
    b+=path([t(p) for p in A['land']],BG,INK,2,True)
    for i,d in enumerate(A['districts']):
        b+=path([t(p) for p in d['polygon']],d['colour'],'#f5f0e5',2,True)
    for c in A['contours']:
        b+=path([t(p) for p in c['points']],'none','#536e51',1.5,False,'4 5')
        x,y=t(c['points'][0]);b+=text(x+4,y-4,str(c['height'])+'m',13,'#35513e')
    for name,e,n,w,h in A['blocks']:
        x,y=t((e,n+h));b+=rect(x,y,w*.8,h*.8,'#f5f0e5','#536165',.7)
    for r in A['routes']:
        pts=[t(p) for p in r['points']]
        if r['kind']=='main': b+=path(pts,'none','#796f5b',11)+path(pts,'none','#fff6df',8)
        elif r['kind']=='minor':b+=path(pts,'none','#fff6df',4)
        else:b+=path(pts,'none','#f5edcf',3,False,'4 4')
    b+=path([t(p) for p in A['rail']['points']],'none','#4b5350',3,False,'8 5')
    if not overlay:
        for q in A.get('map_labels',[]):
            x,y=t(q['point']);b+=text(x,y,q['text'],14,INK)
    for d in A['districts']:
        x,y=t(d['label']);num=A['districts'].index(d)+1
        b+=circle(x,y,18,INK)+text(x,y+6,num,18,'white','middle',700)
    if overlay:
        for r in A['gameplay']['daily']:b+=path([t(p) for p in r['points']],'none','#e68b29',5)
        for r in A['gameplay']['escape']:b+=path([t(p) for p in r['points']],'none','#00565d',4,False,'6 4')
        for e,n,ee,nn in A['gameplay']['witness']:
            b+=path([t((e,n)),t((ee,nn))],'none','#923f51',3,False,'3 3')
        for p in A['gameplay']['phones']:
            x,y=t(p);b+=rect(x-6,y-6,12,12,'#a73540','#fff',1)
    for l in A['landmarks']:
        x,y=t(l['point']);b+=circle(x,y,4,INK)
        if l['venue']:b+=circle(x,y,9,'none',INK,1)
    if not overlay:
        for label,point in [('Retort works',[75,355]),('Market Hall',[385,680]),('Chapel',[185,820]),('Records Court',[765,883]),('Police',[858,931]),('Tivoli',[748,510]),('Winter Rooms',[844,479]),('Harbour Board',[478,391])]:
            x,y=t(point);b+=rect(x-4,y-15,len(label)*7.7+8,20,BG)+text(x,y,label,14,INK,weight=700)
    # Annotated source street magnifier: too small for phone otherwise.
    x,y=t([404,392]);b+=circle(x,y,40,'none','#fff',3)+line(x+40,y,690,795,'white',2)
    b+=rect(686,776,230,64,INK)+text(703,802,"QUAY STREET",18,'#fff',weight=700)+text(703,826,'See Hook detail',17,'#dae3d8')
    b+=text(306,840,'BASIN',15,INK)+text(765,860,'OPEN SEA',18,INK)
    b+=text(50,166,'INLAND STUDY EXTENT',12,MUTED)
    b+=line(902,243,902,194,INK,3)+path([[894,205],[902,192],[910,205]],INK,INK,1,True)+text(902,183,'N',17,INK,'middle',700)
    b+=line(70,865,230,865,INK,4)+text(70,855,'0',14)+text(230,855,'200 m',14,anchor='end')
    for i,d in enumerate(A['districts']):
        col=i%2;row=i//2;x=45+col*465;y=930+row*62
        b+=circle(x+17,y,17,d['colour'])+text(x+17,y+6,i+1,17,INK,'middle',700)+text(x+45,y-2,d['name'],32,weight=700)+text(x+45,y+22,d['role'],18,MUTED)
    if overlay:
        y=1190;b+=line(50,y,105,y,'#e68b29',5)+text(115,y+6,'Daily routes',18)
        b+=line(335,y,390,y,'#00565d',4,'6 4')+text(400,y+6,'Escape intention',18)
        b+=line(665,y,720,y,'#923f51',3,'3 3')+text(730,y+6,'Possible view',18)
        b+=text(45,1238,'Ring = information venue   /   red square = phone',17,MUTED)
        b+=text(45,1266,'Routes, sightlines and timing are not simulation results.',17,MUTED)
        h=1360
    else:
        b+=text(45,1190,'Pale blocks: authored massing  /  dashed green: elevation',17,MUTED)
        b+=text(45,1220,'Circle: information venue  /  solid pale line: main route',17,MUTED)
        h=1320
    save('gameplay-overlay' if overlay else 'atlas-overview',980,h,b,'How the town talks' if overlay else 'MERIDIAN', 'DESIGN INTENT / NOT SIMULATED' if overlay else 'SEVEN DISTRICTS / ONE WORKING TOWN')
def hook():
    """Quay Street as built: vignette-scene.json (48 m, its blocks) and terrace-front.py's road on
    (level to 52 m, one in twelve to 72 m drifting east, the bend at 72 to 80 m turning east).
    North is up; source +z is east/right; atlas = (400+z, 350+x)."""
    s=9;cx=330;yy=1250
    def t(x,z):return cx+z*s,yy-x*s
    ap=A['street_anchor']['approach'];L=A['street_anchor']['length_m']
    x_flat=ap['level_x'][1];x_top,x_far=ap['bend_x'];x_open=ap['open_ground_x'][1]
    def drift(x):
        k=min(1,max(0,(x-x_flat)/(x_top-x_flat)));return 8.0*k*k
    def band(z0,z1,x0,x1,n=12):
        xs=[x0+(x1-x0)*i/n for i in range(n+1)]
        return [t(x,z0+drift(x)) for x in xs]+[t(x,z1+drift(x)) for x in reversed(xs)]
    b=''
    # open ground past the bend, a kerb above the road
    u,v=t(x_open,-22);b+=rect(u,v,82*s,(x_open-x_far-2)*s,'#cfd6bf')
    x,y=t(100,-20);b+=text(x,y,'open ground, garden wall, cottages, trees, the hill behind',15,MUTED)
    x,y=t(96,-20);b+=text(x,y,'(built as a backdrop, x 80 to 108.8 m)',15,MUTED)
    # the street: carriageway and footways
    for z0,z1,col in [(-3,3,'#838b88'),(3.125,5.125,'#d5cdb9'),(-5.125,-3.125,'#d5cdb9')]:
        x,y=t(L,z0);b+=rect(x,y,(z1-z0)*s,L*s,col)
    # the road on: level, the climb with its drift east, the bend turning east
    for z0,z1,col in [(-3,3,'#838b88'),(3.125,5.125,'#d5cdb9'),(-5.125,-3.125,'#d5cdb9')]:
        b+=path(band(z0,z1,L,x_top),col,'none',0,True)
    u,v=t(x_far,5);b+=rect(u,v,55*s,(x_far-x_top)*s,'#838b88')
    u,v=t(x_far+2,-5.125+8);b+=rect(u,v,(60+5.125-8)*s,2*s,'#d5cdb9')
    x,y=t(x_top+3,60);b+=path([[x,y-12],[x+18,y],[x,y+12]],INK,INK,1,True)+text(x+24,y+6,'on east',16,MUTED)
    # backdrop rows on the climb (dashed: built as backdrop, not town)
    b+=path(band(5.125,13.125,48.5,61),'none','#7d8580',1.2,True,'5 4')
    b+=path(band(-13.125,-5.125,48.5,79.5),'none','#7d8580',1.2,True,'5 4')
    # the built blocks
    for blk in S['blocks']:
        z0=5.125 if blk['side']=='east' else -13.125
        for i in range(blk['bays']):
            x0=blk['start_x_m']+i*blk['bay_width_m']
            u,v=t(x0+blk['bay_width_m'],z0);mick=blk['id']=='east_parade' and i==0
            b+=rect(u,v,8*s,blk['bay_width_m']*s,'#995746' if mick else '#b5aea0',INK,1.2)
            label="MICKEY'S" if mick else ('Fish shop' if blk['id']=='east_parade' and i==1 else ("Chandler's" if blk['id']=='east_chandler' else ''))
            if label:b+=text(u+4*s,v+3*s+5,label,13,'white' if mick else INK,'middle',700)
    # Mickey's yard and its lane (canon: a yard with two escapes)
    u,v=t(9,13.125);b+=rect(u,v,6*s,6*s,'#dbc9a4',INK,1.2)
    b+=text(u+3*s,v+3*s+5,'yard',13,INK,'middle')
    lane=next(r for r in A['routes'] if r['id']=='yardlane')['points']
    b+=path([t(n-350,e-400) for e,n in lane],'none','#1d666d',3,False,'6 4')
    # the yard gap
    a0,a1=A['street_anchor']['yard_gap_x'];u,v=t(a1,-13.125);b+=rect(u,v,8*s,(a1-a0)*s,'#e8dfc9',INK,.8)
    # spot heights (atlas datum: street crown + 4.0 m)
    for sp in ap['spot_heights_m']:
        e,n=sp['point'];x,y=t(n-350,e-400);b+=circle(x,y,4,INK)+text(x+9,y+5,f"+{sp['height']:.2f} m",15,INK,weight=700)
    # chainage along the west side
    for xm,lab in [(0,'0'),(L,f'{L:g} m street end'),(x_flat,f'{x_flat:g} m level ends'),(x_top,f'{x_top:g} m top of the 1 in 12'),(x_far,f'{x_far:g} m bend'),(x_open,f'{x_open:g} m hill wall')]:
        x,y=t(xm,-24);b+=line(x,y,x+14,y,MUTED,1)+text(x-6,y+5,lab,14,MUTED,'end')
    b+=text(490,184,'NORTH: Copper Row / market, by Quay Street',20,anchor='middle',weight=700)
    b+=path([[900,260],[900,215]],'none',INK,3)+path([[892,226],[900,213],[908,226]],INK,INK,1,True)+text(900,205,'N',18,INK,'middle',700)
    x,y=t(-1,0);b+=text(x,y+22,'SOUTH: the quay',18,anchor='middle',weight=700)
    y0=1320
    b+=text(54,y0,'Quay Street, as built',30,weight=700)
    b+=text(54,y0+30,f'{L:g} m street (vignette-scene.json); the road on: level to {x_flat:g} m, one in twelve to {x_top:g} m,',17,MUTED)
    b+=text(54,y0+54,f'drifting 8 m east; the bend at {x_top:g} to {x_far:g} m turns east (terrace-front.py, since 3 October).',17,MUTED)
    for i,(a,c) in enumerate([('6 m carriageway','2 m footway each side'),('3 m west yard gap','x = 21 to 24'),("Mickey's: east bay 0",'the minicab office')]):
        x=54+i*300;b+=text(x,y0+100,a,19,weight=700)+text(x,y0+126,c,16,MUTED)
    b+=text(54,y0+170,"Dashed grey: the climb's two rows, built as a backdrop. Teal dashes: Mickey's yard lane.",16,MUTED)
    save('hook-detail',980,1560,b,'Quay Street / the built street','THE HOOK / ADOPTED MAP UPDATED 2026-10-06')
def dim(x1,y1,x2,y2,label):
    return line(x1,y1,x2,y2,'#667578',1)+line(x1-5,y1-5,x1+5,y1+5,'#667578',1)+line(x2-5,y2-5,x2+5,y2+5,'#667578',1)+text((x1+x2)/2,(y1+y2)/2-8,label,17,MUTED,'middle')
def district_details():
    for i,d in enumerate(A['districts']):
        x0=min(p[0] for p in d['polygon']);x1=max(p[0] for p in d['polygon']);n0=min(p[1] for p in d['polygon']);n1=max(p[1] for p in d['polygon'])
        s=min(730/(x1-x0),590/(n1-n0));ox=70;oy=200
        def t(p):return ox+(p[0]-x0)*s,oy+(n1-p[1])*s
        b=path([t(p) for p in d['polygon']],d['colour'],INK,2,True)
        prefix={'hook':'H','copper':'C','exchange':'E','parade':'P','fairview':'F','ironside':'I','gullwing':'G'}[d['id']]
        if d['id']=='hook':
            b+=path([t(p) for p in [[300,240],[385,240],[385,220],[440,220],[440,280],[300,280]]],'#b9d3d2','none',0,True)
        for name,e,n,w,h in A['blocks']:
            if name.startswith(prefix):
                x,y=t((e,n+h));b+=rect(x,y,w*s,h*s,'#efe7d5','#5e6864',1)
        for r in A['routes']:
            # clip all route geometry to district polygon
            pts=[t(p) for p in r['points']]
            clip=f'<clipPath id="dc{r["id"]}"><path d="M'+ ' L'.join(f'{x},{y}' for x,y in [t(p) for p in d['polygon']])+' Z"/></clipPath>'
            route_draw=path(pts,'none','#fff4dc',6 if r['kind']=='main' else 3,False,'4 4' if r['kind']=='foot' else '')
            water_route=(r['id']=='dockfoot' and d['id']=='hook') or (r['id']=='pier' and d['id']=='gullwing')
            b+=route_draw if water_route else clip+f'<g clip-path="url(#dc{r["id"]})">'+route_draw+'</g>'
        for l in A['landmarks']:
            if l['district']==d['id']:
                x,y=t(l['point']);b+=circle(x,y,8,INK)
                if l['id']=='G1':b+=text(x-16,y-16,'Winter Rooms',21,anchor='end',weight=700)
                elif l['id']=='G2':b+=text(x+16,y+38,'Short pier',21,weight=700)
                else:b+=text(x+16,y-10,l['name'],21,weight=700)
        for q in A.get('map_labels',[]):
            if q.get('district')==d['id']:
                x,y=t(q['point']);b+=text(x,y,q['text'],19,INK,weight=700)
        b+=line(70,821,70+100*s,821,INK,3)+text(70,810,'100 m',17,MUTED)
        b+=text(70,860,d['role'],30,weight=700)+text(70,900,f"Proposed relief: {d['height_m'][0]} to {d['height_m'][1]} m",20,MUTED)
        for j,(name,c) in enumerate(d['materials']):
            x=70+j*198;b+=rect(x,940,175,70,c)+text(x,1040,name,18,MUTED)
        b+=text(70,1115,'Objects: '+', '.join(d['objects'][:2]),18,MUTED)+text(70,1145,', '.join(d['objects'][2:]),18,MUTED)
        b+=line(848,280,848,220,INK,3)+text(848,205,'N',20,INK,'middle',700)
        b+=text(70,1205,'Landmarks and terrain share atlas coordinates. Concept sheets: the archive on F:.',16,MUTED)
        save('district-'+d['id']+'-plan',900,1300,b,d['name'],'DISTRICT DETAIL / PROPOSED MATERIALS')
if __name__=='__main__':
    town();town(True);hook();district_details()
    print('Wrote 10 SVG drawings from authored coordinates to',OUT)
