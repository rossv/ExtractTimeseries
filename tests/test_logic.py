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


def test_combine_across_files_preserves_columns(tmp_path):
    file1 = tmp_path / "part1.csv"
    file2 = tmp_path / "part2.csv"

    file1.write_text(
        "\n".join(
            [
                "IDs,id1",
                "Date/Time,valueA,valueB",
                "01/01/2024 00:00,1,10",
                "01/01/2024 01:00,2,20",
            ]
        )
    )

    file2.write_text(
        "\n".join(
            [
                "IDs,id1",
                "Date/Time,valueA,valueB,valueC",
                "01/01/2024 02:00,3,30,300",
                "01/01/2024 03:00,4,40,400",
            ]
        )
    )

    logic.combine_across_files(
        [("node", str(file1)), ("node", str(file2))],
        out_format="csv",
        output_dir=str(tmp_path),
        dat_template="{id}_{short}",
    )

    combined_dir = tmp_path / "combined"
    out_files = list(combined_dir.glob("*.csv"))
    assert len(out_files) == 1

    lines = out_files[0].read_text().splitlines()
    assert lines[0] == "IDs,id1"
    assert lines[1] == "Date/Time,valueA,valueB,valueC"
    assert lines[2] == "01/01/2024 00:00,1.000000,10.000000,nan"
    assert lines[3] == "01/01/2024 01:00,2.000000,20.000000,nan"
    assert lines[4] == "01/01/2024 02:00,3.000000,30.000000,300.000000"
    assert lines[5] == "01/01/2024 03:00,4.000000,40.000000,400.000000"
