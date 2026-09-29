# Diameter involution

On the 12-rail treat notes as \(\mathbb{Z}/12\mathbb{Z}\).

$$
I(n)=n+6 \pmod{12},\qquad T(n)=n+7 \pmod{12}
$$

## What holds

1. **Involution.** \(I^2=\mathrm{id}\). Across 6 o'clock twice is home.
2. **No fixed points.** \(I(n)=n\) would need 6 ≡ 0 (mod 12). Nothing sits on its own mirror.
3. **Six pairs.** (0,6) (1,7) (2,8) (3,9) (4,10) (5,11).
4. **Commutes with the fifth.** \(IT=TI\). Walking +7 then flipping 6 is the same as flipping then walking +7. Because 6+7=13≡1, same residue either order.
5. **Chords.** I sends {0,4,7} Major to {6,10,1} Major-on-6. Minor {0,3,7} → {6,9,1}. Aug {0,4,8} → {6,10,2}, still balanced.

I is translation by the unique element of order 2 in \(\mathbb{Z}/12\). T is translation by 7, which generates (order 12). The group they generate is still cyclic of order 12 plus that involution that *is already inside it* (6=6·1). So I is not a new generator; it is T^6, because 7·6=42≡6 (mod 12).

$$
T^6 = I
$$

Six fifths land on the diameter. That is the whole theory at Yellow.

## What this is not

Not a field rotation derived from CERN. Not Mass Effect. Not T6. Not semitones.
