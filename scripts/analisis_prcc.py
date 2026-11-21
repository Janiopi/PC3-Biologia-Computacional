#!/usr/bin/env python3
"""
Analisis LHS/PRCC del modelo de dengue.

1) Lee la salida del software del curso (carpeta out_dengue): trayectorias, lhsmatrix y prcc.000X
2) Resuelve de forma independiente (scipy, LSODA) las MISMAS combinaciones de parametros
3) Calcula PRCC propio y lo compara con el del software
4) Calcula outcomes adicionales (pico, dia del pico) y genera las figuras

Uso:  python3 analisis_prcc.py [carpeta_salida_software] [carpeta_figuras]
"""
import sys, glob, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import rankdata, t as tdist
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "out_dengue"
FIG = sys.argv[2] if len(sys.argv) > 2 else "figuras"
os.makedirs(FIG, exist_ok=True)

PARAMS = ["b", "beta_h", "beta_v", "sigma_h", "gamma_h", "sigma_v", "mu_v", "m", "u"]
LABELS = [r"$b$", r"$\beta_h$", r"$\beta_v$", r"$\sigma_h$", r"$\gamma_h$",
          r"$\sigma_v$", r"$\mu_v$", r"$m$", r"$u$"]
MU_H = 0.0000391
COLORS = plt.get_cmap("tab10")(np.arange(9))

# ------------------------------------------------------------------ lectura
with open(os.path.join(OUT, "lhsmatrix")) as f:
    nvar, nsim, nout, nsteps = map(int, f.readline().split())
    X = np.array([[float(v) for v in f.readline().split()] for _ in range(nvar)]).T  # (nsim, nvar)
files = sorted(glob.glob(os.path.join(OUT, "[0-9][0-9][0-9][0-9]")))
SW = np.array([np.loadtxt(f) for f in files])            # (nsim, nt, 5): t, ih, ivr, ch, R0
tgrid = SW[0, :, 0]
print(f"Software: {nsim} corridas, {nvar} parametros, {len(tgrid)} tiempos (0..{tgrid[-1]:.0f} d)")

# ------------------------------------------------------------------ PRCC
def prcc(X, y):
    """PRCC de cada columna de X frente a y, con p-valor (t de Student, gl = n-k-1)."""
    n, k = X.shape
    R = np.column_stack([rankdata(X[:, j]) for j in range(k)] + [rankdata(y)])
    C = np.corrcoef(R, rowvar=False)
    if not np.all(np.isfinite(C)):
        return np.full(k, np.nan), np.full(k, np.nan)
    P = np.linalg.inv(C)
    r = -P[:k, k] / np.sqrt(np.diag(P)[:k] * P[k, k])
    tt = r * np.sqrt((n - k - 1) / (1 - r ** 2))
    p = 2 * tdist.sf(np.abs(tt), n - k - 1)
    return r, p

# ------------------------------------------------------------------ modelo en Python
def rhs(t, y, b, bh, bv, sh_, gh, sv_, mv, m, u):
    sh, eh, ih, rh, ch, svr, evr, ivr = y
    lam_h = b * bh * m * ivr
    lam_v = b * bv * ih
    return [MU_H - lam_h * sh - MU_H * sh,
            lam_h * sh - (sh_ + MU_H) * eh,
            sh_ * eh - (gh + MU_H) * ih,
            gh * ih - MU_H * rh,
            sh_ * eh,
            mv - lam_v * svr - (mv + u) * svr,
            lam_v * svr - (sv_ + mv + u) * evr,
            sv_ * evr - (mv + u) * ivr]

def R0f(b, bh, bv, sh_, gh, sv_, mv, m, u):
    return np.sqrt(b * b * bh * bv * m * sh_ * sv_ * mv / (mv + u) /
                   ((gh + MU_H) * (sh_ + MU_H) * (mv + u) * (sv_ + mv + u)))

