<div align="center"> <img src="deepseek-color.png" alt="DeepSeek Logo" width="80" height="80"> <h1>DeepSeek AI File Assistant</h1> </div>


A smart document management tool that uses DeepSeek AI to analyze documents (PDF, DOCX, images) and generate meaningful filenames. Perfect for candidates applying for job as it name your resume/coverletter according to HR/Recruitment Standards & Practices, it automatically extracts key information like names, job titles, and companies to organize files intelligently.

## 🚀 Features

- **Smart Document Analysis**: Powered by DeepSeek-R1 AI model
- **Multi-Format Support**: Process PDF, DOCX, and image files
- **OCR Capabilities**: Extract text from scanned documents and images
- **Intelligent Naming**: Generate context-aware filename suggestions
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI
- **Secure**: Uses Together.ai API for secure AI processing

## 📋 Prerequisites

- Python 3.8+
- Together.ai API key ([Get one here](https://together.ai))
- Tesseract OCR installed on your system

## 🛠️ Installation

1. Clone the repository:

`git clone https://github.com/yourusername/deepseek-ai-file-assistant.git`

`cd deepseek-ai-file-assistant`

2. Install required packages:
bash
pip install -r requirements.txt

3. Install Tesseract OCR:
- **Windows**: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 🚀 Usage

1. Start the application:
`streamlit run app.py`
2. Enter your Together.ai API key in the sidebar
3. Upload a document (PDF, DOCX, or image)
4. Choose from suggested filenames or customize your own
5. Download the renamed file

## 💡 Supported File Types

- PDF documents (`.pdf`)
- Word documents (`.docx`)
- Images (`.png`, `.jpg`, `.jpeg`)

## 🔒 Security

- API keys are handled securely and never stored
- Files are processed locally
- No data is permanently stored

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [DeepSeek AI](https://deepseek.ai) for their powerful AI model
- [Together.ai](https://together.ai) for API services
- [Streamlit](https://streamlit.io) for the web interface framework

## 📧 Contact

Project Link: [https://github.com/fahadyaseen001/deepseek-ai-file-assistant]
