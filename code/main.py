import time

# Helper functions
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_user_input():
    return input("\n👤 Aap: ").strip().lower()

# Keywords
positive_keywords = {"haan", "yes", "btao", "tell", "sure", "ok", "pooch", "continue", "han", "haa", "kya hai"}
negative_keywords = {"nahi", "no", "na", "not", "nope", "n", "enough", "bas", "itna", "kafi"}

# Start conversation
def start_chat():
    step = "start"
    name = None
    age = None

    while True:
        if step == "start":
            slow_print("🤖 Namaste! Main aapki Nursing College admission mein help kar sakta hoon.")
            slow_print("Kya aap hamari B.Sc Nursing program mein admission lena chahte hain?")
            step = "ask_interest"

        elif step == "ask_interest":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("Bahut accha! Admission ke liye pehle main aapki eligibility check karta hoon.")
                slow_print("Kya aapne 12th mein Biology padha tha?")
                step = "ask_biology"
            elif any(k in user for k in negative_keywords):
                slow_print("Koi baat nahi! Agar future mein zarurat ho to contact kariye. Dhanyawad! 🙏")
                break
            else:
                slow_print("Kripya haan ya nahi mein jawab dein.")

        elif step == "ask_biology":
            user = get_user_input()
            if "biology" in user or any(k in user for k in positive_keywords):
                slow_print("Perfect! Aur aapki age kitni hai? Admission ke liye 17-35 years ke beech honi chahiye.")
                step = "ask_age"
            elif any(k in user for k in negative_keywords) or any(sub in user for sub in ["physics", "chemistry", "math"]):
                slow_print("Bina Biology ke admission possible nahi hai. Kya main aapko koi aur info de sakta hoon?")
                break
            else:
                slow_print("Kripya bataiye ki aapne Biology padha tha ya nahi.")

        elif step == "ask_age":
            user = get_user_input()
            try:
                age = int(next(w for w in user.split() if w.isdigit()))
                if 17 <= age <= 35:
                    slow_print("Excellent! Aap completely eligible hain.")
                    slow_print("Ab main aapko hamari B.Sc Nursing program ke baare mein detail mein batata hoon.")
                    slow_print("Kya aap program details jaanna chahenge?")
                    step = "program"
                else:
                    slow_print("Maaf kijiye, age 17-35 ke beech honi chahiye. Aap eligible nahi hain.")
                    break
            except:
                slow_print("Kripya age number mein likhein jaise '19'.")

        elif step == "program":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
🎓 B.Sc Nursing Program:

• 4 saal ka full-time undergraduate course
• Theory + practical training
• Hospital training included
• INC Delhi se recognized

Eligibility:
• Biology in 12th ✓
• PNT exam clear ✓
• Age 17–35 ✓

Kya aap fees ke baare mein jaanna chahenge?
                """)
                step = "fees"
            else:
                step = "end"

        elif step == "fees":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
💰 Fee Structure:

• Tuition: ₹60,000
• Bus: ₹10,000
• Total: ₹70,000

Installments:
• ₹30,000 (admission)
• ₹20,000 (after 1st sem)
• ₹20,000 (after 2nd sem)

Kya aap hostel facilities ke baare mein jaanna chahenge?
                """)
                step = "hostel"
            else:
                step = "end"

        elif step == "hostel":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
🏠 Hostel + Training:

• 24x7 water & electricity
• CCTV, security, warden
• Hospital training with real patients

Kya aap college location ke baare mein jaanna chahenge?
                """)
                step = "location"
            else:
                step = "end"

        elif step == "location":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
📍 College Location:

• Delhi based campus
• Metro connectivity
• Nearby hospitals
• Cultural & career hub

Kya aap recognition ke baare mein jaanna chahenge?
                """)
                step = "recognition"
            else:
                step = "end"

        elif step == "recognition":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
🏆 Recognition:

• INC Delhi approved
• Nationally valid degree
• Govt job eligibility
• Nursing license support

Kya aap training hospitals ke baare mein jaanna chahenge?
                """)
                step = "clinical"
            else:
                step = "end"

        elif step == "clinical":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
🏥 Clinical Training:

• District Hospital (Backundpur)
• CHCs & Regional Hospitals
• Ranchi Neuro Hospital

Kya aap scholarship ke baare mein jaanna chahenge?
                """)
                step = "scholarship"
            else:
                step = "end"

        elif step == "scholarship":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
🎓 Scholarships:

• Govt Scholarship: ₹18k–23k
• Labour Ministry: ₹40k–48k

Apply karna chahiye agar eligible hain!

Kya aap seats ke baare mein jaanna chahenge?
                """)
                step = "seats"
            else:
                step = "end"

        elif step == "seats":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
📊 Seats Available:

• Total: 60 seats
• Competition high, apply early

🎯 Summary chahenge?
                """)
                step = "summary"
            else:
                step = "end"

        elif step == "summary":
            user = get_user_input()
            if any(k in user for k in positive_keywords):
                slow_print("""
📋 SUMMARY:

🎓 Program: B.Sc Nursing (4 yrs)
💰 Fees: ₹70,000/year (3 parts)
🏠 Hostel: Yes
🏥 Training: Real hospital
📍 Location: Delhi
🏆 INC Approved
🎓 Scholarship: Up to ₹48,000
📊 Seats: 60 total

👉 Kya aapko aur kuch poochhna hai?
                """)
                step = "end_conversation"
            else:
                step = "end"

        elif step == "end_conversation":
            user = get_user_input()
            if any(k in user for k in negative_keywords):
                step = "end"
            else:
                slow_print("Aap aur kya jaanna chahenge? (type 'no' to exit)")

        elif step == "end":
            slow_print("\n✅ Dhanyawad! Aapka Nursing Assistant Chatbot se baat karke accha laga. 🙏")
            slow_print("""
📞 Contact:
Phone: +91-9876543210
Email: info@nursingcollege.edu
Website: https://nursingcollege.edu
            """)
            break


# Run the chatbot
if __name__ == "__main__":
    start_chat()
