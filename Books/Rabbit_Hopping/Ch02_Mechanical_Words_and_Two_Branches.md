# Rabbit Hopping — Chapter 2
# Mechanical Words and the Two Branches

For irrational slope `alpha` and intercept `rho`:

[
b_t=lfloor(t+1)alpha+hofloor-lfloor talpha+hofloor.
]

Every token is either 0 or 1.

That binary output is deliberately narrow. It does not know the alphabet letter, note, motor, sign, or final action. It only says which of two branch positions is selected at this step.

Rabbit-Hop then supplies the declared anchor:

[
e_t=2(n_t+j_t)
]

and converts the token to the odd side:

[
o_t=e_t+(2b_t-1).
]

So:

```text
0 -> lower wrapper
1 -> upper wrapper
```

The source and anchor remain in the receipt so the same odd numerical address cannot erase where it came from.

Next: Chapter 3 asks how we know a trace is actually Sturmian.
