
# 🧠 Gabriel's Mind: AI Study Tool

**Gabriel's Mind** is a free AI-powered study tool that helps you deeply engage with your own eBooks, PDFs, or study materials.

It allows you to:
- Upload your documents.
- Ask questions about the content.
- Generate flashcards and quizzes.
- Practice in multiple languages.
- Listen to answers with text-to-speech.

> This tool is not for searching the internet — it helps you learn and test yourself **based on the documents you upload.**

## Features

✅ Upload and preview your PDF file page by page.  
✅ AI Assistant: Ask questions about the document.  
✅ Auto-generated Flashcards and Multiple-Choice Quizzes.  
✅ Listen to AI answers and flashcards with audio playback.  
✅ Supports multiple languages:
- English
- Portuguese
- Spanish
- French
- Italian
- Polish
- Dutch

## 🚀 How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/gabrielsmind.git
cd gabrielsmind
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run gabrielsmind.py
```

## OpenAI API Key

- When you run the app, it will ask you to paste your **OpenAI API Key** securely into the sidebar.
- Get your API key from: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

**Note:** The key is not hardcoded for security reasons.

## How to Add Your PDFs

1. Run the app.
2. Use the **"Upload PDF"** button inside the interface.
3. Your document will be processed automatically.

## Audio Playback

- Uses **Google Text-to-Speech (gTTS)** to read out loud the AI answers and flashcards.
- Language detection for speech is based on your chosen output language.

## Built With

| Tool/Library          | Purpose                        |
|-----------------------|--------------------------------|
| Streamlit             | Web Interface                 |
| LangChain + OpenAI    | Document-based Q&A, Quiz, Flashcards |
| PyMuPDF               | PDF Viewer and Page Handling  |
| gTTS                  | Text-to-Speech Audio          |
| deep-translator       | Multilingual Translation      |

## License

MIT License — Free to use, modify, and share.

## 💡 Contributions Welcome!

Feel free to open issues or submit pull requests if you want to improve the project.

## Stay curious, learn smarter, and enjoy your study journey with **Gabriel's Mind AI Study tool** 🧠✨.
