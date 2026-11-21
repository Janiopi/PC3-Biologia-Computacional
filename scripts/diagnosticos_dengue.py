#!/usr/bin/env python3
"""Diagnósticos adicionales: salida del análisis y carpeta nueva de diagnósticos."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.stats import rankdata
from simular_dengue import rhs, NOMINAL, Y0, PARAMS, validate

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('out', type=Path)
parser.add_argument('destino', type=Path)
args = parser.parse_args()
args.destino.mkdir(parents=True, exist_ok=False)
with (args.out / 'lhsmatrix').open() as stream:
    k, n, _, _ = map(int, stream.readline().split())
    x = np.array([list(map(float, stream.readline().split())) for _ in range(k)]).T
t = np.arange(366)
ih = []; ch = []; iv = []
for p in x:
    sol = solve_ivp(rhs, (0, 365), Y0, args=(p,), t_eval=t, method='LSODA', rtol=1e-9, atol=1e-12)
    if not sol.success:
        raise RuntimeError(sol.message)
    ih.append(sol.y[2]); ch.append(sol.y[4]); iv.append(sol.y[7])
ih = np.array(ih); ch = np.array(ch); iv = np.array(iv)
b,bh,bv,sh,gh,sv,mv,m,u = x.T
r0 = np.sqrt(b*b*bh*bv*m*sh*sv*mv/((gh+.0000391)*(sh+.0000391)*(mv+u)**2*(sv+mv+u)))
peak = ih.max(axis=1); day = ih.argmax(axis=1)
selected = (peak > 2*Y0[2]) & (day > 0) & (day < 365)
outputs = {'Ch365':ch[:,-1], 'pico':peak, 'dia_pico':day, 'R0':r0, 'Ih60':ih[:,60], 'Ih120':ih[:,120], 'Ih240':ih[:,240]}
for name,y in outputs.items():
    mask = selected if name == 'dia_pico' else np.ones(n, dtype=bool)
    fig, axes = plt.subplots(3,3,figsize=(11,9))
    for j,ax in enumerate(axes.flat):
        ax.scatter(rankdata(x[mask,j]), rankdata(y[mask]), s=2, alpha=.3)
        ax.set_xlabel(PARAMS[j]); ax.set_ylabel('Rango '+name)
    fig.tight_layout(); fig.savefig(args.destino / (name+'.png'), dpi=150); plt.close(fig)
fig,axes = plt.subplots(1,2,figsize=(11,4))
controls = []
for control in (0,.05,.15):
    p = NOMINAL.copy(); p[-1] = control
    sol = solve_ivp(rhs,(0,365),Y0,args=(p,),t_eval=t,method='LSODA',rtol=1e-10,atol=1e-12)
    if not sol.success: raise RuntimeError(sol.message)
    error = validate(p,sol.y)
    for ax,idx in zip(axes,(2,4)): ax.plot(t,sol.y[idx],label=f'u={control}')
    controls.append({'u':control,'pico':float(sol.y[2].max()),'dia':int(sol.y[2].argmax()),'Ch365':float(sol.y[4,-1]),'error_rk4_lsoda':float(error)})
for ax,title in zip(axes,('Prevalencia humana','Acumulado a 365 días')):
    ax.set_title(title);ax.set_xlabel('Días');ax.legend()
fig.tight_layout();fig.savefig(args.destino/'controles.png',dpi=150);plt.close(fig)
metadata = {'n':n,'semilla':20261118,'horizonte_dias':365,'RK4_paso':.05,'LSODA_rtol':1e-9,'LSODA_atol':1e-12,'seleccion':'pico>2Ih(0), 0<dia<365','n_seleccion':int(selected.sum()),'maximo_dia365':int((day==365).sum()),'R0_percentiles':np.percentile(r0,[5,50,95]).tolist(),'proporcion_R0_mayor_1':float((r0>1).mean()),'Ch365_percentiles':np.percentile(ch[:,-1],[5,50,95]).tolist(),'controles':controls,'p_valores':'nominales, sin ajuste múltiple'}
(args.destino/'metadatos.json').write_text(json.dumps(metadata,indent=2))
np.savez_compressed(args.destino/'trayectorias_python.npz',X=x,t=t,IH=ih,IV=iv,CH=ch,R0=r0)
print(json.dumps(metadata,indent=2))
