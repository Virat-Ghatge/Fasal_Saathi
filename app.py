import gradio as gr
from brain import predict_crop_yield
from weather import (
    get_current_weather, get_forecast, get_annual_rainfall_estimate,
    format_weather_for_display, format_forecast_for_display, check_api_keys
)

# Crop list
crops = [
    "Arecanut",
    "Arhar/Tur",
    "Bajra",
    "Banana",
    "Barley",
    "Black pepper",
    "Cardamom",
    "Cashewnut",
    "Castor seed",
    "Coconut",
    "Coriander",
    "Cotton(lint)",
    "Cowpea(Lobia)",
    "Dry chillies",
    "Garlic",
    "Ginger",
    "Gram",
    "Groundnut",
    "Guar seed",
    "Horse-gram",
    "Jowar",
    "Jute",
    "Khesari",
    "Linseed",
    "Maize",
    "Masoor",
    "Mesta",
    "Moong(Green Gram)",
    "Moth",
    "Niger seed",
    "Oilseeds total",
    "Onion",
    "Other Cereals",
    "Other Kharif pulses",
    "Other Rabi pulses",
    "Other Summer Pulses",
    "other oilseeds",
    "Peas & beans (Pulses)",
    "Potato",
    "Ragi",
    "Rapeseed &Mustard",
    "Rice",
    "Safflower",
    "Sannhamp",
    "Sesamum",
    "Small millets",
    "Soyabean",
    "Sugarcane",
    "Sunflower",
    "Sweet potato",
    "Tapioca",
    "Tobacco",
    "Turmeric",
    "Urad",
    "Wheat"
]
cropsHindi = [
    "सुपारी",
    "अरहर/तूर",
    "बाजरा",
    "केला",
    "जौ",
    "काली मिर्च",
    "इलायची",
    "काजू",
    "अरंडी का बीज",
    "नारियल",
    "धनिया",
    "कपास (रुई)",
    "लोबिया",
    "सूखी मिर्च",
    "लहसुन",
    "अदरक",
    "चना",
    "मूंगफली",
    "ग्वार बीज",
    "कुल्थी",
    "ज्वार",
    "जूट",
    "खेसारी",
    "अलसी",
    "मक्का",
    "मसूर",
    "मेस्ता",
    "मूंग (हरा चना)",
    "मटकी",
    "नiger बीज",
    "कुल तिलहन",
    "प्याज़",
    "अन्य अनाज",
    "अन्य खरीफ दालें",
    "अन्य रबी दालें",
    "अन्य ग्रीष्म दालें",
    "अन्य तिलहन",
    "मटर और सेम (दालें)",
    "आलू",
    "रागी",
    "सरसों व रेपसीड",
    "धान",
    "कुसुम",
    "सन",
    "तिल",
    "लघु अनाज",
    "सोयाबीन",
    "गन्ना",
    "सूरजमुखी",
    "शकरकंद",
    "कसावा (टैपिओका)",
    "तंबाकू",
    "हल्दी",
    "उड़द",
    "गेहूं"
]

# State list
states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Puducherry",
    "Punjab",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]
statesHindi = [
    "आंध्र प्रदेश",
    "अरुणाचल प्रदेश",
    "असम",
    "बिहार",
    "छत्तीसगढ़",
    "दिल्ली",
    "गोवा",
    "गुजरात",
    "हरियाणा",
    "हिमाचल प्रदेश",
    "जम्मू और कश्मीर",
    "झारखंड",
    "कर्नाटक",
    "केरल",
    "मध्य प्रदेश",
    "महाराष्ट्र",
    "मणिपुर",
    "मेघालय",
    "मिजोरम",
    "नगालैंड",
    "ओडिशा",
    "पुदुचेरी",
    "पंजाब",
    "सिक्किम",
    "तमिलनाडु",
    "तेलंगाना",
    "त्रिपुरा",
    "उत्तर प्रदेश",
    "उत्तराखंड",
    "पश्चिम बंगाल"
]

