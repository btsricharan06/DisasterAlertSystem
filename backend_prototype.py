import requests
import pandas as pd
from datetime import datetime
import joblib
import streamlit as st

API_KEY = "73a446100bca4ea68dc100105251109"
MODEL_PATH = "storm_rf_model.joblib"

# ---------------------------
# Fetching past weather data
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
# Storm Simulation Function
# ---------------------------
def simulate_storm_test(city):
    today = datetime.now().strftime("%Y-%m-%d")
    fake_weather = {
        "city": city,
        "date": today,
        "temp_max": 32,
        "temp_min": 24,
        "precip_mm": 50,   # heavy rainfall
        "windspeed": 80,   # strong winds
        "humidity": 95,    # very humid
        "pressure_mb": 995 # low pressure
    }

    st.subheader("🧪 Storm Simulation Test")
    st.json(fake_weather)   # ✅ show fake weather like normal data
    st.error(f"⚠️ ALERT: Simulated upcoming storm detected in {city}! Take precautions.")

# ---------------------------
# Main App
# ---------------------------
def main():
    st.title("🌩️ Storm Prediction System")

    # City input
    city = st.text_input("Enter a city for prediction:", placeholder="City name")

    # Simulation button
    if city and st.button("Run Storm Simulation Test"):
        simulate_storm_test(city)
        return  # 🚨 Skip normal prediction when simulation runs

    # Normal weather prediction
    if city:
        today = datetime.now().strftime("%Y-%m-%d")
        weather = fetch_historical_weather(city, today)
        if not weather:
            st.error("❌ Could not fetch weather for this city.")
            return
        df_feat = pd.DataFrame([weather])
        df_feat = build_features(df_feat)
        storm, prob = predict_storm(df_feat)

        st.subheader(f"📍 Weather Details for {city}")
        st.json(weather)
        st.info(f"🌩️ Storm probability for {city}: {prob:.2f}")
        if storm:
            st.error(f"⚠️ Storm likely in {city}!")
        else:
            st.success(f"✅ No storm predicted in {city}.")


if __name__ == "__main__":
    main()
