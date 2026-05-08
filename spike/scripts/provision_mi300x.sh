#!/usr/bin/env bash
# Provision an MI300X (or H100 fallback) bare-metal pod for the Phase 0 spike.
#
# Phase 2 hardware-path decision: Path Cloud (see
# .planning/phases/02-phase-0-mimi-feasibility-spike/02-01-HARDWARE-PATH-DECISION.md)
#
# Provider selection via env var GSD_CLOUD_PROVIDER:
#   - tensorwave (default; primary per RBOX/CLAUDE.md §1.2 — $1.71/hr MI300X)
#   - vultr      (backup MI300X provider per RBOX §1.2 — $1.85/hr)
#   - runpod-amd (RunPod with MI300X selected; if available in your region)
#   - runpod-h100 (RunPod NVIDIA H100; fallback only — derate to Strix Halo is harder)
#
# This script DOES NOT replace the dashboard work. Cloud-account authentication and
# payment-method confirmation must be done by the operator via the provider's web
# dashboard. This script captures the steps as documentation and provides idempotent
# helpers for the bits that ARE scriptable.

set -euo pipefail

PROVIDER="${GSD_CLOUD_PROVIDER:-tensorwave}"
SPEND_CAP_MONTHLY_USD="${GSD_SPEND_CAP:-200}"
IMAGE="rocm/pytorch:rocm6.4_ubuntu22.04_py3.10_pytorch_2.5.1"
IMAGE_DIGEST_FILE="${GSD_IMAGE_DIGEST_FILE:-spike/configs/.image-digest}"
VOLUME_NAME="thumbox-spike-vol"
VOLUME_SIZE_GB=100

echo "==> Phase 0 spike provisioning: provider=${PROVIDER}, image=${IMAGE}, spend cap \$${SPEND_CAP_MONTHLY_USD}/mo"

case "${PROVIDER}" in
  tensorwave)
    cat <<'EOF_TW'
==> TensorWave provisioning steps (operator-driven; see https://tensorwave.com)

1. Sign in to TensorWave dashboard.
2. Compute → New Instance:
   - GPU: AMD MI300X (Dedicated MI300X+)
   - Image: rocm/pytorch:rocm6.4_ubuntu22.04_py3.10_pytorch_2.5.1
   - PIN BY DIGEST: after first pull, record the sha256 image digest into
     spike/configs/.image-digest (gitignored) and reference it in
     spike/configs/models.lock.yaml runtime_image.digest field.
   - Volume: create persistent 100 GB volume named "thumbox-spike-vol"
     (HF model caches; persists between pod stop/start).
   - SSH key: paste contents of ~/.ssh/id_ed25519.pub.
3. Billing → Spending limits: apply $${SPEND_CAP_MONTHLY_USD}/mo cap on this project.
4. Once pod is up, copy the SSH endpoint into a local secret file:
     echo 'ssh root@<host> -p <port>' > ~/.thumbox-spike-pod-ssh
5. Smoke test:
     ssh -F ~/.thumbox-spike-pod-ssh root@<host> "rocminfo | grep -i 'AMD Instinct'"
6. Verify NO CUDA on this pod:
     ssh -F ~/.thumbox-spike-pod-ssh root@<host> "command -v nvidia-smi || echo 'no nvidia-smi (correct for AMD pod)'"

EOF_TW
    ;;

  vultr)
    cat <<'EOF_VULTR'
==> Vultr provisioning (backup; see https://vultr.com/products/cloud-gpu/)

Same steps as TensorWave with these substitutions:
- Provider dashboard: vultr.com
- GPU: AMD MI300X via "Cloud GPU" → MI300X (24-month prepaid: $1.75/GPU-hr; on-demand: $1.85/hr)
- Region: confirm MI300X availability before instance creation; some regions require sales contact
- Storage: 100 GB block storage attached as /mnt/data

EOF_VULTR
    ;;

  runpod-amd)
    cat <<'EOF_RP_AMD'
==> RunPod AMD (MI300X) provisioning (https://runpod.io)

1. Sign in to RunPod.
2. Pods → Deploy → filter for AMD MI300X.
3. Image: rocm/pytorch:rocm6.4_ubuntu22.04_py3.10_pytorch_2.5.1 (or RunPod's pre-validated ROCm image)
4. Volume: 100 GB Network Volume, mount at /workspace/volume (RunPod convention)
5. Pin image digest after first pull (see TensorWave instructions above)
6. Apply Project-level spending limit of $${SPEND_CAP_MONTHLY_USD}/mo (Settings → Billing)

Note: RunPod's MI300X availability varies by region; if not available, fall back to runpod-h100
or switch to tensorwave/vultr.

EOF_RP_AMD
    ;;

  runpod-h100)
    cat <<'EOF_RP_H100'
==> RunPod H100 provisioning (fallback only)

WARNING: H100 is NVIDIA/CUDA, not AMD/ROCm. The Strix Halo derating math gets harder
because of cross-vendor differences (memory architecture, runtime stack). Plan 02-05
must publish raw H100 numbers and explain why CUDA→Strix Halo derate is less direct
than MI300X→Strix Halo. Use only if MI300X is unavailable everywhere.

1. Sign in to RunPod.
2. Pods → Secure Cloud → H100 PCIe ($2.39/hr) or H100 SXM ($2.69/hr).
3. Image: nvcr.io/nvidia/pytorch:25.04-py3 (CUDA 12.4, RBOX-validated)
4. Volume: 100 GB Network Volume.
5. Pin image digest after first pull.
6. Apply Project spending limit $${SPEND_CAP_MONTHLY_USD}/mo.

After provisioning, set runtime profile to `cuda` (not `rocm`) in spike/configs/runtime.yaml
profile selection at run time.

EOF_RP_H100
    ;;

  *)
    echo "ERROR: unknown GSD_CLOUD_PROVIDER='${PROVIDER}'" >&2
    echo "Valid: tensorwave | vultr | runpod-amd | runpod-h100" >&2
    exit 1
    ;;
esac

cat <<EOF

==> Operator checklist before declaring DEV-1045 / Plan 02-01 Task 2 complete:

[ ] Pod is reachable: \`ssh\` returns within 10s
[ ] \`rocminfo\` (or \`nvidia-smi\` if H100) lists the expected GPU
[ ] Image digest recorded at ${IMAGE_DIGEST_FILE} (gitignored; do NOT commit)
[ ] Volume \`${VOLUME_NAME}\` (or equivalent) attached and writable
[ ] Spending limit \$${SPEND_CAP_MONTHLY_USD}/mo applied at provider's dashboard
[ ] SSH connection notes captured outside the repo

When done: reply 'provisioned' to resume Plan 02-01 Task 4 (Mimi encode/decode loop).

==> To shut down: bash spike/scripts/teardown_mi300x.sh
EOF
