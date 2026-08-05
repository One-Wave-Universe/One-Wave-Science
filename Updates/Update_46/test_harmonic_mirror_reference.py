from harmonic_mirror_reference import DrivenMirror, alphabet_packet, harmonic_packet


def test_examples() -> None:
    assert harmonic_packet(1).__dict__ == {"identity": 1, "carrier": 4, "lower": 3, "upper": 5}
    assert harmonic_packet(2).__dict__ == {"identity": 2, "carrier": 6, "lower": 5, "upper": 7}
    assert alphabet_packet(1) == ((1, 2, 1), (1, 2, 3))


def test_shared_boundary() -> None:
    for n in range(1, 12):
        assert harmonic_packet(n).upper == harmonic_packet(n + 1).lower


def test_driven_width() -> None:
    system = DrivenMirror(sigma=0.0)
    for _ in range(1000):
        lower, _, upper = system.step()
        assert abs(((upper - lower) % 12.0) - 2.0) < 1e-9
