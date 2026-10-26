import numpy as np, itertools, math

def build_net(K,J,V):
    vals=np.linspace(0,1,V)
    E=np.array(list(itertools.product(range(V),repeat=K*J))).reshape(-1,K,J)
    return vals[E]

def run(K,J,V,T,seed,deliver,ctx,valfun):
    """valfun(c) -> comparator value at this round (a floor achievable by some arm)."""
    rng=np.random.default_rng(seed)
    net=build_net(K,J,V); N=net.shape[0]; logN=math.log(N)
    w=np.ones(N); gamma=0.5; eta=gamma/K
    tot=0.0; comp=0.0
    cnt=np.zeros(K,dtype=int); Ai=0.0; Qi=0; compQi=0.0
    for t in range(T):
        s=t+1
        if (s & (s-1))==0:
            w=np.ones(N); gamma=min(0.5,math.sqrt(K*logN/s)); eta=gamma/K
        c=ctx[t]
        rec=np.argmax(net[:,np.arange(K),c],axis=1)
        q=w/w.sum(); xi=np.zeros(K); np.add.at(xi,rec,q)
        p=(1-gamma)*xi+gamma/K; p=p/p.sum()
        I=rng.choice(K,p=p)
        m=deliver(cnt,I,c,t)
        Y=1.0 if rng.random()<=m else 0.0
        tot+=Y; comp+=valfun(c)
        if I==0:
            Ai+=m; Qi+=1; compQi+=valfun(c)
        yhat=np.zeros(K); yhat[I]=Y/p[I]
        w*=np.exp(eta*yhat[rec]); w/=w.max()
    return dict(tot=tot,comp=comp,N=N,logN=logN,Ai=Ai,Qi=Qi,compQi=compQi)

def Rbound(K,T,logN):
    # doubling sum of 3 sqrt(K 2^k logN) + 2 K logN, k=0..log2(T)
    m=int(math.ceil(math.log2(T+1)))
    return sum(3*math.sqrt(K*(2**k)*logN)+2*K*logN for k in range(m))

K=3; J=3; V=2; T=2048
net_eps=1.0/(V-1)/2      # net resolution (half a value step)
rng=np.random.default_rng(7)
# ---- Part (C) style: agent 0 honest with floor g0; agents 1,2 strategic, floor 0
g0=[0.0,0.5,1.0]
def valC(c): return g0[c[0]]
def mk_deliverC(mode,B):
    def f(cnt,I,c,t):
        cnt[I]+=1
        if I==0: return g0[c[0]]
        if mode=="zero": return 0.0
        if mode=="bait": return 1.0 if cnt[I]<=B else 0.0
        if mode=="mimic": return g0[c[0]]*0.999 if cnt[I]<=B else 0.0
    return f
print("PART (C) test: benchmark sum_t g0(c0), K=%d J=%d V=%d T=%d"%(K,J,V,T))
for mode,B in [("zero",0),("bait",64),("bait",256),("mimic",256)]:
    worst=-1e9
    for seed in range(5):
        ctx=rng.integers(0,J,size=(T,K))
        r=run(K,J,V,T,seed,mk_deliverC(mode,B),ctx,valC)
        R=Rbound(K,T,r["logN"]); slack=r["tot"]-(r["comp"]-2*net_eps*T-R)
        worst=max(worst,-slack)
    print("  %-6s B=%-4d ALG-bench+2epsT+R min slack=%.1f (violation if <0): %s  [R=%.0f, 2epsT=%.0f, N=%d]"%(mode,B,-worst,-worst>=0,R,2*net_eps*T,r["N"]))

print()
print("PART (C) raw regret (bench - ALG), bound is vacuous at this horizon:")
for mode,B in [("zero",0),("bait",64),("bait",256),("mimic",256)]:
    vals=[]
    for seed in range(5):
        ctx=rng.integers(0,J,size=(T,K))
        r=run(K,J,V,T,seed,mk_deliverC(mode,B),ctx,valC)
        vals.append(r["comp"]-r["tot"])
    print("  %-6s B=%-4d raw regret mean=%.1f max=%.1f  (T=%d, 2epsT=%.0f)"%(mode,B,np.mean(vals),max(vals),T,2*net_eps*T))

# ---- Part (A) style deterrence test: agent 0 = deviator (floor 0), agents 1..K-1 play S*
M=[[0.0,0.0,0.0],[0.3,0.9,0.5],[0.8,0.2,0.6]]   # M_j on the J cells; agent 0 irrelevant
def valA(c): return max(M[j][c[j]] for j in range(1,K))     # V_i(X)
def mk_deliverA(mode,B):
    def f(cnt,I,c,t):
        cnt[I]+=1
        if I>=1: return M[I][c[I]]
        if mode=="zero": return 0.0
        if mode=="bait": return 1.0 if cnt[0]<=B else 0.0
        if mode=="half": return 0.5
    return f
print()
print("PART (A) deterrence: check  Abar_i >= sum_{t in Q_i} V_i - 2 eps H - R  (conservation)")
for mode,B in [("zero",0),("bait",128),("half",0)]:
    for seed in range(3):
        ctx=rng.integers(0,J,size=(T,K))
        r=run(K,J,V,T,seed,mk_deliverA(mode,B),ctx,valA)
        R=Rbound(K,T,r["logN"])
        lhs=r["Ai"]; rhs=r["compQi"]-2*net_eps*T-R
        raw=r["compQi"]-r["Ai"]
        print("  %-5s seed=%d Qi=%4d  Abar=%.1f  sum V_i over Q_i=%.1f  raw gap=%.1f  (allowance 2epsT+R=%.0f) ok=%s"%(mode,seed,r["Qi"],lhs,r["compQi"],raw,2*net_eps*T+R,lhs>=rhs))
