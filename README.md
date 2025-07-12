## 🏥 Nursing Admission Chatbot

A conversational AI assistant built using **Streamlit** and **LLM prompt engineering** that helps students inquire about **B.Sc Nursing admission details** interactively in Hindi-English mix. From eligibility checks to fees and scholarships, the chatbot guides users step by step with personalized and human-like responses.

---

### 🎯 Features

* **Interactive Guided Chat**: Simulates a human-like admission counselor.
* **Prompt Engineering**: Designed to follow a fixed yet flexible conversation flow using natural language.
* **Multilingual Input**: Accepts Hinglish queries ("haan", "kya hai", "nahi", etc.).
* **Eligibility Checker**: Dynamically verifies biology subject and age criteria.
* **Topic-wise Information**: Offers details on:

  * Program overview
  * Fees structure
  * Hostel & training facilities
  * Scholarships
  * Seats and recognition
* **Conversation Summary**: Recaps important details at the end.
* **Contact Box**: Displays contact info once the chat ends.
* **Beautiful UI**: Clean and colorful Streamlit layout with chat-style bubbles.

---

### 📸 Demo

It is in the real_chat_bot_implimentation.pdf

---

### 🛠️ Tech Stack

* **Python**
* **Streamlit** – UI and interaction
* **Prompt Engineering** – Custom crafted flow
* **Session State** – To handle user memory
* **HTML/CSS** – For bubble chat design
* **(Optional)** FAISS / LangChain – for extended knowledge integration

---

### 🚀 Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/nursing-chatbot.git
cd nursing-chatbot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
streamlit run app.py
```
### 🧠 How It Works

The chatbot simulates a conversation in a structured yet natural way:

1. Starts with a **greeting and interest check**
2. Follows up with **eligibility verification (Biology + Age)**
3. Shares details about the **program, fees, hostel, training, etc.**
4. Asks users if they want to know more
5. Ends with a **summary and contact info**

---

### 📈 Future Plans

* 🔊 **Voice Input/Output**
* 🌍 **Multilingual support**
* 📱 **WhatsApp / Telegram integration**
* 📊 **Admin dashboard**
* 📃 **PDF export of chat transcript**
* 🤖 **LLM integration for dynamic queries**

---
