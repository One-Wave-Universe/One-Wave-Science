#!/usr/bin/env python3
"""Finite reference receipts for G-721a through G-721e.

These tests validate declared word constructions. They do not validate android movement.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import csv, json, math

OUT=Path(__file__).resolve().parent

def factors(word:str,n:int)->set[str]:
    return {word[i:i+n] for i in range(len(word)-n+1)}

def complexity(word:str,max_n:int):
    return {n:len(factors(word,n)) for n in range(1,max_n+1)}

def balanced_binary(word:str,max_n:int)->bool:
    for n in range(1,max_n+1):
        counts=[f.count('1') for f in factors(word,n)]
        if counts and max(counts)-min(counts)>1:
            return False
    return True

def mechanical(alpha:float,rho:float,N:int)->str:
    return ''.join(str(math.floor((t+1)*alpha+rho)-math.floor(t*alpha+rho)) for t in range(N))

def substitute(seed:str,rules:dict[str,str],min_len:int)->str:
    w=seed
    while len(w)<min_len:
        w=''.join(rules[c] for c in w)
    return w

def fib_word(min_len:int)->str:
    return substitute('0',{'0':'01','1':'0'},min_len)

def trib_word(min_len:int)->str:
    return substitute('0',{'0':'01','1':'02','2':'0'},min_len)

def plastic_generations(gens:int):
    rules={'I':'EO','E':'I','O':'E'}
    w='I'; rows=[]
    for g in range(gens):
        rows.append({'generation':g,'length':len(w),'I':w.count('I'),'E':w.count('E'),'O':w.count('O'),'prefix':w[:80]})
        w=''.join(rules[c] for c in w)
    return rows

N=5000; max_n=12
phi=(1+5**0.5)/2
fib=fib_word(N)[:N]
sturm=mechanical(math.sqrt(2)-1,0.173,N)
trib=trib_word(N)[:N]
plast=plastic_generations(18)

rows=[]
for label,word,target in [('fibonacci',fib,lambda n:n+1),('sturmian_sqrt2',sturm,lambda n:n+1),('tribonacci_AR',trib,lambda n:2*n+1)]:
    c=complexity(word,max_n)
    for n,v in c.items():
        rows.append({'family':label,'factor_length':n,'observed_complexity':v,'target_complexity':target(n),'pass':v==target(n)})

with (OUT/'factor_complexity.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
with (OUT/'plastic_padovan_generations.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=plast[0].keys());w.writeheader();w.writerows(plast)

plastic_recurrence=[]
for i in range(len(plast)-3):
    plastic_recurrence.append(plast[i+3]['length']==plast[i+1]['length']+plast[i]['length'])

report={
 'sample_length':N,
 'max_factor_length':max_n,
 'fibonacci':{
   'prefix':fib[:60],
   'complexity_pass':all(r['pass'] for r in rows if r['family']=='fibonacci'),
   'balanced_pass':balanced_binary(fib,max_n),
   'one_frequency':fib.count('1')/N,
   'expected_one_frequency_by_this_convention':1/(phi*phi)
 },
 'sturmian_sqrt2_minus_1':{
   'alpha':math.sqrt(2)-1,'rho':0.173,
   'complexity_pass':all(r['pass'] for r in rows if r['family']=='sturmian_sqrt2'),
   'balanced_pass':balanced_binary(sturm,max_n),
   'one_frequency':sturm.count('1')/N
 },
 'tribonacci_arnoux_rauzy_reference':{
   'prefix':trib[:60],
   'complexity_pass':all(r['pass'] for r in rows if r['family']=='tribonacci_AR'),
   'alphabet':sorted(set(trib))
 },
 'plastic_padovan':{
   'substitution':{'I':'EO','E':'I','O':'E'},
   'lengths':[r['length'] for r in plast],
   'padovan_recurrence_pass':all(plastic_recurrence),
   'last_length_ratio':plast[-1]['length']/plast[-2]['length']
 },
 'scope':'Finite word receipts only. No motor or physical validation.'
}
(OUT/'reference_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
