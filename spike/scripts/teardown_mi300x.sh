#!/usr/bin/env bash
# Tear down the Phase 0 spike pod and verify billing has stopped.
#
# Cost-cap discipline: Phase 0 budget is $200 across all phases (see Phase 2
# hardware-path decision doc, "Cost Ceiling" section). Idle pods accrue charges.
# Always run this after a benchmark session if the pod won't be reused within a few hours.

set -euo pipefail

PROVIDER="${GSD_CLOUD_PROVIDER:-tensorwave}"

echo "==> Tearing down Phase 0 pod on provider=${PROVIDER}"

case "${PROVIDER}" in
  tensorwave)
    cat <<'EOF_TW'
==> TensorWave teardown (operator-driven)

1. Dashboard → Compute → select the thumbox-spike pod.
2. Stop pod (preserves persistent volume; cheaper if you'll resume within 24 hours).
   OR
   Terminate pod + delete volume (zero ongoing cost; loses HF model cache).
3. Confirm Billing → Current usage shows the pod stopped (line item ends now).
4. If volume retained, note: storage cost continues (~$0.10/GB/month for 100 GB = $10/mo).
   Acceptable for a 2-week spike. If pausing > 30 days, delete the volume and re-pull models.

EOF_TW
    ;;

  vultr)
    cat <<'EOF_VULTR'
==> Vultr teardown

1. Dashboard → Compute → select the thumbox-spike instance.
2. Destroy or Stop. Stop preserves data; Destroy zeros it.
3. Block storage: separate destroy step.
4. Confirm hourly billing stopped on the instance.

EOF_VULTR
    ;;

  runpod-amd|runpod-h100)
    cat <<'EOF_RP'
==> RunPod teardown

1. Dashboard → Pods → select the thumbox-spike pod.
2. Stop (preserves data on Network Volume; volume continues billing) or Terminate (zero cost).
3. Network Volume: separate Stop / Delete option in Storage tab.
4. Confirm Billing → Spending shows pod is stopped.

EOF_RP
    ;;

  *)
    echo "ERROR: unknown GSD_CLOUD_PROVIDER='${PROVIDER}'" >&2
    exit 1
    ;;
esac

cat <<'EOF'

==> Cost reconciliation checklist:

[ ] Pod is in Stopped or Terminated state (verify via dashboard, not from CLI alone)
[ ] Hourly compute billing line item ends at expected timestamp
[ ] If volume retained, expected ongoing cost is documented in spike/bench/cost-log.md
[ ] If spend approaches $150 (soft trigger), reconfirm budget with operator before next session
EOF
