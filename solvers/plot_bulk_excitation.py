"""Plot measured outputs only; requires optional matplotlib."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).parent
r=json.loads((root/'bulk_excitation_results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(11,4),layout='constrained')
for label,key in [('Stationary','stationary'),('Phase perturbation','phase_perturbed'),('Amplitude perturbation','amplitude_perturbed')]:
    trace=r['evolution'][key]['trace']; ax[0].plot([x['time'] for x in trace],[x['core_fraction_r2'] for x in trace],label=label)
t=r['linear_control']['trace']; ax[0].plot([x['time'] for x in t],[x['core_fraction_r2'] for x in t],'--',label='Linear control')
ax[0].set(xlabel='Model time (dimensionless)',ylabel='Norm fraction within radius 2',ylim=(0,1.04),title='Localization and spreading')
ax[0].legend(fontsize=8); ax[0].grid(alpha=.2)
t=r['domain_controls']; ax[1].plot([x['box_length'] for x in t],[x['rms_radius'] for x in t],'o-',label='a = 1: enlarge domain')
t=r['spacing_controls']; ax[1].scatter([x['box_length'] for x in t],[x['rms_radius'] for x in t],marker='s',label='a = 1, 0.5: same box')
ax[1].set(xlabel='Periodic box length (dimensionless)',ylabel='RMS excitation radius',title='Finite-domain and spacing controls')
ax[1].legend(fontsize=8); ax[1].grid(alpha=.2)
fig.suptitle('Hypothetical four-coordinate nonlinear closure — not a particle-mass prediction',fontsize=11)
fig.savefig(root/'bulk_excitation_controls.svg')
fig.savefig(root/'bulk_excitation_controls.png',dpi=160)
