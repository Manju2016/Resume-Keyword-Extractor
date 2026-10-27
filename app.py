import csv
import io
import json
import secrets

from flask import Flask, render_template, request, jsonify, Response

from resume_parser import extract_resume_text

from keyword_extractor import (
    extract_keywords,
    extract_qualifications,
    extract_resume_details
)



app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Temporary storage for extracted results.
# The uploaded resume itself is not stored.
results_store = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/results")
def results():
    result_key = request.args.get("key")
    results_data = results_store.get(result_key) if result_key else None

    return render_template(
        "results.html",
        results_data=results_data
    )


@app.route("/extract", methods=["POST"])
def extract():
    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "error": "Please select a resume."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    try:
        # Read the uploaded resume
        text = extract_resume_text(file)

        # Extract skills and other resume details
        skills = extract_keywords(text)
        qualifications = extract_qualifications(text)
        details = extract_resume_details(text)

        # Generate a temporary results key
        result_key = secrets.token_urlsafe(16)

        # Store the extracted results
        results_store[result_key] = {
            "filename": file.filename,
            "status": "complete",
            "skills": skills,
            "unverified": [],
            "qualifications": qualifications,
            "education": details["education"],
            "certifications": details["certifications"],
            "keywords": details["keywords"],
            "contact": details["contact"],
            "experience": details["experience"],
            "internships": details["internships"],
            "projects": details["projects"],
            "word_count": len(text.split()),
            "text": text
        }

        return jsonify({
            "success": True,
            "redirect": f"/results?key={result_key}"
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Resume extraction failed")

        return jsonify({
            "success": False,
            "error": "Could not process this resume. Please try another file."
        }), 500



@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "success": False,
        "error": "The file exceeds the 10 MB limit."
    }), 413

@app.route("/download")
def download():
    result_key = request.args.get("key")
    file_format = request.args.get("format", "json").lower()

    data = results_store.get(result_key) if result_key else None

    if not data:
        return jsonify({
            "success": False,
            "error": "Results not found. Please upload your resume again."
        }), 404

    if file_format == "json":
        report = json.dumps(data, indent=4, ensure_ascii=False)

        return Response(
            report,
            mimetype="application/json",
            headers={
                "Content-Disposition":
                    "attachment; filename=resume_analysis.json"
            }
        )

    elif file_format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["Category", "Extracted Details"])

        for category, value in data.items():
            if isinstance(value, dict):
                for subcategory, items in value.items():
                    writer.writerow([
                        f"{category} - {subcategory}",
                        ", ".join(map(str, items))
                        if isinstance(items, list)
                        else str(items)
                    ])

            elif isinstance(value, list):
                writer.writerow([
                    category,
                    ", ".join(map(str, value))
                ])

            else:
                writer.writerow([category, str(value)])

        return Response(
            "\ufeff" + output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={
                "Content-Disposition":
                    "attachment; filename=resume_analysis.csv"
            }
        )

    return jsonify({
        "success": False,
        "error": "Unsupported format. Choose JSON or CSV."
    }), 400
if __name__ == "__main__":
    app.run(debug=True)