# Season list
seasons = [
 "Kharif",
 "Rabi",
 
 "Summer",
 "Autumn",
 "Winter",
 
 "Whole Year"
 ]
seasonsHindi = [
    "खरीफ",
    "रबी",
    
    "गर्मी",
    "पतझड़",
    "सर्दी",

    "पूरा वर्ष"
]


cropsOdi = [
    "ଗୁଆ",
    "ଆରହର",
    "ବାଜରା",
    "କଦଳୀ",
    "ଜୌ",
    "କଳା ଗୋଲମରିଚ",
    "ଏଲାଚୀ",
    "କାଜୁ",
    "ରେଣୁ",
    "ନଡିଆ",
    "ଧନିଆ",
    "କପାସ",
    "ବିଲାତି ବିଚି",
    "ଶୁଖିଲା ଲଙ୍କା",
    "ରସୁଣ",
    "ଅଦା",
    "ଚଣା",
    "ବାଦାମ",
    "ଗୁଆର ବିଆ",
    "କୁଳଥି",
    "ଜୁଆର",
    "ପଟ",
    "ଖେସାରି",
    "ଆଳସି",
    "ମକା",
    "ମସୁର",
    "ମେଷ୍ଟା",
    "ମୁଗ",
    "ମଟି",
    "ଖାଦିଆ",
    "ତେଲବିଆ ସମୁଦାୟ",
    "ପିଆଜ",
    "ଅନ୍ୟାନ୍ୟ ଧାନ୍ୟ",
    "ଅନ୍ୟାନ୍ୟ ଖରିଫ ଡାଲି",
    "ଅନ୍ୟାନ୍ୟ ରବି ଡାଲି",
    "ଅନ୍ୟାନ୍ୟ ଗ୍ରୀଷ୍ମ ଡାଲି",
    "ଅନ୍ୟାନ୍ୟ ତେଲବିଆ",
    "ମଟର ଓ ବିନ୍ସ",
    "ଆଳୁ",
    "ମାଣ୍ଡିଆ",
    "ତିଳି/ସରସପ",
    "ଧାନ",
    "କୁସୁମ",
    "ସନ",
    "ତିଳ",
    "ଛୋଟ ଧାନ୍ୟ",
    "ସୋୟାବିନ",
    "ଅଖୁ",
    "ସୁର୍ଯ୍ୟମୁଖୀ",
    "ଗାଣ୍ଠିଆଳୁ",
    "କାସା",
    "ଧୂମ୍ରପତ୍ର",
    "ହଳଦି",
    "ବିରି",
    "ଗହମ"
]


statesOdi = [
    "ଆନ୍ଧ୍ର ପ୍ରଦେଶ",
    "ଅରୁଣାଚଳ ପ୍ରଦେଶ",
    "ଆସାମ",
    "ବିହାର",
    "ଛତିଶଗଡ଼",
    "ଦିଲ୍ଲୀ",
    "ଗୋଆ",
    "ଗୁଜରାଟ",
    "ହରିୟାଣା",
    "ହିମାଚଳ ପ୍ରଦେଶ",
    "ଜମ୍ମୁ କାଶ୍ମୀର",
    "ଝାରଖଣ୍ଡ",
    "କର୍ଣ୍ଣାଟକ",
    "କେରଳ",
    "ମଧ୍ୟ ପ୍ରଦେଶ",
    "ମହାରାଷ୍ଟ୍ର",
    "ମଣିପୁର",
    "ମେଘାଳୟ",
    "ମିଜୋରାମ",
    "ନାଗାଲ୍ୟାଣ୍ଡ",
    "ଓଡ଼ିଶା",
    "ପୁଡୁଚେରୀ",
    "ପଞ୍ଜାବ",
    "ସିକିମ",
    "ତାମିଳନାଡୁ",
    "ତେଲଙ୍ଗାନା",
    "ତ୍ରିପୁରା",
    "ଉତ୍ତର ପ୍ରଦେଶ",
    "ଉତ୍ତରାଖଣ୍ଡ",
    "ପଶ୍ଚିମ ବଙ୍ଗ"
]


