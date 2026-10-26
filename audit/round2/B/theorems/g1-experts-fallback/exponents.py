from fractions import Fraction as F
rows=[]
for K in [2,3,4,5]:
    for d in [1,2,3]:
        D=K*d
        a_price=F(d+2,d+3)
        a_fb_old=F(D+d+3,2*(d+3))
        a_fb_net=F(d+1,d+2)
        a_CG=F(D+2,D+3)
        pa_old=max(a_price,a_fb_old)
        pa_new=max(a_price,a_fb_net)
        rows.append((K,d,D,float(a_price),float(a_fb_old),float(a_fb_net),float(pa_old),float(pa_new),float(a_CG)))
hdr=("K","d","D","price","fb_grid","fb_net","PA_grid","PA_net","CG")
print("| "+" | ".join(hdr)+" |")
print("|"+"---|"*len(hdr))
for r in rows:
    print("| "+" | ".join(str(x) if isinstance(x,int) else "%.4f"%x for x in r)+" |")
# strictness of (d+1)/(d+2) < (d+2)/(d+3)
print()
for d in range(0,12):
    lhs=F(d+1,d+2); rhs=F(d+2,d+3)
    print(d, float(lhs), float(rhs), lhs<rhs, float(rhs-lhs), 1.0/((d+2)*(d+3)))
