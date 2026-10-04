#!/usr/bin/env python3
"""Snapshot provider-native metadata. No measurements or model parameters fabricated."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError

from open_data_fetch import allowed_hosts, fetch_json, load_registry, source_by_id, utc_now


def endpoints(record, event):
    if not str(record).isdigit() or not event.replace('_', '').isalnum():
        raise ValueError("Use a numeric CERN record and an alphanumeric GWOSC event ID")
    return [("cern-open-data", f"https://opendata.cern.ch/api/records/{record}"),
            ("gwosc", f"https://gwosc.org/api/v2/events/{event}"),
            ("gwosc", f"https://gwosc.org/api/v2/events/{event}/strain-files")]


def retry_fetch(url, hosts, timeout):
    for attempt in range(3):
        try:
            return fetch_json(url, hosts, timeout)
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(0.5 * 2**attempt)


def summary(source, record):
    if not isinstance(record, dict):
        raise ValueError("Expected provider JSON object; preserve raw response and inspect schema")
    if source == "cern-open-data":
        m = record.get("metadata", {})
        if not m or not record.get("id"):
            raise ValueError("CERN response lacks record ID/metadata")
        return {"record_id": record["id"], "doi": m.get("doi"),
                "title": m.get("title"), "experiment": m.get("experiment"),
                "license": m.get("license"), "release": record.get("updated"),
                "files": m.get("files", []), "units": None,
                "classification": "provider_metadata_not_event_measurements"}
    # Strain-file metadata contains detector/GPS/sample rate and provider links.
    if "results" in record:
        if not isinstance(record["results"], list):
            raise ValueError("GWOSC results must be an array")
        return {"record_id": None, "files": record["results"],
                "results_count": record.get("results_count"),
                "strain_units": "dimensionless strain (not downloaded)",
                "classification": "provider_metadata_not_strain_samples"}
    if not record.get("name") or not isinstance(record.get("versions"), list):
        raise ValueError("GWOSC event response lacks name/versions")
    return {"record_id": record["name"], "run": record.get("run"),
            "versions": record.get("versions"), "units": None,
            "classification": "provider_event_metadata_not_measurements"}


def snapshot(source, url, output, hosts, max_pages=10, timeout=30, fetcher=retry_fetch):
    pages, seen = [], set()
    for index in range(max_pages):
        if not url or url in seen:
            break
        seen.add(url)
        raw, record, transport = fetcher(url, hosts, timeout)
        digest = hashlib.sha256(raw).hexdigest()
        raw_path = output / f"{source}-{digest}.raw"
        raw_path.write_bytes(raw)
        # Preserve exact bytes even if the provider schema has changed.
        page = {"source_id": source, "requested_url": url, "transport": transport,
                "retrieved_at_utc": utc_now(), "raw_body_file": raw_path.name,
                "sha256": digest, "bytes": len(raw), "source_record": record,
                "summary": summary(source, record)}
        page_path = output / f"{source}-{digest}.json"
        page_path.write_text(json.dumps(page, indent=2, sort_keys=True) + "\n")
        pages.append({key: page[key] for key in
                      ("source_id", "requested_url", "retrieved_at_utc", "raw_body_file", "sha256", "bytes", "summary")})
        pages[-1]["envelope_file"] = page_path.name
        url = record.get("next")
        if url: time.sleep(0.5)
    count = sum(len(p["summary"].get("files", [])) for p in pages)
    totals = [p["summary"]["results_count"] for p in pages
              if p["summary"].get("results_count") is not None]
    count_mismatch = bool(totals) and (len(set(totals)) != 1 or count != totals[0])
    complete = not url and not count_mismatch
    return {"status": "complete" if complete else "incomplete",
            "reason": ("provider count mismatch" if count_mismatch else
                       "page cap or repeated next link" if url else None),
            "next_url": url, "pages": pages}


def verify_bundle(output):
    receipt = json.loads((output / "receipt.json").read_text())
    for request in receipt["requests"]:
        for page in request["pages"]:
            raw = (output / page["raw_body_file"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != page["sha256"]:
                raise ValueError("Raw source hash mismatch: " + page["raw_body_file"])
            envelope = json.loads((output / page["envelope_file"]).read_text())
            if envelope["source_record"] != json.loads(raw) or envelope["sha256"] != page["sha256"]:
                raise ValueError("Envelope differs from provider response")
    observed_complete = all(r["status"] == "complete" for r in receipt["requests"])
    if receipt["all_complete"] != observed_complete:
        raise ValueError("Receipt status does not match request statuses")
    return observed_complete


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cern-record", default="5501")
    parser.add_argument("--gwosc-event", default="GW150914")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--verify", action="store_true", help="Verify saved bodies/envelopes without network")
    args = parser.parse_args()
    if not 1 <= args.max_pages <= 100 or not 1 <= args.timeout <= 120:
        parser.error("max-pages 1..100 and timeout 1..120 required")
    if args.verify:
        complete = verify_bundle(args.output)
        print(json.dumps({"hashes_verified": True, "all_complete": complete}))
        return 0 if complete else 1
    args.output.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    tasks = endpoints(args.cern_record, args.gwosc_event)
    receipt = {"schema": "one-wave-science-metadata-receipt-v1",
               "started_at_utc": utc_now(), "scope": "metadata acquisition only; no physical validation",
               "registry_sha256": hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest(),
               "requests": []}
    for source, url in tasks:
        try:
            result = snapshot(source, url, args.output,
                              allowed_hosts(source_by_id(registry, source)),
                              args.max_pages, args.timeout)
        except (Exception, SystemExit) as exc:
            result = {"status": "failed", "error": str(exc), "pages": []}
        receipt["requests"].append({"source_id": source, "url": url, **result})
    receipt["finished_at_utc"] = utc_now()
    receipt["all_complete"] = all(r["status"] == "complete" for r in receipt["requests"])
    (args.output / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"receipt": str(args.output / "receipt.json"),
                      "all_complete": receipt["all_complete"],
                      "statuses": [r["status"] for r in receipt["requests"]]}))
    return 0 if receipt["all_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
