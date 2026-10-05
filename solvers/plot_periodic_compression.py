"""Render measured traces only; no reconstructed excitation imagery."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
r=json.loads((root/'periodic_compression_results.json').read_text())
fig,axes=plt.subplots(1,3,figsize=(14,4),layout='constrained')
selected=[r['runs'][0],r['runs'][-1]]+r['refinement_controls']
for q in selected:
    p=q['parameters'];trace=q['trace']
    label=f"eta={p['eta']:g}, A={p['amplitude']:g}, N={p['active_sites']}, dt={p['dt']:g}"
    axes[0].plot([x['t'] for x in trace],[x['excitation_activity_inside_radius2'] for x in trace],label=label)
    axes[1].plot([x['t'] for x in trace],[x['full_state_return_error'] for x in trace],label=label)
axes[0].axhline(.8,color='black',ls=':',label='screen threshold')
axes[1].axhline(.1,color='black',ls=':')
for q in r['growth_onset_controls']:
    axes[2].plot([x['t'] for x in q['trace']],[x['peak_amplitude'] for x in q['trace']],label=f"dt={q['parameters']['dt']:g}")
for ax,title,ylabel in zip(axes,['Localization control','Full-state return','Growth onset refinement'],['Activity fraction inside radius 2','Distance from initial state / initial size','Peak excitation amplitude']):
    ax.set(title=title,xlabel='Dimensionless evolution time',ylabel=ylabel)
    ax.grid(alpha=.2);ax.legend(fontsize=7)
fig.suptitle('Reciprocal FCC candidate: finite recurrence screen, not a physical clock',fontsize=12)
fig.savefig(root/'periodic_compression_controls.svg')
