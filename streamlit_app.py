import streamlit as st
import base64
from PIL import Image
import requests
from chatbot import custom_chatbot_intro, wala_custom_chatbot_intro

print("DEVELOPER NOTE: Sprinkle 00")

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

# Define the buttons for each level
level1_buttons = ['Pre-Deployment', 'Sahod o Wages', 'Repatriation']
level2_buttons = {
    'Pre-Deployment': ['Paghahanap ng Trabaho at Ahensya', 'Mga Kontrata at Mga Kailangan', 'Sahod at Kompensasyon', 'Pagbabalik at Karagdagang Impormasyon', 'Oriyantrasyon at Sertipikasyon', 'Wala dito ang tanong ko.'],
    'Sahod o Wages': ['Pangkalahatang Impormasyon', 'Pag-aabuso at Pag-uulat', 'Kompensasyon at Mga Benepisyo', 'Embassy at Tulong', 'Wala dito ang tanong ko.'],
    'Repatriation': ['Pagpapauwi at Mga Reklamo', 'Mga Proseso ng SENA', 'Money Claims', 'Saklaw ng Seguro', 'Embassy at Tulong', 'Serbisyo at Membership ng OWWA', 'Wala dito ang tanong ko.']
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
    'Oriyantrasyon at Sertipikasyon': [
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
        "Undocumented po ako paano po ako makakahingi ng tulong?"
    ],
    'Kompensasyon at Mga Benepisyo': [
        "Sabi ng amo ko at agency dito, na dapat ko daw bayaran ang plane ticket ko, tama po ba ito?",
        "Sino ang magbabayad para sa aking airfare kung ako ay terminate?",
        "Hindi ako binibigyan ng pagkain ng amo ko, ang food allowance ba ay included sa kontrata?"
    ],
    'Embassy at Tulong': [
        "Saan ang embassy at MWO/POLO?",
        "May immediate access ka ba sa pinakamalapit na embahada o konsulado ng Pilipinas?",
        "Kailangan mo ba ng contact information para sa mga opisina ng MWO?"
    ],
    'Pagpapauwi at Mga Reklamo': [
        "Nakauwi na po ako pinas, paano mag-file ng reklamo sa akin recruitment agency?"
    ],
    'Mga Proseso ng SENA': [
        "Ano ang SENA?",
        "Ano ang mga kailangan dalhin sa SENA?",
        "Pwede ba magsama ng lawyer sa SENA?"
    ],
    'Money Claims': [
        "Ano ang money claims?",
        "Saan ako pwede magfile ng money claims?",
        "Hindi ko natapos ang kontrata ko sa aking employer dahil sa pang aabuso. ano ang gagawin?",
        "Ano ang proseso sa pagfile ng money claims sa NLRC?",
        "Ano ang prescriptive period ng money claims?",
        "Ano ang joint and solidary liability?"
    ],
    'Saklaw ng Seguro': [
        "Ano ang Compulsory Insurance Coverage for Agency-Hired Migrant Workers?",
        "Sino ang sakop ng Agency-Hired OFW Compulsory Insurance?",
        "Ano-ano ang mga benefits at coverages ng Agency-Hired OFW Compulsory Insurance?"
    ],
    'Serbisyo at Membership ng OWWA': [
        "Gusto mo bang malaman ang support services na ibinibigay ng OWWA?",
        "Ikaw ba ay isang active OWWA member?"
    ]
}
print("DEVELOPER NOTE: Sprinkle 0")
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

print("DEVELOPER NOTE: Sprinkle 1")
# Display buttons based on the current level
if st.session_state.level == 1:
    st.write("Para sa mga kababayan nating OFW na pupunta sa Saudi Arabia at gustong malaman ang tungkol sa pre-departure, deployment, at repatriation, nandito ang serbisyong ito para tulungan kayo!")
    # st.header("Pumili ng pangunahing paksa:")
    for button in level1_buttons:
        if st.button(button):
            if button == "Wala dito ang tanong ko.":
                st.session_state.level = 5
            else:
                st.session_state.path.append(button)
                st.session_state.level = 2
            st.rerun()

    print("DEVELOPER NOTE: Sprinkle 2")

elif st.session_state.level == 2:
    print("DEVELOPER NOTE: Sprinkle 2.5")
    st.write("Para sa mga kababayan nating OFW na pupunta sa Saudi Arabia at gustong malaman ang tungkol sa pre-departure, deployment, at repatriation, nandito ang serbisyong ito para tulungan kayo!")
    main_topic = st.session_state.path[0]
    for button in level2_buttons[main_topic]:
        if st.button(button):
            if button == "Wala dito ang tanong ko.":
                st.session_state.level = 5
            elif button == "Kailangan mo ba ng tulong sa pagsasalin ng iyong kontrata sa Tagalog?":
                st.session_state.level = 6
            elif button == "Ano ang mga medical tests?":
                st.session_state.level = 7
            else:
                st.session_state.path.append(button)
                st.session_state.level = 3
            st.rerun()
    print("DEVELOPER NOTE: Sprinkle 3")
    if st.button("Back"):
        go_back()

    print("The session state is:", st.session_state.level)
    print("DEVELOPER NOTE: Sprinkle 3.5")

    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)

