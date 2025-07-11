# app.py
import streamlit as st
from response_engine import get_response, extract_tag
import time

st.set_page_config(page_title="Nursing Admission Assistant", page_icon="🏥", layout="wide")

# CSS styling
st.markdown("""
<style>
    .main-container {
        display: flex;
        justify-content: center;
    }
    .chat-box {
        width: 700px;
        max-width: 90%;
        margin-top: 10px;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        background: #fefefe;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .chat-bubble {
        padding: 12px 18px;
        margin-bottom: 10px;
        max-width: 75%;
        border-radius: 20px;
        line-height: 1.4;
        display: inline-block;
        clear: both;
        animation: fadeIn 0.3s ease-in;
    }
    .user {
        background-color: #667eea;
        color: white;
        float: right;
        text-align: right;
    }
    .bot {
        background-color: #f5576c;
        color: white;
        float: left;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Keywords
positive_keywords = {"haan", "yes", "btao", "tell", "sure", "ok", "pooch", "continue", "han", "haa", "kya hai"}
negative_keywords = {"nahi", "no", "na", "not", "nope", "n", "enough", "bas", "itna", "kafi"}

# Topic map for later conversation
topic_suggestions = {
    "program": "Program details aur duration",
    "fee": "Fees structure aur payment options", 
    "hostel": "Hostel facilities aur accommodation",
    "training": "Clinical training aur hospital experience",
    "location": "College location aur nearby facilities",
    "recognition": "Recognition aur accreditation",
    "scholarship": "Scholarship opportunities",
    "seats": "Available seats aur admission process",
    "eligibility": "Complete eligibility criteria"
}

# Session initialization
if "chat" not in st.session_state:
    st.session_state.chat = []
    st.session_state.step = "start"
    st.session_state.name = None
    st.session_state.age = None
    st.session_state.topics_asked = set()
    st.session_state.all_topics = set(topic_suggestions.keys())
    st.session_state.current_topic = None

# Sidebar info
with st.sidebar:
    st.markdown("### 🏥 College Info")
    st.info("**Program:** B.Sc Nursing  \n**Location:** Delhi  \n**Seats:** 60  \n**Recognition:** INC")
    st.markdown("### 📌 Topics Available")
    for tag, label in topic_suggestions.items():
        st.write(f"- {label}")

# Centered layout
st.markdown("<h2 style='text-align:center;'>💬 Nursing Admission Chat</h2>", unsafe_allow_html=True)
st.markdown("<div class='main-container'><div class='chat-box'>", unsafe_allow_html=True)

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, msg in st.session_state.chat:
        role = "user" if sender == "user" else "bot"
        st.markdown(f'<div class="chat-bubble {role}">{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bot functions
def add_bot(message):
    st.session_state.chat.append(("bot", message))

def add_user(message):
    st.session_state.chat.append(("user", message))

def typing_effect(text, delay=0.3):
    with st.spinner("🤖 Typing..."):
        time.sleep(1)
    add_bot(text)

# Main conversation logic following the exact flow
def process_user_input(user_input):
    user_input = user_input.strip()
    add_user(user_input)
    clean_input = user_input.lower()

    # Step 1: Initial greeting
    if st.session_state.step == "start":
        typing_effect("Namaste! Main aapki Nursing College admission mein help kar sakta hoon. Kya aap hamari B.Sc Nursing program mein admission lena chahte hain?")
        st.session_state.step = "ask_interest"

    # Step 2: Check interest in admission
    elif st.session_state.step == "ask_interest":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("Bahut accha! Admission ke liye pehle main aapki eligibility check karta hoon. Kya aapne 12th mein Biology padha tha?")
            st.session_state.step = "ask_biology"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Agar future mein kabhi nursing career ke baare mein sochenge to main hamesha available hoon aapki help ke liye. Dhanyawad!")
            st.session_state.step = "end"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 3: Biology requirement check
    elif st.session_state.step == "ask_biology":
        if any(keyword in clean_input for keyword in positive_keywords) or "biology" in clean_input:
            typing_effect("Perfect! Aur aapki age kitni hai? Admission ke liye 17-35 years ke beech honi chahiye.")
            st.session_state.step = "ask_age"
        elif any(keyword in clean_input for keyword in negative_keywords) or any(subject in clean_input for subject in ["physics", "chemistry", "maths", "math"]):
            typing_effect("B.Sc Nursing mein admission ke liye Biology avashyak hai. Bina Biology ke admission possible nahi hai. Kya main aapko koi aur information de sakta hoon?")
            st.session_state.step = "end"
        else:
            typing_effect("Kripya bataiye ki aapne 12th mein Biology padha tha ya nahi.")

    # Step 4: Age verification
    elif st.session_state.step == "ask_age":
        try:
            # Extract age from user input
            age_words = user_input.split()
            age = None
            for word in age_words:
                if word.isdigit():
                    age = int(word)
                    break
            
            if age is None:
                typing_effect("Kripya apni age number mein likhein, jaise '19' ya '22 saal'.")
                return
                
            st.session_state.age = age
            if 17 <= age <= 35:
                typing_effect("Excellent! Aap completely eligible hain. Ab main aapko hamari B.Sc Nursing program ke baare mein detail mein batata hoon. Kya aap program details jaanna chahenge?")
                st.session_state.step = "ask_program_details"
            else:
                typing_effect("Sorry, admission ke liye age 17-35 years ke beech honi chahiye. Aapki current age eligibility criteria mein nahi aati. Kya main aapko koi aur information de sakta hoon?")
                st.session_state.step = "end"
        except:
            typing_effect("Kripya apni age number mein likhein, jaise '19' ya '22 saal'.")

    # Step 5: Program details
    elif st.session_state.step == "ask_program_details":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Hamare B.Sc Nursing Program ke baare mein:

• Yeh ek 4 saal ka full-time undergraduate program hai
• Theoretical aur practical training dono milti hai  
• Hospital training included hai jahan aap real patients ke saath kaam karenge
• Program Indian Nursing Council (INC) Delhi se recognized hai

Complete Eligibility Criteria:
• Biology in 12th grade ✓
• PNT exam (Pre-Nursing Test) clear karna compulsory hai
• Age 17-35 years ✓

Kya aap fees structure ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_fees"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Kya aap kisi aur topic ke baare mein jaanna chahenge?")
            st.session_state.step = "topic_selection"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 6: Fees structure
    elif st.session_state.step == "ask_fees":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Complete Fee Structure batata hoon:

Annual Fees:
• Tuition Fee: ₹60,000 INR
• Bus Fee: ₹10,000 INR
• Total Annual Fees: ₹70,000 INR

Payment Schedule (3 installments mein):
• 1st Installment: ₹30,000 (admission ke time)
• 2nd Installment: ₹20,000 (first semester ke baad)
• 3rd Installment: ₹20,000 (second semester ke baad)

Ye payment plan fees burden kam karta hai. Kya aap hostel facilities ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_hostel"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Kya aap kisi aur topic ke baare mein jaanna chahenge?")
            st.session_state.step = "topic_selection"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 7: Hostel facilities
    elif st.session_state.step == "ask_hostel":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Hostel Facilities:

Basic Amenities:
• 24x7 water aur electricity supply
• CCTV surveillance complete security ke liye
• Warden hamesha available on-site

Training Facilities:
• Hospital training included hai jahan aap real patients ke saath practical experience gain karenge
• Ye hands-on training aapko industry-ready banata hai

Kya aap college location ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_location"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Kya aap kisi aur topic ke baare mein jaanna chahenge?")
            st.session_state.step = "topic_selection"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 8: Location details
    elif st.session_state.step == "ask_location":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""College Location:
Hamara college Delhi mein located hai - capital city ka advantage aur better opportunities milte hain.

Delhi location benefits:
• Metro connectivity se easy commute
• Multiple hospitals nearby for practical training
• Better career opportunities post-graduation
• Cultural aur educational hub

Kya aap recognition aur accreditation ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_recognition"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Thik hai! Kya aap recognition aur accreditation ke baare mein jaanna chahenge?")
            st.session_state.step = "ask_recognition"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 9: Recognition and accreditation
    elif st.session_state.step == "ask_recognition":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Recognition aur Accreditation:

Hamara college Indian Nursing Council (INC) Delhi se recognized hai. Ye bahut important hai kyunki:
• Degree nationally accepted hai
• Government jobs mein eligible rahenge
• Further studies ke liye qualification valid hai

INC (Indian Nursing Council) recognition ka matlab:
• Quality education standards maintain karte hain
• Curriculum nationally approved hai
• Graduates ko nursing license milne mein koi problem nahi
• Employment opportunities better hain

Kya aap clinical training locations ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_clinical_training"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Samjha! Kya aap clinical training locations ke baare mein jaanna chahenge?")
            st.session_state.step = "ask_clinical_training"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 10: Clinical training
    elif st.session_state.step == "ask_clinical_training":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Clinical Training Locations:

Aapko practical training in locations mein milegi:
• District Hospital (Backundpur)
• Community Health Centers
• Regional Hospital (Chartha)
• Ranchi Neurosurgery and Allied Science Hospital (Ranchi, Jharkhand)

Ye diverse training locations aapko different specializations mein experience dete hain. Kya aap scholarship opportunities ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_scholarship"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Kya aap scholarship opportunities ke baare mein jaanna chahenge?")
            st.session_state.step = "ask_scholarship"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 11: Scholarship opportunities
    elif st.session_state.step == "ask_scholarship":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Scholarship Opportunities:

Available Scholarships:
• Government Post-Matric Scholarship: ₹18,000-₹23,000
• Labour Ministry Scholarships: ₹40,000-₹48,000 (agar Labour Registration hai)

Ye scholarships aapki fees significantly reduce kar sakti hain! Eligible students ko apply karna chahiye.

Kya aap total seats availability ke baare mein jaanna chahenge?""")
            st.session_state.step = "ask_seats"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Thik hai! Kya aap total seats availability ke baare mein jaanna chahenge?")
            st.session_state.step = "ask_seats"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Step 12: Seats availability
    elif st.session_state.step == "ask_seats":
        if any(keyword in clean_input for keyword in positive_keywords):
            typing_effect("""Seat Availability:
• Total 60 seats available hain hamare B.Sc Nursing program mein
• Limited seats hain, so early application recommended hai
• Competition bhi rahta hai admission ke liye

Complete Eligibility Criteria Summary:
Required:
• Biology in 12th grade ✓
• PNT Exam (Pre-Nursing Test) clear karna compulsory
• Age: 17-35 years ✓

Kya aap koi aur information chahenge ya main aapko summary de dun?""")
            st.session_state.step = "final_summary"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Koi baat nahi! Kya aap final summary chahenge?")
            st.session_state.step = "final_summary"
        else:
            typing_effect("Kripya haan ya nahi mein jawab dein.")

    # Final summary or topic selection
    elif st.session_state.step == "final_summary":
        if any(keyword in clean_input for keyword in positive_keywords) or "summary" in clean_input:
            typing_effect("""📋 Complete Summary:

🎓 Program: B.Sc Nursing (4 years)
💰 Total Fees: ₹70,000 per year
🏠 Hostel: Available with 24x7 facilities
🏥 Training: Real hospital experience
📍 Location: Delhi (Metro connectivity)
🏆 Recognition: INC Delhi approved
💰 Scholarships: Up to ₹48,000 available
📊 Seats: 60 total seats

Dhanyawad! Kya aap koi aur information chahenge?""")
            st.session_state.step = "end_conversation"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Dhanyawad! Admission ke liye aur koi sawal ho to main hamesha available hoon. 🙏")
            st.session_state.step = "end"
        else:
            typing_effect("Kripya bataiye ki aap summary chahenge ya bas itna hi kaafi hai.")

    # Topic selection handling
    elif st.session_state.step == "topic_selection":
        # Check for specific topic keywords
        if "eligibility" in clean_input:
            typing_effect("""Complete Eligibility Criteria:

Required:
• Biology in 12th grade ✓
• PNT Exam (Pre-Nursing Test) clear karna compulsory
• Age: 17-35 years ✓

Additional Requirements:
• 12th pass with minimum 45% marks
• Medical fitness certificate
• Character certificate from school
• Domicile certificate (if applicable)

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "fee" in clean_input or "fees" in clean_input:
            typing_effect("""Complete Fee Structure:

Annual Fees:
• Tuition Fee: ₹60,000 INR
• Bus Fee: ₹10,000 INR
• Total Annual Fees: ₹70,000 INR

Payment Schedule (3 installments mein):
• 1st Installment: ₹30,000 (admission ke time)
• 2nd Installment: ₹20,000 (first semester ke baad)
• 3rd Installment: ₹20,000 (second semester ke baad)

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "hostel" in clean_input:
            typing_effect("""Hostel Facilities:

Basic Amenities:
• 24x7 water aur electricity supply
• CCTV surveillance complete security ke liye
• Warden hamesha available on-site

Training Facilities:
• Hospital training included hai
• Real patients ke saath practical experience

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "training" in clean_input:
            typing_effect("""Clinical Training Locations:

Aapko practical training in locations mein milegi:
• District Hospital (Backundpur)
• Community Health Centers
• Regional Hospital (Chartha)
• Ranchi Neurosurgery and Allied Science Hospital (Ranchi, Jharkhand)

Ye diverse training locations aapko different specializations mein experience dete hain.

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "location" in clean_input:
            typing_effect("""College Location:

Hamara college Delhi mein located hai - capital city ka advantage aur better opportunities milte hain.

Delhi location benefits:
• Metro connectivity se easy commute
• Multiple hospitals nearby for practical training
• Better career opportunities post-graduation
• Cultural aur educational hub

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "recognition" in clean_input:
            typing_effect("""Recognition aur Accreditation:

Hamara college Indian Nursing Council (INC) Delhi se recognized hai. Ye bahut important hai kyunki:
• Degree nationally accepted hai
• Government jobs mein eligible rahenge
• Further studies ke liye qualification valid hai

INC recognition ka matlab:
• Quality education standards maintain karte hain
• Curriculum nationally approved hai
• Graduates ko nursing license milne mein koi problem nahi

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "scholarship" in clean_input:
            typing_effect("""Scholarship Opportunities:

Available Scholarships:
• Government Post-Matric Scholarship: ₹18,000-₹23,000
• Labour Ministry Scholarships: ₹40,000-₹48,000 (agar Labour Registration hai)

Ye scholarships aapki fees significantly reduce kar sakti hain! Eligible students ko apply karna chahiye.

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif "seats" in clean_input:
            typing_effect("""Seat Availability:

• Total 60 seats available hain hamare B.Sc Nursing program mein
• Limited seats hain, so early application recommended hai
• Competition bhi rahta hai admission ke liye

Kya aap koi aur topic ke baare mein jaanna chahenge?""")
            st.session_state.step = "topic_selection"
        elif any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Dhanyawad! Admission ke liye aur koi sawal ho to main hamesha available hoon. 🙏")
            st.session_state.step = "end"
        else:
            typing_effect("Kripya bataiye ki aap kis topic ke baare mein jaanna chahte hain: eligibility, fees, hostel, training, location, recognition, scholarship, seats")

    # End conversation handling
    elif st.session_state.step == "end_conversation":
        if any(keyword in clean_input for keyword in negative_keywords):
            typing_effect("Dhanyawad! Admission ke liye aur koi sawal ho to main hamesha available hoon. 🙏")
            st.session_state.step = "end"
        else:
            typing_effect("Kripya bataiye ki aap kya aur jaanna chahenge.")

# Handle user input
if st.session_state.step not in ["end"]:
    user_input = st.chat_input("Apna message likhiye...")
    if user_input:
        process_user_input(user_input)
        st.rerun()

# Topic selection buttons when in topic_selection step
if st.session_state.step == "topic_selection":
    st.markdown("### 🔍 Kripya koi topic select karein:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Eligibility Criteria"):
            process_user_input("eligibility")
            st.rerun()
        if st.button("💰 Fees Structure"):
            process_user_input("fees")
            st.rerun()
        if st.button("🏠 Hostel Facilities"):
            process_user_input("hostel")
            st.rerun()
        if st.button("🏥 Clinical Training"):
            process_user_input("training")
            st.rerun()
    
    with col2:
        if st.button("📍 College Location"):
            process_user_input("location")
            st.rerun()
        if st.button("🏆 Recognition"):
            process_user_input("recognition")
            st.rerun()
        if st.button("🎓 Scholarship"):
            process_user_input("scholarship")
            st.rerun()
        if st.button("📊 Available Seats"):
            process_user_input("seats")
            st.rerun()
    
    if st.button("❌ Bas itna hi chahiye"):
        process_user_input("nahi")
        st.rerun()

if st.session_state.step == "end":
    # Final message with contact info
    st.markdown("""
    <div style="margin-top:20px; padding:15px; background-color:#e6f7ff; border-left: 6px solid #1890ff; border-radius: 5px;">
        <h4>📞 Contact Information:</h4>
        <ul style="padding-left:20px;">
            <li><b>Phone:</b> +91-9876543210</li>
            <li><b>Email:</b> info@nursingcollege.edu</li>
            <li><b>Website:</b> <a href="https://nursingcollege.edu" target="_blank">nursingcollege.edu</a></li>
        </ul>
        <p>Agar aapko admission process mein help chahiye, to bina hichkichaye contact kariye! 🙏</p>
    </div>
    """, unsafe_allow_html=True)

    # Restart button
    if st.button("🔁 Nayi Baatcheet Shuru Karein"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


st.markdown("</div></div>", unsafe_allow_html=True)