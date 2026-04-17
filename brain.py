import joblib
import pandas as pd
import numpy as np

# Load model v3 only (fixed model without data leakage)
model_artifacts = joblib.load("pred_model_v3.pkl")
model = model_artifacts['model']
label_encoders = model_artifacts['label_encoders']
feature_columns = model_artifacts['feature_columns']

# Translation dictionaries for recommendations
recommendations_dict = {
    "low_rain": {
        "English": "⚠️ Rainfall is low — consider increasing irrigation or choosing drought-resistant crop varieties.",
        "Hindi": "⚠️ वर्षा कम है — सिंचाई बढ़ाने या सूखा-प्रतिरोधी फसल varieties को चुनने पर विचार करें।",
        "Odia": "⚠️ ବର୍ଷା କମ୍ — ସିଚାଇ ବୃଦ୍ଧି କରିବା କିମ୍ବା ଅନାବୃଷ୍ଟି-ସହିଷ୍ଣୁ ଫସଳ ଚୟନ କରନ୍ତୁ।"
    },
    "high_rain": {
        "English": "💧 Excess rainfall expected — ensure proper drainage and consider water-tolerant crops.",
        "Hindi": "💧 अत्यधिक वर्षा की संभावना — उचित जल निकासी सुनिश्चित करें और जल-सहनशील फसलों पर विचार करें।",
        "Odia": "💧 ଅଧିକ ବର୍ଷା ସମ୍ଭାବନା — ଠିକ ଭାବରେ ପାଣି ନିଷ୍କାଶନ କରନ୍ତୁ ଏବଂ ଜଳ-ସହିଷ୍ଣୁ ଫସଳ ବାଛନ୍ତୁ।"
    },
    "low_fert": {
        "English": "🌱 Fertilizer per hectare is low — consider soil testing and targeted nutrient application. Recommended: 100-300 kg/ha based on soil health.",
        "Hindi": "🌱 प्रति हेक्टेयर उर्वरक कम है — मिट्टी परीक्षण और लक्षित पोषक तत्व अनुप्रयोग पर विचार करें। अनुशंसित: 100-300 किग्रा/हेक्टेयर।",
        "Odia": "🌱 ପ୍ରତି ହେକ୍ଟରରେ ସାର କମ୍ — ମାଟି ପରୀକ୍ଷଣ ଏବଂ ଲକ୍ଷ୍ୟିତ ପୋଷକ ତତ୍ୱ ପ୍ରୟୋଗ କରନ୍ତୁ। ସୁପାରିସ: 100-300 କି.ଗ୍ରା./ହେକ୍ଟର।"
    },
    "high_fert": {
        "English": "🧪 Fertilizer per hectare is very high — risk of nutrient runoff and soil degradation. Consider precision farming techniques.",
        "Hindi": "🧪 प्रति हेक्टेयर उर्वरक बहुत अधिक है — पोषक तत्व क्षरण और मिट्टी क्षरण का जोखिम। सटीक खेती तकनीकों पर विचार करें।",
        "Odia": "🧪 ପ୍ରତି ହେକ୍ଟରରେ ସାର ଅଧିକ — ପୋଷକ ତତ୍ୱ କ୍ଷୟ ଏବଂ ମାଟି ଅବକ୍ଷୟର ଝୁକି। ସଠିକ କୃଷି ପ୍ରଯୁକ୍ତି ବିବେଚନା କରନ୍ତୁ।"
    },
    "high_pest": {
        "English": "🐞 High pesticide per hectare — risk of pest resistance and environmental damage. Consider Integrated Pest Management (IPM).",
        "Hindi": "🐞 प्रति हेक्टेयर कीटनाशक अधिक है — कीट प्रतिरोध और पर्यावरण क्षति का जोखिम। समेकित कीट प्रबंधन (IPM) अपनाएं।",
        "Odia": "🐞 ପ୍ରତି ହେକ୍ଟରରେ କୀଟନାଶକ ଅଧିକ — କୀଟ ପ୍ରତିରୋଧ ଏବଂ ପରିବେଶ କ୍ଷତିର ଝୁକି। ସମନ୍ୱିତ କୀଟ ପରିଚାଳନା (IPM) ଅବଲମ୍ବନ କରନ୍ତୁ।"
    },
    "optimal": {
        "English": "✅ Your inputs are well-balanced. Maintain current practices and monitor weather forecasts.",
        "Hindi": "✅ आपके इनपुट संतुलित हैं। वर्तमान प्रथाओं को बनाए रखें और मौसम पूर्वानुमान पर नजर रखें।",
        "Odia": "✅ ଆପଣଙ୍କର ଇନପୁଟ୍ ସମତୁଳିତ। ବର୍ତ୍ତମାନ ପ୍ରକ୍ରିଆ ରଖନ୍ତୁ ଏବଂ ପାଣିପାଗ ପୂର୍ବାନୁମାନ ପରିଖ୍ଯାତ କରନ୍ତୁ।"
    },
    "rainfall_perfect": {
        "English": "🌧️ Rainfall is optimal for this crop. Good drainage recommended during heavy spells.",
        "Hindi": "🌧️ वर्षा इस फसल के लिए अनुकूल है। भारी बारिश के दौरान अच्छा जल निकासी सुनिश्चित करें।",
        "Odia": "🌧️ ଏହି ଫସଳ ପାଇଁ ବର୍ଷା ଉତ୍ତମ। ପ୍ରବଳ ବର୍ଷା ସମୟରେ ଭଲ ଜଳ ନିଷ୍କାଶନ ସୁନିଶ୍ଚିତ କରନ୍ତୁ।"
    },
    "small_farm": {
        "English": "🏡 Small farm detected — consider intercropping for better land use and crop insurance for risk protection.",
        "Hindi": "🏡 छोटा खेत — बेहतर भूमि उपयोग के लिए मिश्रित खेती और जोखिम सुरक्षा के लिए फसल बीमा पर विचार करें।",
        "Odia": "🏡 ଛୋଟ ଖେତ — ଉନ୍ନତ ଭୂମି ବ୍ୟବହାର ପାଇଁ ମିଶ୍ରିତ ଫସଳ ଏବଂ ଝୁକି ସୁରକ୍ଷା ପାଇଁ ଫସଳ ବୀମା ବିଚାର କରନ୍ତୁ।"
    },
    "large_farm": {
        "English": "🚜 Large farm detected — consider mechanization and precision agriculture for efficiency.",
        "Hindi": "🚜 बड़ा खेत — दक्षता के लिए यंत्रीकरण और सटीक कृषि पर विचार करें।",
        "Odia": "🚜 ବଡ଼ ଖେତ — ଦକ୍ଷତା ପାଇଁ ଯନ୍ତ୍ରୀକରଣ ଏବଂ ସଠିକ କୃଷି ବିଚାର କରନ୍ତୁ।"
    }
}

