import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.data_fetch import fetch_power_data, fetch_smap_soil_moisture, fetch_modis_ndvi
from src.simulation import simulate_season, CROPS

st.set_page_config(page_title="AgriSense: NASA-Powered Smart Farming Simulator", page_icon="🌾")

st.title("🌾 AgriSense: NASA-Powered Smart Farming Simulator")
st.markdown("Simulate farming decisions using real NASA data. Choose crops, irrigation, and fertilization to maximize yield while maintaining sustainability.")

# Location: Bangladesh (Dhaka)
LAT, LON = 23.8103, 90.4125

# Fetch climate data for last 3 months (as proxy for forecast)
end_date = datetime.now()
start_date = datetime.now() - timedelta(days=90)
climate_df = fetch_power_data(LAT, LON, start_date, end_date)

if climate_df is not None:
    avg_rainfall = climate_df['PRECTOTCORR'].mean()
    avg_temp = climate_df['T2M'].mean()
    st.subheader("🌦️ NASA Climate Data (Last 3 Months)")
    st.write(f"Average Rainfall: {avg_rainfall:.1f} mm")
    st.write(f"Average Temperature: {avg_temp:.1f} °C")

    # Plot climate data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=climate_df.index, y=climate_df['PRECTOTCORR'], mode='lines', name='Rainfall (mm)'))
    fig.add_trace(go.Scatter(x=climate_df.index, y=climate_df['T2M'], mode='lines', name='Temperature (°C)', yaxis='y2'))
    fig.update_layout(title="Climate Data", yaxis=dict(title="Rainfall"), yaxis2=dict(title="Temperature", overlaying='y', side='right'))
    st.plotly_chart(fig)

    with st.expander("ℹ️ Learn about NASA POWER Data"):
        st.write("This climate forecast comes from NASA's POWER dataset, which provides solar and meteorological data. It helps predict weather patterns for better farming decisions.")

else:
    st.error("Failed to fetch climate data. Using default values.")
    avg_rainfall, avg_temp = 100, 25

# User inputs
st.subheader("🚜 Make Your Farming Decisions")
crop = st.selectbox("Choose Crop", list(CROPS.keys()))
irrigation = st.slider("Irrigation (mm)", 0, 1000, 200)
fertilizer = st.slider("Fertilizer (kg/ha)", 0, 300, 100)

if st.button("Simulate Season"):
    yield_val, sustain = simulate_season(crop, irrigation, fertilizer, avg_rainfall, avg_temp)

    st.subheader("📊 Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Crop Yield", f"{yield_val:.1f} tons/ha")
    with col2:
        st.metric("Sustainability Score", f"{sustain:.0f}/100")

    # Visualizations
    st.subheader("📈 Visualizations")
    # Mock soil moisture over time
    dates = [start_date + timedelta(days=i) for i in range(90)]
    soil_moisture = [fetch_smap_soil_moisture(LAT, LON, d) for d in dates]
    ndvi = [fetch_modis_ndvi(LAT, LON, d) for d in dates]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=dates, y=soil_moisture, mode='lines', name='Soil Moisture (%)'))
    fig2.add_trace(go.Scatter(x=dates, y=ndvi, mode='lines', name='NDVI (Vegetation Health)', yaxis='y2'))
    fig2.update_layout(title="Soil and Vegetation Data", yaxis=dict(title="Soil Moisture"), yaxis2=dict(title="NDVI", overlaying='y', side='right'))
    st.plotly_chart(fig2)

    with st.expander("ℹ️ Learn about NASA SMAP and MODIS Data"):
        st.write("Soil moisture data from NASA's SMAP mission shows water content in soil, affecting irrigation needs. NDVI from MODIS indicates vegetation health, helping assess crop growth.")

    # Feedback
    if sustain < 50:
        st.warning("⚠️ Your sustainability score is low. Consider reducing water or fertilizer usage.")
    elif yield_val < CROPS[crop]["base_yield"] * 0.8:
        st.info("💡 Yield is low. Try adjusting irrigation or fertilizer based on climate data.")

st.markdown("---")
st.markdown("Built with NASA data for educational purposes.")