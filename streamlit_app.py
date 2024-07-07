import streamlit as st
import base64
from PIL import Image
# from chatbot import *

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

st.write("Para sa mga kababayan nating OFW na pupunta sa Saudi Arabia at gustong malaman ang tungkol sa pre-departure, deployment, at repatriation, nandito ang serbisyong ito para tulungan kayo!")

# Define button sets for each level
level1_buttons = ['Pre-Deployment', 'Wages', 'Repatriation', 'Contract']
level2_buttons = {
    'Pre-Deployment': ['Ano ang mga kinakailangang dokumento?', 'Paano ako makakadalo sa PDOS?', 'Ano ang mga medical tests?', 'May specific na training programs ba?', 'Wala dito ang tanong ko.'],
    'Wages': ['Paano masisiguro ang tamang sahod?', 'Ano ang gagawin kung huli ang bayad?', 'Paano i-report ang discrepancies?', 'May legal protections ba para sa wage theft?', 'Wala dito ang tanong ko.'],
    'Repatriation': ['Ano ang mga hakbang para sa mabilis na pag-uwi?', 'Sino ang pwedeng kontakin?', 'Anong financial assistance ang available?', 'Paano iayos ang pagpapadala ng gamit?', 'Wala dito ang tanong ko.'],
    'Contract': ['Ano ang dapat tingnan sa kontrata?', 'Paano masisiguro kung legal ang kontrata?', 'Ano ang gagawin kung may bagong kontrata?', 'Paano makakuha ng legal advice?', 'Kailangan mo ba ng tulong sa pagsasalin ng iyong kontrata sa Tagalog?', 'Wala dito ang tanong ko.']
}
level3_buttons = {
    'Ano ang mga kinakailangang dokumento?': [
        'Mayroon ka na bang valid na passport, o kailangan mo ng tulong sa pag-aapply?',
        'Kailangan mo ba ng gabay para makakuha ng Overseas Employment Certificate (OEC)?',
        'Alam mo ba ang mga specific na visa requirements para sa bansang pupuntahan mo?',
        'Kailangan mo ba ng tulong para ma-verify ang kontrata mo sa POEA?'
    ],
    'Paano ako makakadalo sa PDOS?': [
        'Alam mo ba ang proseso ng pagpaparehistro para sa PDOS, o kailangan mo ng detalyadong hakbang?',
        'Gusto mo bang malaman ang pinakamalapit na lokasyon ng PDOS seminar?',
        'Kailangan mo ba ng tulong sa mga dokumentong kailangan para makadalo sa PDOS?',
        'Interesado ka ba sa online PDOS dahil sa lokasyon mo?'
    ],
    'Ano ang mga medical tests?': [
        'May nahanap ka na bang sertipikadong klinika para sa mga tests, o kailangan mo ng rekomendasyon?',
        'Kailangan mo ba ng detalyadong listahan ng mga medical tests na kailangan para sa trabaho mo?',
        'Mayroon ka bang partikular na health concerns na gusto mong pag-usapan bago magpatest?',
        'Gusto mo bang malaman ang mga gastos na kasama sa medical tests?'
    ],
    'May specific na training programs ba?': [
        'Anong uri ng trabaho ang pupuntahan mo, at kailangan mo ba ng specific skill training para dito?',
        'Kailangan mo ba ng language training para sa bansang pupuntahan mo?',
        'Gusto mo bang malaman kung saan makakahanap ng cultural orientation programs?',
        'Interesado ka ba sa safety at security training na kaugnay sa trabaho mo?'
    ],
    'Paano masisiguro ang tamang sahod?': [
        'Kailangan mo ba ng tulong sa pag-unawa sa mga detalye ng sahod sa kontrata mo?',
        'Kailangan mo ba ng payo kung paano itago ang mga natatanggap mong sahod?',
        'May mga discrepancies ba sa inaasahan at natatanggap mong sahod?',
        'Gusto mo bang malaman ang mga hakbang kung sa tingin mo ay ninanakawan ka ng sahod?'
    ],
    'Ano ang gagawin kung huli ang bayad?': [
        'Sinubukan mo na bang pag-usapan ito nang direkta sa employer mo?',
        'Alam mo ba ang local labor laws tungkol sa tamang pagbabayad ng sahod?',
        'Kailangan mo ba ng tulong sa pag-dokumento ng mga na-delay na bayad?',
        'Gusto mo bang malaman kung paano i-escalate ang isyu sa POLO o embahada?'
    ],
    'Paano i-report ang discrepancies?': [
        'Nakalap mo na ba ang lahat ng kinakailangang ebidensya tulad ng pay slips at kontrata?',
        'Alam mo ba ang proseso ng pag-report sa POLO at embahada?',
        'Kailangan mo ba ng gabay sa paggamit ng online platforms para mag-file ng reklamo?',
        'Naghahanap ka ba ng mga local organizations na pwedeng tumulong sa kaso mo?'
    ],
    'May legal protections ba para sa wage theft?': [
        'Gusto mo bang malaman ang mga specific na karapatan sa ilalim ng Migrant Workers Act (RA 8042)?',
        'Interesado ka bang malaman ang mga legal remedies sa bansa kung saan ka nagtatrabaho?',
        'Kailangan mo ba ng contacts para sa labor attachés o legal aid services?',
        'Alam mo ba ang proseso ng pag-file ng claims para sa wage theft?'
    ],
    'Ano ang mga hakbang para sa mabilis na pag-uwi?': [
        'May immediate access ka ba sa pinakamalapit na embahada o konsulado ng Pilipinas?',
        'Alam mo ba ang mga dokumentong kailangan para sa emergency repatriation?',
        'Kailangan mo ba ng tulong sa pag-inform sa employer mo tungkol sa iyong repatriation needs?',
        'Gusto mo bang malaman ang support services na ibinibigay ng POLO at OWWA?'
    ],
    'Sino ang pwedeng kontakin?': [
        'Nakipag-ugnayan ka na ba sa embahada o konsulado ng Pilipinas sa bansa kung nasaan ka?',
        'Kailangan mo ba ng contact information para sa mga opisina ng POLO?',
        'Alam mo ba ang mga NGOs na nagbibigay ng repatriation support para sa OFWs?',
        'Gusto mo bang malaman ang mga hotline o emergency contact numbers?'
    ],
    'Anong financial assistance ang available?': [
        'Nakarehistro ka ba sa OWWA para sa repatriation benefits?',
        'Kailangan mo ba ng impormasyon sa specific financial aid programs mula sa DFA?',
        'Interesado ka bang malaman ang tungkol sa livelihood assistance para sa mga repatriated OFWs?',
        'Gusto mo bang malaman ang emergency financial assistance mula sa mga NGOs?'
    ],
    'Paano iayos ang pagpapadala ng gamit?': [
        'Kailangan mo ba ng rekomendasyon para sa mga maaasahang cargo at logistics companies?',
        'Alam mo ba ang mga customs regulations para sa pagpapadala ng mga gamit pabalik sa Pilipinas?',
        'Kailangan mo ba ng tulong sa dokumentasyon na kailangan para sa pagpapadala?',
        'Naghahanap ka ba ng payo sa pag-pack at pag-secure ng mga gamit para sa shipment?'
    ],
    'Ano ang dapat tingnan sa kontrata?': [
        'Klaro ba sa iyo ang job description at responsibilities na nakalagay sa kontrata?',
        'Kailangan mo ba ng detalyadong breakdown ng sahod, benepisyo, at payment schedule?',
        'Alam mo ba ang working hours, rest days, at leave entitlements mo?',
        'Gusto mo bang magtanong ng legal advice sa mga terms na hindi malinaw o patas?'
    ],
    'Paano masisiguro kung legal ang kontrata?': [
        'Na-verify na ba ng POEA ang kontrata mo?',
        'Kailangan mo ba ng tulong sa pag-confirm ng mga pirma at seal sa kontrata?',
        'Alam mo ba ang mga kinakailangang stamps para sa kontrata mo?',
        'Gusto mo bang kumonsulta sa legal adviser para masiguradong valid ang kontrata?'
    ],
    'Ano ang gagawin kung may bagong kontrata?': [
        'Na-compare mo na ba ang mga bagong terms ng kontrata sa original na kontrata?',
        'Kailangan mo ba ng tulong sa pag-unawa kung bakit may bagong kontrata?',
        'Alam mo ba ang mga karapatan mo kung pinipilit kang pumirma ng bagong kontrata?',
        'Gusto mo bang i-report ang sitwasyon sa POEA o magtanong ng legal advice?'
    ],
    'Paano makakuha ng legal advice?': [
        'Kailangan mo ba ng contact information para sa pinakamalapit na POLO o embahada?',
        'Alam mo ba ang legal aid services na ibinibigay ng OWWA?',
        'Na-dokumento mo na ba ang lahat ng instances ng paglabag sa kontrata?',
        'Gusto mo bang malaman ang proseso ng pag-file ng formal na reklamo?'
    ]
}

