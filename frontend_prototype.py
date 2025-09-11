import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import joblib
import streamlit as st

# ---------------------------
# Page config & hide default menu/footer
# ---------------------------
st.set_page_config(
    page_title="Storm Prediction",
    page_icon="🌩️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------
# Config
# ---------------------------
API_KEY = "73a446100bca4ea68dc100105251109"
MODEL_PATH = "storm_rf_model.joblib"
DAYS_HISTORY = 7
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata"]

# ---------------------------
# Fetch historical weather
# ---------------------------
def fetch_historical_weather(city, date):
    url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if "forecast" not in data:
        return None
    day = data["forecast"]["forecastday"][0]["day"]
    return {
        "city": city,
        "date": date,
        "temp_max": day["maxtemp_c"],
        "temp_min": day["mintemp_c"],
        "precip_mm": day["totalprecip_mm"],
        "windspeed": day["maxwind_kph"],
        "humidity": day["avghumidity"],
        "pressure_mb": 1013,
    }

# ---------------------------
# Build features
# ---------------------------
def build_features(df, past_n=3):
    df = df.sort_values("date").reset_index(drop=True)
    df["temp_diff"] = df["temp_max"] - df["temp_min"]
    max_lag = min(past_n, len(df) - 1)

    for lag in range(1, max_lag + 1):
        df[f"temp_diff_lag{lag}"] = df["temp_diff"].shift(lag)
        df[f"precip_mm_lag{lag}"] = df["precip_mm"].shift(lag)
        df[f"windspeed_lag{lag}"] = df["windspeed"].shift(lag)
        df[f"humidity_lag{lag}"] = df["humidity"].shift(lag)
        df[f"pressure_mb_lag{lag}"] = df["pressure_mb"].shift(lag)

    if max_lag > 0:
        df["precip_rolling"] = df["precip_mm"].rolling(max_lag, min_periods=1).sum().shift(1)
        df["windspeed_rolling"] = df["windspeed"].rolling(max_lag, min_periods=1).max().shift(1)
        df["humidity_rolling"] = df["humidity"].rolling(max_lag, min_periods=1).mean().shift(1)
        df["pressure_rolling"] = df["pressure_mb"].rolling(max_lag, min_periods=1).mean().shift(1)
    else:
        df["precip_rolling"] = df["precip_mm"]
        df["windspeed_rolling"] = df["windspeed"]
        df["humidity_rolling"] = df["humidity"]
        df["pressure_rolling"] = df["pressure_mb"]

    df = df.fillna(method="bfill").fillna(method="ffill")
    return df

# ---------------------------
# Predict storm
# ---------------------------
def predict_storm(df_features):
    clf, feature_cols, imputer = joblib.load(MODEL_PATH)
    for col in feature_cols:
        if col not in df_features.columns:
            df_features[col] = 0
    X = df_features[feature_cols]
    X_imputed = pd.DataFrame(imputer.transform(X), columns=feature_cols)
    storm_pred = clf.predict(X_imputed)[0]
    storm_prob = clf.predict_proba(X_imputed)[0][1]
    return storm_pred, storm_prob

# ---------------------------
# Streamlit UI
# ---------------------------
def main():
    st.title("🌩️ Storm Prediction System")
    st.write("Predict storms using last 7 days of weather data.")

    city = st.text_input("Enter a city for prediction:", placeholder="Type a city name")
    if city:
        today = datetime.now().strftime("%Y-%m-%d")
        weather = fetch_historical_weather(city, today)

        if not weather:
            st.error("❌ Could not fetch weather for this city.")
            return

        # Display current weather details
        st.subheader(f"📍 Weather details for {city} ({today})")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌡️ Max Temp (°C)", weather["temp_max"])
            st.metric("🌡️ Min Temp (°C)", weather["temp_min"])
            st.metric("💧 Humidity (%)", weather["humidity"])
        with col2:
            st.metric("🌧️ Precipitation (mm)", weather["precip_mm"])
            st.metric("💨 Wind Speed (kph)", weather["windspeed"])
            st.metric("🔽 Pressure (mb)", weather["pressure_mb"])

        # Automatically predict storm risk
        df_feat = pd.DataFrame([weather])
        df_feat = build_features(df_feat)
        if df_feat.empty:
            st.error("⚠️ Not enough data to build features.")
            return

        storm, prob = predict_storm(df_feat)

        # Alert message (auto, no button needed)
        st.subheader("🔮 Prediction Result")
        st.info(f"🌩️ Storm probability for {city}: {prob:.2f}")

        if storm:
            st.error(f"⚠️ ALERT: Storm likely in {city}! Stay safe.")
        else:
            st.success(f"✅ No storm predicted in {city}. Conditions look stable.")


if __name__ == "__main__":
    main()
