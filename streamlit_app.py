import streamlit as st
import base64
from PIL import Image
import requests
from csv_db import get_value_from_csv
from chatbot_update import chat_ensemble

print("DEVELOPER NOTE: Page is running...")

# Access the OpenAI API key
api_key = st.secrets["api_key"]
openai_api_key = api_key

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def gpt4o_chatbot(base64_image):
    # Getting the base64 string
    # base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Translate this text into Tagalog."
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())

# Function to get base64 of the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to the logo image
logo_path = "logos.png"
logo_base64 = get_base64_of_bin_file(logo_path)

# Add CMA logo to top center and subtitle underneath
st.markdown(f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="CMA Logo" style="width: 200px; margin-bottom: 10px;">
        <h3 style="margin-top: 0;">Migrant Rights are Human Rights</h3>
    </div>
""", unsafe_allow_html=True)

# # <h1 style="margin-bottom: 5px;">Center for Migrant Advocacy<br>AI Assistant 🤖</h1>

# Function to display each Q&A
def display_q_and_a(question, answer):
    with st.expander(question):
        st.write(answer)
        # if st.button("Makipag-usap sa ___ 🤖", key=f"btn_{question}"):
        #     st.session_state.level = 4
        #     st.rerun()
    

# Define the buttons for each level
level1_buttons = ['Pre-Deployment', 'Sahod o Wages', 'Repatriation']
level2_buttons = {
    'Pre-Deployment': ['Paghahanap ng Trabaho at Ahensya', 'Mga Kontrata at Mga Kailangan', 'Sahod at Kompensasyon', 'Pagbabalik at Karagdagang Impormasyon', 'Oryentasyon at Sertipikasyon'],
    'Sahod o Wages': ['Pangkalahatang Impormasyon', 'Pag-aabuso at Pag-uulat', 'Kompensasyon at Mga Benepisyo', 'Migrant Workers Office (dating POLO)'],
    'Repatriation': ['Pagpapauwi at Pagfile ng mga Reklamo', 'Mga Proseso ng SENA', 'Money Claims o Mga hindi nabayarang sahod at mga danyos', 'Compulsory Insurance Coverage for Agency-Hired Migrant Workers', 'OWWA Programs and Services']
}

level3_buttons = {
    'Paghahanap ng Trabaho at Ahensya': [
        "Saan pwede maghanap ng trabaho sa Saudi Arabia?",
        "Paano malalaman kung legit ang recruitment agency?",
        "Ano ang PESO?",
        "Saan ang opisina ng OWWA?",
        "Saan ang opisina ng DMW?",
        "Saan ang opisina ng DFA?"
    ],
    'Mga Kontrata at Mga Kailangan': [
        "Gaano katagal ang kontrata sa Saudi Arabia?",
        "Ano ang mga requirements na kailangan na ipasa sa recruitment agency?",
        "Aling mga dokumento ang dapat isumite para sa pagproseso at dokumentasyon ng kontrata ng mga bagong hire?",
        "Aling mga dokumento ang dapat isumite para sa pagproseso at dokumentasyon ng kontrata ng mga bagong upahang kasambahay?"
    ],
    'Sahod at Kompensasyon': [
        "Magkano ang sahod ng domestic worker sa Saudi Arabia?",
        "Magkano ang sahod isang OFW sa Saudi Arabia?"
    ],
    'Pagbabalik at Karagdagang Impormasyon': [
        "Pwede ba bumalik kapag natapos ang kontrata?",
        "Saan ako maaaring pumunta para sa karagdagang impormasyon?"
    ],
    'Oryentasyon at Sertipikasyon': [
        "Ano ang PDOS?",
        "Kailangan mo ba ng gabay para makakuha ng Overseas Employment Certificate (OEC)?"
    ],
    'Pangkalahatang Impormasyon': [
        "Ano ang iqama?",
        "Ano ang PAOS?",
        "Ano ang ibig sabihin ng khadama?",
        "Ano ang ibig sabihin ng quit claim?",
        "Ano ang ibig sabihin ng SENA?"
    ],
    'Pag-aabuso at Pag-uulat': [
        "Inaabuso po ako ng amo ko, saan po pwedeng humingi ng tulong?",
        "Saan pwede magreport kung hindi binibigay ng amo ko ang sahod ko?",
        "Sarado na po ang agency ko sa pinas, sino po ang maaaring ireklamo?",
        "Undocumented po ako paano po ako makakahingi ng tulong?",
        "Hindi ko natapos ang kontrata ko sa aking employer dahil sa pang aabuso. ano ang gagawin?"
    ],
    'Kompensasyon at Mga Benepisyo': [
        "Sabi ng amo ko at agency dito, na dapat ko daw bayaran ang plane ticket ko, tama po ba ito?",
        "Sino ang magbabayad para sa aking airfare kung ako ay terminate?",
        "Hindi ako binibigyan ng pagkain ng amo ko, ang food allowance ba ay included sa kontrata?"
    ],
    'Migrant Workers Office (dating POLO)': [
        "Saan ang embassy at MWO/POLO?",
        "May immediate access ka ba sa pinakamalapit na embahada o konsulado ng Pilipinas?",
        "Kailangan mo ba ng contact information para sa mga opisina ng MWO?"
    ],
    'Pagpapauwi at Pagfile ng mga Reklamo': [
        "Nakauwi na po ako pinas, paano mag-file ng reklamo sa akin recruitment agency?"
    ],
    'Mga Proseso ng SENA': [
        "Ano ang SENA?",
        "Paano magfile ng complaint para sa SENA?",
        "Pwede ba magsama ng lawyer sa SENA?"
    ],
    'Money Claims o Mga hindi nabayarang sahod at mga danyos': [
        "Ano ang money claims?",
        "Saan ako pwede magfile ng money claims?",
        "Ano ang proseso sa pagfile ng money claims sa NLRC?",
        "Ano ang prescriptive period ng money claims?",
        "Ano ang joint and solidary liability?"
    ],
    'Compulsory Insurance Coverage for Agency-Hired Migrant Workers': [
        "Ano ang Compulsory Insurance Coverage for Agency-Hired Migrant Workers?",
        "Ano-ano ang mga benefits at coverages ng Agency-Hired OFW Compulsory Insurance?"
    ],
    'OWWA Programs and Services': [
        "Gusto mo bang malaman ang support services na ibinibigay ng OWWA?"
    ]
}
print("DEVELOPER NOTE: Initializing State")
if 'level' in st.session_state:
    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)
if 'step' not in st.session_state:
    st.session_state.step = 1
# Initialize session state
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.path = []
    st.session_state.responses = {}
    st.session_state.forward_query = ""

def go_back():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.path.pop()
        st.session_state.step = 1

def go_back():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.path.pop()
        st.session_state.step = 1

def back_to_beginning():
    st.session_state.level = 1
    st.session_state.path = []
    st.session_state.responses = {}
    st.session_state.forward_query = ""
    st.session_state.messages = []
    st.session_state.step = 1
    st.rerun()

# Custom CSS to make all buttons the same width and stack horizontally
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: auto;
        margin: 5px 0;
        white-space: normal;
    }
    .stButton > button:hover {
        background-color: #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

print("DEVELOPER NOTE: Main Page Successful")
# Display buttons based on the current level
if st.session_state.level == 1:
    st.write("**Magandandang Araw!**")
    st.write("Para sa mga kababayan nating OFW na may gustong malaman tungkol sa pagtratrabaho sa Saudi Arabia,  maaari lamang pumili sa mga sumusunod:")
    for button in level1_buttons:
        if st.button(button):
            st.session_state.path.append(button)
            st.session_state.level = 2
            st.rerun()

    print("DEVELOPER NOTE: Sub-Page Successful")

elif st.session_state.level == 2:
    print("DEVELOPER NOTE: Entering Session State Level 2")
    st.write("Para sa mga kababayan nating OFW na may gustong malaman tungkol sa pagtratrabaho sa Saudi Arabia,  maaari lamang pumili sa mga sumusunod:")
    main_topic = st.session_state.path[0]
    for button in level2_buttons[main_topic]:
        if st.button(button):
            if button == "Wala dito ang nais kong itanong.":
                st.session_state.level = 4
            else:
                st.session_state.path.append(button)
                st.session_state.level = 3
            st.rerun()
    print("DEVELOPER NOTE: Exiting Session State Level 2")
    if st.button("Back"):
        go_back()
        st.rerun()

elif st.session_state.level == 3 and st.session_state.step in [1, 8, 9, 10, 11, 12, 13, 20]:
    print("DEVELOPER NOTE: Entering Session State 3")
    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)
    st.write("**Ako ang CMA AI Assistant na nagbibigay ng mga impormasyon na makakatulong sa mga Overseas Filipino Workers at kanilang mga pamilya.**")
    st.write("**DAPAT TANDAAN:** Sa usaping legal, ang bawat reklamo o kaso ay may pagkakaiba kaya mas mainam na komunsulta sa isang abogado. Ang impormasyon na maibibigay ko ay pangkalahatan lamang at para sa mga iba pa pang katanungan narito din ako para i-konek ka sa CMA caseworker.")
    main_topic = st.session_state.path[0]
    sub_topic = st.session_state.path[1]
    qa_list = level3_buttons[sub_topic]
    print("The main_topic is:", main_topic)
    print("The sub_topic is:", sub_topic)
    print("The qa_list is:", qa_list)
    for qa in qa_list:
        csv_answer = get_value_from_csv(main_topic, sub_topic, qa)
        display_q_and_a(qa, csv_answer)
    
    with st.expander("Wala dito ang nais kong itanong."):
        if st.button("Makipag-usap sa ___ 🤖", key=f"btn_{sub_topic}"):
            st.session_state.level = 4
            st.rerun()

    back, balik_sa_simula = st.columns(2)
    if back.button("⬅️ Back", key="back"):
        go_back()
        st.rerun()
    if balik_sa_simula.button("↪️ Balik sa Simula", key="balik_sa_simula"):
        back_to_beginning()
        st.rerun()

    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)
    
elif st.session_state.level == 4:
    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)
    st.write("**Ako ang CMA AI Assistant  na nagbibigay ng mga impormasyon na makakatulong sa mga Overseas Filipino Workers at kanilang mga pamilya.**")
    st.write("**DAPAT TANDAAN:** Sa usaping legal, ang bawat reklamo o kaso ay may pagkakaiba kaya mas mainam na komunsulta sa isang abogado. Ang impormasyon na maibibigay ko ay pangkalahatan lamang at para sa mga iba pa pang katanungan narito din ako para i-konek ka sa CMA caseworker.")
    
    main_topic = st.session_state.path[0]
    sub_topic = st.session_state.path[1]
    chat_ensemble(main_topic, sub_topic)

    back, balik_sa_simula = st.columns(2)
    if back.button("⬅️ Back", key="back"):
        back_to_beginning()
        st.rerun()
    if balik_sa_simula.button("↪️ Balik sa Simula", key="balik_sa_simula"):
        back_to_beginning()
        st.rerun()

# Contract Upload Feature to be tested by CMA Only 
elif st.session_state.level == 6: 
    # Title of the app
    st.title("Contract Upload")
    st.write("Mag-upload ng larawan ng iyong kontrata dito:")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.read()

        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Malaki!")

    if st.button("Back"):
        go_back()
        st.rerun()
        
    if st.button("Balik sa Simula"):
        back_to_beginning()
        st.rerun()


### Sidebar

with st.sidebar:
    st.header("Hello! 👋 Ako si ___ ang inyong friendly AI Assistant 🤖.")
    st.caption("Tumutulong ako sa mga Overseas Filipino Workers sa pamamagitan nang pagbigay ng mga kasagutan sa mgatanong tungkol sa pre-deployment, onsite, at repatriation.")
    st.caption("Narito ako upang gabayan ka!")

    # st.divider()

    with st.expander("Sino si CMA?"):
        st.caption("*Ang Center for Migrant Advocacy - Philippines* ay isang advocacy group na nagtataguyod ng mga karapatan ng mga overseas Filipinos, land or sea-based migrant workers, Filipino immigrants at kanilang mga pamilya. Tumutulong ang center na mapabuti ang kalagayang pang-ekonomiya, panlipunan at pampulitika ng mga OFWs at kanilang mga pamilya sa pamamagitan ng policy research and advocacy, capacity-building, networking/partnerships, at direct assistance/case assistance.")

    with st.expander("Bakit mahalaga ang AI Assistant na ito?"):
        st.caption("Ang AI assistance na ito ay idinisenyo para idulog ang mga isyu at mapalakas ang kakayahan ng mga manggagawa na ipaglaban ang kanilang mga karapatan. Sa pamamagitan ng mga sumusunod: ")
        st.caption("*Legal Information and Guidance:* Nagbibigay ng madaling maintindihang impormasyon tungkol sa karapatang legal at proseso.")
        st.caption("*24/7 Availability:*  Madali ma-access at mabilis na nakakapagbigay ng mahalagang impormasyon anumang oras.")
        st.caption("*Pagkonekta sa Tamang Ahensya ng Gobyerno:* Nagbibigay gabay kung saang ahensya ng gobyerno dapat idulog ang problema ng isang OFW.")

    with st.expander("Privacy Disclaimer"):
        st.caption("Ang AI Assistant na ito ay naglalayong magbigay ng mahalagang impormasyon tungkol sa iyong mga issues o problema sa pagtratrabaho sa ibang bansa at hindi para kumukolekta ng iyong personal na impormasyon. Ginagamit namin ang impormasyong ito upang maunawaan ang iba't ibang sitwasyon ng mga OFW at kanilang mga pamilya at kung paano sumangguni sa gobyerno o iba pang NGO tungkol sa iyong sitwasyon o problema. Maaari ka ring makipag-usap sa aming case manager pagkatapos gamitin ang AI Assistant na ito.")


    url = "https://www.facebook.com/centerformigrantadvocacyph/"
    html_content = f'<p style="text-align:center; font-size:12px;">For all other inquiries, please contact us M-F between 9-5pm (Manila) on <a href="{url}" target="_blank">Facebook</a></p>'
    st.markdown(html_content, unsafe_allow_html=True)