elif st.session_state.level == 3 and st.session_state.step in [1, 8, 9, 10, 11, 12, 13]:
    print("DEVELOPER NOTE: Inside ensemble session state step")
    st.write("Ang CMA AI Assistant ay nagbibigay ng impormasyon, suporta, at mga mapagkukunan para sa mga Overseas Filipino Workers at kanilang mga pamilya. Gayunpaman, limitado ang aking mga serbisyo sa di-agarang gabay at pangkalahatang impormasyon legal. Hindi ako nagbibigay ng direktang legal na representasyon o interbensyon sa mga emerhensya.")
    main_topic = st.session_state.path[0]
    sub_topic = st.session_state.path[1]
    custom_chatbot_intro(sub_topic, level3_buttons)

    back, balik_sa_simula = st.columns(2)
    if back.button("⬅️ Back", key="back"):
        go_back()
        st.rerun()
    if balik_sa_simula.button("↪️ Balik sa Simula", key="balik_sa_simula"):
        back_to_beginning()
        st.rerun()

    print("The session state level is:", st.session_state.level)
    print("The session state step is:", st.session_state.step)
    
elif st.session_state.level == 5:
    st.write("Ang CMA AI Assistant ay nagbibigay ng impormasyon, suporta, at mga mapagkukunan para sa mga Overseas Filipino Workers at kanilang mga pamilya. Gayunpaman, limitado ang aking mga serbisyo sa di-agarang gabay at pangkalahatang impormasyon legal. Hindi ako nagbibigay ng direktang legal na representasyon o interbensyon sa mga emerhensya.")
    main_topic = st.session_state.path[0]
    wala_custom_chatbot_intro(main_topic)

    if st.button("Back"):
        go_back()
        st.rerun()
        
    if st.button("Balik sa Simula"):
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
    st.header("Hello! 👋 Ako si ang inyong friendly AI Assistant 🤖.")
    st.caption("Tumutulong ako sa mga overseas Filipino worker sa mga tanong tungkol sa pre-deployment, legal na karapatan, at repatriation. Kung kailangan mo ng impormasyon o tulong, narito ako para magbigay ng tumpak na impormasyon at suporta. Sabik akong tulungan ka!")
    # st.divider()

    with st.expander("Sino si CMA?"):
        st.caption("Ang Center for Migrant Advocacy – Philippines ay isang advocacy group na nagtataguyod ng mga karapatan ng mga overseas Filipinos, land or sea-based migrant workers, Filipino immigrants at kanilang mga pamilya. Tumutulong ang center na mapabuti ang kalagayang pang-ekonomiya, panlipunan at pampulitika ng mga migranteng pamilyang Pilipino saanman sa pamamagitan ng pagtataguyod ng patakaran, pagpapakalat ng impormasyon, networking, pagbuo ng kakayahan at direktang tulong.")

    with st.expander("Bakit mahalaga ang AI Assistant na ito?"):
        st.caption("Ang Center for Migrant Advocacy ay nag-aanyaya sa pakikipagtulungan at puna upang pinuhin at i-optimize ang solusyon na ito, na tinitiyak na epektibong natutugunan nito ang magkakaibang pangangailangan ng mga OFW. Ang session na ito ay naglalayon na mangalap ng mahalagang feedback mula sa dati at kasalukuyang mga OFW upang pinuhin ang disenyo at functionality ng AI assistant. Napakahalaga ng ganitong mga pananaw habang nagsisikap ang CMA na magkaroon ng makabuluhang epekto sa buhay ng mga OFW sa pamamagitan ng makabagong teknolohiya. Inaasahan namin ang iyong pakikilahok at mga kontribusyon habang tinutuklasan namin ang mga posibilidad ng pagbabagong inisyatiba na ito.")

    with st.expander("Privacy Disclaimer"):
        st.caption("Ang AI Assistant na ito ay naglalayong magbigay ng makatotohanang impormasyon tungkol sa iyong sitwasyon at hindi pa kumukolekta ng iyong personal na impormasyon. Ginagamit namin ang impormasyong ito upang maunawaan ang iba't ibang sitwasyon ng mga OFW at kanilang mga pamilya at kung paano sumangguni sa gobyerno o iba pang NGO tungkol sa iyong sitwasyon o problema. Maaari kang makipag-usap sa isang case manager pagkatapos gamitin ang AI Assistant na ito.")

    st.caption('<p style="text-align:center">For other inquiries, please email us at: cma@cmaphils.net </p>', unsafe_allow_html=True)
