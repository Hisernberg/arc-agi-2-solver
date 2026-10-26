#!/usr/bin/env python3
"""One-shot: locate v39's actual kernel coordinates (ACL quirk: canonical owner +
title-derived slug), get status + quota delta. Usage: status_v39_once.py [expected_slug_hint]"""
import json, sys, datetime, requests
from kagglesdk.kaggle_http_client import KaggleHttpClient
from kagglesdk.kernels.types.kernels_api_service import (
    ApiGetAcceleratorQuotaStatisticsRequest, ApiGetAcceleratorQuotaStatisticsResponse,
    ApiListKernelsRequest, ApiListKernelsResponse, KernelsListSortType)

TOK_NEW = "__ROTATED_KGAT__"

def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%m-%d %H:%M:%S')}] {m}", flush=True)

# ---- locate the v39 kernel: filter by our canonical owners (ACL quirk) ----
c = KaggleHttpClient(api_token=TOK_NEW)
mine = []
for owner in ("kragglenote2forwork", "dasshovon"):
    try:
        req = ApiListKernelsRequest()
        req.sort_by = KernelsListSortType.DATE_RUN
        req.page = 1
        req.page_size = 10
        req.user = owner
        resp = c.call("kernels.KernelsApiService", "ListKernels", req, ApiListKernelsResponse)
        for k in getattr(resp, "kernels", []) or []:
            ref = getattr(k, "ref", None)
            if ref and "v39" in str(ref):
                mine.append(str(ref))
    except Exception as e:
        log(f"ListKernels {owner} failed: {type(e).__name__}: {str(e)[:120]}")
if not mine:
    log("no v39 kernel visible yet (ListKernels DATE_RUN top-10)")
    for k in getattr(resp, "kernels", []) or []:
        log(f"  recent: {getattr(k, 'ref', '?')}")
    sys.exit(2)
target = mine[0]
owner, slug = target.split("/")
log(f"LOCATED: {target}")

r = requests.get("https://www.kaggle.com/api/v1/kernels/pull",
                 headers={"Authorization": f"Bearer {TOK_NEW}"},
                 params={"user_name": owner, "kernel_slug": slug}, timeout=60)
if r.status_code == 200:
    d = r.json()
    md = d.get("metadata", {})
    log(f"version={md.get('currentVersionNumber')} title={md.get('title')!r}")
    st = d.get("latestRun", {}) or {}
    log(f"run status={st.get('status')} errorMessage={st.get('errorMessage')!r}")
else:
    log(f"pull HTTP {r.status_code}: {r.text[:200]}")

qreq = ApiGetAcceleratorQuotaStatisticsRequest()
qd = c.call("kernels.KernelsApiService", "GetAcceleratorQuotaStatistics", qreq,
            ApiGetAcceleratorQuotaStatisticsResponse).to_dict()
g = qd.get("gpuQuota", {})
log(f"quota now: used={g.get('timeUsed')} allowed={g.get('totalTimeAllowed')} reserved={g.get('timeReserved')}")
with open("/home/z/my-project/arc/oct26_work/v39_coords.json", "w") as f:
    json.dump({"owner": owner, "slug": slug}, f)