y0 = [0.999, 0, 0.001, 0, 0, 1, 0, 0]
tfine = np.arange(0, 365.0001, 1.0)
IH = np.zeros((nsim, len(tfine))); IV = np.zeros_like(IH); CH = np.zeros_like(IH)
for i in range(nsim):
    s = solve_ivp(rhs, (0, 365), y0, t_eval=tfine, args=tuple(X[i]), method="LSODA", rtol=1e-9, atol=1e-12)
    if not s.success:
        raise RuntimeError(s.message)
    IH[i], CH[i], IV[i] = s.y[2], s.y[4], s.y[7]
R0 = np.array([R0f(*X[i]) for i in range(nsim)])

# ------------------------------------------------------------------ comparacion trayectorias
idx = [int(round(t)) for t in tgrid]          # tgrid es multiplo de 5 d, tfine paso 1 d
d_ih = np.abs(IH[:, idx] - SW[:, :, 1]).max()
d_iv = np.abs(IV[:, idx] - SW[:, :, 2]).max()
d_ch = np.abs(CH[:, idx] - SW[:, :, 3]).max()
d_r0 = np.abs(R0 - SW[:, 5, 4]).max()
print("\n== Trayectorias: maxima diferencia absoluta software (RK4, h=0.05) vs scipy (LSODA) ==")
print(f"  ih: {d_ih:.2e}   ivr: {d_iv:.2e}   ch: {d_ch:.2e}   R0: {d_r0:.2e}")

# ------------------------------------------------------------------ comparacion PRCC en el tiempo
names = ["ih", "ivr", "ch"]
def read_prcc(path):
    return np.array([[float(v) for v in l.split("\t") if v.strip()]
                     for l in open(path) if l.strip() and len(l.split("\t")) > 8])
orig_dir = os.path.join(OUT, "prcc_original")
have_orig = os.path.isdir(orig_dir)
print("\n== PRCC: maxima diferencia absoluta frente al calculo independiente en Python ==")
print("  (todos los parametros y tiempos)       " + ("prcc original   prcc_fix" if have_orig else "prcc del software"))
PY_T = {}
for k, nm in enumerate(names):
    S = read_prcc(os.path.join(OUT, f"prcc.000{k+1}"))
    ts = S[:, 0]
    sw_r = S[:, 8::2][:, :nvar]; sw_p = S[:, 9::2][:, :nvar]
    arr = {"ih": IH, "ivr": IV, "ch": CH}[nm]
    py_r = np.array([prcc(X, arr[:, int(round(t))])[0] for t in ts])
    rounded_r = np.array([prcc(X, SW[:, np.argmin(np.abs(tgrid - t)), k + 1])[0] for t in ts])
    same_data_error = np.nanmax(np.abs(rounded_r - sw_r))
    print(f"  {nm}: PRCC sobre datos redondeados idénticos: {same_data_error:.6g}")
    d_fix = np.nanmax(np.abs(py_r - sw_r))
    if have_orig:
        So = read_prcc(os.path.join(orig_dir, f"prcc.000{k+1}"))
        d_orig = np.abs(py_r - So[:, 8::2][:, :nvar]).max()
        print(f"  {nm:4s}: {d_orig:.3f}            {d_fix:.3f}")
    else:
        print(f"  {nm:4s}: {d_fix:.3f}")
    PY_T[nm] = (ts, sw_r, sw_p, py_r)

# ------------------------------------------------------------------ outcomes escalares
peak = IH.max(axis=1)
tpk = tfine[IH.argmax(axis=1)]
epi = (peak > 2 * y0[2]) & (tpk > 0) & (tpk < 365)
fin = CH[:, -1]
out_sc = {"Acumulado a 365 días": (fin, np.ones(nsim, bool)),
          "Pico de infectados": (peak, np.ones(nsim, bool)),
          "Día del pico (pico > 2Ih(0), interior)": (tpk, epi),
          "R0": (R0, np.ones(nsim, bool))}
res_sc = {}
print("\n== PRCC de outcomes escalares (Python) ==")
for nm, (y, mask) in out_sc.items():
    r, p = prcc(X[mask], y[mask]); res_sc[nm] = (r, p, int(mask.sum()))
    top = np.argsort(-np.abs(r))[:3]
    print(f"  {nm} (n={mask.sum()}): " + ", ".join(f"{PARAMS[j]}={r[j]:+.2f}" for j in top))

