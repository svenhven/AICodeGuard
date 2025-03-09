from flask import Flask, request, jsonify, send_from_directory
from ai_model import CodeAnalyzer

app = Flask(__name__, static_folder="static")  # Pastikan static_folder="static"
analyzer = CodeAnalyzer()

@app.route("/review", methods=["POST"])
def review_code():
    data = request.json
    code = data.get("code", "")
    if not code:
        return jsonify({"error": "Kode tidak ditemukan"}), 400
    
    result = analyzer.analyze(code)
    return jsonify({
        "analysis": result,
        "metadata": {
            "model": "CodeBERT",
            "version": "2.0.0",
            "processed_at": "2025-03-08"
        }
    })

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)