seasonsOdi = [
 "ଖରିଫ",
 "ରବି",
 "ଗ୍ରୀଷ୍ମ",
 "ଶରତ",
 "ଶୀତ",
 "ସାରା ବର୍ଷ"
]


custom_css = """
body, .dark, .dark * {
    background-color: #19282F !important; /* Background */
}
.gradio-container{
background-color: #D3ECA7 !important; /* Background */
}
button {
    background-color: #CFFFE2 !important; /* Buttons */
    color: black !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
}
button:hover {
    background-color: #A1B57D !important; /* Darker on hover */
    color: white !important;
}
footer, .svelte-1ipelgc, .svelte-1rjryrr {
    display: none !important;
    visibility: hidden !important;
}
#mybox {
    background-color: #747c24 !important;
    border-radius: 10px;
    padding: 50px;
}
input[type="radio"] {
    transform: scale(1.5);
    margin: 8px;
"""

# Language switch logic
def update_fields(language):
    if language == "English":
        return (
            gr.update(choices=crops, label="Crop", interactive=True),
            gr.update(choices=seasons, label="Season", interactive=True),
            gr.update(choices=states, label="State", interactive=True),
            gr.update(label="Area (in hectares)"),#, placeholder="Enter area"),
            gr.update(label="Annual Rainfall (mm)"),#, placeholder="Enter rainfall"),
            gr.update(label="Fertilizer Usage (kg)"),#, placeholder="Enter fertilizer usage"),
            gr.update(label="Pesticide Usage (kg)"),#, placeholder="Enter pesticide usage"),
            gr.update(value="Predict Yield"),
            gr.update(label="Predicted Yield (t/ha)"),
            gr.update(value="", label="Recommendations", lines=6)
        )

    elif language == "Hindi":
        return (
            gr.update(choices=cropsHindi, label="फसल", interactive=True),
            gr.update(choices=seasonsHindi, label="मौसम", interactive=True),
            gr.update(choices=statesHindi, label="राज्य", interactive=True),
            gr.update(label="क्षेत्रफल (हेक्टेयर में)"),#, placeholder="क्षेत्रफल दर्ज करें"),
            gr.update(label="वार्षिक वर्षा (मिमी)"),#, placeholder="वर्षा दर्ज करें"),
            gr.update(label="उर्वरक उपयोग (किग्रा)"),#, placeholder="उर्वरक दर्ज करें"),
            gr.update(label="कीटनाशक उपयोग (किग्रा)"),#, placeholder="कीटनाशक दर्ज करें"),
            gr.update(value="उपज की भविष्यवाणी करें"),
            gr.update(label="अनुमानित उपज"),
            gr.update(value="", label="अनुशंसाएँ", lines=6)
        )

    elif language == "Odia":
        return (
            gr.update(choices=cropsOdi, label="ଫସଳ", interactive=True),
            gr.update(choices=seasonsOdi, label="ଋତୁ", interactive=True),
            gr.update(choices=statesOdi, label="ରାଜ୍ୟ", interactive=True),
            gr.update(label="କ୍ଷେତ୍ରଫଳ (ହେକ୍ଟରରେ)"),#, placeholder="କ୍ଷେତ୍ରଫଳ ଲେଖନ୍ତୁ"),
            gr.update(label="ବାର୍ଷିକ ବର୍ଷା (ମି.ମି.)"),#, placeholder="ବର୍ଷାର ପରିମାଣ ଲେଖନ୍ତୁ"),
            gr.update(label="ସର ବ୍ୟବହାର (କି.ଗ୍ରା.)"),#, placeholder="ସର ବ୍ୟବହାର ଲେଖନ୍ତୁ"),
            gr.update(label="କୀଟନାଶକ ବ୍ୟବହାର (କି.ଗ୍ରା.)"),#, placeholder="କୀଟନାଶକ ବ୍ୟବହାର ଲେଖନ୍ତୁ"),
            gr.update(value="ଉତ୍ପାଦନ ପୂର୍ବାନୁମାନ କରନ୍ତୁ"),
            gr.update(label="ଅନୁମାନିତ ଉତ୍ପାଦନ"),
            gr.update(value="", label="ସୁପାରିସ", lines=6)
        )


