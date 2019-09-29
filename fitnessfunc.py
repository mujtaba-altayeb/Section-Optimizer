import numpy as np

steel_bars = {
    "8": {"Assad": 59, "Abanoob": 59.5, "Omega": 58.5, "Abulgasim": 58, "GIAD": 59},
    "10": {"Assad": 60, "Abanoob": 59.5, "Omega": 58.5, "Abulgasim": 58, "GIAD": 59},
    "12": {"Assad": 60, "Abanoob": 59.5, "Omega": 58.5, "Abulgasim": 58, "GIAD": 59},
    "16": {"Assad": 60.5, "Abanoob": 59.5, "Omega": 59.5, "Abulgasim": 58, "GIAD": 59},
    "20": {"Assad": 62, "Abanoob": 59.5, "Omega": 59.5, "Abulgasim": 58, "GIAD": 59},
    "25": {"Assad": 63, "Abanoob": 59.5, "Omega": 59.5, "Abulgasim": 58, "GIAD": 59},
}

brands = ["Assad", "Abanoob", "Omega", "Abulgasim", "GIAD"]


def design_section(gk, qk, l, b, h, cover, Ast_dia, Asc_dia, fcu, fy, brand):
    w = (1.4 * gk + 1.6 * qk)
    d = h - cover - Ast_dia / 2
    d_prime = cover + Asc_dia / 2
    mu = 0.156 * fcu * b * (d ** 2) * (10 ** -6)
    m = (w * l ** 2 / 8)

    # calculation of z
    k = (m * 10 ** 6) / (fcu * b * (d ** 2))
    k_prime = 0.156

    if m > mu:
        z = d * (0.5 + np.sqrt(0.25 - (k_prime / 0.9)))
        Asc_req = ((m - mu) * 10 ** 6) / (0.87 * fy * (d - d_prime))
        Ast_req = (mu * 10 ** 6) / (0.87 * fy * z) + Asc_req
    else:
        z = d * (0.5 + np.sqrt((0.25 - (k / 0.9))))
        Ast_req = (m * 10 ** 6) / (0.87 * fy * z)
        Asc_req = 0

    selected_brand = brands[int(brand)]

    n_bars_t = np.ceil(Ast_req / ((np.pi * Ast_dia ** 2) / 4))
    n_bars_c = np.ceil(Asc_req / ((np.pi * Asc_dia ** 2) / 4))

    ast_prov = n_bars_t * np.pi * (Ast_dia ** 2) / 4
    asc_prov = n_bars_c * np.pi * (Asc_dia ** 2) / 4

    price_t = steel_bars[str(int(Ast_dia))][selected_brand]
    price_c = steel_bars[str(int(Asc_dia))][selected_brand]

    cost = Ast_req*price_t + Asc_req*price_c + b + h

    return cost, n_bars_t, n_bars_c
