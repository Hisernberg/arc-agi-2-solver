#!/usr/bin/env python3
"""Submit v40 -> competition slot via merged token. Slot-check -> gate -> CreateCodeSubmission.
Coordinates from arc/oct26_work/v40_coords.json."""
import json, sys, time, datetime, subprocess, os
from kagglesdk.kaggle_http_client import KaggleHttpClient
from kagglesdk.competitions.types.competition_api_service import (
    ApiGetSubmissionLimitsRequest, ApiSubmissionLimits,
    ApiCreateCodeSubmissionRequest, ApiCreateCodeSubmissionResponse)

TOK_NEW = "__ROTATED_KGAT__"
COMP = "arc-prize-2026-arc-agi-2"
_c = json.load(open("/home/z/my-project/arc/oct26_work/v40_coords.json"))
OWNER, SLUG = _c["owner"], _c["slug"]
VERSION = 1

DESC = ("Oct-27 v40 (3.8 series locked per user directive): v37-exp lineage (v34b core + shape-a2) "
        "with PROVEN qwen3-8-27b-fp8-repacked-v1 leg FORCED (boot-receipted in v39 ref 57662636; "
        "ARC_V38_LEG_SWAP=0, Tufa glob inert) + ONE lever: LOW-EFFORT COUNCIL REFILL "
        "(ARC_V40_COUNCIL=1) - v34-A second-sample refill jobs run as no-think reasoning_effort=low "
        "fast-pass answers (v32d-receipted per-job override), ~10x cheaper per answer so the leftover "
        "window covers many more distinct attempt_2 candidates; kill switch =0 -> byte-identical v34 "
        "refill. Tool fill PARKED (receipts: widened dihedral/cmap/shift/tile/kron sweep, train 17 "
        "fired P~0.94, eval 0/120 -> closed). Build gates: byte-identity cells 1-29/31/33-35 vs v39 "
        "+ AST clean; commit gates G1/G2/G4/G5 incl. proven-leg boot receipt.")

def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] {m}", flush=True)

def main():
    client = KaggleHttpClient(api_token=TOK_NEW)
    req = ApiGetSubmissionLimitsRequest(); req.competition_name = COMP
    lim = client.call("competitions.CompetitionApiService", "GetSubmissionLimits",
                      req, ApiSubmissionLimits).to_dict()
    log(f"limits: {json.dumps(lim)}")
    if not lim.get("numAllowedNow"):
        log("ABORT: no slot now (daily reset pending) — v40 stays gated for the next slot")
        return 2
    g = subprocess.run(["/usr/bin/python3.13", "/home/z/my-project/scripts/gate_v40.py"],
                       capture_output=True, text=True)
    print(g.stdout[-2500:])
    if g.returncode != 0:
        log("ABORT: gate_v40 FAILED"); return 1
    for attempt in (1, 2, 3):
        try:
            req2 = ApiCreateCodeSubmissionRequest()
            req2.competition_name = COMP
            req2.kernel_owner = OWNER
            req2.kernel_slug = SLUG
            req2.kernel_version = VERSION
            req2.file_name = "submission.json"
            req2.submission_description = DESC
            resp = client.call("competitions.CompetitionApiService", "CreateCodeSubmission",
                               req2, ApiCreateCodeSubmissionResponse)
            d2 = resp.to_dict() if hasattr(resp, "to_dict") else {"raw": str(resp)}
            log(f"SUBMITTED: {json.dumps(d2, default=str)[:300]}")
            return 0
        except Exception as e:
            log(f"submit try{attempt} rejected: {type(e).__name__}: {str(e)[:250]}")
        time.sleep(20)
    return 1

if __name__ == "__main__":
    sys.exit(main())
