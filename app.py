from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "navi_secret_key"

@app.route("/")
def index():
    session["target"] = random.randint(1, 100)
    session["attempts"] = 0
    session["ai_low"] = 1
    session["ai_high"] = 100
    session["ai_attempts"] = 0
    return render_template("index.html")

@app.route("/guess", methods=["POST"])
def guess():
    user_guess = int(request.json["guess"])
    target = session["target"]
    session["attempts"] += 1

    if user_guess == target:
        result = "정답이랑깨 잘했다부러!"
    elif user_guess < target:
        result = "더 높아 잘맞춰봐!"
    else:
        result = "낮다니까 잘혀봐!"

    # AI 이진 탐색
    ai_guess = (session["ai_low"] + session["ai_high"]) // 2
    session["ai_attempts"] += 1

    if ai_guess == target:
        ai_result = "🤖 AI 정답!"
    elif ai_guess < target:
        session["ai_low"] = ai_guess + 1
        ai_result = "더 높음"
    else:
        session["ai_high"] = ai_guess - 1
        ai_result = "더 낮음"

    game_over = False
    winner = ""

    if user_guess == target:
        game_over = True
        winner = "🎉 당신 승리!"
    elif ai_guess == target:
        game_over = True
        winner = "🤖 AI 승리!"
    elif session["attempts"] >= 7:
        game_over = True
        winner = f"❌ 실패! 정답은 {target}"

    return jsonify({
        "result": result,
        "ai_guess": ai_guess,
        "ai_result": ai_result,
        "attempts": session["attempts"],
        "ai_attempts": session["ai_attempts"],
        "game_over": game_over,
        "winner": winner
    })

if __name__ == "__main__":
    app.run(port=5001, debug=False)