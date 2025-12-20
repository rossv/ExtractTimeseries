import streamlit as st
import os
import pandas as pd
from core import list_ids, list_params, extract_data, convert_units
from utils import init_session_state, get_out_files, format_file_size, sanitize_filename  # <--- NEW IMPORT

st.set_page_config(page_title="SWMM Timeseries Extractor", layout="wide", page_icon="🌊")

# Initialize State
init_session_state()

# --- UI Helper: File Selector ---
def file_selector(folder_path):
    filenames = get_out_files(folder_path)
    if not filenames:
        st.warning("No .out files found in this directory.")
        return None
    
    # Create a display map so user sees "File.out (2.5 GB)"
    display_map = {f: f"{os.path.basename(f)} ({format_file_size(f)})" for f in filenames}
    
    selected_file = st.selectbox(
        "Select .out file", 
        filenames, 
        format_func=lambda x: display_map[x]
    )
    return selected_file

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("1. Source Selection")
    working_dir = st.text_input("Root Folder Path", value=os.getcwd())
    
    if os.path.isdir(working_dir):
        outfile = file_selector(working_dir)
    else:
        st.error("Invalid directory path")
        outfile = None

    st.header("4. Output Settings")
    output_format = st.selectbox("Format", ["csv", "dat", "tsf"])
    output_dir = st.text_input("Output Directory", value=os.path.join(working_dir, "extracted"))

# --- Main Page ---
st.title("🌊 SWMM Unified Extractor")
st.markdown("Extract timeseries from binary `.out` files efficiently.")

if outfile:
    st.info(f"Selected File: `{os.path.basename(outfile)}`")
    
    # --- Tabbed Interface ---
    tab_ids, tab_params, tab_units, tab_run = st.tabs(["Select Elements", "Select Parameters", "Unit Config", "Run Extraction"])
    
    # 1. Element Selection
    with tab_ids:
        col1, col2 = st.columns([1, 2])
        with col1:
            element_type = st.selectbox("Element Type", ["node", "link", "subcatchment", "system", "pollutant"])
        
        with col2:
            # Dynamic ID Discovery
            if 'ids' not in st.session_state or st.session_state.get('last_file') != outfile:
                with st.spinner("Scanning file for IDs..."):
                    st.session_state['ids'] = list_ids(outfile, element_type)
                    st.session_state['last_file'] = outfile
            
            all_ids = st.session_state['ids']
            
            # Search/Filter
            search_term = st.text_input("Search IDs", "")
            filtered_ids = [i for i in all_ids if search_term.lower() in i.lower()] if search_term else all_ids
            
            selected_ids = st.multiselect("Select IDs to Extract", filtered_ids, default=[])
            
            if st.checkbox("Select All Filtered (Caution: May be slow for 1000+ items)"):
                selected_ids = filtered_ids

    # 2. Parameter Selection
    with tab_params:
        avail_params = list_params(outfile, element_type)
        selected_params = st.multiselect(f"Select Parameters for {element_type}", avail_params)

    # 3. Units Configuration
    with tab_units:
        st.write("Convert outputs to specific units.")
        c1, c2, c3 = st.columns(3)
        with c1:
            flow_unit = st.selectbox("Flow Units", ["cfs", "cms", "mgd", "l/s", "gpm"], index=0)
        with c2:
            len_unit = st.selectbox("Length/Head Units", ["ft", "m"], index=0)
        with c3:
            vel_unit = st.selectbox("Velocity Units", ["ft/s", "m/s"], index=0)

    # 4. Execution
    with tab_run:
        st.subheader("Summary")
        st.write(f"Extracting **{len(selected_ids)}** {element_type}s × **{len(selected_params)}** params")
        
        if st.button("Start Extraction", type="primary"):
            if not selected_ids or not selected_params:
                st.error("Please select at least one ID and one Parameter.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                os.makedirs(output_dir, exist_ok=True)
                
                total_ops = len(selected_ids) * len(selected_params)
                completed = 0
                
                for i, eid in enumerate(selected_ids):
                    # Combine mode logic could go here (single file per ID)
                    combined_df = pd.DataFrame()
                    
                    for param in selected_params:
                        status_text.text(f"Extracting {eid} - {param}...")
                        
                        try:
                            df = extract_data(outfile, element_type, eid, param)
                            
                            # Auto-detect param type for unit conversion (simplified)
                            p_type = "other"
                            if "flow" in param.lower(): p_type = "flow"
                            elif "depth" in param.lower(): p_type = "depth"
                            elif "head" in param.lower(): p_type = "head"
                            elif "veloc" in param.lower(): p_type = "velocity"
                            
                            target_unit = None
                            if p_type == "flow": target_unit = flow_unit
                            elif p_type in ["depth", "head"]: target_unit = len_unit
                            elif p_type == "velocity": target_unit = vel_unit
                            
                            # Assume defaults (cfs/ft) for source, or add config
                            df = convert_units(df, p_type, "cfs" if p_type=="flow" else "ft", target_unit)
                            
                            # Rename column
                            df.columns = [f"{param}_{target_unit}"]
                            
                            if combined_df.empty:
                                combined_df = df
                            else:
                                combined_df = combined_df.join(df, how="outer")
                                
                        except Exception as e:
                            st.warning(f"Failed {eid}/{param}: {e}")
                        
                        completed += 1
                        progress_bar.progress(min(completed / total_ops, 1.0))
                    
                    # Write to disk
                    if not combined_df.empty:
                        out_name = f"{element_type}_{eid}.{output_format}"
                        out_path = os.path.join(output_dir, out_name)
                        
                        if output_format == "csv":
                            combined_df.to_csv(out_path)
                        elif output_format == "dat":
                            combined_df.to_csv(out_path, sep="\t")
                        
                st.success(f"Done! Files saved to: {output_dir}")
                st.balloons()
