import streamlit as st
from vina import Vina
import os

st.set_page_config(page_title="AutoDock Vina Web App", page_icon="🧬")
st.title("🧬 AutoDock Vina Web App")
st.write("Perform online molecular docking using the official Scripps AutoDock Vina Engine.")

# File Uploader Section
receptor_file = st.file_uploader("1. Upload Receptor PDBQT File (.pdbqt)", type=["pdbqt"])
ligand_file = st.file_uploader("2. Upload Ligand PDBQT File (.pdbqt)", type=["pdbqt"])

st.subheader("Grid Box Settings (Binding Pocket)")
col1, col2, col3 = st.columns(3)
with col1:
    cx = st.number_input("Center X", value=0.0)
    sx = st.number_input("Size X", value=15.0)
with col2:
    cy = st.number_input("Center Y", value=0.0)
    sy = st.number_input("Size Y", value=15.0)
with col3:
    cz = st.number_input("Center Z", value=0.0)
    sz = st.number_input("Size Z", value=15.0)

exhaustiveness = st.slider("Exhaustiveness (Accuracy)", min_value=4, max_value=16, value=8)

if st.button("🚀 Start Docking"):
    if receptor_file and ligand_file:
        with st.spinner("Docking in progress... Please wait a moment..."):
            try:
                # Save uploaded files temporarily
                with open("receptor.pdbqt", "wb") as f:
                    f.write(receptor_file.getbuffer())
                with open("ligand.pdbqt", "wb") as f:
                    f.write(ligand_file.getbuffer())
                
                # Initialize AutoDock Vina Engine
                v = Vina(sf_name='vina')
                v.set_receptor('receptor.pdbqt')
                v.set_ligand_from_file('ligand.pdbqt')
                
                # Setup Grid Box Maps
                v.compute_vina_maps(center=[cx, cy, cz], size=[sx, sy, sz])
                
                # Execute Docking
                v.dock(exhaustiveness=exhaustiveness, n_poses=9)
                
                # Save Poses to File
                v.write_poses('output_poses.pdbqt', n_poses=9, overwrite=True)
                
                st.success("🎉 Docking Completed Successfully!")
                
                # Download Button for Results
                with open("output_poses.pdbqt", "rb") as f:
                    st.download_button(
                        label="📥 Download Docking Results (.pdbqt)",
                        data=f,
                        file_name="docking_results.pdbqt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload both Receptor and Ligand files to proceed.")
