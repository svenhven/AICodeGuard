from flask import Flask, request
from ai_model import CodeAnalyzer

app = Flask(__name__)
analyzer = CodeAnalyzer()

@app.route("/review", methods=["POST"])
def review_code():
    data = request.json
    code = data.get("code", "")
    result = analyzer.analyze(code)
    return {"comment": result}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)