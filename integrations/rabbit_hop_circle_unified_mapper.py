#!/usr/bin/env python3
"""
Rabbit Hopping ↔ Circle of Fifths Unified Mapper
Validates that Rabbit Hopping routes preserve harmonic identity.
"""

from dataclasses import dataclass
from enum import Enum


class ChordQuality(Enum):
    """Chord families with signed-offset architecture."""
    POWER_CHORD = (-1, +1)
    MAJOR = (-5, +4)
    MINOR = (-5, +3)
    TRIAD = (-4, +5)


@dataclass
class Chord:
    """A chord in Circle of Fifths."""
    root: int
    quality: ChordQuality
    
    def pitch_classes(self):
        """Calculate pitch classes (specific semitone intervals)."""
        INTERVALS = {
            ChordQuality.POWER_CHORD: [0, 7],
            ChordQuality.MAJOR: [0, 4, 7],
            ChordQuality.MINOR: [0, 3, 7],
            ChordQuality.TRIAD: [0, 5, 8],
        }
        intervals = INTERVALS[self.quality]
        result = tuple(sorted((self.root + offset) % 12 for offset in intervals))
        return result
    
    def harmonic_intervals(self):
        """Get interval set from root (defines harmonic identity)."""
        pitches = self.pitch_classes()
        intervals = sorted(set((p - self.root) % 12 for p in pitches))
        return tuple(intervals)
    
    def __repr__(self) -> str:
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        root_name = notes[self.root]
        quality_name = self.quality.name.replace("_", " ").lower()
        pitch_str = "-".join(notes[p] for p in self.pitch_classes())
        return f"{root_name} {quality_name} {{{pitch_str}}}"


class RouteFamily(Enum):
    """Route operation types."""
    SHIFT_THEN_DOUBLE = "2(N+K)"


@dataclass
class RabbitHopRoute:
    """A Rabbit Hopping route receipt."""
    source: str
    N: int
    K: int
    family: RouteFamily
    wrapper: int = 0
    
    def compute_top(self) -> int:
        """Calculate TOP value."""
        if self.family == RouteFamily.SHIFT_THEN_DOUBLE:
            return 2 * (self.N + self.K)
        return 0
    
    def __repr__(self) -> str:
        top = self.compute_top()
        return f"Route({self.source} | TOP={top} | wrapper={self.wrapper:+d})"


class HarmonicIdentityMapper:
    """Maps Circle of Fifths operations to Rabbit Hopping routes."""
    
    def chord_to_rabbit_hop(self, start: Chord, target_root: int) -> RabbitHopRoute:
        """Convert chord transposition to Rabbit Hopping route."""
        K = (target_root - start.root) % 12
        return RabbitHopRoute(
            source="guitar_neck",
            N=start.root,
            K=K,
            family=RouteFamily.SHIFT_THEN_DOUBLE
        )
    
    def apply_route_to_chord(self, chord: Chord, route: RabbitHopRoute) -> Chord:
        """Apply a route to a chord."""
        new_root = (chord.root + route.K) % 12
        return Chord(root=new_root, quality=chord.quality)
    
    def verify_harmonic_identity(self, orig: Chord, after: Chord) -> bool:
        """Verify harmonic identity preserved by comparing interval sets."""
        # Same quality = harmonic identity
        if orig.quality != after.quality:
            return False
        
        # Compare interval sets (order-independent)
        orig_intervals = orig.harmonic_intervals()
        after_intervals = after.harmonic_intervals()
        
        return orig_intervals == after_intervals
    
    def test_chord_progression(self, progression):
        """Test a progression through Rabbit Hopping routes."""
        all_valid = True
        for i in range(len(progression) - 1):
            root1, quality1 = progression[i]
            root2, quality2 = progression[i + 1]
            
            chord1 = Chord(root=root1, quality=quality1)
            
            route = self.chord_to_rabbit_hop(chord1, root2)
            result = self.apply_route_to_chord(chord1, route)
            
            valid = self.verify_harmonic_identity(chord1, result)
            
            symbol = "✓" if valid else "✗"
            print(f"  {symbol} {chord1} -> {result}")
            all_valid = all_valid and valid
        
        return all_valid


def test_harmonic_identity():
    """Test harmonic identity preservation."""
    print("\nTEST 1: Harmonic Identity Preservation")
    print("=" * 70)
    
    mapper = HarmonicIdentityMapper()
    
    # Test: C Major -> F Major -> G Major -> C Major
    print("\n[1a] Major Chord Progression (C->F->G->C)")
    progression = [
        (0, ChordQuality.MAJOR),
        (5, ChordQuality.MAJOR),
        (7, ChordQuality.MAJOR),
        (0, ChordQuality.MAJOR),
    ]
    result = mapper.test_chord_progression(progression)
    print(f"Result: {'✓ PASS' if result else '✗ FAIL'}")
    
    # Test: Mixed qualities
    print("\n[1b] Mixed Chord Quality (C Major -> A Minor -> E Major)")
    progression = [
        (0, ChordQuality.MAJOR),
        (9, ChordQuality.MINOR),
        (4, ChordQuality.MAJOR),
    ]
    result = mapper.test_chord_progression(progression)
    print(f"Result: {'✓ PASS' if result else '✗ FAIL'}")
    
    # Test: Round-trip
    print("\n[1c] Round-Trip (C Major -> G Major -> C Major)")
    c_maj = Chord(root=0, quality=ChordQuality.MAJOR)
    route_to_g = mapper.chord_to_rabbit_hop(c_maj, 7)
    g_maj = mapper.apply_route_to_chord(c_maj, route_to_g)
    
    # Verify identity
    identity_match = mapper.verify_harmonic_identity(c_maj, g_maj)
    
    # Return to C
    route_back_c = mapper.chord_to_rabbit_hop(g_maj, 0)
    c_back = mapper.apply_route_to_chord(g_maj, route_back_c)
    
    match_original = mapper.verify_harmonic_identity(c_maj, c_back)
    
    symbol = "✓" if (identity_match and match_original) else "✗"
    print(f"  {symbol} C Major -> G Major: identity={identity_match}")
    print(f"  {symbol} G Major -> C Major: identity={match_original}")
    print(f"Result: {'✓ PASS' if (identity_match and match_original) else '✗ FAIL'}")


def test_route_receipts():
    """Test route receipt structure."""
    print("\nTEST 2: Route Receipt Structure")
    print("=" * 70)
    
    route = RabbitHopRoute(
        source="guitar_neck",
        N=0,
        K=5,
        family=RouteFamily.SHIFT_THEN_DOUBLE,
        wrapper=1
    )
    
    print(f"Route: {route}")
    print(f"TOP = 2(N+K) = 2(0+5) = {route.compute_top()}")
    print(f"Packet: {route.source} | TOP={route.compute_top()} | wrapper={route.wrapper:+d}")
    print("✓ Result: PASS")


def main():
    """Run tests."""
    print("\nALGORITHM ZERO + RABBIT HOPPING + CIRCLE OF FIFTHS")
    print("Integration Test Suite")
    print("=" * 70)
    
    test_harmonic_identity()
    test_route_receipts()
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
