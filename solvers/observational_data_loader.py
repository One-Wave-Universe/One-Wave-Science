#!/usr/bin/env python3
"""
Observational Data Loader for One-Wave Framework Validators

Purpose:
- Replace hard-coded test data with real observational sources
- Connect validators to scientific data archives (NASA MAST, GAIA, HEASARC, etc.)
- Provide data interface that supports both real and synthetic fallback modes
- Track data provenance for publication

Architecture:
- ObservationalDataSource: Abstract base class
- RealDataSource subclasses: Connect to actual archives
- SyntheticFallback: Hard-coded test data (when real source unavailable)
- DataCache: Local caching to reduce archive queries

Status:
- PHASE 1 (Current): Data source abstraction and cache layer
- PHASE 2: Real archive connectors (MAST, GAIA, HEASARC)
- PHASE 3: Data validation and uncertainty propagation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json
import os
from datetime import datetime


@dataclass
class DataRecord:
    """A single observational data point."""
    name: str
    value: float
    uncertainty: float
    units: str
    source: str  # Archive or paper reference
    timestamp: str  # ISO 8601 date of observation or retrieval


@dataclass
class Dataset:
    """Complete dataset from observational source."""
    name: str
    source: str  # Archive name (MAST, GAIA, etc.)
    reference: str  # Paper reference (Sofue et al. 1999, etc.)
    data_type: str  # "rotation_curve", "spectrum", "image", etc.
    records: List[DataRecord]
    metadata: Dict


class ObservationalDataSource(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    def fetch(self, query: Dict) -> Dataset:
        """Fetch dataset matching query."""
        pass

    @abstractmethod
    def available_queries(self) -> List[str]:
        """List available queries for this source."""
        pass


class SyntheticFallback(ObservationalDataSource):
    """
    Hard-coded test data fallback.

    This is what current solvers use. It's included here to:
    1. Make the dependency explicit
    2. Allow transition to real data
    3. Support offline testing

    WARNING: Solvers should not rely on this for "validation" claims.
    Only use for development and methodology testing.
    """

    def __init__(self):
        self.data = {
            "milky_way_rotation": {
                "name": "Milky Way Rotation Curve",
                "source": "SYNTHETIC",
                "reference": "Sofue et al. (1999), Battaglia et al. (2005) — SYNTHETIC FALLBACK",
                "data_type": "rotation_curve",
                "units": "km/s",
                "description": "Hard-coded synthetic data. NOT actual observational data.",
                "records": [
                    (0.5, 0, 20),      # (radius_kpc, velocity_kms, error_kms)
                    (1, 100, 20),
                    (2, 150, 25),
                    (3, 180, 30),
                    (4, 200, 30),
                    (5, 210, 20),
                    (6, 215, 20),
                    (8, 220, 15),
                    (10, 220, 15),
                    (12, 215, 20),
                    (15, 210, 25),
                    (20, 200, 30),
                    (25, 190, 35),
                    (30, 180, 40),
                ]
            },
            "andromeda_rotation": {
                "name": "Andromeda (M31) Rotation Curve",
                "source": "SYNTHETIC",
                "reference": "Chemin et al. (2009), Corbelli & Salucci (2000) — SYNTHETIC FALLBACK",
                "data_type": "rotation_curve",
                "units": "km/s",
                "description": "Hard-coded synthetic data. NOT actual observational data.",
                "records": [
                    (2, 80, 15),
                    (4, 160, 20),
                    (6, 210, 25),
                    (8, 240, 20),
                    (10, 250, 15),
                    (15, 240, 20),
                    (20, 220, 25),
                    (25, 200, 30),
                    (30, 185, 30),
                    (35, 170, 35),
                    (40, 155, 40),
                    (50, 140, 45),
                ]
            }
        }

    def fetch(self, query: Dict) -> Dataset:
        """Fetch synthetic data by name."""
        query_name = query.get("name", "").lower()

        if "milky_way" in query_name or "mw" in query_name:
            return self._build_dataset("milky_way_rotation")
        elif "andromeda" in query_name or "m31" in query_name:
            return self._build_dataset("andromeda_rotation")
        else:
            raise ValueError(f"Unknown query: {query}")

    def _build_dataset(self, key: str) -> Dataset:
        """Convert internal format to Dataset."""
        info = self.data[key]
        records = [
            DataRecord(
                name=f"{info['name']} point {i}",
                value=vel,
                uncertainty=err,
                units=info["units"],
                source=info["source"],
                timestamp=datetime.now().isoformat()
            )
            for i, (radius, vel, err) in enumerate(info["records"])
        ]

        return Dataset(
            name=info["name"],
            source=info["source"],
            reference=info["reference"],
            data_type=info["data_type"],
            records=records,
            metadata={"radius_kpc": [r for r, v, e in info["records"]]}
        )

    def available_queries(self) -> List[str]:
        return list(self.data.keys())


class DataCache:
    """
    Local cache for fetched data.

    Reduces repeated archive queries and enables offline work.
    Cache is stored as JSON in project directory.
    """

    def __init__(self, cache_dir: str = "/tmp/claude_data_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, source: str, query: Dict) -> str:
        """Generate cache key from source and query."""
        query_str = json.dumps(query, sort_keys=True)
        return f"{source}_{hash(query_str)}"

    def fetch(self, source: str, query: Dict) -> Optional[Dataset]:
        """Try to fetch from cache. Return None if not cached."""
        cache_file = os.path.join(self.cache_dir, self.get_cache_key(source, query) + ".json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    print(f"[CACHE HIT] {source}: {query}")
                    return self._deserialize(data)
            except Exception as e:
                print(f"[CACHE ERROR] Failed to load {cache_file}: {e}")
        return None

    def store(self, source: str, query: Dict, dataset: Dataset) -> None:
        """Store dataset in cache."""
        cache_file = os.path.join(self.cache_dir, self.get_cache_key(source, query) + ".json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(self._serialize(dataset), f, indent=2)
                print(f"[CACHED] {source}: {query}")
        except Exception as e:
            print(f"[CACHE WRITE ERROR] {cache_file}: {e}")

    def _serialize(self, dataset: Dataset) -> Dict:
        """Convert Dataset to JSON-serializable dict."""
        return {
            "name": dataset.name,
            "source": dataset.source,
            "reference": dataset.reference,
            "data_type": dataset.data_type,
            "records": [
                {
                    "name": r.name,
                    "value": r.value,
                    "uncertainty": r.uncertainty,
                    "units": r.units,
                    "source": r.source,
                    "timestamp": r.timestamp
                }
                for r in dataset.records
            ],
            "metadata": dataset.metadata
        }

    def _deserialize(self, data: Dict) -> Dataset:
        """Reconstruct Dataset from dict."""
        records = [
            DataRecord(**r) for r in data["records"]
        ]
        return Dataset(
            name=data["name"],
            source=data["source"],
            reference=data["reference"],
            data_type=data["data_type"],
            records=records,
            metadata=data["metadata"]
        )


class ValidatorDataInterface:
    """
    Unified interface for validators to access data.

    Handles:
    - Fallback to synthetic when real source unavailable
    - Caching for performance
    - Data validation and tracking
    """

    def __init__(self, use_real_data: bool = False):
        self.use_real_data = use_real_data
        self.synthetic = SyntheticFallback()
        self.cache = DataCache()
        self.sources: Dict[str, ObservationalDataSource] = {
            "synthetic": self.synthetic,
        }

    def fetch_observational_data(self, source: str, query: Dict) -> Tuple[Dataset, bool]:
        """
        Fetch data, returning (dataset, is_real).

        is_real = True if data came from real archive
        is_real = False if data came from synthetic fallback
        """
        # Try cache first
        cached = self.cache.fetch(source, query)
        if cached:
            is_real = (cached.source != "SYNTHETIC")
            return cached, is_real

        # Try to fetch from requested source
        if source in self.sources:
            dataset = self.sources[source].fetch(query)
            self.cache.store(source, query, dataset)
            is_real = (dataset.source != "SYNTHETIC")
            return dataset, is_real

        # Fallback to synthetic
        if self.use_real_data:
            print(f"WARNING: Real data requested but source '{source}' unavailable. Using synthetic fallback.")
        dataset = self.synthetic.fetch(query)
        self.cache.store(source, query, dataset)
        return dataset, False

    def register_source(self, name: str, source: ObservationalDataSource) -> None:
        """Register a new data source."""
        self.sources[name] = source

    def list_sources(self) -> List[str]:
        """List available sources."""
        return list(self.sources.keys())


def main():
    """Demonstrate data interface."""
    print("=" * 70)
    print("OBSERVATIONAL DATA LOADER — Interface Demo")
    print("=" * 70)
    print()

    interface = ValidatorDataInterface(use_real_data=False)

    print("Available sources:", interface.list_sources())
    print()

    print("Fetching Milky Way rotation curve...")
    dataset, is_real = interface.fetch_observational_data(
        "synthetic",
        {"name": "milky_way_rotation"}
    )

    print(f"Source: {dataset.source}")
    print(f"Real data: {is_real}")
    print(f"Reference: {dataset.reference}")
    print(f"Points: {len(dataset.records)}")
    print()

    print("First 5 data points:")
    for record in dataset.records[:5]:
        print(f"  {record.name}: {record.value} ± {record.uncertainty} {record.units}")
    print()

    print("=" * 70)
    print("NOTE: Currently using SYNTHETIC data for testing")
    print("TODO: Implement real data sources (MAST, GAIA, HEASARC)")
    print("=" * 70)


if __name__ == "__main__":
    main()
