import os
import pandas as pd
import swmmtoolbox.swmmtoolbox as swmmtoolbox
from datetime import datetime

# Unit Conversion Constants
FLOW_TO_CFS = {
    "cfs": 1.0, "cms": 35.3146667, "mgd": 1.54722865, "gpm": 0.00222800926, "l/s": 0.0353146667
}
LENGTH_TO_FT = {
    "ft": 1.0, "m": 3.2808399, "in": 1/12.0, "cm": 0.032808399
}
VEL_TO_FTPS = {
    "ft/s": 1.0, "m/s": 3.2808399
}

def list_ids(outfile, item_type):
    """
    Safely discover IDs from a SWMM .out file.
    Returns a sorted list of ID strings.
    """
    try:
        if item_type == "pollutant":
            obj = swmmtoolbox.SwmmExtract(outfile)
            return sorted(list(obj.names[3]))
        
        # swmmtoolbox catalog returns: [('type', 'id'), ...]
        catalog = swmmtoolbox.catalog(outfile, item_type)
        return sorted({row[1] for row in catalog if row and len(row) > 1})
    except Exception as e:
        return []

def list_params(outfile, item_type):
    """
    List available parameters (variables) for a given item type.
    """
    try:
        if item_type == "pollutant":
            return ["Concentration"]
        
        vars_ = swmmtoolbox.listvariables(outfile)
        # vars_ is list of [type, variable_name, units]
        return sorted({row[1] for row in vars_ if row and row[0] == item_type})
    except Exception:
        return []

def extract_data(outfile, item_type, elem_id, param):
    """
    Extracts a single series as a DataFrame.
    """
    label = f"{item_type},{elem_id},{param}"
    try:
        # swmmtoolbox.extract returns a DataFrame or Series
        data = swmmtoolbox.extract(outfile, label)
        
        # Standardize to DataFrame with index as datetime
        if isinstance(data, pd.Series):
            data = data.to_frame(name="value")
        
        # Ensure column name is clean
        data.columns = ["value"]
        return data
    except Exception as e:
        raise ValueError(f"Could not extract {label}: {e}")

def convert_units(df, param_type, from_unit, to_unit):
    """
    Applies unit conversion to a DataFrame column 'value'.
    """
    if not from_unit or not to_unit or from_unit == to_unit:
        return df
    
    factor = 1.0
    
    if param_type == "flow":
        factor = FLOW_TO_CFS.get(from_unit, 1.0) / FLOW_TO_CFS.get(to_unit, 1.0)
    elif param_type in ["depth", "head"]:
        factor = LENGTH_TO_FT.get(from_unit, 1.0) / LENGTH_TO_FT.get(to_unit, 1.0)
    elif param_type == "velocity":
        factor = VEL_TO_FTPS.get(from_unit, 1.0) / VEL_TO_FTPS.get(to_unit, 1.0)
        
    df["value"] = df["value"] * factor
    return df
