# 📚 Chat with PDF

A fully local Streamlit app that lets you upload PDF files and chat with them using an LLM.  
Supports Google Gemini

🗂️ Project Structure


CLAUDEPDF/
├── app.py               Main Streamlit application
├── html_templates.py    SS and HTML templates
├── requirements.txt     Python dependencies
├── .env                 .env and add your API key
├── Dockerfile
├── .dockerignore
└── README.md



## 🚀 Quick Start

### 1. Clone / download the project

in CMD 
cd CLAUDEPDF


### 2. Create a virtual environment

```cmd
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Set up your API key

```cmd
cp .env.example .env
```

Open `.env` and fill in gemini 2.5 flashAPI of:

```env
Google Gemini (free tier available → https://aistudio.google.com/apikey)
GOOGLE_API_KEY=your_key_here

```

### 5. Run the app

```cmd
streamlit run app.py
```



## Getting a Free Google Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click Create API key
4. Copy it into your .env file

No credit card required for the free tier.



## 🧠 How It Works


PDF upload
   ↓
Extract text  (PyPDF2)
   ↓
Split into chunks  (RecursiveCharacterTextSplitter)
   ↓
Embed chunks  (Gemini / OpenAI embeddings)
   ↓
Store in FAISS vector index  (in-memory, local)
   ↓
User asks question
   ↓
Retrieve top-4 relevant chunks  (semantic search)
   ↓
LLM generates answer with chat memory
   ↓
Display in chat UI




## Tips

- Works best with text based PDFs (not scanned images)
- You can upload multiple PDFs at once all be searchable together
- The conversation has memory follow up questions work naturally
- Click Clear conversation in the sidebar to start fresh
