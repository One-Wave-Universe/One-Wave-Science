#include "expressive_coder/mirror.hpp"

#include <cassert>
#include <iostream>

using namespace expressive_coder;

int main() {
    assert(mirror_gate(Gate::G1) == Gate::G6);
    assert(mirror_gate(Gate::G2) == Gate::G5);
    assert(mirror_gate(Gate::G3) == Gate::G4);
    assert(mirror_gate(Gate::G4) == Gate::G3);
    assert(mirror_gate(Gate::G5) == Gate::G2);
    assert(mirror_gate(Gate::G6) == Gate::G1);

    for (int raw = 1; raw <= 6; ++raw) {
        const auto gate = gate_from_int(raw);
        assert(gate.has_value());
        assert(mirror_gate(mirror_gate(*gate)) == *gate);
    }

    const auto field_g4 = gate_pair(Side::Field, Gate::G4);
    assert(field_g4.has_value());
    assert(field_g4->field == Gate::G4);
    assert(field_g4->void_gate == Gate::G3);

    const auto void_g4 = gate_pair(Side::Void, Gate::G4);
    assert(void_g4.has_value());
    assert(void_g4->field == Gate::G3);
    assert(void_g4->void_gate == Gate::G4);

    assert(is_mirror_boundary(Gate::G4));
    assert(!is_mirror_boundary(Gate::G3));
    assert(!gate_pair_from_raw(Side::Field, 0).has_value());
    assert(!gate_pair_from_raw(Side::Void, 7).has_value());

    std::cout << "STEP02_MIRROR_PASS\n";
    return 0;
}
