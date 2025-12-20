import sys
from pathlib import Path

import types

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

mock_swmmtoolbox = types.ModuleType("swmmtoolbox.swmmtoolbox")
mock_swmmtoolbox.SwmmExtract = lambda *args, **kwargs: None
mock_swmmtoolbox.catalog = lambda *args, **kwargs: []
mock_swmmtoolbox.listvariables = lambda *args, **kwargs: []
mock_swmmtoolbox.extract = lambda *args, **kwargs: None
sys.modules["swmmtoolbox"] = types.ModuleType("swmmtoolbox")
sys.modules["swmmtoolbox.swmmtoolbox"] = mock_swmmtoolbox

from core import convert_units


def test_flow_cfs_and_cms_roundtrip():
    df_to_cms = pd.DataFrame({"value": [35.3146667, 70.6293334]})
    converted_cms = convert_units(df_to_cms.copy(), "flow", "cfs", "cms")
    assert converted_cms["value"].tolist() == pytest.approx([1.0, 2.0])

    df_to_cfs = pd.DataFrame({"value": [1.0, 2.0]})
    converted_cfs = convert_units(df_to_cfs.copy(), "flow", "cms", "cfs")
    assert converted_cfs["value"].tolist() == pytest.approx([35.3146667, 70.6293334])


def test_flow_cfs_and_mgd_roundtrip():
    df_to_mgd = pd.DataFrame({"value": [1.0, 2.0]})
    converted_mgd = convert_units(df_to_mgd.copy(), "flow", "cfs", "mgd")
    assert converted_mgd["value"].tolist() == pytest.approx([0.646316889, 1.292633778])

    df_to_cfs = pd.DataFrame({"value": [0.646316889, 1.292633778]})
    converted_cfs = convert_units(df_to_cfs.copy(), "flow", "mgd", "cfs")
    assert converted_cfs["value"].tolist() == pytest.approx([1.0, 2.0])


def test_length_head_ft_and_m_roundtrip():
    df_to_m = pd.DataFrame({"value": [3.2808399, 6.5616798]})
    converted_m = convert_units(df_to_m.copy(), "head", "ft", "m")
    assert converted_m["value"].tolist() == pytest.approx([1.0, 2.0])

    df_to_ft = pd.DataFrame({"value": [1.0, 2.0]})
    converted_ft = convert_units(df_to_ft.copy(), "head", "m", "ft")
    assert converted_ft["value"].tolist() == pytest.approx([3.2808399, 6.5616798])


def test_velocity_ftps_and_mps_roundtrip():
    df_to_mps = pd.DataFrame({"value": [3.2808399, 6.5616798]})
    converted_mps = convert_units(df_to_mps.copy(), "velocity", "ft/s", "m/s")
    assert converted_mps["value"].tolist() == pytest.approx([1.0, 2.0])

    df_to_ftps = pd.DataFrame({"value": [1.0, 2.0]})
    converted_ftps = convert_units(df_to_ftps.copy(), "velocity", "m/s", "ft/s")
    assert converted_ftps["value"].tolist() == pytest.approx([3.2808399, 6.5616798])


def test_convert_units_identity_and_noop():
    base_df = pd.DataFrame({"value": [1.0, 2.0]})

    same_units = convert_units(base_df.copy(), "flow", "cfs", "cfs")
    assert same_units["value"].tolist() == [1.0, 2.0]

    missing_units = convert_units(base_df.copy(), "flow", None, None)
    assert missing_units["value"].tolist() == [1.0, 2.0]
