#!/usr/bin/env python3
"""Bounded native archive queries. Saved ECSV is client output, not raw HTTP."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source", choices=("mast", "heasarc", "gaia-archive"))
    p.add_argument("--coordinates", default="83.6331 22.0145", help="ICRS RA Dec in degrees")
    p.add_argument("--radius-deg", type=float, default=0.01)
    p.add_argument("--mission", default="HST")
    p.add_argument("--inventory", action="store_true", help="MAST bounded first page without a cone filter")
    p.add_argument("--catalog", default="numaster")
    p.add_argument("--adql", default="SELECT TOP 10 source_id,ra,dec FROM gaiadr3.gaia_source")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not 0 < args.radius_deg <= 0.1:
        p.error("radius must be positive and at most 0.1 degree")
    if not args.adql.strip().upper().startswith("SELECT TOP "):
        p.error("Gaia query must use a bounded SELECT TOP statement")
    args.output.mkdir(parents=True, exist_ok=True)
    receipt = {"source_id": args.source, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
               "query": {k: v for k, v in vars(args).items() if k != "output"},
               "scope": "provider table as returned by native client; no One-Wave transform; not raw HTTP bytes"}
    try:
        from astropy.coordinates import SkyCoord
        import astropy.units as u
        ra, dec = map(float, args.coordinates.split())
        position = SkyCoord(ra, dec, unit="deg", frame="icrs")
        if args.source == "mast":
            from astroquery.mast import Observations
            Observations.TIMEOUT = 30
            if args.inventory:
                table = Observations.query_criteria(obs_collection=args.mission, pagesize=10, page=1)
                receipt["scope"] = "MAST first page, at most 10 observations; not complete mission inventory"
            else:
                table = Observations.query_criteria(coordinates=position, radius=args.radius_deg * u.deg,
                                                    obs_collection=args.mission)
            receipt["provider_url"] = "https://mast.stsci.edu/"
        elif args.source == "heasarc":
            from astroquery.heasarc import Heasarc
            Heasarc.TIMEOUT = 30
            table = Heasarc.query_region(position, catalog=args.catalog, radius=args.radius_deg * u.deg)
            receipt["provider_url"] = "https://heasarc.gsfc.nasa.gov/"
        else:
            from astroquery.gaia import Gaia
            table = Gaia.launch_job(args.adql).get_results()
            receipt["provider_url"] = "https://gea.esac.esa.int/archive/"
        path = args.output / "provider-table.ecsv"
        table.write(path, format="ascii.ecsv", overwrite=True)
        receipt.update(status="acquired", row_count=len(table), file=path.name,
                       sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                       column_units={name: str(table[name].unit) if table[name].unit else None for name in table.colnames},
                       clients={name: importlib.metadata.version(name) for name in ("astroquery", "astropy")})
    except Exception as exc:
        receipt.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    (args.output / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] == "acquired" else 1


if __name__ == "__main__": raise SystemExit(main())
