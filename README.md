# Resume Keyword Extractor

A web-based resume analysis application built with Python, Flask, HTML, CSS, and JavaScript. It extracts useful information from uploaded resumes and presents the results in a clean, user-friendly interface.

## Overview

The Resume Keyword Extractor helps users identify skills, educational qualifications, certifications, and technical keywords from their resumes.

Users can upload a supported resume file, review the extracted information on a separate results page, view the extracted text, and download the analysis report in JSON or CSV format.

## Features

* **Resume Upload:** Upload PDF, DOCX, and TXT resumes.
* **Text Extraction:** Extract readable text from supported documents.
* **Skill Extraction:** Identify skills using predefined categories and matching rules.
* **Education Analysis:** Extract educational qualifications from resume content.
* **Certification Extraction:** Identify certifications listed under recognized resume sections.
* **Technical Keywords:** Display technical terms identified in the resume.
* **Results Dashboard:** Present extracted information in a structured interface.
* **Resume Text Preview:** View the text extracted from the uploaded document.
* **JSON Report:** Download the analysis results as a JSON file.
* **CSV Report:** Export the analysis results to a CSV file that can be opened in spreadsheet applications.
* **File Validation:** Restrict uploads to supported file extensions and a maximum file size of 10 MB.
* **Responsive Interface:** Use the application through a modern web interface.

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Lucide Icons

### Backend

* Python
* Flask

### Document Processing

* PyMuPDF for PDF text extraction
* python-docx for DOCX document processing
* Python text-processing and keyword-matching logic

### Deployment

* GitHub for source code management
* Render for web application hosting

## Project Structure

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

## Getting Started

### Prerequisites

Install the following software:

* Python 3
* Visual Studio Code
* Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/Resume-Keyword-Extractor.git
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username.

### 2. Open the project directory

```bash
cd Resume-Keyword-Extractor
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open the local address displayed in your terminal, usually:

```text
http://127.0.0.1:5000
```

### 7. Analyze a resume

1. Open the application.
2. Upload a PDF, DOCX, or TXT resume.
3. Submit the file for analysis.
4. Review the extracted skills, qualifications, certifications, and technical keywords.
5. Preview the extracted resume text.
6. Download the report in JSON or CSV format.

## Deployment

This application can be deployed as a Flask web service on Render.

Recommended configuration:

* **Runtime:** Python 3
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`

Connect the GitHub repository to Render and deploy the application using these settings.

## Limitations

* The current application uses rule-based text extraction and keyword matching; it is not a trained machine learning model.
* Extraction accuracy depends on the document's text quality and formatting.
* Scanned PDFs and image-only documents may require OCR before their text can be extracted.
* The extractor does not guarantee that every skill, qualification, or certification will be identified correctly.
* Extracted information should be reviewed by the user.
* Analysis results are currently stored in server memory and may be lost when the application restarts.
* This prototype is not intended to make hiring decisions or automatically determine a candidate's suitability for a job.

## Future Improvements

* Add OCR support for scanned resumes.
* Improve section detection and extraction accuracy.
* Support additional document formats.
* Add job-description matching and skill-gap analysis.
* Improve the extraction of experience, projects, and contact details.
* Introduce persistent storage with appropriate privacy controls.
* Add automated tests and more robust error handling.

## Privacy

Resumes can contain personal information. Do not upload confidential documents to a public repository or use real resumes as test data without appropriate permission.

The current prototype uses in-memory result storage rather than a persistent database. Review its data handling and deployment configuration before using it with sensitive information.

## Disclaimer

This project is an educational software prototype intended to demonstrate document processing, text extraction, keyword matching, and web application development. Results may be incomplete or inaccurate and should be verified by the user.

## Author

**Manjunath Sunil**

B.Tech — Artificial Intelligence and Machine Learning

GitHub: https://github.com/Manju2016



If you find this project useful, feel free to explore the source code and suggest improvements.