def predict_with_improved_model(crop, season, state, area, rainfall, fertilizer, pesticide, year=2026):
    """Predict using the improved model with engineered features"""
    # Calculate derived features
    fertilizer_per_hectare = fertilizer / area if area > 0 else 0
    pesticide_per_hectare = pesticide / area if area > 0 else 0
    rainfall_per_area = rainfall / area if area > 0 else 0

    # Determine categorical bins
    if rainfall < 500:
        rainfall_category = 'Low'
    elif rainfall < 1500:
        rainfall_category = 'Medium'
    elif rainfall < 3000:
        rainfall_category = 'High'
    else:
        rainfall_category = 'Very_High'

    if area < 1000:
        area_category = 'Small'
    elif area < 10000:
        area_category = 'Medium'
    elif area < 100000:
        area_category = 'Large'
    else:
        area_category = 'Very_Large'

    # Create interaction features
    crop_season = f"{crop}_{season.strip()}"
    state_season = f"{state}_{season.strip()}"

    # Build input data
    input_data = {
        'Crop': crop,
        'Season': season.strip(),
        'State': state,
        'Area': area,
        'Annual_Rainfall': rainfall,
        'Fertilizer': fertilizer,
        'Pesticide': pesticide,
        'Year': year,
        'Year_Squared': year ** 2,
        'Fertilizer_per_hectare': fertilizer_per_hectare,
        'Pesticide_per_hectare': pesticide_per_hectare,
        'Rainfall_per_area': rainfall_per_area,
        'Rainfall_Category': rainfall_category,
        'Area_Category': area_category,
        'Crop_Season': crop_season,
        'State_Season': state_season
    }

    # Convert to DataFrame
    df_input = pd.DataFrame([input_data])

    # Encode categorical features
    categorical_cols = ['Crop', 'Season', 'State', 'Rainfall_Category',
                      'Area_Category', 'Crop_Season', 'State_Season']

    for col in categorical_cols:
        if col in label_encoders:
            try:
                df_input[col] = label_encoders[col].transform(df_input[col].astype(str))
            except ValueError:
                # Unknown category - use mode (most frequent)
                df_input[col] = 0

    # Ensure column order matches training
    df_input = df_input[feature_columns]

    # Predict
    prediction = model.predict(df_input)[0]
    return max(0, prediction)

