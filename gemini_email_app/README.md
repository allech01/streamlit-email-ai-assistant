📬 Gemini Email AI Assistant with Gmail Integration
This Streamlit application leverages Google's Gemini AI to analyze emails, providing quick summaries, suggesting auto-replies, flagging potential spam/phishing, and classifying sentiment. It offers flexible input methods, including pasting email text, uploading files, and integrating directly with your Gmail inbox to fetch and analyze unread messages.

✨ Features
AI-Powered Email Analysis: Utilizes Google Gemini to process email content.

1-Line Summaries: Get a concise overview of any email.

Auto-Reply Suggestions: Receive professionally crafted auto-reply drafts.

Spam/Phishing Detection: Flags emails with a severity score (None, Light, Moderate, High).

Sentiment Analysis: Classifies email sentiment (Neutral, Urgent, Aggressive).

Greeting-Only Detection: Identifies emails that are purely greetings with no links, allowing for automated responses.

Multiple Input Methods:

Paste email content directly into a text area.

Upload .txt files for single emails or .csv files for batch processing (if implemented).

Gmail Integration: Securely fetch and analyze unread emails from your Gmail inbox.

Automated Gmail Auto-Reply: Option to automatically send a suggested auto-reply to detected greeting-only emails.

Security-Focused: API keys are managed securely using Streamlit's st.secrets.

🚀 How It Works
The application uses the google-generativeai library to interact with the gemini-2.0-flash model. When an email is provided (via text input, file upload, or Gmail fetch), the application constructs a prompt for the Gemini model, requesting specific analytical outputs (summary, auto-reply, spam flag, sentiment, greeting check). For Gmail integration, it connects to your IMAP and SMTP servers using Python's imaplib and smtplib to fetch unread messages and, optionally, send replies.

🔧 Prerequisites
Before you begin, ensure you have the following:

Python 3.8+: Installed on your system. We recommend using Anaconda for easy environment management.

Git: Installed and configured on your system (for cloning this repository).

Google Gemini API Key: Obtain one from Google AI Studio.

Gmail Account with App Password: If you plan to use the Gmail integration feature, you'll need:

A Gmail account.

A generated App Password for that Gmail account. This is crucial for security as it allows the app to access your Gmail without using your main Google password. You can generate one in your Google Account Security settings under "2-Step Verification" -> "App passwords."

⚙️ Setup and Installation
Follow these steps to get the Streamlit Email AI Assistant up and running on your local machine:

1. Clone the Repository
Open your Anaconda Prompt (or terminal) and clone this repository. Navigate to the directory where you want to store your project (e.g., C:\Users\aliar\):

cd C:\Users\aliar\
git clone https://github.com/allech01/streamlit-email-ai-assistant.git
cd streamlit-email-ai-assistant

2. Create a Python Virtual Environment (Recommended)
It's good practice to create a virtual environment to manage dependencies for your project.

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Install all the required Python libraries using the requirements.txt file:

pip install -r requirements.txt

4. Configure API Keys Securely
Do NOT hardcode your API keys directly into gemini_app.py! This project uses Streamlit's recommended method for managing secrets via .streamlit/secrets.toml.

a.  Create the .streamlit directory:
From your project root (streamlit-email-ai-assistant), run:
bash mkdir .streamlit 

b.  Create secrets.toml:
Inside the newly created .streamlit folder, create a file named secrets.toml. Open it with a plain text editor (like Notepad, VS Code, etc.) and add your API keys:

```toml
# .streamlit/secrets.toml

gemini_api_key = "YOUR_ACTUAL_GEMINI_API_KEY_GOES_HERE"

# Uncomment and fill this if you want to store your Gmail App Password securely
# gmail_app_password = "YOUR_GMAIL_APP_PASSWORD_GOES_HERE"
```
**Remember to replace `"YOUR_ACTUAL_GEMINI_API_KEY_GOES_HERE"` with your actual Google Gemini API Key.** If you also want to store your Gmail App Password here, uncomment that line and fill it in.

c.  Ensure .gitignore is set up:
Verify that your .gitignore file (located in the project root: streamlit-email-ai-assistant/) contains the following line to prevent your secrets from being uploaded to GitHub:

```gitignore
.streamlit/secrets.toml
```
If you don't have a `.gitignore` yet, create one in the project root and add this line along with other common ignores (see previous discussions if needed).

5. Run the Application
Once all dependencies are installed and secrets are configured, you can run your Streamlit app:

streamlit run gemini_app.py

This command will open the application in your default web browser.

🚀 Usage
Paste Email Content: Simply paste the text of an email into the "Paste Email Content Here:" text area and observe the AI analysis results.

Upload Files:

For a single email: Upload a .txt file containing the email content.

For multiple emails: Upload a .csv file (ensure each row/column contains an email if the app supports batch processing, which you might need to implement further).

Gmail Integration:

Expand the "🔐 Admin Panel & Gmail Integration" section.

Enter your Gmail address and the Gmail App Password you generated.

(Optional) Check "Enable Auto-Reply to Gmail" if you want the app to send automated replies to greeting-only emails.

Click "📬 Fetch Unread Gmail and Analyze" to process your inbox.

🔒 Security Note
Your API keys and sensitive credentials (like Gmail App Passwords) should NEVER be committed directly to your public GitHub repository. This project utilizes Streamlit's st.secrets feature and a .gitignore file to ensure these are kept out of version control. Always follow this best practice for any sensitive information.