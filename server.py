"""Flask application for emotion detection."""
from flask import Flask, request, jsonify, render_template
from .emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template("index.html")

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """Detects emotion in the provided text."""
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "").strip() if data else ""

    else:
        text = request.args.get("textToAnalyze", "")

    result = emotion_detector(text)

    if result is None or result["dominant_emotion"] is None:
        return jsonify({"error": "Invalid text! Please try again."}), 400

    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    response_message = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({"message": response_message, "result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
