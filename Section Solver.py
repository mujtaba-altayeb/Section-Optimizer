import numpy as np
import math


def calculate(gk, qk, l, b, h, cover, Ast_dia, Asc_dia, fcu, fy):

    w = (1.4*gk+1.6*qk)*l
    d = h-cover-Ast_dia/2
    d_prime = cover - Asc_dia / 2
    m = w*l/8
    mu = 0.156*fcu*b*(d**2)*(10**-6)

    print(f"M = {m}")
    print(f"Mu = {mu}")

    # calculation of z
    k = (m * 10 ** 6) / (fcu * b * (d ** 2))
    k_prime = 0.156

    print()
    if k <= k_prime:
        print("Mu > M")
        print("OK.")
        z = d * (0.5 + math.sqrt((0.25 - (k / 0.9))))
        Ast_req = (m * 10 ** 6) / (0.87 * fy * z)
        Asc_req = 0
    else:
        z = d * (0.5 + np.sqrt(0.25 - (k_prime / 0.9)))
        Ast_req = (m * 10 ** 6) / (0.87 * fy * z)
        Asc_req = ((m-mu)*10**6)/(0.87*fy*(d-d_prime))

    n_bars_t = math.ceil(Ast_req / ((math.pi * Ast_dia ** 2) / 4))
    n_bars_c = math.ceil(Asc_req / ((math.pi * Asc_dia ** 2) / 4))

    Ast_prov = (math.pi * Ast_dia ** 2)*n_bars_t / 4
    Asc_prov = (math.pi * Asc_dia ** 2)*n_bars_c / 4

    print(f"Ast_req = {Ast_req}")
    print(f"Asc_req = {Asc_req}")

    print(f"Ast_prov = {Ast_prov}")
    print(f"Asc_prov = {Asc_prov}")

    print(f"n_bars_t = {n_bars_t}")
    print(f"n_bars_c = {n_bars_c}")
