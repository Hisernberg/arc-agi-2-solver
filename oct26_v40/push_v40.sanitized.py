#!/usr/bin/env python3
"""Push v40 (3.8 leg locked + low-effort council refill) as NEW kernel:
dasshovon/arc26-nvarc-v40. Mounts = v38/v39 commit list 1:1 (unchanged)."""
import json, sys, time, datetime
from kagglesdk.kaggle_http_client import KaggleHttpClient
from kagglesdk.kernels.types.kernels_api_service import (
    ApiSaveKernelRequest, ApiSaveKernelResponse, KernelExecutionType)

TOK_NEW = "__ROTATED_KGAT__"
TEXT = open("/home/z/my-project/arc/oct26_work/arc26-nvarc-v40.ipynb").read()
SLUG = "dasshovon/arc26-nvarc-v40"

def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] {m}", flush=True)

def attempt():
    req = ApiSaveKernelRequest()
    req.slug = SLUG
    req.new_title = "ARC26 NVARC v40 (3.8 leg + council refill)"
    req.text = TEXT
    req.language = "python"
    req.kernel_type = "notebook"
    req.is_private = True
    req.enable_gpu = True
    req.enable_internet = False
    req.dataset_data_sources = [
        "mirzamilanfarabi/arc3-vllm-h100-wheelhouse-v3",
        "konstantinboyko/flash-attn-2-8-2",
        "keithtyser/taaf-duck-qwen38-serving-v1",
        "driessmit1/vrfai-qwen3-6-27b-fp8-hf-snapshot",
    ]
    req.kernel_data_sources = ["konstantinboyko/unsloth-2025-9-7-torch-2-8-0-py3-12-patched"]
    req.competition_data_sources = ["arc-prize-2026-arc-agi-2"]
    req.model_data_sources = [
        "sorokin/qwen3_4b_grids15_sft139/Transformers/bfloat16/1",
        "foysalemonshanto/qwen3-8-27b-fp8-repacked-v1/PyTorch/hf-fp8/1",
    ]
    req.machine_shape = "NvidiaL4"
    req.docker_image = ("gcr.io/kaggle-private-byod/python@"
                        "sha256:57e612b484cf3df5026ee4dcc3cb176974b22b2bc0937fb1e16132a8be4cb13c")
    req.docker_image_pinning_type = "LATEST"
    req.category_ids = ["gpu"]
    req.kernel_execution_type = KernelExecutionType.SAVE_AND_RUN_ALL
    try:
        c = KaggleHttpClient(api_token=TOK_NEW)
        resp = c.call("kernels.KernelsApiService", "SaveKernel", req, ApiSaveKernelResponse)
        err = resp.__dict__.get("_error")
        vn = resp.__dict__.get("_version_number")
        log(f"push: error={err} version={vn}")
        return err, vn
    except Exception as e:
        log(f"push EXCEPTION {type(e).__name__}: {str(e)[:300]}")
        return str(e), None

def main():
    for i in range(1, 4):
        err, vn = attempt()
        if err in (None, "", "None") and vn not in (None, "None", 0, "0"):
            log(f"SUCCESS: {SLUG} version {vn} queued (commit run requested on merged pool)")
            return 0
        log(f"attempt {i} failed -> retry in 20 s")
        time.sleep(20)
    return 1

if __name__ == "__main__":
    sys.exit(main())
