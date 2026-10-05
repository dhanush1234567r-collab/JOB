from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Job Portal Backend is Running!"

@app.route("/jobs")
def jobs():
    return jsonify([
        {"title": "Python Developer", "location": "Chennai"},
        {"title": "AWS DevOps Engineer", "location": "Bangalore"},
        {"title": "Web Developer", "location": "Coimbatore"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
