def ids_need_refresh(state, outfile, element_type):
    """Return True when cached IDs should be recomputed.

    The Streamlit app caches discovered IDs in ``st.session_state`` to avoid
    rescanning large ``.out`` files on every render. The cache must be
    invalidated whenever:

    - No IDs have been cached yet.
    - The selected file changes.
    - The selected element type changes (e.g., node → link).
    """

    return (
        "ids" not in state
        or state.get("last_file") != outfile
        or state.get("last_item_type") != element_type
    )
