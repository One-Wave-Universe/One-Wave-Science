"""Exploratory translator atlas; does not extend the locked runtime grammar."""
from fractions import Fraction
import json
from pathlib import Path

FAMILIES = {
    'original': ('2*N', (0,), 'locked'),
    'odd_up': ('2*N+1', (0,), 'alias of locked ascending_after K=1'),
    'ascending_after': ('2*N+K', (1, 2, 3), 'locked'),
    'ascending_before': ('2*(N+K)', (1, 2, 3), 'locked'),
    'half': ('N/2', (0,), 'exploratory rational'),
    'subtract_then_half': ('(N-K)/2', (1, 2, 3), 'user-clarified exploratory division'),
    'half_then_subtract': ('N/2-K', (1, 2, 3), 'exploratory rational'),
}


def top(n, family, k=0):
    if type(n) is not int or n < 1 or type(k) is not int:
        raise ValueError('N positive integer; K integer')
    if family not in FAMILIES:
        raise ValueError('Unknown family')
    if (family in ('original', 'odd_up', 'half') and k != 0) or (
            family not in ('original', 'odd_up', 'half') and k < 1):
        raise ValueError('Invalid K for family')
    n = Fraction(n)
    return {'original': lambda: 2*n, 'odd_up': lambda: 2*n+1,
            'ascending_after': lambda: 2*n+k,
            'ascending_before': lambda: 2*(n+k), 'half': lambda: n/2,
            'subtract_then_half': lambda: (n-k)/2,
            'half_then_subtract': lambda: n/2-k}[family]()


def recover(value, family, k=0):
    v = Fraction(value)
    return {'original': lambda: v/2, 'odd_up': lambda: (v-1)/2,
            'ascending_after': lambda: (v-k)/2,
            'ascending_before': lambda: v/2-k, 'half': lambda: 2*v,
            'subtract_then_half': lambda: 2*v+k,
            'half_then_subtract': lambda: 2*(v+k)}[family]()


def packets(size, family, k=0, inverted=False, opposing=False):
    if type(size) is not int or size not in (12, 26):
        raise ValueError('Domain must be 12 or 26')
    labels = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') if size == 26 else [
        'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    if inverted:
        labels.reverse()
    indices = list(range(1, size+1))
    if opposing:
        indices.reverse()
    result = []
    for sign in (-1, 1):
        for n in indices:
            t = top(n, family, k)
            for side in (-1, 1):
                w = sign*(t + side*(-1 if inverted else 1))
                result.append(dict(label=labels[n-1], n=n, sign=sign,
                    family=family, k=k, inverted=inverted, opposing=opposing,
                    logical_side=side, x=sign*n, top=str(sign*t), wrapper=str(w),
                    top_parity=None if t.denominator != 1 else int(t) % 2))
    return result


def export(path):
    views = []
    for size in (26, 12):
        for family, (formula, steps, status) in FAMILIES.items():
            for k in steps:
                for inverted in (False, True):
                    for opposing in (False, True):
                        views.append(dict(size=size, family=family, formula=formula,
                            k=k, status=status, inverted=inverted, opposing=opposing,
                            packets=packets(size, family, k, inverted, opposing)))
    Path(path).write_text(json.dumps(views, separators=(',', ':')))
    return len(views)


if __name__ == '__main__':
    print('Views:', export(Path(__file__).with_name('atlas-data.json')))
