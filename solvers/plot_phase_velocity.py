"""Plot actual phase/velocity-search traces, with stopped cases labeled."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
r=json.loads((root/'phase_velocity_results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
for q in r['runs']:
    p=q['parameters'];a=q['trace']
    label=f"{p['kind']}, A={p['amplitude']:g}, eta={p['eta']:g}"+(' [stopped]' if not q['gates']['completed'] else '')
    axes[0].plot([v['t'] for v in a],[v['localized_fraction'] for v in a],label=label)
    b=[v for v in a if v['return_to_time5_error'] is not None]
    axes[1].plot([v['t'] for v in b],[v['return_to_time5_error'] for v in b],label=label)
axes[0].axhline(.8,color='black',ls=':')
axes[1].axhline(.1,color='black',ls=':')
axes[1].set_yscale('symlog',linthresh=.1)
axes[1].set_ylim(bottom=0)
for ax,title,y in zip(axes,['Fixed-origin localization','Full-state return to time-5 reference'],['Excitation activity fraction inside radius 2','State-distance / reference size']):
    ax.set(title=title,xlabel='Dimensionless time',ylabel=y);ax.grid(alpha=.2);ax.legend(fontsize=7)
fig.suptitle('FCC phase/velocity seeds under unchanged reciprocal law',fontsize=12)
fig.savefig(root/'phase_velocity_controls.svg')
