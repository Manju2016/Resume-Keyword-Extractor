import re


SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript",
        "C", "C++", "C#", "SQL", "R", "PHP", "Cython"
    ],
    "AI and Machine Learning": [
        "Artificial Intelligence", "Machine Learning",
        "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Neural Networks",
        "Generative AI", "Large Language Models",
        "Reinforcement Learning", "Transfer Learning",
        "Feature Engineering", "Model Evaluation",
        "Classification", "Regression", "Clustering"
    ],
    "Frameworks and Libraries": [
        "Flask", "Django", "FastAPI", "React",
        "Angular", "Node.js", "TensorFlow", "PyTorch",
        "Keras", "Scikit-learn", "Pandas", "NumPy",
        "Matplotlib", "OpenCV", "spaCy", "NLTK",
        "Bootstrap", "Spring Boot"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite",
        "Oracle", "Redis", "SQL Server", "Firebase"
    ],
    "Developer Tools": [
        "Git", "GitHub", "Docker", "Kubernetes",
        "Linux", "Jupyter Notebook", "Google Colab",
        "Visual Studio Code", "VS Code", "AWS",
        "Azure", "Google Cloud", "Jenkins", "Postman"
    ],
    "Web Technologies": [
        "HTML", "CSS", "REST API", "RESTful API",
        "JSON", "XML", "AJAX", "Tailwind CSS"
    ],
    "Data and Analytics": [
        "Data Analysis", "Data Science",
        "Data Visualization", "Power BI", "Tableau",
        "Microsoft Excel", "Statistics", "ETL"
    ],
    "Soft Skills": [
        "Communication", "Teamwork", "Leadership",
        "Problem Solving", "Critical Thinking",
        "Time Management", "Adaptability",
        "Collaboration", "Project Management"
    ]
}


def contains_term(text, term):
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_keywords(text):
    results = {}

    for category, terms in SKILL_CATEGORIES.items():
        found = []

        for term in terms:
            if contains_term(text, term):
                found.append(term)

        if found:
            results[category] = sorted(set(found), key=str.lower)

    return results


def extract_qualifications(text):
    patterns = [
        r"\bB.?\s?Tech\b",
        r"\bB.?\s?E.?\b",
        r"\bM.?\s?Tech\b",
        r"\bM.?\s?E.?\b",
        r"\bBCA\b",
        r"\bMCA\b",
        r"\bB.?\s?Sc\b",
        r"\bM.?\s?Sc\b",
        r"\bMBA\b",
        r"\bPh.?\s?D.?\b",
        r"\bBachelor(?:'s)?\b",
        r"\bMaster(?:'s)?\b",
        r"\bDiploma\b"
    ]

    found = []

    for pattern in patterns:
        found.extend(re.findall(pattern, text, re.IGNORECASE))

    return sorted(set(item.strip() for item in found), key=str.lower)


def extract_education(text):
    """Extract education entries from a resume."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    education_headers = {
        "education",
        "educational qualification",
        "academic qualification",
        "academic background"
    }

    stop_headers = {
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "technical skills",
        "skills",
        "certifications",
        "certificates",
        "achievements",
        "references"
    }

    education_lines = []
    inside_education = False

    for line in lines:
        normalized = re.sub(r"[:\s]+$", "", line.lower()).strip()

        if normalized in education_headers:
            inside_education = True
            continue

        if inside_education and normalized in stop_headers:
            break

        if inside_education:
            education_lines.append(line)

    if not education_lines:
        education_lines = [
            line for line in lines
            if any(
                contains_term(line, degree)
                for degree in [
                    "B.Tech", "B.E.", "M.Tech", "M.E.",
                    "BCA", "MCA", "B.Sc", "M.Sc",
                    "MBA", "Bachelor", "Master", "Diploma"
                ]
            )
        ]

    results = []

    for line in education_lines:
        degree_matches = extract_qualifications(line)

        if not degree_matches:
            continue

        year_match = re.search(r"\b(?:19|20)\d{2}\b", line)

        score_match = re.search(
            r"\b(?:CGPA|GPA|percentage|percent|marks)\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?\s*%?)",
            line,
            re.IGNORECASE
        )

        results.append({
            "degree": ", ".join(degree_matches),
            "institution": "",
            "year": year_match.group(0) if year_match else "",
            "details": line
        })

    return results



def extract_certifications(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    start_headers = {
        "certification",
        "certifications",
        "certificate",
        "certificates",
        "licenses and certifications",
        "certifications and courses",
        "courses and certifications",
        "professional certifications",
        "training and certifications"
    }

    stop_headers = {
        "education",
        "experience",
        "work experience",
        "professional experience",
        "internships",
        "projects",
        "skills",
        "technical skills",
        "achievements",
        "references",
        "languages",
        "interests"
    }

    results = []
    inside_section = False

    for line in lines:
        heading = re.sub(r"[:\s]+$", "", line.lower()).strip()

        if heading in start_headers:
            inside_section = True
            continue

        if inside_section and heading in stop_headers:
            break

        if inside_section:
            cleaned = re.sub(r"^[•●▪\-*]\s*", "", line).strip()

            if cleaned:
                results.append(cleaned)

    return list(dict.fromkeys(results))




def extract_section(text, section_names, stop_names):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    collected = []
    inside_section = False

    normalized_names = {name.lower() for name in section_names}
    normalized_stops = {name.lower() for name in stop_names}

    for line in lines:
        heading = re.sub(r"[:\s]+$", "", line.lower()).strip()

        if heading in normalized_names:
            inside_section = True
            continue

        if inside_section and heading in normalized_stops:
            break

        if inside_section:
            collected.append(line)

    return collected


def extract_contact_details(text):
    email_match = re.search(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        text,
        re.IGNORECASE
    )

    phone_match = re.search(
        r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?"
        r"(?:\(?\d{3,5}\)?[-.\s]?)?\d{5,10}(?!\w)",
        text
    )

    urls = re.findall(
        r"(?:https?://)?(?:www\.)?"
        r"(?:linkedin\.com|github\.com)/[^\s,;]+",
        text,
        re.IGNORECASE
    )

    return {
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0).strip() if phone_match else "",
        "links": list(dict.fromkeys(urls))
    }


def extract_resume_details(text):
    stop_headers = [
        "education",
        "experience",
        "work experience",
        "professional experience",
        "internships",
        "projects",
        "technical skills",
        "skills",
        "certifications",
        "certificates",
        "achievements",
        "references"
    ]

    education = extract_education(text)

    experience = extract_section(
        text,
        ["experience", "work experience", "professional experience"],
        stop_headers + ["experience"]
    )

    internships = extract_section(
        text,
        ["internships", "internship experience"],
        stop_headers + ["internships"]
    )

    projects = extract_section(
        text,
        ["projects", "academic projects", "personal projects"],
        stop_headers + ["projects"]
    )

    contact = extract_contact_details(text)

    keywords = [
        {"term": keyword, "source": category}
        for category, terms in extract_keywords(text).items()
        for keyword in terms
    ]

    return {
        "contact": contact,
        "education": education,
        "experience": experience,
        "internships": internships,
        "projects": projects,
        "certifications": extract_certifications(text),
        "keywords": keywords
    }

