from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
#CORS(app)  # Allow cross-origin requests from student browsers

# Game state
prompts = [
    "Invent a terrible new superhero power.",
    "Name a sequel to a movie that shouldn’t exist.",
    "Describe the worst possible flavor of ice cream.",
    "A new law that nobody would follow.",
    "The next big TikTok trend that everyone will hate.",
    "Name a new mythical creature.",
    "Write the title of a book nobody should read.",
    "Describe an invention that makes life slightly worse.",
    "A new holiday that makes no sense.",
    "Create the worst possible app idea.",
    "Come up with a ridiculous slogan for a made-up company.",
    "Invent the worst sports team mascot ever.",
    "Write a tagline for a fake reality TV show.",
    "A phrase that would go viral on social media for all the wrong reasons.",
    "Name a villain that no hero could ever beat."
]

def get_random_prompt():
    return random.choice(prompts)


current_prompt = ""
submissions = []
team_scores = {}
current_prompt = get_random_prompt()

@app.route("/prompt", methods=["GET"])
def get_prompt():
    return jsonify({"prompt": current_prompt})

@app.route("/submit", methods=["POST"])
def submit_answer():
    global submissions
    data = request.json
    team = data.get("team")
    answer = data.get("answer")
    if not team or not answer:
        return jsonify({"error": "Missing team or answer"}), 400
    submissions.append({"team": team, "answer": answer})
    return jsonify({"status": "ok", "message": "Answer received!"})

@app.route("/submissions", methods=["GET"])
def get_submissions():
    shuffled = submissions.copy()
    random.shuffle(shuffled)
    return jsonify(shuffled)

@app.route("/reset", methods=["POST"])
def reset_round():
    global current_prompt, submissions
    current_prompt = get_random_prompt()
    submissions = []
    return jsonify({"status": "ok", "prompt": current_prompt})

@app.route("/vote", methods=["POST"])
def vote_winner():
    data = request.form
    winning_team = data.get("team")
    if not winning_team:
        return jsonify({"error": "Missing team"}), 400
    team_scores[winning_team] = team_scores.get(winning_team, 0) + 1
    return jsonify({"status": "ok", "team_scores": team_scores})

@app.route("/scores", methods=["GET"])
def get_scores():
    return jsonify(team_scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