# Initialize session state
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.path = []
    st.session_state.responses = {}
    st.session_state.forward_query = ""

def back():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.path.pop()

def get_yes_no_responses(questions):
    responses = {}
    for question in questions:
        responses[question] = st.checkbox(question, key=question)
    return responses

def build_query():
    query = []
    for path in st.session_state.path:
        query.append(path)
        if path in st.session_state.responses:
            for question, answer in st.session_state.responses[path].items():
                query.append(f"{question}: {'Oo' if answer else 'Hindi'}")
    return " > ".join(query)

def summarize_responses():
    summary = []
    for path in st.session_state.path:
        if path in st.session_state.responses:
            for question, answer in st.session_state.responses[path].items():
                summary.append(f"{question}: {'Oo' if answer else 'Hindi'}")
    return " ".join(summary)

# # Define button sets for each level
# level1_buttons = ['Pre-Deployment', 'Wages', 'Repatriation', 'Wala dito ang tanong ko']
# level2_buttons = {
#     'Pre-Deployment': ['Sub-topic 1A', 'Sub-topic 1B', 'Sub-topic 1C', 'Sub-topic 1D', 'Wala dito ang tanong ko'],
#     'Wages': ['Sub-topic 2A', 'Sub-topic 2B', 'Sub-topic 2C', 'Sub-topic 2D', 'Wala dito ang tanong ko'],
#     'Repatriation': ['Sub-topic 3A', 'Sub-topic 3B', 'Sub-topic 3C', 'Sub-topic 3D', 'Wala dito ang tanong ko']
# }
# level3_buttons = {
#     'Sub-topic 1A': ['Detail 1A1', 'Detail 1A2', 'Detail 1A3', 'Detail 1A4', 'Wala dito ang tanong ko'],
#     'Sub-topic 1B': ['Detail 1B1', 'Detail 1B2', 'Detail 1B3', 'Detail 1B4', 'Wala dito ang tanong ko'],
#     'Sub-topic 1C': ['Detail 1C1', 'Detail 1C2', 'Detail 1C3', 'Detail 1C4', 'Wala dito ang tanong ko'],
#     'Sub-topic 1D': ['Detail 1D1', 'Detail 1D2', 'Detail 1D3', 'Detail 1D4', 'Wala dito ang tanong ko'],
#     'Sub-topic 2A': ['Detail 2A1', 'Detail 2A2', 'Detail 2A3', 'Detail 2A4', 'Wala dito ang tanong ko'],
#     'Sub-topic 2B': ['Detail 2B1', 'Detail 2B2', 'Detail 2B3', 'Detail 2B4', 'Wala dito ang tanong ko'],
#     'Sub-topic 2C': ['Detail 2C1', 'Detail 2C2', 'Detail 2C3', 'Detail 2C4', 'Wala dito ang tanong ko'],
#     'Sub-topic 2D': ['Detail 2D1', 'Detail 2D2', 'Detail 2D3', 'Detail 2D4', 'Wala dito ang tanong ko'],
#     'Sub-topic 3A': ['Detail 3A1', 'Detail 3A2', 'Detail 3A3', 'Detail 3A4', 'Wala dito ang tanong ko'],
#     'Sub-topic 3B': ['Detail 3B1', 'Detail 3B2', 'Detail 3B3', 'Detail 3B4', 'Wala dito ang tanong ko'],
#     'Sub-topic 3C': ['Detail 3C1', 'Detail 3C2', 'Detail 3C3', 'Detail 3C4', 'Wala dito ang tanong ko'],
#     'Sub-topic 3D': ['Detail 3D1', 'Detail 3D2', 'Detail 3D3', 'Detail 3D4', 'Wala dito ang tanong ko']
# }

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

