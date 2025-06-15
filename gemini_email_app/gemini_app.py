import streamlit as st
import google.generativeai as genai
import pandas as pd
import io
import imaplib, email, smtplib
from email.message import EmailMessage

# --- Gemini API Setup ---
# Access API key securely using st.secrets
# Make sure you have a .streamlit/secrets.toml file with gemini_api_key = "YOUR_API_KEY"
try:
    genai.configure(api_key=st.secrets["gemini_api_key"])
except KeyError:
    st.error("Gemini API Key not found! Please set it in your .streamlit/secrets.toml file.")
    st.stop() # Stop the app from running if the key is missing

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("📬 Gemini Email AI Assistant with Gmail Integration")
st.markdown("Analyze emails with AI from pasted text, uploaded files, or your Gmail inbox.")

email_body = st.text_area("Paste Email Content Here:", height=200)
uploaded_file = st.file_uploader("Upload a .txt file (1 email) or .csv (multiple emails)", type=["txt", "csv"])

with st.expander("🔐 Admin Panel & Gmail Integration"):
    admin_password = st.text_input("Enter Admin Password: ", type="password")
    gmail_user = st.text_input("Gmail Address")
    gmail_app_password = st.text_input("Gmail App Password", type="password") # This too should ideally be in secrets
    auto_reply_toggle = st.checkbox("Enable Auto-Reply to Gmail")
    check_gmail_button = st.button("📬 Fetch Unread Gmail and Analyze")

batch_results = []

# --- Analyze Gemini Wrapper ---
def analyze_text(email_text):
    prompt = f"""
    Analyze the following email and provide:

    1. A 1-line summary
    2. A professional auto-reply suggestion
    3. A spam/phishing flag and score (None, Light, Moderate, High)
    4. Sentiment classification (Neutral, Urgent, Aggressive)
    5. Does this email appear to be a greeting only with no links?

    Email:
    {email_text}
    """
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else ""

# --- Gmail Fetch ---
if check_gmail_button and gmail_user and gmail_app_password:
    st.info("Connecting to Gmail and fetching unread messages...")
    try:
        # Note: Ideally, gmail_app_password should also come from st.secrets
        # For simplicity in this example, it's still from text_input, but be aware.
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(gmail_user, gmail_app_password)
        imap.select("inbox")
        status, messages = imap.search(None, '(UNSEEN)')
        email_ids = messages[0].split()

        if not email_ids:
            st.warning("No unread emails found.")
        else:
            for mail_id in email_ids:
                status, msg_data = imap.fetch(mail_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                ai_output = analyze_text(body)
                st.markdown("---")
                st.markdown(f"**📨 From:** {msg['From']}")
                st.markdown(f"**📝 Subject:** {msg['Subject']}")

                lines = ai_output.splitlines()
                parsed = {"Summary": "", "AutoReply": "", "SpamCheck": "", "Sentiment": "", "GreetingOnly": ""}
                for line in lines:
                    if "summary" in line.lower():
                        parsed["Summary"] = line.split(":")[-1].strip()
                    elif "auto-reply" in line.lower():
                        parsed["AutoReply"] = line.split(":")[-1].strip()
                    elif "spam" in line.lower():
                        parsed["SpamCheck"] = line.split(":")[-1].strip()
                    elif "sentiment" in line.lower():
                        parsed["Sentiment"] = line.split(":")[-1].strip()
                    elif "greeting" in line.lower():
                        parsed["GreetingOnly"] = line.split(":")[-1].strip()

                st.markdown(f"**🔎 Summary:** {parsed['Summary']}")
                st.markdown(f"**💬 Auto-Reply Suggestion:** {parsed['AutoReply']}")

                spam = parsed['SpamCheck'].lower()
                if "light" in spam:
                    st.markdown(f"**Spam Check:** ⚠️ <span style='color:gold'>{parsed['SpamCheck']}</span>", unsafe_allow_html=True)
                elif "moderate" in spam:
                    st.markdown(f"**Spam Check:** ⚠️ <span style='color:orange'>{parsed['SpamCheck']}</span>", unsafe_allow_html=True)
                elif "high" in spam:
                    st.markdown(f"**Spam Check:** 🚨 <span style='color:red'>{parsed['SpamCheck']}</span>", unsafe_allow_html=True)
                    st.warning("This message is highly suspicious. Do you want to mark it as spam?")
                    if st.button(f"🚫 Mark '{msg['Subject']}' as Spam"):
                        st.info("Message flagged as spam.")
                else:
                    st.markdown(f"**Spam Check:** ✅ <span style='color:green'>None</span>", unsafe_allow_html=True)

                sentiment = parsed['Sentiment'].lower()
                if "neutral" in sentiment:
                    st.markdown(f"**Sentiment:** 🟦 <span style='color:gray'>{parsed['Sentiment']}</span>", unsafe_allow_html=True)
                elif "urgent" in sentiment:
                    st.markdown(f"**Sentiment:** 🔥 <span style='color:orange'>{parsed['Sentiment']}</span>", unsafe_allow_html=True)
                elif "aggressive" in sentiment:
                    st.markdown(f"**Sentiment:** 🚨 <span style='color:red'>{parsed['Sentiment']}</span>", unsafe_allow_html=True)

                if "yes" in parsed["GreetingOnly"].lower():
                    st.success("Detected greeting-only email with no links. Auto-reply will be sent.")
                    st.markdown(f"**Auto Reply Sent:** {parsed['AutoReply']}")

                if auto_reply_toggle:
                    reply = EmailMessage()
                    reply["From"] = gmail_user
                    reply["To"] = msg["From"]
                    reply["Subject"] = "RE: " + msg["Subject"]
                    reply.set_content(parsed['AutoReply'])
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(gmail_user, gmail_app_password)
                        smtp.send_message(reply)
                    st.success("Auto-reply sent successfully.")

        imap.logout()
    except Exception as e:
        st.error(f"Gmail integration error: {str(e)}")