import streamlit as st
from vina import Vina
import os

st.title("🧬 AutoDock Vina Web App")
st.write("Scripps AutoDock Vina Engine ko use karte hue online molecular docking karein.")

# Files upload karne ke options
receptor_file = st.file_uploader("1. Apni Receptor PDBQT File Upload Karein (.pdbqt)", type=["pdbqt"])
ligand_file = st.file_uploader("2. Apni Ligand PDBQT File Upload Karein (.pdbqt)", type=["pdbqt"])

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
        with st.spinner("Docking chal rahi hai... Bara-e-maharbani thora intezar karein..."):
            try:
                # Files ko temporary save karna taake Vina parh sake
                with open("receptor.pdbqt", "wb") as f:
                    f.write(receptor_file.getbuffer())
                with open("ligand.pdbqt", "wb") as f:
                    f.write(ligand_file.getbuffer())
                
                # Scripps AutoDock Vina Engine ko initialize karna
                v = Vina(sf_name='vina')
                v.set_receptor('receptor.pdbqt')
                v.set_ligand_from_file('ligand.pdbqt')
                
                # Grid box setup karna
                v.compute_vina_maps(center=[cx, cy, cz], size=[sx, sy, sz])
                
                # Docking run karna
                v.dock(exhaustiveness=exhaustiveness, n_poses=9)
                
                # Results save karna
                v.write_poses('output_poses.pdbqt', n_poses=9, overwrite=True)
                
                st.success("🎉 Docking Mukammal Ho Gayi!")
                
                # Output file download karne ka button
                with open("output_poses.pdbqt", "rb") as f:
                    st.download_button(
                        label="📥 Download Docking Results (.pdbqt)",
                        data=f,
                        file_name="docking_results.pdbqt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Koi masla aaya hai: {str(e)}")
    else:
        st.warning("Bara-e-maharbani Receptor aur Ligand dono files upload karein.")
