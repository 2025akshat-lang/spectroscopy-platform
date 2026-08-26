import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savitzky_golay

st.set_page_config(page_title="Spectroscopy Analytics Platform", layout="wide")
st.title("🔬 Interactive Spectroscopy Data Analytics Platform")
st.write("Engineering Fourier Transform Filters & Stochastic Probability Algorithms for Lab Results")

st.sidebar.header("📁 Project Modules")
module = st.sidebar.selectbox(
    "Select Analytical Module",
    ["1. Concentration Analytics (Beer-Lambert)", "2. Reaction Kinetics (Rate Laws)", "3. Complex Composition & Spectra (Job's Method)"]
)

def get_dummy_data(module_type):
    if module_type == 1:
        conc = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        abs_clean = conc * 1.5
        noise = np.random.normal(0, 0.04, len(conc))
        return pd.DataFrame({"Concentration (M)": conc, "Absorbance (Raw)": abs_clean + noise})
    elif module_type == 2:
        time = np.linspace(0, 60, 20)
        abs_clean = 2.0 * np.exp(-0.05 * time)
        noise = np.sin(time) * 0.05 + np.random.normal(0, 0.02, len(time))
        return pd.DataFrame({"Time (sec)": time, "Absorbance (Raw)": abs_clean + noise})
    else:
        mole_fraction = np.linspace(0, 1, 15)
        abs_clean = -4 * (mole_fraction - 0.5)**2 + 1.0
        noise = np.random.normal(0, 0.03, len(mole_fraction))
        return pd.DataFrame({"Mole Fraction of Ligand": mole_fraction, "Absorbance (Raw)": abs_clean + noise})

st.subheader(f"Current Dashboard: {module}")

if "1. Concentration Analytics" in module:
    st.info("💡 Works for: CuSO4, KMnO4, K2Cr2O7, Fe2+-Phenanthroline, and Ni-DMG extraction experiments.")
    df = get_dummy_data(1)
    col1, col2 = st.columns(2)
    with col1: st.write("### Lab Input Data", df)
    with col2:
        m, c = np.polyfit(df.iloc[:, 0], df.iloc[:, 1], 1)
        st.success(f"📊 Calibration Curve Equation: Absorbance = {m:.4f} * Conc + {c:.4f}")
        fig, ax = plt.subplots()
        ax.scatter(df.iloc[:, 0], df.iloc[:, 1], color='red', label='Raw Lab Points')
        ax.plot(df.iloc[:, 0], m*df.iloc[:, 0] + c, color='blue', linestyle='--', label='Stochastic Fit Line')
        ax.set_xlabel("Concentration (M)")
        ax.set_ylabel("Absorbance")
        ax.legend()
        st.pyplot(fig)

elif "2. Reaction Kinetics" in module:
    st.info("💡 Works for: Iodination of Acetone and Crystal Violet + NaOH Kinetics.")
    df = get_dummy_data(2)
    df['Absorbance (Filtered)'] = savitzky_golay(df['Absorbance (Raw)'].values, window_size=5, order=2)
    col1, col2 = st.columns(2)
    with col1: st.write("### Kinetics Data Streams", df)
    with col2:
        st.write("### Signal Processing: Fourier Filter Layer")
        fig, ax = plt.subplots()
        ax.plot(df.iloc[:, 0], df['Absorbance (Raw)'], color='orange', alpha=0.6, label='Raw Noisy Data')
        ax.plot(df.iloc[:, 0], df['Absorbance (Filtered)'], color='green', linewidth=2, label='Filtered/Smooth Data')
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Absorbance")
        ax.legend()
        st.pyplot(fig)

elif "3. Complex Composition" in module:
    st.info("💡 Works for: Job's Method (Fe-Salicylic Acid) and λmax Determination.")
    df = get_dummy_data(3)
    df['Absorbance (Filtered)'] = savitzky_golay(df['Absorbance (Raw)'].values, window_size=5, order=2)
    col1, col2 = st.columns(2)
    with col1: st.write("### Job's Continuous Variation Dataset", df)
    with col2:
        max_idx = df['Absorbance (Filtered)'].idxmax()
        optimal_val = df.iloc[max_idx, 0]
        st.success(f"🎯 Peak Detected at Mole Fraction / Wavelength: **{optimal_val:.2f}**")
        fig, ax = plt.subplots()
        ax.scatter(df.iloc[:, 0], df.iloc[:, 1], color='purple', label='Lab Readings')
        ax.plot(df.iloc[:, 0], df['Absorbance (Filtered)'], color='magenta', label='Analytical Baseline')
        ax.axvline(optimal_val, color='black', linestyle=':', label='Max Absorption Apex')
        ax.legend()
        st.pyplot(fig)