def generate_recommendations(language, area, rainfall, fertilizer, pesticide):
    """Generate contextual recommendations"""
    recommendations = []

    fertilizer_per_hectare = fertilizer / area if area > 0 else 0
    pesticide_per_hectare = pesticide / area if area > 0 else 0

    # Determine area category
    if area < 1000:
        area_category = 'Small'
    elif area < 10000:
        area_category = 'Medium'
    elif area < 100000:
        area_category = 'Large'
    else:
        area_category = 'Very_Large'

    # Rainfall-based recommendations
    if rainfall < 500:
        recommendations.append(recommendations_dict["low_rain"][language])
    elif rainfall > 3000:
        recommendations.append(recommendations_dict["high_rain"][language])
    elif 1000 <= rainfall <= 2500:
        recommendations.append(recommendations_dict["rainfall_perfect"][language])

    # Fertilizer recommendations
    if fertilizer_per_hectare < 100:
        recommendations.append(recommendations_dict["low_fert"][language])
    elif fertilizer_per_hectare > 1000:
        recommendations.append(recommendations_dict["high_fert"][language])

    # Pesticide recommendations
    if pesticide_per_hectare > 50:
        recommendations.append(recommendations_dict["high_pest"][language])

    # Farm size recommendations
    if area_category == 'Small':
        recommendations.append(recommendations_dict["small_farm"][language])
    elif area_category == 'Very_Large':
        recommendations.append(recommendations_dict["large_farm"][language])

    # If no specific recommendations
    if not recommendations:
        recommendations.append(recommendations_dict["optimal"][language])

    return "\n\n".join(recommendations)

def predict_crop_yield(language, crop, season, state, area, rainfall, fertilizer, pesticide):
    """
    Predict crop yield using the improved model (or legacy as fallback).
    Returns: (predicted_yield, recommendations)
    """
    try:
        prediction = predict_with_improved_model(
            crop, season, state, area, rainfall, fertilizer, pesticide, year=2026
        )
        recommendations = generate_recommendations(language, area, rainfall, fertilizer, pesticide)
        return round(prediction, 4), recommendations

    except Exception as e:
        print(f"Model prediction error: {e}")
        # Simple heuristic fallback
        base_yield = 2.0
        rain_factor = min(rainfall / 1500, 2.0) if rainfall > 0 else 1.0
        fert_factor = min(fertilizer / (area * 200), 1.5) if area > 0 else 1.0

        fallback_prediction = base_yield * rain_factor * fert_factor
        return round(fallback_prediction, 4), recommendations_dict["optimal"][language]


# Keep backward compatibility
__all__ = ['predict_crop_yield']