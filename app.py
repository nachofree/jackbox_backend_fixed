from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
#CORS(app)  # Allow cross-origin requests from student browsers

# Game state
prompts = [
    {"id": 1, "text": "Write a haiku about debugging code.", "category": "creative"},
    {"id": 2, "text": "Invent the worst possible variable name.", "category": "humor"},
    {"id": 3, "text": "Write an error message that would terrify a developer.", "category": "humor"},
    {"id": 4, "text": "Pitch a startup idea in one sentence.", "category": "pitch"},
    {"id": 5, "text": "Describe JavaScript in exactly 5 words.", "category": "creative"},
    {"id": 6, "text": "Suggest a new name for Python.", "category": "humor"},
    {"id": 7, "text": "Invent a new programming language slogan.", "category": "creative"},
    {"id": 8, "text": "What would be the mascot for a new language?", "category": "creative"},
    {"id": 9, "text": "Describe Git in one emoji.", "category": "humor"},
    {"id": 10, "text": "Write a fake commit message.", "category": "humor"},
    {"id": 11, "text": "What’s the worst feature a framework could add?", "category": "humor"},
    {"id": 12, "text": "Name a programming language after a food.", "category": "creative"},
    {"id": 13, "text": "Describe cloud computing to a caveman.", "category": "pitch"},
    {"id": 14, "text": "Write a funny 404 page message.", "category": "humor"},
    {"id": 15, "text": "If HTML was a person, describe them.", "category": "creative"},
    {"id": 16, "text": "Invent a new tech company name.", "category": "pitch"},
    {"id": 17, "text": "Write a single line that sums up coding.", "category": "creative"},
    {"id": 18, "text": "Describe recursion without using the word recursion.", "category": "creative"},
    {"id": 19, "text": "What’s the funniest bug you can imagine?", "category": "humor"},
    {"id": 20, "text": "Suggest the best possible team name for a hackathon.", "category": "creative"},
]


def get_random_prompt():
    return random.choice(prompts)


current_prompt = ""
submissions = []
team_scores = {}
current_prompt = get_random_prompt()

@app.route("/prompt", methods=["GET"])
def get_prompt():
    return jsonify(current_prompt), {"Access-Control-Allow-Origin":"*"}

@app.route("/submit", methods=["POST"])
def submit_answer():
    print(request.form)
    global submissions
    team = request.form['team']
    answer = request.form['answer']
    if not team or not answer:
        return jsonify({"error": "Missing team or answer"}), 400, {"Access-Control-Allow-Origin":"*"}
    submissions.append({"team": team, "answer": answer})
    return jsonify({"status": "ok", "message": "Answer received!"}), {"Access-Control-Allow-Origin":"*"}

@app.route("/submissions", methods=["GET"])
def get_submissions():
    shuffled = submissions.copy()
    random.shuffle(shuffled)
    return jsonify(shuffled), {"Access-Control-Allow-Origin":"*"}

@app.route("/reset", methods=["POST"])
def reset_round():
    global current_prompt, submissions
    current_prompt = get_random_prompt()
    submissions = []
    return jsonify({"status": "ok", "prompt": current_prompt}), {"Access-Control-Allow-Origin":"*"}

@app.route("/vote", methods=["POST"])
def vote_winner():
    winning_team = request.form["team"]
    if not winning_team:
        return jsonify({"error": "Missing team"}), 400
    team_scores[winning_team] = team_scores.get(winning_team, 0) + 1
    return jsonify({"status": "ok", "team_scores": team_scores}), {"Access-Control-Allow-Origin":"*"}

@app.route("/scores", methods=["GET"])
def get_scores():
    return jsonify(team_scores), {"Access-Control-Allow-Origin":"*"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
