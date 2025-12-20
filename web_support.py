import io
import json
from typing import Dict, Iterable, List

from core import convert_units, extract_data, list_ids, list_params


PARAM_KEYWORDS = {
    "flow": ["flow", "discharge"],
    "depth": ["depth"],
    "head": ["head"],
    "velocity": ["vel", "velocity"],
}


def infer_param_type(param: str) -> str:
    plower = param.lower()
    for key, tokens in PARAM_KEYWORDS.items():
        for token in tokens:
            if token in plower:
                return key
    return "other"


def list_ids_js(outfile: str, element_type: str) -> List[str]:
    return list_ids(outfile, element_type)


def list_params_js(outfile: str, element_type: str) -> List[str]:
    return list_params(outfile, element_type)


def extract_to_text(
    outfile: str,
    element_type: str,
    ids: Iterable[str],
    params: Iterable[str],
    units: Dict[str, str],
    output_format: str = "csv",
) -> Dict[str, str]:
    """Return a mapping of filename -> file contents as string."""

    sep = "\t" if output_format == "tsv" else ","
    results: Dict[str, str] = {}

    for eid in ids:
        combined = None
        for param in params:
            df = extract_data(outfile, element_type, eid, param)
            ptype = infer_param_type(param)
            src_unit = "cfs" if ptype == "flow" else "ft"

            if ptype == "flow":
                target_unit = units.get("flow")
            elif ptype in {"depth", "head"}:
                target_unit = units.get("length")
            elif ptype == "velocity":
                target_unit = units.get("velocity")
            else:
                target_unit = None

            df = convert_units(df, ptype, src_unit, target_unit)
            df.columns = [f"{param}_{target_unit or ''}".strip("_")]

            if combined is None:
                combined = df
            else:
                combined = combined.join(df, how="outer")

        if combined is None:
            continue

        buffer = io.StringIO()
        combined.to_csv(buffer, sep=sep)
        results[f"{element_type}_{eid}.{output_format}"] = buffer.getvalue()

    return results


if __name__ == "__main__":
    # Convenience for local manual testing
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("outfile")
    parser.add_argument("element_type")
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--params", nargs="*", default=[])
    parser.add_argument("--flow-unit", default="cfs")
    parser.add_argument("--length-unit", default="ft")
    parser.add_argument("--velocity-unit", default="ft/s")
    parser.add_argument("--format", default="csv")
    args = parser.parse_args()

    output = extract_to_text(
        outfile=args.outfile,
        element_type=args.element_type,
        ids=args.ids,
        params=args.params,
        units={
            "flow": args.flow_unit,
            "length": args.length_unit,
            "velocity": args.velocity_unit,
        },
        output_format=args.format,
    )
    print(json.dumps(output, indent=2) or "No data extracted")
