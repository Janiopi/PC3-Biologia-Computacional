#!/usr/bin/env python3
"""Simulación nominal independiente: python3 scripts/simular_dengue.py SALIDA [--u VALOR]."""
import argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PARAMS = ['b', 'beta_h', 'beta_v', 'sigma_h', 'gamma_h', 'sigma_v', 'mu_v', 'm', 'u']
STATES = ['sh', 'eh', 'ih', 'rh', 'ch', 'svr', 'evr', 'ivr']
NOMINAL = [0.6, 0.4, 0.7, 0.1667, 0.2, 0.1, 0.0714, 3.0, 0.05]
Y0 = np.array([0.999, 0, 0.001, 0, 0, 1, 0, 0])
MU_H = 0.0000391


def rhs(t, y, p):
    b, bh, bv, sigma_h, gamma_h, sigma_v, mu_v, m, u = p
    sh, eh, ih, rh, ch, svr, evr, ivr = y
    infection_h = b * bh * m * ivr * sh
    infection_v = b * bv * ih * svr
    return np.array([MU_H - infection_h - MU_H * sh,
                     infection_h - (sigma_h + MU_H) * eh,
                     sigma_h * eh - (gamma_h + MU_H) * ih,
                     gamma_h * ih - MU_H * rh, sigma_h * eh,
                     mu_v - infection_v - (mu_v + u) * svr,
                     infection_v - (sigma_v + mu_v + u) * evr,
                     sigma_v * evr - (mu_v + u) * ivr])


def validate(p, solution):
    reference = [Y0.copy()]
    y = Y0.copy()
    h = 0.05
    for step in range(7300):
        k1 = rhs(0, y, p)
        k2 = rhs(0, y + h * k1 / 2, p)
        k3 = rhs(0, y + h * k2 / 2, p)
        k4 = rhs(0, y + h * k3, p)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if (step + 1) % 20 == 0:
            reference.append(y.copy())
    error = np.max(np.abs(solution - np.array(reference).T))
    assert error < 1e-5, error
    assert np.max(np.abs(solution[:4].sum(axis=0) - 1)) < 1e-8
    assert solution.min() >= -1e-10
    assert np.diff(solution[4]).min() >= -1e-10
    for y in solution.T:
        assert abs(rhs(0, y, p)[5:].sum() - (p[6] - (p[6] + p[8]) * y[5:].sum())) < 1e-12
    return error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('salida', type=Path)
    parser.add_argument('--u', type=float, default=0.05)
    args = parser.parse_args()
    if not np.isfinite(args.u) or args.u < 0:
        parser.error('--u debe ser finito y no negativo')
    if args.salida.exists():
        parser.error('La carpeta de salida debe ser nueva')
    p = NOMINAL.copy()
    p[-1] = args.u
    t = np.arange(366)
    result = solve_ivp(rhs, (0, 365), Y0, args=(p,), t_eval=t,
                       method='LSODA', rtol=1e-10, atol=1e-12)
    if not result.success:
        raise RuntimeError(result.message)
    error = validate(p, result.y)
    args.salida.mkdir(parents=True)
    np.savetxt(args.salida / 'trayectorias.csv',
               np.column_stack([t, result.y.T, p[3] * result.y[1]]), delimiter=',',
               header='dia,' + ','.join(STATES) + ',incidencia', comments='')
    (args.salida / 'parametros.txt').write_text('\n'.join(f'{k}={v}' for k, v in zip(PARAMS, p)))
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, indices, title in zip(axes, [[0, 1, 2, 3], [5, 6, 7], [4]],
                                  ['Humanos (fracciones)', 'Mosquitos (abundancia relativa basal)', 'Casos acumulados (fracción humana)']):
        for i in indices:
            ax.plot(t, result.y[i], label=STATES[i])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('Días')
        ax.legend()
        ax.grid(alpha=0.3)
    fig.tight_layout()
    for extension in ['png', 'svg']:
        fig.savefig(args.salida / f'trayectorias.{extension}')
    plt.close(fig)
    print(f'Balances verificados; error máximo frente a RK4: {error:.3e}')


if __name__ == '__main__':
    main()
