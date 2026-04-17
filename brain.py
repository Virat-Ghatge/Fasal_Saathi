import joblib
import pandas as pd

# Load model once globally for efficiency
model = joblib.load("pred_model.pkl")
expected_features = model.get_booster().feature_names

def predict_crop_yield(language,crop, season, state, area, rainfall, fertilizer, pesticide):
    """
    Predict crop yield using user inputs from Gradio.
    """
    # Build input dictionary
    input_data = {
        'Crop': crop,
        'Season': season,
        'State': state,
        'Area': area,
        'Annual_Rainfall': rainfall,
        'Fertilizer': fertilizer,
        'Pesticide': pesticide
    }

    # Convert to DataFrame
    df = pd.DataFrame([input_data])

    # One-hot encode
    df_encoded = pd.get_dummies(df)

    # Add missing columns
    for col in expected_features:
        if col not in df_encoded:
            df_encoded[col] = 0

    # Reorder columns
    df_encoded = df_encoded[expected_features]

    # Predict
    prediction = model.predict(df_encoded)[0]
    # Calculate per unit area metrics
    fert_per_hectare = fertilizer / area if area else 0
    pest_per_hectare = pesticide / area if area else 0

    recommendations_dict = {
        "low_rain": {
            "English": "⚠️ Rainfall is low — consider increasing irrigation.",
            "Hindi": "⚠️ वर्षा कम है — सिंचाई बढ़ाने पर विचार करें।",
            "Odia": "⚠️ ବର୍ଷା କମ୍ — ସିଚାଇ ବୃଦ୍ଧି କରନ୍ତୁ।"
        },
        "high_rain": {
            "English": "💧 Excess rainfall — ensure proper drainage.",
            "Hindi": "💧 अत्यधिक वर्षा — उचित निकासी सुनिश्चित करें।",
            "Odia": "💧 ଅଧିକ ବର୍ଷା — ଠିକ ଭାବରେ ପାଣି ନିଷ୍କାଶନ କରନ୍ତୁ।"
        },
        "low_fert": {
            "English": "🌱 Fertilizer per hectare is low — consider soil enrichment.",
            "Hindi": "🌱 प्रति हेक्टेयर उर्वरक कम है — मिट्टी की उर्वरता बढ़ाने पर विचार करें।",
            "Odia": "🌱 ପ୍ରତି ହେକ୍ଟରରେ ସର କମ୍ — ମାଟି ସମୃଦ୍ଧି କରନ୍ତୁ।"
        },
        "high_fert": {
            "English": "🧪 Fertilizer per hectare is very high — check for nutrient overload.",
            "Hindi": "🧪 प्रति हेक्टेयर उर्वरक बहुत अधिक है — पोषक तत्वों की अधिकता की जांच करें।",
            "Odia": "🧪 ପ୍ରତି ହେକ୍ଟରରେ ସର ଅଧିକ — ପୋଷକତତ୍ୱ ଅଧିକ ହେବାକୁ ଯାଞ୍ଚ କରନ୍ତୁ।"
        },
        "high_pest": {
            "English": "🐞 High pesticide per hectare — monitor for resistance or overuse.",
            "Hindi": "🐞 प्रति हेक्टेयर कीटनाशक अधिक है — प्रतिरोध या अति-उपयोग पर नजर रखें।",
            "Odia": "🐞 ପ୍ରତି ହେକ୍ଟରରେ କୀଟନାଶକ ଅଧିକ — ପ୍ରତିରୋଧ କିମ୍ବା ଅଧିକ ବ୍ୟବହାର ପରୀକ୍ଷା କରନ୍ତୁ।"
        },
        "balanced": {
            "English": "✅ Inputs look balanced — maintain current practices.",
            "Hindi": "✅ इनपुट संतुलित हैं — वर्तमान प्रथाओं को बनाए रखें।",
            "Odia": "✅ ଇନପୁଟ୍ ସମତୁଳିତ — ବର୍ତ୍ତମାନ ପ୍ରକ୍ରିୟା ରଖନ୍ତୁ।"
        }
    }

    # Generate recommendations
       # Generate recommendations
    recommendations = []

    if rainfall < 500:
        recommendations.append(recommendations_dict["low_rain"][language])
    elif rainfall > 3000:
        recommendations.append(recommendations_dict["high_rain"][language])

    if fert_per_hectare < 100:
        recommendations.append(recommendations_dict["low_fert"][language])
    elif fert_per_hectare > 1000:
        recommendations.append(recommendations_dict["high_fert"][language])

    if pest_per_hectare > 50:
        recommendations.append(recommendations_dict["high_pest"][language])

    if not recommendations:
        recommendations.append(recommendations_dict["balanced"][language])

    return round(prediction, 4), "\n".join(recommendations)