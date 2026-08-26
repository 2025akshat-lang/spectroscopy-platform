import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Spectroscopy Analytics Platform", layout="wide")
st.title(" Interactive Spectroscopy Data Analytics Platform")
st.write("Engineering Analytics and Predictive Modeling for Spectroscopic Lab Results")

st.sidebar.header(" Project Modules")
module = st.sidebar.selectbox(
    "Select Analytical Module",
    ["1. Concentration Analytics (Beer-Lambert)", "2. Reaction Kinetics (Rate Laws)", "3. Complex Composition & Spectra (Job's Method)"]
)

st.subheader(f"Current Dashboard: {module}")

if "1. Concentration Analytics" in module:
    st.info(" Works for: CuSO4, KMnO4, K2Cr2O7, Fe2+-Phenanthroline, and Ni-DMG extraction experiments.")
    
    st.markdown(" Input Lab Readings")
    st.write("Modify the values below to verify any custom or real lab data instantly:")
    
    # Live editable data grid for Professor/User
    default_data = {
        "Concentration (M)": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        "Absorbance": [0.0, 0.31, 0.58, 0.92, 1.21, 1.48]
    }
    df_input = pd.DataFrame(default_data)
    
    # This makes the table fully interactive on screen!
    edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)
    
    # Extract values safely
    conc = edited_df.iloc[:, 0].values
    absorbance = edited_df.iloc[:, 1].values
    
    if len(conc) > 1 and len(absorbance) > 1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 📊 Stochastic Linear Regression Fit")
            m, c = np.polyfit(conc, absorbance, 1)
            st.success(f"📈 Calibration Curve: **Absorbance = {m:.4f} * Conc + ({c:.4f})**")
            
            # Interactive prediction for unknown sample
            st.markdown("#### 🎯 Verify Unknown Sample")
            unknown_abs = st.number_input("Enter Absorbance of Unknown Sample:", min_value=0.0, max_value=3.0, value=0.75, step=0.01)
            predicted_conc = (unknown_abs - c) / m
            st.metric(label="Calculated Concentration", value=f"{predicted_conc:.4f} M")
            
        with col2:
            fig, ax = plt.subplots()
            ax.scatter(conc, absorbance, color='red', s=100, label='Lab Readings')
            ax.plot(conc, m*conc + c, color='blue', linestyle='--', linewidth=2, label='Fit Line (y=mx+c)')
            ax.set_xlabel("Concentration (M)")
            ax.set_ylabel("Absorbance")
            ax.legend()
            st.pyplot(fig)
    else:
        st.warning("Please enter at least 2 rows of data to calculate the calibration curve.")

elif "2. Reaction Kinetics" in module:
    st.info("💡 Works for: Iodination of Acetone and Crystal Violet + NaOH Kinetics.")
    
    # Editable data for Kinetics
    default_kinetics = {
        "Time (seconds)":,
        "Absorbance (Raw)": [2.0, 1.62, 1.35, 1.10, 0.88, 0.71, 0.59]
    }
    df_kinetics = pd.DataFrame(default_kinetics)
    edited_kinetics = st.data_editor(df_kinetics, num_rows="dynamic", use_container_width=True)
    
    time = edited_kinetics.iloc[:, 0].values
    abs_raw = edited_kinetics.iloc[:, 1].values
    
    # Calculate simple rolling average to smooth
    df_calc = pd.DataFrame({"abs": abs_raw})
    abs_filtered = df_calc['abs'].rolling(window=3, min_periods=1, center=True).mean().values
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📈 Kinetics Parameter Extraction")
        if len(time) > 1 and len(abs_raw) > 1:
            # Avoid log of zero/negative
            safe_abs = np.where(abs_filtered > 0, abs_filtered, 0.001)
            ln_abs = np.log(safe_abs)
            k, c_k = np.polyfit(time, -ln_abs, 1)
            st.success(f"⏱️ Rate Constant (k): **{k:.4f} s⁻¹**")
            st.info(f"🧬 Calculated Half-life (t₁/₂): **{0.693/k:.2f} seconds**")
            
    with col2:
        fig, ax = plt.subplots()
        ax.plot(time, abs_raw, color='orange', marker='o', alpha=0.5, label='Raw Noisy Data')
        ax.plot(time, abs_filtered, color='green', marker='s', linewidth=2, label='Filtered Data Layer')
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Absorbance")
        ax.legend()
        st.pyplot(fig)

elif "3. Complex Composition" in module:
    st.info("💡 Works for: Job's Method (Fe-Salicylic Acid) and λmax Determination.")
    
    default_jobs = {
        "Mole Fraction / Wavelength": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "Absorbance": [0.0, 0.25, 0.48, 0.71, 0.89, 0.98, 0.85, 0.66, 0.42, 0.21, 0.0]
    }
    df_jobs = pd.DataFrame(default_jobs)
    edited_jobs = st.data_editor(df_jobs, num_rows="dynamic", use_container_width=True)
    
    x_val = edited_jobs.iloc[:, 0].values
    y_val = edited_jobs.iloc[:, 1].values
    
    col1, col2 = st.columns(2)
    with col1:
        if len(y_val) > 0:
            max_idx = np.argmax(y_val)
            optimal_val = x_val[max_idx]
            st.success(f"🎯 Peak Detected Apex at: **{optimal_val:.2f}**")
            st.write("Professor can change the table values to shift the peak position automatically.")
            
    with col2:
        fig, ax = plt.subplots()
        ax.scatter(x_val, y_val, color='purple', s=80, label='Lab Points')
        ax.plot(x_val, y_val, color='magenta', linestyle='-', label='Analytical Baseline')
        if len(y_val) > 0:
            ax.axvline(optimal_val, color='black', linestyle=':', label='Max Peak Apex')
        ax.legend()
        st.pyplot(fig)
