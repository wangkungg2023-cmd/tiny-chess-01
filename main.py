import json,os,sys,urllib.request,urllib.error,random
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("no env")
def post(p,b):
 r=urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(r)as f:return json.load(f)
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
V=[0,100,320,330,500,900,0]
PST=[
[0]*64,
[0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0,10,10,20,30,30,20,10,10,20,20,30,40,40,30,20,20,50,50,50,50,50,50,50,50,0,0,0,0,0,0,0,0],
[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],
[0,-5,5,10,10,5,-5,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,5,10,20,20,20,10,10,5,0,0,0,0,0,0,0,0],
[-10,-10,-5,0,0,-5,-10,-10,-10,0,0,5,5,0,0,-10,-5,0,5,10,10,5,0,-5,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,-5,0,0,5,5,0,0,-5,-10,-10,-5,0,0,-5,-10,-10],
[20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30]]
PKE=[-50,-30,-30,-30,-30,-30,-30,-50,-30,-30,0,0,0,0,-30,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-20,-10,0,0,-10,-20,-30,-50,-30,-30,-30,-30,-30,-30,-50]
KN=[-14,-31,-33,-18,14,31,33,18];KG=[-1,-15,-16,-17,1,15,16,17];BD=[-15,-17,15,17];RD=[-1,-16,1,16]
_r=random.Random(20261118)
ZB=[[_r.getrandbits(64)for _ in range(128)]for _ in range(13)]
ZC=[_r.getrandbits(64)for _ in range(16)];ZE=[_r.getrandbits(64)for _ in range(128)];ZS=_r.getrandbits(64)
IDX=[(s//16)*8+s%16 if not s&0x88 else 0 for s in range(128)]
MATE=100000;INF=1000000
class Abort(Exception):pass
class Pos:
 __slots__=("b","t","c","ep","hm","wk","bk","h")
def parse(fen):
 p=Pos();b=[0]*128;p.b=b;f=fen.split();r=7;fl=0
 for ch in f[0]:
  if ch=="/":r-=1;fl=0
  elif ch.isdigit():fl+=int(ch)
  else:
   v="pnbrqk".index(ch.lower())+1;s=r*16+fl;b[s]=v if ch.isupper()else -v
   if ch=="K":p.wk=s
   if ch=="k":p.bk=s
   fl+=1
 p.t=1 if f[1]=="w"else -1
 p.c=sum((1<<i)for i,k in enumerate("KQkq")if k in f[2])
 p.ep=-1
 if f[3]!="-":p.ep=(int(f[3][1])-1)*16+"abcdefgh".index(f[3][0])
 p.hm=int(f[4])if len(f)>4 else 0
 p.h=hash_of(p);return p
def hash_of(p):
 h=0;b=p.b
 for s in range(128):
  if not s&0x88 and b[s]:h^=ZB[b[s]+6][s]
 h^=ZC[p.c]
 if p.ep>=0:h^=ZE[p.ep]
 if p.t<0:h^=ZS
 return h
def attacked(p,sq,by):
 b=p.b
 if by>0:
  if(not (sq-17)&0x88 and b[sq-17]==1)or(not (sq-15)&0x88 and b[sq-15]==1):return 1
 else:
  if(not (sq+17)&0x88 and b[sq+17]==-1)or(not (sq+15)&0x88 and b[sq+15]==-1):return 1
 for d in KN:
  s=sq+d
  if not s&0x88 and b[s]==2*by:return 1
 for d in KG:
  s=sq+d
  if not s&0x88 and b[s]==6*by:return 1
 for d in BD:
  s=sq+d
  while not s&0x88:
   if b[s]:
    if b[s]==3*by or b[s]==5*by:return 1
    break
   s+=d
 for d in RD:
  s=sq+d
  while not s&0x88:
   if b[s]:
    if b[s]==4*by or b[s]==5*by:return 1
    break
   s+=d
 return 0
def gen_moves(p,capt=False):
 b=p.b;t=p.t;ms=[];ap=ms.append
 for s in range(128):
  if s&0x88:continue
  pc=b[s]
  if not pc or(pc>0)!=(t>0):continue
  a=abs(pc)
  if a==1:
   d=16*t;one=s+d
   if not capt and not b[one]:
    if one//16 in(0,7):
     for pr in(5,4,3,2):ap((s,one,pr*t))
    else:
     ap((s,one,0))
     if s//16==(1 if t>0 else 6)and not b[s+2*d]:ap((s,s+2*d,0))
   for dd in(d-1,d+1):
    to=s+dd
    if to&0x88:continue
    if b[to]and(b[to]>0)!=(t>0):
     if to//16 in(0,7):
      for pr in(5,4,3,2):ap((s,to,pr*t))
     else:ap((s,to,0))
    elif to==p.ep:ap((s,to,0))
  elif a==2 or a==6:
   for d in(KN if a==2 else KG):
    to=s+d
    if to&0x88:continue
    if not b[to]or(b[to]>0)!=(t>0):
     if not capt or b[to]:ap((s,to,0))
  else:
   for d in(BD if a==3 else RD if a==4 else KG):
    to=s+d
    while not to&0x88:
     if b[to]:
      if(b[to]>0)!=(t>0):ap((s,to,0))
      break
     if not capt:ap((s,to,0))
     to+=d
 if not capt:
  if t>0:
   if p.c&1 and not b[5]and not b[6]and b[7]==4 and not attacked(p,4,-1)and not attacked(p,5,-1)and not attacked(p,6,-1):ap((4,6,0))
   if p.c&2 and not b[3]and not b[2]and not b[1]and b[0]==4 and not attacked(p,4,-1)and not attacked(p,3,-1)and not attacked(p,2,-1):ap((4,2,0))
  else:
   if p.c&4 and not b[117]and not b[118]and b[119]==-4 and not attacked(p,116,1)and not attacked(p,117,1)and not attacked(p,118,1):ap((116,118,0))
   if p.c&8 and not b[115]and not b[114]and not b[113]and b[112]==-4 and not attacked(p,116,1)and not attacked(p,115,1)and not attacked(p,114,1):ap((116,114,0))
 return ms
CM={0:13,7:14,112:7,119:11,4:12,116:3}
def make(p,m):
 fr,to,pr=m;b=p.b;pc=b[fr];cap=b[to];csq=to
 if abs(pc)==1 and to==p.ep and not cap:
  csq=to-16*p.t;cap=b[csq]
 undo=(cap,csq,p.c,p.ep,p.hm,p.h)
 h=p.h^ZC[p.c]^ZS
 if p.ep>=0:h^=ZE[p.ep]
 p.ep=-1
 if cap:h^=ZB[cap+6][csq];b[csq]=0
 b[fr]=0;b[to]=pr if pr else pc
 h^=ZB[pc+6][fr]^ZB[(pr if pr else pc)+6][to]
 if abs(pc)==6:
  if pc>0:p.wk=to
  else:p.bk=to
  if to-fr==2:b[fr+1]=b[fr+3];b[fr+3]=0;h^=ZB[b[fr+1]+6][fr+3]^ZB[b[fr+1]+6][fr+1]
  elif fr-to==2:b[fr-1]=b[fr-4];b[fr-4]=0;h^=ZB[b[fr-1]+6][fr-4]^ZB[b[fr-1]+6][fr-1]
 if fr in CM:p.c&=CM[fr]
 if to in CM:p.c&=CM[to]
 if abs(pc)==1:
  p.hm=0
  if abs(to-fr)==32:p.ep=(fr+to)//2;h^=ZE[p.ep]
 elif cap:p.hm=0
 else:p.hm+=1
 p.h=h^ZC[p.c];p.t=-p.t
 return undo
def unmake(p,m,undo):
 fr,to,pr=m;b=p.b;cap,csq,oc,oep,ohm,oh=undo
 p.t=-p.t;p.c=oc;p.ep=oep;p.hm=ohm;p.h=oh
 pc=p.t if pr else b[to]
 b[fr]=pc;b[to]=0
 if cap:b[csq]=cap
 if abs(pc)==6:
  if pc>0:p.wk=fr
  else:p.bk=fr
  if to-fr==2:b[fr+3]=b[fr+1];b[fr+1]=0
  elif fr-to==2:b[fr-4]=b[fr-1];b[fr-1]=0
def evaluate(p):
 b=p.b;s=0;ph=0;kmg=0;keg=0
 for sq in range(128):
  if sq&0x88:continue
  pc=b[sq]
  if not pc:continue
  a=abs(pc);i=IDX[sq]
  if pc<0:i^=56
  if a==6:
   kmg+=PST[6][i]if pc>0 else -PST[6][i]
   keg+=PKE[i]if pc>0 else -PKE[i]
   continue
  ph+=V[a]if a>1 else 0
  v=V[a]+PST[a][i]
  s+=v if pc>0 else -v
 if ph<=1200:s+=keg
 else:s+=kmg
 return s*p.t
NODES=[0];BUDGET=[70000];TT={};HIST={};PATH=set();KILL={};HH={}
def make_null(p):
 u=(p.ep,p.hm,p.h)
 h=p.h^ZS
 if p.ep>=0:h^=ZE[p.ep]
 p.ep=-1;p.hm+=1;p.h=h;p.t=-p.t
 return u
def unmake_null(p,u):
 p.ep,p.hm,p.h=u;p.t=-p.t
def order_key(p,m,ttm):
 if m==ttm:return 1<<30
 cap=p.b[m[1]]
 if abs(p.b[m[0]])==1 and m[1]==p.ep and not cap:cap=-p.t
 s=0
 if cap:s=1<<20+V[abs(cap)]*16-V[abs(p.b[m[0]])]
 if m[2]:s+=1<<19+V[abs(m[2])]
 return s
def qs(p,alpha,beta,ply):
 NODES[0]+=1
 if NODES[0]>BUDGET[0]:raise Abort
 ksq=p.wk if p.t>0 else p.bk
 chk=attacked(p,ksq,-p.t)
 if chk:
  ms=gen_moves(p)
 else:
  st=evaluate(p)
  if st>=beta:return beta
  if st>alpha:alpha=st
  ms=gen_moves(p,True)
 ms.sort(key=lambda m:order_key(p,m,None),reverse=True)
 legal=0
 for m in ms:
  u=make(p,m)
  if attacked(p,p.wk if p.t<0 else p.bk,p.t):unmake(p,m,u);continue
  legal+=1
  sc=-qs(p,-beta,-alpha,ply+1)
  unmake(p,m,u)
  if sc>=beta:return beta
  if sc>alpha:alpha=sc
 if chk and not legal:return -MATE+ply
 return alpha
def search(p,depth,alpha,beta,ply):
 if ply>0 and(p.hm>=100 or p.h in PATH or HIST.get(p.h,0)):return 0
 if depth<=0:return qs(p,alpha,beta,ply)
 NODES[0]+=1
 if NODES[0]>BUDGET[0]:raise Abort
 a0=alpha;ttm=None
 e=TT.get(p.h)
 if e and e[0]>=depth:
  if e[1]==0:return e[2]
  if e[1]==1:alpha=max(alpha,e[2])
  else:beta=min(beta,e[2])
  if alpha>=beta:return e[2]
  ttm=e[3]
 elif e:ttm=e[3]
 ksq=p.wk if p.t>0 else p.bk
 chk=attacked(p,ksq,-p.t)
 if chk:depth+=1
 elif depth>=3 and ply>0:
  st=evaluate(p)
  if st>=beta and any(2<=abs(x)<=5 for x in p.b if x and(x>0)==(p.t>0)):
   u=make_null(p)
   sc=-search(p,depth-3,-beta,-beta+1,ply+1)
   unmake_null(p,u)
   if sc>=beta:return beta
 ms=gen_moves(p)
 kl=KILL.get(ply,())
 ms.sort(key=lambda m:order_key(p,m,ttm)+(1<<18 if m in kl else 0)+HH.get((p.b[m[0]],m[1]),0),reverse=True)
 best=-INF;bm=None;legal=0
 PATH.add(p.h)
 for i,m in enumerate(ms):
  u=make(p,m)
  if attacked(p,p.wk if p.t<0 else p.bk,p.t):unmake(p,m,u);continue
  legal+=1
  quiet=u[0]==0 and not m[2]
  if legal==1:
   sc=-search(p,depth-1,-beta,-alpha,ply+1)
  else:
   r=1 if(depth>=3 and legal>3 and quiet and not chk)else 0
   sc=-search(p,depth-1-r,-alpha-1,-alpha,ply+1)
   if sc>alpha and r:sc=-search(p,depth-1,-alpha-1,-alpha,ply+1)
   if sc>alpha and sc<beta:sc=-search(p,depth-1,-beta,-alpha,ply+1)
  unmake(p,m,u)
  if sc>best:best=sc;bm=m
  if sc>alpha:alpha=sc
  if alpha>=beta:
   if quiet:
    KILL[ply]=(m,kl[0]if kl else m)
    HH[(p.b[m[0]],m[1])]=HH.get((p.b[m[0]],m[1]),0)+depth*depth
   break
 PATH.discard(p.h)
 if not legal:return -MATE+ply if chk else 0
 TT[p.h]=(depth,2 if best<=a0 else 1 if best>=beta else 0,best,bm)
 return best
def uci_of(m):
 s="abcdefgh"[m[0]%16]+str(m[0]//16+1)+"abcdefgh"[m[1]%16]+str(m[1]//16+1)
 if m[2]:s+="pnbrqk"[abs(m[2])-1]
 return s
def parse_uci(u,t):
 fr=(int(u[1])-1)*16+"abcdefgh".index(u[0]);to=(int(u[3])-1)*16+"abcdefgh".index(u[2])
 pr=0
 if len(u)==5:pr=("pnbrqk".index(u[4])+1)*t
 return(fr,to,pr)
def choose(g):
 p=parse(g["start_fen"]);HIST.clear()
 HIST[p.h]=1
 for u in g["moves"]:
  make(p,parse_uci(u,p.t));HIST[p.h]=HIST.get(p.h,0)+1
 legal=g["legal_moves"]
 ms=[m for m in gen_moves(p)if uci_of(m)in legal]
 if not ms:return legal[0]
 if len(ms)==1:return uci_of(ms[0])
 NODES[0]=0;TT.clear();KILL.clear();PATH.clear()
 best=ms[0]
 depth=1
 try:
  while depth<=64:
   cur=None;bs=-INF;a=-INF
   ms.sort(key=lambda m:order_key(p,m,best),reverse=True)
   PATH.add(p.h)
   for m in ms:
    u=make(p,m)
    if attacked(p,p.wk if p.t<0 else p.bk,p.t):unmake(p,m,u);continue
    sc=-search(p,depth-1,-INF,INF,1)
    unmake(p,m,u)
    if cur is None or sc>bs:bs=sc;cur=m
    if sc>a:a=sc
   PATH.discard(p.h)
   if cur is not None:best=cur
   depth+=1
 except Abort:
  pass
 return uci_of(best)
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  try:mv=choose(g)
  except Exception:mv=g["legal_moves"][0]
  g=post("/move",{"game":g["game"],"move":mv})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
