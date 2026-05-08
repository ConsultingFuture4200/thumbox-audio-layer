"""Unit tests for spike.derate."""

from __future__ import annotations

import pytest

from spike.derate import (
    BANDWIDTH_CI_FRAC,
    BANDWIDTH_GB_S,
    derate_compute_to_strix,
    derate_decode_latency_to_strix,
    derate_vram_to_strix,
)


def test_decode_derate_a100_to_strix_uses_bandwidth_ratio():
    a100 = BANDWIDTH_GB_S["a100_80gb_pcie"]
    strix = BANDWIDTH_GB_S["strix_halo"]
    expected_ratio = a100 / strix

    result = derate_decode_latency_to_strix(50.0, source_gpu="a100_80gb_pcie")

    assert result["method"] == "bandwidth"
    assert pytest.approx(result["ratio"], rel=0.01) == round(expected_ratio, 2)
    assert pytest.approx(result["predicted_strix_ms"], rel=0.05) == 50.0 * expected_ratio
    assert result["ci_low_ms"] < result["predicted_strix_ms"] < result["ci_high_ms"]
    assert result["ci_pct"] == BANDWIDTH_CI_FRAC * 100.0


def test_decode_derate_mi300x_to_strix_matches_rbox_methodology():
    # RBOX §7.1: MI300X 5.3 TB/s spec, 80% realized = 4240 GB/s.
    # Strix Halo 212 GB/s realized. Ratio ~20×.
    result = derate_decode_latency_to_strix(50.0, source_gpu="mi300x")
    assert pytest.approx(result["ratio"], rel=0.01) == round(4240.0 / 212.0, 2)
    assert result["predicted_strix_ms"] >= 50.0 * 19  # at least 19× slower


def test_decode_derate_unsupported_method_raises():
    with pytest.raises(ValueError, match="unsupported method"):
        derate_decode_latency_to_strix(50.0, method="latency-ratio")


def test_compute_derate_a100_to_strix_15x_factor():
    # Strix Halo prompt processing ~15× slower than A100 (Phoronix Nov 2025).
    result = derate_compute_to_strix(100.0, source_gpu="a100_80gb_pcie")
    assert result["method"] == "compute"
    assert result["ratio"] >= 15.0  # at least 15×
    assert result["ci_pct"] == 30.0  # wider CI than bandwidth


def test_vram_derate_capacity_fit_pass():
    result = derate_vram_to_strix(48.0, strix_halo_allocatable_gb=96.0)
    assert result["method"] == "capacity-fit"
    assert result["fits"] is True
    assert result["headroom_gb"] == 48.0


def test_vram_derate_capacity_fit_fail():
    result = derate_vram_to_strix(120.0, strix_halo_allocatable_gb=96.0)
    assert result["fits"] is False
    assert result["headroom_gb"] < 0


def test_vram_derate_sensitivity_grid():
    # Plan 02-05 should publish across {64, 96, 120} GB allocations.
    measured = 48.0
    for budget in (64.0, 96.0, 120.0):
        result = derate_vram_to_strix(measured, strix_halo_allocatable_gb=budget)
        assert result["fits"] is True
        assert result["headroom_gb"] == budget - measured
