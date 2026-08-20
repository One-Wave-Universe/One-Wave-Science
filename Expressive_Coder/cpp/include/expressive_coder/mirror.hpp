#pragma once

#include "expressive_coder/primitives.hpp"

#include <optional>

namespace expressive_coder {

struct GatePair {
    Gate field;
    Gate void_gate;
};

constexpr Gate mirror_gate(Gate gate) noexcept {
    switch (gate) {
        case Gate::G1: return Gate::G6;
        case Gate::G2: return Gate::G5;
        case Gate::G3: return Gate::G4;
        case Gate::G4: return Gate::G3;
        case Gate::G5: return Gate::G2;
        case Gate::G6: return Gate::G1;
    }
    return Gate::G1;
}

constexpr bool is_mirror_boundary(Gate gate) noexcept {
    return gate == Gate::G4;
}

constexpr std::optional<GatePair> gate_pair(Side side, Gate gate) noexcept {
    if (side == Side::Field) {
        return GatePair{gate, mirror_gate(gate)};
    }
    return GatePair{mirror_gate(gate), gate};
}

constexpr std::optional<GatePair> gate_pair_from_raw(Side side, int raw_gate) noexcept {
    const auto gate = gate_from_int(raw_gate);
    if (!gate) {
        return std::nullopt;
    }
    return gate_pair(side, *gate);
}

}  // namespace expressive_coder