# Inject custom CSS for the "Ask AI Assistant" button
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: auto;
        margin: 5px 0;
        white-space: normal;
    }
    div.stButton > button:hover {
        background-color: #ddd;
    }
    div.stButton > button:has(span:contains('Ask AI Assistant')) {
        background-color: #d4edda !important;
        color: #155724 !important;
        font-weight: bold !important;
        border: 2px solid #155724 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Display buttons based on the current level
if st.session_state.level == 1:
    # st.header("Pumili ng pangunahing paksa:")
    for button in level1_buttons:
        if st.button(button):
            if button == "Wala dito ang tanong ko.":
                st.session_state.level = 5
            else:
                st.session_state.path.append(button)
                st.session_state.level = 2
            st.rerun()
elif st.session_state.level == 2:
    main_topic = st.session_state.path[0]
    if main_topic in level2_buttons:
        # st.header(f"Pumili ng sub-topic sa ilalim ng {main_topic}:")
        for button in level2_buttons[main_topic]:
            if st.button(button):
                if button == "Wala dito ang tanong ko.":
                    st.session_state.level = 5
                elif button == "Kailangan mo ba ng tulong sa pagsasalin ng iyong kontrata sa Tagalog?":
                    st.session_state.level = 6
                else:
                    st.session_state.path.append(button)
                    st.session_state.level = 3
                st.rerun()
        if st.button("Balik"):
            back()
            st.rerun()
elif st.session_state.level == 3:
    sub_topic = st.session_state.path[1]
    if sub_topic in level3_buttons:
        st.header(f"Piliin kung 'Oo':")
        st.session_state.responses[sub_topic] = get_yes_no_responses(level3_buttons[sub_topic])

        if st.button("Ask AI Assistant"):
            st.session_state.forward_query = summarize_responses()
            st.session_state.level = 5
            st.rerun()
            # st.write("Generated Query: ", st.session_state.forward_query)
        if st.button("Balik"):
            back()
            st.rerun()
elif st.session_state.level == 4:
    if st.button("Balik sa Simula"):
        st.session_state.level = 1
        st.session_state.path = []
        st.session_state.responses = {}
        st.session_state.forward_query = ""
        st.rerun()
    # custom_chatbot()
    st.header("Chatbot")
    st.text_input("Ano ang iyong tanong?", key="user_question")
    if st.button("Isumite"):
        st.write(f"Salamat sa iyong tanong: {st.session_state.user_question}")
    

elif st.session_state.level == 5:
    if st.button("Balik sa Simula"):
        st.session_state.level = 1
        st.session_state.path = []
        st.session_state.responses = {}
        st.session_state.forward_query = ""
        st.rerun()
    # custom_chatbot()
    st.header("Chatbot (Not Yet Functional)")
    # st.text_input("You asked: " + str(st.session_state.forward_query), key="user_question")
    st.text_input(" ", key="user_question")
    if st.button("Isumite"):
        st.write(f"Salamat sa iyong tanong: {st.session_state.user_question}")
    
elif st.session_state.level == 6: 
    if st.button("Balik sa Simula"):
        st.session_state.level = 1
        st.session_state.path = []
        st.session_state.responses = {}
        st.session_state.forward_query = ""
        st.rerun()  
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
        st.write("Malaki! I-click ang 'Ask AI Assistant.")

        # Optionally, save the uploaded file to disk
        with open(f"/workspaces/cma_app/uploaded_images/uploaded_image_{uploaded_file.name}", "wb") as f:
            f.write(bytes_data)
            # st.write("Image saved.")
    else:
        st.write("Wala pang na-upload na larawan.")


### Sidebar

with st.sidebar:
    st.header("Hello! 👋 Ako si ang inyong friendly AI Assistant 🤖.")
    st.caption("Tumutulong ako sa mga overseas Filipino worker sa mga tanong tungkol sa pre-deployment, legal na karapatan, at repatriation. Kung kailangan mo ng impormasyon o tulong, narito ako para magbigay ng tumpak na impormasyon at suporta. Sabik akong tulungan ka!")
    # st.divider()

    with st.expander("Sino si CMA?"):
        st.caption("The Center for Migrant Advocacy – Philippines is an advocacy group that promotes the rights of overseas Filipinos, land or sea-based migrant workers, Filipino immigrants and their families. The center helps to improve the economic, social and political conditions of migrant Filipino families everywhere through policy advocacy, information dissemination, networking, capability-building and direct assistance.")

    with st.expander("Bakit mahalaga ang AI Assistant na ito?"):
        st.caption("Ang Center for Migrant Advocacy ay nag-aanyaya sa pakikipagtulungan at puna upang pinuhin at i-optimize ang solusyon na ito, na tinitiyak na epektibong natutugunan nito ang magkakaibang pangangailangan ng mga OFW. Ang session na ito ay naglalayon na mangalap ng mahalagang feedback mula sa dati at kasalukuyang mga OFW upang pinuhin ang disenyo at functionality ng AI assistant. Napakahalaga ng ganitong mga pananaw habang nagsisikap ang CMA na magkaroon ng makabuluhang epekto sa buhay ng mga OFW sa pamamagitan ng makabagong teknolohiya. Inaasahan namin ang iyong pakikilahok at mga kontribusyon habang tinutuklasan namin ang mga posibilidad ng pagbabagong inisyatiba na ito.")

    with st.expander("Privacy Disclaimer"):
        st.caption("Ang AI Assistant na ito ay naglalayong magbigay ng makatotohanang impormasyon tungkol sa iyong sitwasyon at hindi pa kumukolekta ng iyong personal na impormasyon. Ginagamit namin ang impormasyong ito upang maunawaan ang iba't ibang sitwasyon ng mga OFW at kanilang mga pamilya at kung paano sumangguni sa gobyerno o iba pang NGO tungkol sa iyong sitwasyon o problema. Maaari kang makipag-usap sa isang case manager pagkatapos gamitin ang AI Assistant na ito.")

    st.caption('<p style="text-align:center">Made with ❤️ by CMA</p>', unsafe_allow_html=True)
