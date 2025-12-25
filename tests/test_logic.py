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


def test_export_dat_csv_coerce_index_and_format(tmp_path, monkeypatch):
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-02-01 00:00", "2024-02-01 01:30"]),
            "flow": [1.23456, 2.34567],
        },
        index=[10, 20],
    )

    monkeypatch.chdir(tmp_path)

    time_format = "%m/%d/%Y %H:%M"
    float_format = "%.3f"

    logic.file_export_dat(
        df,
        "coerced.dat",
        header="IDs:\tflow",
        time_format=time_format,
        float_format=float_format,
    )

    logic.file_export_csv(
        df,
        "coerced.csv",
        header="IDs,flow",
        time_format=time_format,
        float_format=float_format,
    )

    dat_lines = (tmp_path / "coerced.dat").read_text().splitlines()
    csv_lines = (tmp_path / "coerced.csv").read_text().splitlines()

    assert dat_lines[0] == "IDs:\tflow"
    assert dat_lines[1].startswith("Date/Time\t")
    assert dat_lines[2] == "02/01/2024 00:00\t1.235"

    assert csv_lines[0] == "IDs,flow"
    assert csv_lines[1].startswith("Date/Time,")
    assert csv_lines[2] == "02/01/2024 00:00,1.235"
