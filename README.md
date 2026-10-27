# 📄 Resume Keyword Extractor

A web-based application that extracts useful information, skills, qualifications, education, and keywords from uploaded resumes. The application supports PDF, DOCX, and TXT files and presents the extracted information in a structured, user-friendly format.

## 🌐 Live Demo

**Try the application here:**

🚀 https://resume-keyword-extractor-za5t.onrender.com

**GitHub Repository:**
https://github.com/Manju2016/Resume-Keyword-Extractor

---

## 📌 Project Overview

Resume Keyword Extractor is a Python-based web application designed to simplify the process of identifying important information from resumes.

Users can upload their resumes and view extracted information without manually searching through the entire document. The application processes the uploaded file, extracts its text, identifies relevant information using a rule-based extraction approach, and displays the results on a dedicated results page.

The project demonstrates document processing, text extraction, web development, and report generation using Python.

## ✨ Features

* 📤 **Resume Upload:** Upload resumes through a simple web interface.
* 📁 **Multiple File Formats:** Supports PDF, DOCX, and TXT files.
* 📝 **Text Extraction:** Extracts text from uploaded documents.
* 🧠 **Keyword Extraction:** Identifies relevant skills, qualifications, education, and other information using rule-based processing.
* 📊 **Structured Results:** Displays extracted information in an organized format.
* 📥 **JSON Export:** Download extracted results as a JSON report.
* 📈 **CSV Export:** Download extracted results as a CSV report.
* 💻 **Web Interface:** Provides an interactive interface built with HTML, CSS, and JavaScript.
* ☁️ **Online Deployment:** Hosted on Render for access through a web browser.

## 🛠️ Technologies Used

| Technology     | Purpose                                 |
| -------------- | --------------------------------------- |
| Python         | Core application logic                  |
| Flask          | Backend web framework                   |
| PyMuPDF        | PDF text extraction                     |
| python-docx    | DOCX document processing                |
| HTML5          | Webpage structure                       |
| CSS3           | Styling and layout                      |
| JavaScript     | Frontend interactions                   |
| JSON           | Structured report export                |
| CSV            | Tabular report export                   |
| Git and GitHub | Version control and source code hosting |
| Render         | Application deployment                  |

## ⚙️ How It Works

1. The user opens the application.
2. The user uploads a resume in PDF, DOCX, or TXT format.
3. The backend processes the uploaded file.
4. Text is extracted from the document.
5. The keyword extraction component identifies relevant information.
6. The application displays the extracted results.
7. The user can download the results in JSON or CSV format.

## 🖥️ Application Workflow

**Resume Upload → Text Extraction → Keyword Processing → Results Display → Report Download**

## 📂 Project Structure

```text
Resume-Keyword-Extractor/
│
├── app.py
├── resume_parser.py
├── keyword_extractor.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── results.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
```

### File Description

* `app.py` — Flask application, routing, result handling, and report downloads.
* `resume_parser.py` — Extracts text from supported resume formats.
* `keyword_extractor.py` — Processes extracted text and identifies relevant keywords and information.
* `requirements.txt` — Lists the Python dependencies.
* `templates/index.html` — Main resume upload page.
* `templates/results.html` — Displays extracted results and download options.
* `static/css/style.css` — Application styling.
* `static/js/script.js` — Frontend interactions.
* `.gitignore` — Excludes virtual environments, temporary files, and other files that should not be committed.

## 🚀 Run the Project Locally

Follow these steps to run the application on your computer.

### Prerequisites

Install the following:

* Python
* Git
* Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Manju2016/Resume-Keyword-Extractor.git
```

### 2. Open the Project Folder

```bash
cd Resume-Keyword-Extractor
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows Command Prompt:**

```bash
.venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the Application

```bash
python app.py
```

### 7. Open the Website

Open your browser and visit:

http://127.0.0.1:5000

The application should now be available locally.

## 📤 Supported File Formats

| Format        | Extension | Purpose                        |
| ------------- | --------- | ------------------------------ |
| PDF           | `.pdf`    | Extract text from PDF resumes  |
| Word Document | `.docx`   | Extract text from Word resumes |
| Text File     | `.txt`    | Process plain-text resumes     |

## 📥 Export Options

The application provides two report formats:

* **JSON:** Useful for storing and processing structured resume information programmatically.
* **CSV:** Useful for viewing extracted information in spreadsheet applications that support CSV files.

## 🔍 Current Implementation

The current version uses document text extraction and rule-based keyword processing to identify relevant information from resumes.

It demonstrates a practical document-processing workflow, combining a Python backend with a browser-based interface and downloadable reports.

## ⚠️ Limitations

* Keyword extraction depends on the implemented rules and patterns.
* Resume layouts and formatting can affect text extraction.
* Scanned PDFs may require OCR support to extract text reliably.
* Extracted information may need manual verification.
* The current version does not use a trained machine-learning model for keyword extraction.
* Application results may not persist after a server restart because the current implementation uses in-memory storage.

## 🔮 Future Enhancements

Potential improvements include:

* NLP-based skill and entity extraction.
* Support for additional resume formats.
* OCR integration for scanned resumes.
* Resume-to-job-description matching.
* Job-specific keyword analysis.
* Improved extraction of education, experience, and certifications.
* Database integration for persistent storage.
* User authentication and secure document management.
* More comprehensive validation and automated testing.

## 🎯 Project Objectives

* Simplify resume information extraction.
* Demonstrate document parsing using Python.
* Build a web application using Flask.
* Present extracted information in a structured format.
* Support downloadable reports.
* Practice version control and application deployment.

## 👨‍💻 Author

**Manjunath Sunil**

B.Tech — Artificial Intelligence and Machine Learning

### Project Links

* **Live Application:** https://resume-keyword-extractor-za5t.onrender.com
* **GitHub Repository:** https://github.com/Manju2016/Resume-Keyword-Extractor

## 📜 License

This project is available for educational and portfolio purposes. A formal open-source license has not been specified yet.

---

⭐ If you find this project interesting, consider exploring the repository and its implementation.
