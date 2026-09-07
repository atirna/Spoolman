"""Regression tests for API response models."""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from spoolman.api.v1.models import Filament, Spool, Vendor


@pytest.fixture
def extra() -> list[SimpleNamespace]:
    return [
        SimpleNamespace(key="smooth_time", value="0.035"),
        SimpleNamespace(key="enabled", value="true"),
        SimpleNamespace(key="label", value='"PLA"'),
        SimpleNamespace(key="range", value="[1, null]"),
    ]


@pytest.fixture
def vendor(extra: list[SimpleNamespace]) -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        registered=datetime(2024, 1, 1, tzinfo=timezone.utc),
        name="Vendor",
        comment=None,
        empty_spool_weight=None,
        external_id=None,
        extra=extra,
    )


@pytest.fixture
def filament(extra: list[SimpleNamespace], vendor: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        registered=datetime(2024, 1, 1, tzinfo=timezone.utc),
        name="Filament",
        vendor=vendor,
        material=None,
        price=None,
        density=1.24,
        diameter=1.75,
        weight=None,
        spool_weight=None,
        article_number=None,
        comment=None,
        settings_extruder_temp=None,
        settings_bed_temp=None,
        color_hex=None,
        multi_color_hexes=None,
        multi_color_direction=None,
        external_id=None,
        extra=extra,
    )


def test_response_models_decode_extra_values(
    filament: SimpleNamespace,
    extra: list[SimpleNamespace],
    vendor: SimpleNamespace,
):
    spool = SimpleNamespace(
        id=1,
        registered=datetime(2024, 1, 1, tzinfo=timezone.utc),
        first_used=None,
        last_used=None,
        filament=filament,
        price=None,
        initial_weight=None,
        spool_weight=None,
        used_weight=0,
        location=None,
        lot_nr=None,
        comment=None,
        archived=False,
        extra=extra,
        tags=[],
    )
    expected = {"smooth_time": 0.035, "enabled": True, "label": "PLA", "range": [1, None]}

    assert Vendor.from_db(vendor).extra == expected
    assert Filament.from_db(filament).extra == expected
    assert Spool.from_db(spool).extra == expected
