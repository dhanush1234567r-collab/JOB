import json, os, uuid
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
CORS(app)

DATA_DIR = "/data"
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
APPS_FILE = os.path.join(DATA_DIR, "applications.json")
os.makedirs(RESUME_DIR, exist_ok=True)
ALLOWED = {".pdf", ".doc", ".docx"}

jobs = [
    {"id": 1,  "title": "Python Developer",       "company": "Hexaware Technologies", "location": "Chennai",    "type": "Full-time",  "salary": "₹6 LPA"},
    {"id": 2,  "title": "DevOps Engineer",        "company": "Amazon",                "location": "Bangalore",  "type": "Full-time",  "salary": "₹12 LPA"},
    {"id": 3,  "title": "Web Developer",          "company": "Tech India",            "location": "Salem",      "type": "Full-time",  "salary": "₹4 LPA"},
    {"id": 4,  "title": "Java Developer",         "company": "TCS",                   "location": "Chennai",    "type": "Full-time",  "salary": "₹5 LPA"},
    {"id": 5,  "title": "Data Analyst",           "company": "Zoho",                  "location": "Coimbatore", "type": "Full-time",  "salary": "₹6 LPA"},
    {"id": 6,  "title": "React Developer",        "company": "Freshworks",            "location": "Chennai",    "type": "Full-time",  "salary": "₹9 LPA"},
    {"id": 7,  "title": "Python Intern",          "company": "Infosys",               "location": "Bangalore",  "type": "Internship", "salary": "₹15K / month"},
    {"id": 8,  "title": "UI/UX Designer",         "company": "Wipro",                 "location": "Hyderabad",  "type": "Full-time",  "salary": "₹7 LPA"},
    {"id": 9,  "title": "Software Tester",        "company": "Cognizant",             "location": "Chennai",    "type": "Full-time",  "salary": "₹4.5 LPA"},
    {"id": 10, "title": "Web Dev Intern",         "company": "Startup Hub",           "location": "Salem",      "type": "Internship", "salary": "₹10K / month"},
    {"id": 11, "title": "Cloud Engineer",         "company": "HCL Technologies",      "location": "Noida",      "type": "Full-time",  "salary": "₹10 LPA"},
    {"id": 12, "title": "Backend Engineer",       "company": "Paytm",                 "location": "Noida",      "type": "Full-time",  "salary": "₹14 LPA"},
    {"id": 13, "title": "Cyber Security Analyst", "company": "Capgemini",             "location": "Chennai",    "type": "Full-time",  "salary": "₹8 LPA"},
    {"id": 14, "title": "Data Science Intern",    "company": "Mu Sigma",              "location": "Bangalore",  "type": "Internship", "salary": "₹20K / month"},
    {"id": 15, "title": "Site Reliability Eng.",  "company": "Flipkart",              "location": "Bangalore",  "type": "Full-time",  "salary": "₹18 LPA"},
    {"id": 16, "title": "Network Engineer",       "company": "Tech Mahindra",         "location": "Madurai",    "type": "Full-time",  "salary": "₹5 LPA"},
    {"id": 17, "title": "Mobile App Developer",   "company": "Ideas2IT",              "location": "Trichy",     "type": "Full-time",  "salary": "₹7 LPA"},
    {"id": 18, "title": "QA Intern",              "company": "Kaar Technologies",     "location": "Coimbatore", "type": "Internship", "salary": "₹12K / month"},
    {"id": 19, "title": "AWS Cloud Engineer",     "company": "ABC Technologies",      "location": "Pune",       "type": "Full-time",  "salary": "₹11 LPA"},
    {"id": 20, "title": "Business Analyst",       "company": "Accenture",             "location": "Mumbai",     "type": "Full-time",  "salary": "₹9 LPA"},
]

def load_apps():
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_apps(apps):
    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

@app.route("/api/jobs")
def get_jobs():
    return jsonify(jobs)

@app.route("/api/apply/<int:job_id>", methods=["POST"])
def apply(job_id):
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    cover = request.form.get("cover_letter", "").strip()
    resume = request.files.get("resume")

    if not name or not email or not phone:
        return jsonify({"message": "Name, email, phone required"}), 400
    if not resume or not resume.filename:
        return jsonify({"message": "Resume upload pannunga"}), 400

    ext = os.path.splitext(resume.filename)[1].lower()
    if ext not in ALLOWED:
        return jsonify({"message": "Resume PDF / DOC / DOCX mattum"}), 400

    saved_name = f"{uuid.uuid4().hex}_{secure_filename(resume.filename)}"
    resume.save(os.path.join(RESUME_DIR, saved_name))

    apps = load_apps()
    apps.append({
        "job_id": job_id, "job": job["title"], "company": job["company"],
        "name": name, "email": email, "phone": phone,
        "cover_letter": cover, "resume": saved_name,
        "applied_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_apps(apps)
    return jsonify({"message": f"Applied to {job['title']} at {job['company']}"})

@app.route("/api/applications")
def applications():
    return jsonify(load_apps())

@app.route("/api/resumes/<path:filename>")
def resume_file(filename):
    return send_from_directory(RESUME_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
