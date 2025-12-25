import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
import logic


def test_export_helpers_accept_plain_filenames(tmp_path, monkeypatch):
    df = pd.DataFrame(
        {"flow": [1.0, 2.5]},
        index=pd.to_datetime(["2024-01-01 00:00", "2024-01-01 01:00"]),
    )

    monkeypatch.chdir(tmp_path)

    logic.file_export_tsf(
        df,
        "plain.tsf",
        header1="IDs:\tflow",
        header2="Date/Time\tflow",
        time_format="%m/%d/%Y %H:%M",
        float_format="%.3f",
    )

    logic.file_export_dat(
        df,
        "plain.dat",
        header="IDs:\tflow",
        time_format="%m/%d/%Y %H:%M",
        float_format="%.3f",
    )

    logic.file_export_csv(
        df,
        "plain.csv",
        header="IDs,flow",
        time_format="%m/%d/%Y %H:%M",
        float_format="%.3f",
    )

    expected_headers = {
        "plain.tsf": ["IDs:\tflow", "Date/Time\tflow"],
        "plain.dat": ["IDs:\tflow", "Date/Time\tflow"],
        "plain.csv": ["IDs,flow", "Date/Time,flow"],
    }

    for name, headers in expected_headers.items():
        path = tmp_path / name
        assert path.is_file()
        lines = path.read_text().splitlines()
        assert lines[: len(headers)] == headers
