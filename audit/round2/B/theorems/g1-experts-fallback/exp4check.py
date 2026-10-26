import numpy as np, itertools, math, sys

def build_net(K,J,V):
    """All K-tuples of grid-constant functions with values in {0,...,V-1}/(V-1).
    Expert e is an array shape (K,J) of values; policy = argmax_j e[j, c_j]."""
    vals=np.linspace(0,1,V)
    tuples=list(itertools.product(range(V),repeat=K*J))
    E=np.array(tuples).reshape(-1,K,J)
    return vals[E]

def run(K,J,V,T,seed,adversary,g,ctx,gamma_mode="doubling"):
    rng=np.random.default_rng(seed)
    net=build_net(K,J,V); N=net.shape[0]
    # precompute policy action for each expert and each cell profile
    logN=math.log(N)
    w=np.ones(N); epoch=0; epoch_start=0
    gamma=min(0.5,math.sqrt(K*logN/1.0)); gamma=min(gamma,0.5)
    tot=0.0; comp=0.0
    state=adversary.init(K)
    for t in range(T):
        s=t+1
        if (s & (s-1))==0:  # s is a power of two -> new epoch
            plan=s
            w=np.ones(N)
            gamma=min(0.5,math.sqrt(K*logN/plan)); eta=gamma/K
        c=ctx[t]                      # cell index per agent, shape (K,)
        # expert recommendations
        rec=np.argmax(net[:,np.arange(K),c],axis=1)   # (N,)
        q=w/w.sum()
        xi=np.zeros(K)
        np.add.at(xi,rec,q)
        p=(1-gamma)*xi+gamma/K
        I=rng.choice(K,p=p/p.sum())
        m=adversary.deliver(state,I,c,t)
        Y=1.0 if rng.random()<=m else 0.0
        tot+=Y
        yhat=np.zeros(K); yhat[I]=Y/p[I]
        w*= np.exp(eta*yhat[rec])
        w/=w.max()
        comp+=max(g[j][c[j]] for j in range(K))
    return tot,comp,N,logN

class Deceiver:
    """agent 0 honest: delivers its floor exactly. agents>=1: deliver 1 for the
    first B selections, then 0 (floor 0)."""
    def __init__(self,g,B): self.g=g; self.B=B
    def init(self,K): return np.zeros(K,dtype=int)
    def deliver(self,cnt,I,c,t):
        cnt[I]+=1
        if I==0: return self.g[0][c[0]]
        return 1.0 if cnt[I]<=self.B else 0.0

if __name__=="__main__":
    K=2; J=3; V=3; T=4096
    g=[[0.0,0.5,1.0],[0.0,0.0,0.0]]   # agent 0 honest floors, agent 1 floor 0
    rng=np.random.default_rng(0)
    res=[]
    for seed in range(6):
        ctx=rng.integers(0,J,size=(T,K))
        adv=Deceiver(g,B=T//4)
        tot,comp,N,logN=run(K,J,V,T,seed,adv,g,ctx)
        R=3*math.sqrt(K*T*logN)+2*K*logN
        res.append((tot,comp,comp-tot,R))
        print("seed %d  ALG=%.1f  BENCH=%.1f  regret=%.1f  bound R=%.1f  ok=%s"%(seed,tot,comp,comp-tot,R,comp-tot<=R))
    print("N=%d logN=%.3f"%(N,logN))
