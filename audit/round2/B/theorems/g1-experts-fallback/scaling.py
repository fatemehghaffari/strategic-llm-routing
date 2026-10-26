import numpy as np, itertools, math
def build_net(K,J,V):
    vals=np.linspace(0,1,V)
    E=np.array(list(itertools.product(range(V),repeat=K*J))).reshape(-1,K,J)
    return vals[E]
def run(K,J,V,T,seed,deliver,ctx,valfun):
    rng=np.random.default_rng(seed)
    net=build_net(K,J,V); N=net.shape[0]; logN=math.log(N)
    w=np.ones(N); gamma=0.5; eta=gamma/K
    cnt=np.zeros(K,dtype=int); Ai=0.0; Qi=0; compQi=0.0
    for t in range(T):
        s=t+1
        if (s&(s-1))==0:
            w=np.ones(N); gamma=min(0.5,math.sqrt(K*logN/s)); eta=gamma/K
        c=ctx[t]; rec=np.argmax(net[:,np.arange(K),c],axis=1)
        q=w/w.sum(); xi=np.zeros(K); np.add.at(xi,rec,q)
        p=(1-gamma)*xi+gamma/K; p=p/p.sum(); I=rng.choice(K,p=p)
        m=deliver(cnt,I,c,t); Y=1.0 if rng.random()<=m else 0.0
        if I==0: Ai+=m; Qi+=1; compQi+=valfun(c)
        yhat=np.zeros(K); yhat[I]=Y/p[I]; w*=np.exp(eta*yhat[rec]); w/=w.max()
    return Ai,Qi,compQi,logN
K=3;J=3;V=2
M=[[0,0,0],[0.3,0.9,0.5],[0.8,0.2,0.6]]
def valA(c): return max(M[j][c[j]] for j in range(1,K))
def dz(cnt,I,c,t):
    cnt[I]+=1
    return 0.0 if I==0 else M[I][c[I]]
rng=np.random.default_rng(11)
for T in [1024,2048,4096,8192,16384]:
    gaps=[]
    for seed in range(4):
        ctx=rng.integers(0,J,size=(T,K))
        Ai,Qi,cq,logN=run(K,J,V,T,seed,dz,ctx,valA)
        gaps.append(cq-Ai)
    m=np.mean(gaps)
    print("T=%6d  mean gap=%8.1f  gap/sqrt(K T logN)=%.3f"%(T,m,m/math.sqrt(K*T*logN)))
