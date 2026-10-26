import numpy as np
# Section 1.2: cost(h,L) = h^{-m} L + n L^{-1/2} + n h, L at its analytic optimum vs L pinned at n^{2/3}
def cost(n, m, pin):
    lh = np.linspace(-9, -1e-6, 200000); h = 10**lh
    L = n**(2/3) if pin else (n*h**m/2)**(2/3)
    return (h**(-m)*L + n/np.sqrt(L) + n*h).min()
ns = np.logspace(6, 24, 40)
for pin in [False, True]:
    print("L pinned at n^{2/3}" if pin else "L retuned per cell")
    for m in [1, 2, 3, 4, 6]:
        e = np.array([cost(n, m, pin) for n in ns])
        s = np.polyfit(np.log(ns), np.log(e), 1)[0]
        print("  m=%d  fitted exponent %.5f   (m+2)/(m+3)=%.5f   1-1/(3(m+1))=%.5f"
              % (m, s, (m+2)/(m+3), 1-1/(3*(m+1))))
