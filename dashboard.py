from pathlib import Path

import pandas as pd
import streamlit as st

from src.pipeline import run

st.set_page_config(page_title="Data Platform Observability", layout="wide")
st.title("Data Platform Observability")
st.caption("Synthetic operational data • quality contracts • incremental-ready pipeline")

input_path = Path("data/raw/events.csv")
output_dir = Path("data/curated")
if not input_path.exists():
    st.info("Run: python -m src.generate_data --output data/raw/events.csv")
    st.stop()

if st.button("Run pipeline"):
    st.session_state["quality"] = run(input_path, output_dir)

quality = st.session_state.get("quality")
if quality is None and (output_dir / "quality_metrics.json").exists():
    import json
    quality = json.loads((output_dir / "quality_metrics.json").read_text())

if quality:
    cols = st.columns(4)
    cols[0].metric("Input rows", f"{quality['input_rows']:,}")
    cols[1].metric("Curated rows", f"{quality['output_rows']:,}")
    cols[2].metric("Dropped rows", f"{quality['dropped_rows']:,}")
    cols[3].metric("Null rate", f"{quality['null_rate']:.2%}")
    gold = pd.read_csv(output_dir / "gold_service_daily.csv")
    st.subheader("Daily service performance")
    st.dataframe(gold.tail(100), use_container_width=True)

