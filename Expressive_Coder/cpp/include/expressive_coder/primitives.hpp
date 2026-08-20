#pragma once

#include <cstdint>
#include <optional>
#include <string_view>

namespace expressive_coder {

enum class Side : std::uint8_t {
    Field = 0,
    Void = 1,
};

enum class Gate : std::uint8_t {
    G1 = 1,
    G2 = 2,
    G3 = 3,
    G4 = 4,
    G5 = 5,
    G6 = 6,
};

enum class CycleStep : std::uint8_t {
    Begin = 1,
    BuildA = 2,
    Hold = 3,
    BuildB = 4,
    Break = 5,
    Loop = 6,
};

enum class ScaleBand : std::uint8_t {
    Micro = 0,
    Small = 1,
    Medium = 2,
    Large = 3,
    Macro = 4,
};

enum class View : std::uint8_t {
    Inward = 0,
    Outward = 1,
    Across = 2,
    Over = 3,
};

enum class Move : std::int8_t {
    Compress = -1,
    Hold = 0,
    Expand = 1,
};

enum class Choice : std::uint8_t {
    Nothing = 0,
    Everything = 1,
};

enum class VoidDecision : std::uint8_t {
    Allow = 0,
    Correct = 1,
    Override = 2,
    Hold = 3,
    Escalate = 4,
};

constexpr std::optional<Gate> gate_from_int(int raw) noexcept {
    switch (raw) {
        case 1: return Gate::G1;
        case 2: return Gate::G2;
        case 3: return Gate::G3;
        case 4: return Gate::G4;
        case 5: return Gate::G5;
        case 6: return Gate::G6;
        default: return std::nullopt;
    }
}

constexpr std::optional<Move> move_from_int(int raw) noexcept {
    switch (raw) {
        case -1: return Move::Compress;
        case 0: return Move::Hold;
        case 1: return Move::Expand;
        default: return std::nullopt;
    }
}

constexpr int to_int(Gate gate) noexcept {
    return static_cast<int>(gate);
}

constexpr int to_int(Move move) noexcept {
    return static_cast<int>(move);
}

constexpr int scale_percent(ScaleBand scale) noexcept {
    switch (scale) {
        case ScaleBand::Micro: return 0;
        case ScaleBand::Small: return 25;
        case ScaleBand::Medium: return 50;
        case ScaleBand::Large: return 75;
        case ScaleBand::Macro: return 100;
    }
    return -1;
}

constexpr std::string_view name(Side side) noexcept {
    switch (side) {
        case Side::Field: return "Field";
        case Side::Void: return "Void";
    }
    return "InvalidSide";
}

constexpr std::string_view name(Gate gate) noexcept {
    switch (gate) {
        case Gate::G1: return "Gate1";
        case Gate::G2: return "Gate2";
        case Gate::G3: return "Gate3";
        case Gate::G4: return "Gate4";
        case Gate::G5: return "Gate5";
        case Gate::G6: return "Gate6";
    }
    return "InvalidGate";
}

constexpr std::string_view name(CycleStep step) noexcept {
    switch (step) {
        case CycleStep::Begin: return "Begin";
        case CycleStep::BuildA: return "Build";
        case CycleStep::Hold: return "Hold";
        case CycleStep::BuildB: return "Build";
        case CycleStep::Break: return "Break";
        case CycleStep::Loop: return "Loop";
    }
    return "InvalidCycleStep";
}

constexpr std::string_view name(ScaleBand scale) noexcept {
    switch (scale) {
        case ScaleBand::Micro: return "Micro/Floor";
        case ScaleBand::Small: return "Small/Low";
        case ScaleBand::Medium: return "Medium/Mid";
        case ScaleBand::Large: return "Large/High";
        case ScaleBand::Macro: return "Macro/Ceiling";
    }
    return "InvalidScaleBand";
}

constexpr std::string_view name(View view) noexcept {
    switch (view) {
        case View::Inward: return "Inward";
        case View::Outward: return "Outward";
        case View::Across: return "Across";
        case View::Over: return "Over";
    }
    return "InvalidView";
}

constexpr std::string_view name(Move move) noexcept {
    switch (move) {
        case Move::Compress: return "Compress";
        case Move::Hold: return "Hold";
        case Move::Expand: return "Expand";
    }
    return "InvalidMove";
}

constexpr std::string_view name(Choice choice) noexcept {
    switch (choice) {
        case Choice::Nothing: return "Nothing";
        case Choice::Everything: return "Everything";
    }
    return "InvalidChoice";
}

constexpr std::string_view name(VoidDecision decision) noexcept {
    switch (decision) {
        case VoidDecision::Allow: return "ALLOW";
        case VoidDecision::Correct: return "CORRECT";
        case VoidDecision::Override: return "OVERRIDE";
        case VoidDecision::Hold: return "HOLD";
        case VoidDecision::Escalate: return "ESCALATE";
    }
    return "INVALID_DECISION";
}

}  // namespace expressive_coder
