from flask import Flask, render_template, request, session, jsonify
import random
import os

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
        result = "🎉 정답입니다!"
    elif user_guess < target:
        result = "📈 더 높습니다!"
    else:
        result = "📉 더 낮습니다!"

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)