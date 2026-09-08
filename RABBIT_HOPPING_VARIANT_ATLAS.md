# Rabbit-hop system translator variant atlas

The 2026-09-08 user handoff and corrections are mapped in [the variant guide](docs/rabbit_hop_variants/README.md).

- [Interactive signed XY atlas](docs/rabbit_hop_variants/atlas.html): download/open locally, or use the [Jetson preview](http://192.168.4.45:8765/translators/atlas.html) on the same LAN.
- [Exact arithmetic and corpus generator](docs/rabbit_hop_variants/translator_variants.py).
- [Regression tests](docs/rabbit_hop_variants/test_translator_variants.py).
- [Original source](docs/rabbit_hop_variants/source.txt), interpreted with the explicit corrections in the guide.

This adds a tested exploration surface. Existing [locked runtime grammar](RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md) remains the runtime authority; the newly clarified division families are documented and plotted without replacing its bounded integer-address rail.
