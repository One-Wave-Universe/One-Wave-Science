#include "expressive_coder/primitives.hpp"

#include <cassert>
#include <iostream>
#include <string_view>

using namespace expressive_coder;

static_assert(static_cast<int>(Move::Compress) == -1);
static_assert(static_cast<int>(Move::Hold) == 0);
static_assert(static_cast<int>(Move::Expand) == 1);
static_assert(static_cast<int>(Gate::G1) == 1);
static_assert(static_cast<int>(Gate::G6) == 6);

int main() {
    for (int raw = 1; raw <= 6; ++raw) {
        const auto gate = gate_from_int(raw);
        assert(gate.has_value());
        assert(to_int(*gate) == raw);
    }

    assert(!gate_from_int(0).has_value());
    assert(!gate_from_int(7).has_value());
    assert(!gate_from_int(-1).has_value());

    assert(move_from_int(-1) == Move::Compress);
    assert(move_from_int(0) == Move::Hold);
    assert(move_from_int(1) == Move::Expand);
    assert(!move_from_int(-2).has_value());
    assert(!move_from_int(2).has_value());

    assert(scale_percent(ScaleBand::Micro) == 0);
    assert(scale_percent(ScaleBand::Small) == 25);
    assert(scale_percent(ScaleBand::Medium) == 50);
    assert(scale_percent(ScaleBand::Large) == 75);
    assert(scale_percent(ScaleBand::Macro) == 100);

    assert(name(CycleStep::Begin) == std::string_view{"Begin"});
    assert(name(CycleStep::BuildA) == std::string_view{"Build"});
    assert(name(CycleStep::Hold) == std::string_view{"Hold"});
    assert(name(CycleStep::BuildB) == std::string_view{"Build"});
    assert(name(CycleStep::Break) == std::string_view{"Break"});
    assert(name(CycleStep::Loop) == std::string_view{"Loop"});

    assert(name(Choice::Nothing) == std::string_view{"Nothing"});
    assert(name(Choice::Everything) == std::string_view{"Everything"});
    assert(name(VoidDecision::Allow) == std::string_view{"ALLOW"});
    assert(name(VoidDecision::Override) == std::string_view{"OVERRIDE"});

    std::cout << "STEP01_PRIMITIVES_PASS\n";
    return 0;
}
