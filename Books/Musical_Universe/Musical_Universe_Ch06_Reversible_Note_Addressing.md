# Musical Universe — Chapter 6
# Reversible Note Addressing

Music uses the same address core without becoming the alphabet.

The established music adapter maps the twelve chromatic pitch classes to source ranks 1..12, then calls the shared reversible route core.

```text
note
-> pitch class
-> source rank
-> G-764 packet
-> G-765 route
-> G-766 wrapper
-> G-767 reconstruction receipt
```

The Circle of Fifths remains the music-domain cycle owned by E-514:

```text
forward fifth = +7 semitones mod 12
reverse fifth = -7 semitones mod 12
```

Rabbit-Hop does not replace that circle. It gives each selected note position a reversible machine address.

A letter and a note may occupy the same numeric address under their respective adapters. That means **same translator address**, not same meaning.

For example, alphabet rank 3 and chromatic music rank 3 can produce the same ORIGINAL route packet. Their domain labels remain separate in the receipt.

This is the bridge needed for language-to-music translation: translate both through the shared address packet while retaining the domain label and route history.