# Weather-related functions
def fetch_weather_data(state):
    """Fetch weather data when state is selected"""
    if not state:
        return "Select a state to see weather", "No forecast available", None

    # Get current weather
    current = get_current_weather(state)
    weather_text = format_weather_for_display(current) if current else "Weather API not configured. Please add API key to .env file"

    # Get forecast
    forecast = get_forecast(state, days=7)
    forecast_text = format_forecast_for_display(forecast) if forecast else "Forecast unavailable"

    # Get estimated annual rainfall
    annual_rainfall = get_annual_rainfall_estimate(state)

    return weather_text, forecast_text, annual_rainfall

def update_rainfall_with_weather(state, current_rainfall):
    """Update rainfall input with estimated annual rainfall"""
    if not state:
        return current_rainfall

    estimated = get_annual_rainfall_estimate(state)
    return estimated


with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🌾 Fasal Saathi - Crop Yield Prediction")
    gr.Markdown("### AI-powered crop yield prediction and recommendations for Indian farmers")

    with gr.Column(elem_id="mybox"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🌐 Select Language")
                language = gr.Radio(choices=["English", "Hindi", "Odia"], label="", value="English")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🌱 Crop Information")
                crop = gr.Dropdown(choices=crops, label="Crop")
                season = gr.Radio(choices=seasons, label="Season")

            with gr.Column(scale=1):
                gr.Markdown("### 📍 Location")
                state = gr.Dropdown(choices=states, label="State")

                # Weather display
                gr.Markdown("### 🌤️ Weather Information")
                weather_info = gr.Textbox(label="Current Weather", lines=4, interactive=False)
                fetch_weather_btn = gr.Button("🔄 Fetch Weather Data", size="sm")

            with gr.Column(scale=1):
                gr.Markdown("### 📊 Farm Details")
                area = gr.Number(label="Area (in hectares)", value=None, minimum=0.1)

                gr.Markdown("### 🌧️ Input Usage")
                rainfall = gr.Number(label="Annual Rainfall (mm)", value=None, minimum=0)
                auto_rainfall_btn = gr.Button("📍 Auto-fill from State", size="sm")
                fertilizer = gr.Number(label="Fertilizer Usage (kg)", value=None, minimum=0)
                pesticide = gr.Number(label="Pesticide Usage (kg)", value=None, minimum=0)

        # Weather forecast section
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📅 7-Day Weather Forecast")
                forecast_info = gr.Textbox(label="Forecast", lines=10, interactive=False)

        submit = gr.Button("🔮 Predict Yield", size="lg")

        with gr.Row():
            with gr.Column(scale=1):
                output = gr.Number(label="Predicted Yield (t/ha)", interactive=False)
            with gr.Column(scale=2):
                advice = gr.Textbox(label="💡 Recommendations", lines=8, interactive=False)

    language.change(
        fn=update_fields,
        inputs=language,
        outputs=[crop, season, state, area, rainfall, fertilizer, pesticide, submit, output, advice],
    )

    # Weather data fetching
    state.change(
        fn=fetch_weather_data,
        inputs=state,
        outputs=[weather_info, forecast_info, rainfall]
    )

    fetch_weather_btn.click(
        fn=fetch_weather_data,
        inputs=state,
        outputs=[weather_info, forecast_info, rainfall]
    )

    auto_rainfall_btn.click(
        fn=update_rainfall_with_weather,
        inputs=[state, rainfall],
        outputs=rainfall
    )

    submit.click(
        fn=predict_crop_yield,
        inputs=[language, crop, season, state, area, rainfall, fertilizer, pesticide],
        outputs=[output, advice]
    )

demo.launch(debug=True, server_port=8888)