# guardar tabla CSV
with open(os.path.join(FIG, "prcc_outcomes_escalares.csv"), "w") as f:
    f.write("outcome,n," + ",".join(f"PRCC_{p}" for p in PARAMS) + "," + ",".join(f"p_{p}" for p in PARAMS) + "\n")
    for nm, (r, p, n) in res_sc.items():
        f.write(f'"{nm}",{n},' + ",".join(f"{v:.4f}" for v in r) + "," + ",".join(f"{v:.3g}" for v in p) + "\n")

# ------------------------------------------------------------------ FIGURA 1: trayectorias
fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
for a, (arr_i, ttl) in zip(ax, [(1, "Infectados humanos $I_h$"), (2, "Mosquitos infecciosos $I_v$ (fracción basal)"), (3, "Casos acumulados $C_h$")]):
    Y = SW[:, :, arr_i]
    a.fill_between(tgrid, np.percentile(Y, 5, axis=0), np.percentile(Y, 95, axis=0), alpha=0.25, color="tab:blue", label="5–95 %")
    a.fill_between(tgrid, np.percentile(Y, 25, axis=0), np.percentile(Y, 75, axis=0), alpha=0.45, color="tab:blue", label="25–75 %")
    a.plot(tgrid, np.median(Y, axis=0), color="navy", label="mediana")
    a.set_title(ttl, fontsize=10); a.set_xlabel("Tiempo (días)"); a.grid(alpha=0.3)
ax[0].set_ylabel("Fracción"); ax[0].legend(fontsize=8)
fig.suptitle("Incertidumbre de las trayectorias (999 corridas LHS, software del curso)", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_trayectorias.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ FIGURA 2: PRCC vs tiempo (software)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
titles = {"ih": "PRCC: infectados $I_h$", "ivr": "PRCC: mosquitos infecciosos $I_v$", "ch": "PRCC: casos acumulados $C_h$"}
for a, nm in zip(ax, names):
    ts, r, p, _ = PY_T[nm]
    for j in range(nvar):
        a.plot(ts, r[:, j], color=COLORS[j], lw=1.5, label=LABELS[j])
        sig = p[:, j] < 0.05
        a.plot(ts[sig], r[sig, j], "o", color=COLORS[j], ms=3.5)
    a.axhline(0, color="k", lw=0.6); a.set_ylim(-1, 1); a.set_title(titles[nm], fontsize=10)
    a.set_xlabel("Tiempo (días)"); a.grid(alpha=0.3)
ax[0].set_ylabel("PRCC")
h, l = ax[0].get_legend_handles_labels()
fig.legend(h, l, ncol=9, fontsize=9, loc="lower center", frameon=False)
fig.suptitle("PRCC calculado con el software del curso (prcc con reinicio de empates; puntos: p < 0.05)", fontsize=11)
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(os.path.join(FIG, "fig2_prcc_tiempo.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ FIGURA 3: PRCC de outcomes escalares (barras)
sel = ["Acumulado a 365 días", "Pico de infectados", "Día del pico (pico > 2Ih(0), interior)"]
fig, ax = plt.subplots(1, 3, figsize=(14, 3.9), sharey=True)
for a, nm in zip(ax, sel):
    r, p, n = res_sc[nm]
    bars = a.bar(range(nvar), r, color=[("tab:red" if v > 0 else "tab:blue") for v in r], alpha=0.85)
    for j in range(nvar):
        if p[j] < 0.05:
            a.text(j, r[j] + (0.04 if r[j] >= 0 else -0.09), "*", ha="center", fontsize=13)
    a.axhline(0, color="k", lw=0.6); a.set_ylim(-1, 1); a.set_xticks(range(nvar)); a.set_xticklabels(LABELS)
    a.set_title(f"{nm}\n(n={n})", fontsize=10); a.grid(axis="y", alpha=0.3)
ax[0].set_ylabel("PRCC")
fig.suptitle("PRCC frente a outcomes escalares (* p < 0.05; rojo = efecto positivo, azul = negativo)", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_prcc_outcomes.png"), dpi=150); plt.close(fig)

print(f"\nFiguras y CSV guardados en: {FIG}/")
