"""Executable coverage registry for chapter-driven One-Wave simulators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Coverage(Enum):
    PLANNED = "planned"
    DIAGNOSTIC = "diagnostic_only"
    ENGINE_PARTIAL = "engine_partial"
    ENGINE_VALIDATED = "engine_validated"
    VISUAL_PARTIAL = "visual_partial"
    COMPLETE = "complete"


@dataclass(frozen=True)
class ChapterSimulator:
    chapter: str
    scale: str
    motions: Tuple[str, ...]
    interactions: Tuple[str, ...]
    gray_control: str
    one_wave_extension: str
    engine: str
    coverage: Coverage
    visual_scene: str


REGISTRY = (
    ChapterSimulator("Book1_Ch01_What_Is_A_Particle", "Micro", ("localized recurrence", "Point/Path/Field rotation"), ("Field confinement",), "linear field packet", "persistent bounded excitation", "micro/vortex_diagnostics.py", Coverage.DIAGNOSTIC, "micro_particle"),
    ChapterSimulator("Book1_Ch02_The_Proton", "Micro", ("quark-vortex circulation", "proton-knot rotation"), ("gluonic/boundary tension", "vortex coupling"), "QCD reference observables", "nested vortex/knot PPF", "UNBUILT", Coverage.PLANNED, "proton_knot"),
    ChapterSimulator("Book1_Ch03_Scale_Invariance", "Micro-to-Macro", ("isotropic dilation", "cross-scale transfer"), ("gradient-curvature balance",), "dimensional analysis", "declared scale transforms", "micro/vortex_diagnostics.py", Coverage.DIAGNOSTIC, "scale_lens"),
    ChapterSimulator("Book1_Ch04_The_Electron", "Micro", ("shell circulation", "phase transport"), ("electric/magnetic shell coupling",), "Maxwell/quantum controls", "Field-shell PPF", "UNBUILT", Coverage.PLANNED, "electron_shell"),
    ChapterSimulator("Book1_Ch05_The_Neutron", "Micro", ("internal coupled circulation",), ("proton/electron-field candidate coupling",), "measured neutron properties", "neutral composite recurrence", "UNBUILT", Coverage.PLANNED, "neutron_composite"),
    ChapterSimulator("Book1_Ch06_The_Nucleus", "Micro", ("collective nuclear modes", "internal rotation"), ("binding", "shell overlap", "boundary response"), "nuclear structure controls", "multi-knot Field coupling", "UNBUILT", Coverage.PLANNED, "nucleus_modes"),
    ChapterSimulator("Book1_Ch07_The_Photon", "Micro/Small", ("propagation", "polarization rotation"), ("lattice/Field transport",), "Maxwell wave propagation", "One-Wave propagation channel", "UNBUILT", Coverage.PLANNED, "photon_transport"),
    ChapterSimulator("Book1_Ch08_The_Neutrino", "Micro/Small", ("weakly coupled propagation", "phase evolution"), ("low-overlap Field coupling",), "measured oscillation controls", "One-Wave weak-coupling candidate", "UNBUILT", Coverage.PLANNED, "neutrino_phase"),
    ChapterSimulator("Book1_Ch09_No_Observer_Effect", "Micro", ("measurement-window sampling",), ("Field-window coupling",), "measurement/operator control", "extended Field measurement", "UNBUILT", Coverage.PLANNED, "measurement_window"),
    ChapterSimulator("Book1_Ch10_Time_At_Micro_Scale", "Micro", ("phase recurrence", "clock transport"), ("damping/dispersion",), "relativistic clock and wave controls", "recurrence-time candidate", "UNBUILT", Coverage.PLANNED, "micro_clock"),
    ChapterSimulator("Book1_Ch11_No_Antimatter", "Micro", ("opposite phase/orientation",), ("Field excitation interaction",), "particle/antiparticle observations", "orientation-not-separate-substance hypothesis", "UNBUILT", Coverage.PLANNED, "phase_orientation"),
    ChapterSimulator("Book1_Ch12_Gravity_At_Micro_Scale", "Micro-to-Large", ("restoring displacement", "orbital Path"), ("gradient response", "tidal response"), "Newtonian plus relativistic baseline", "derived mechanism correction", "UNBUILT", Coverage.PLANNED, "gravity_bridge"),
    ChapterSimulator("Book1_Ch13_Electricity_And_Magnetism", "Micro-to-Large", ("current", "Field rotation", "precession"), ("electric/magnetic coupling",), "Maxwell plus LLG controls", "nested EM-PPF", "UNBUILT", Coverage.PLANNED, "em_rotation"),
    ChapterSimulator("Book1_Ch14_Mass_Effect", "Micro", ("carried-pattern displacement",), ("four interactions and cross-couplings",), "inertial-response controls", "C-318 work metric", "four_interaction_sim.html", Coverage.VISUAL_PARTIAL, "mass_effect"),
    ChapterSimulator("Book1_Ch15_The_Higgs_Field_Is_The_Lattice", "Micro", ("boundary crossing", "mode response"), ("lattice/excitation coupling",), "Standard Model Higgs control", "Mirror-boundary work candidate", "UNBUILT", Coverage.PLANNED, "higgs_lattice"),
    ChapterSimulator("Book1_Ch16_Memory_As_Compressed_State", "Micro/Neural", ("compression", "retention", "release"), ("hysteresis", "phase lock"), "finite-state and control baselines", "five-state commitment memory", "logic_core/commitment_map.py", Coverage.ENGINE_PARTIAL, "memory_state"),
    ChapterSimulator("Book1_Ch17_AI_And_Human_Same_Architecture", "Neural", ("six-route recurrence", "two-system coupling"), ("choice/movement", "Gate-7 candidate"), "network-controller controls", "M4 heterogeneous architecture", "logic_core", Coverage.ENGINE_PARTIAL, "mind_coupling"),
    ChapterSimulator("Book2_Ch01_The_Cell", "Small", ("membrane flow", "internal transport", "division"), ("boundary exchange", "chemical/electrical signaling"), "cell-biophysics controls", "cellular PPF recurrence", "UNBUILT", Coverage.PLANNED, "cell_field"),
    ChapterSimulator("Book5_Ch1_Galaxies_and_Dark_Matter", "Macro", ("galactic rotation", "spiral-arm transport", "cluster flow"), ("baryonic gravity", "tidal field", "wake candidate"), "observed rotation/lensing controls", "nested trail/wake correction", "UNBUILT", Coverage.PLANNED, "galaxy_arms"),
    ChapterSimulator("Book5_Ch2_Stars", "Large/Macro", ("stellar rotation", "convection", "orbit"), ("gravity", "pressure", "EM transport"), "stellar-structure controls", "stellar PPF", "UNBUILT", Coverage.PLANNED, "star_system"),
    ChapterSimulator("Book5_Ch3_Supernovae", "Macro", ("collapse", "bounce", "ejection"), ("gravity", "pressure", "nuclear/transport response"), "supernova controls", "Build-Break-Loop classification", "UNBUILT", Coverage.PLANNED, "supernova_break"),
    ChapterSimulator("Book5_Ch4_Black_Holes_and_Quasars", "Macro", ("accretion", "rotation", "jet ejection"), ("relativistic gravity", "plasma/EM", "pressure release"), "GRMHD reference", "One-Wave mechanism overlay", "UNBUILT", Coverage.PLANNED, "quasar_release"),
    ChapterSimulator("Book5_Ch5_Stellar_Nucleosynthesis", "Macro/Micro", ("compression", "reaction flow", "ejection"), ("nuclear reaction network", "thermal/pressure transport"), "validated reaction networks", "cross-scale recurrence receipts", "UNBUILT", Coverage.PLANNED, "nucleosynthesis"),
)


def validate_registry() -> None:
    chapters = [item.chapter for item in REGISTRY]
    if len(chapters) != len(set(chapters)):
        raise AssertionError("duplicate chapter simulator entry")
    for item in REGISTRY:
        if not item.motions or not item.interactions or not item.gray_control:
            raise AssertionError(f"incomplete simulator declaration: {item.chapter}")
        if item.coverage is not Coverage.PLANNED and item.engine == "UNBUILT":
            raise AssertionError(f"implemented status without engine: {item.chapter}")


def coverage_counts() -> dict[str, int]:
    counts = {status.value: 0 for status in Coverage}
    for item in REGISTRY:
        counts[item.coverage.value] += 1
    return counts


if __name__ == "__main__":
    validate_registry()
    print(f"chapter_count={len(REGISTRY)}")
    print(coverage_counts())

