from flask import Flask, request, jsonify
from flask_cors import CORS
from JobScrappingAssistant.backend.automation import run_job_search

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "AI Auto Job Search Backend Running"
    })

@app.route("/apply-jobs", methods=["POST"])
def apply_jobs():

    data = request.json

    job_role = data.get("job_role")
    location = data.get("location")

    print(f"Searching jobs for: {job_role} in {location}")

    try:

        result = run_job_search(job_role, location)

        return jsonify(result)

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "message": "Automation failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)