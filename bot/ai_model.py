from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os
import uuid

class CodeAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base")
        self.max_length = 512
        self.output_dir = "static"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_heatmap(self, code_snippet, quality_score, issues):
        lines = code_snippet.split('\n')
        scores = [quality_score / 100] * len(lines)
        for i, line in enumerate(lines):
            if len(line) > 120:
                scores[i] = max(scores[i] - 0.2, 0)
            if re.search(r"eval\(|exec\(", line):
                scores[i] = max(scores[i] - 0.4, 0)
            if re.search(r"range\(.{0,10}1000", line):
                scores[i] = max(scores[i] - 0.3, 0)

        plt.figure(figsize=(10, len(lines) * 0.5 + 1))
        sns.heatmap(
            [scores],
            annot=[scores],
            cmap="RdYlGn",
            cbar=True,
            fmt='.2f',
            yticklabels=[f"L{i+1}: {line[:30]}..." for i, line in enumerate(lines)],
            xticklabels=[]
        )
        plt.title("Heatmap Kualitas Kode (0.0 = Buruk, 1.0 = Baik)", pad=20)
        plt.tight_layout()

        image_id = str(uuid.uuid4())
        image_path = os.path.join(self.output_dir, f"{image_id}.png")
        plt.savefig(image_path, bbox_inches='tight', dpi=100)
        plt.close()
        return image_path

    def analyze(self, code_snippet):
        inputs = self.tokenizer(code_snippet, return_tensors="pt", truncation=True, max_length=self.max_length)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1).tolist()[0]
            prediction = torch.argmax(outputs.logits, dim=1).item()

        base_score = 100 if prediction == 0 else 50
        issues, suggestions = [], []
        lines = code_snippet.split('\n')
        if any(len(line) > 120 for line in lines):
            issues.append("Baris kode terlalu panjang (>120 karakter)")
            suggestions.append("Pisah jadi beberapa baris")
            base_score -= 20
        if re.search(r"eval\(|exec\(", code_snippet):
            issues.append("Penggunaan eval/exec berisiko")
            suggestions.append("Gunakan ast.literal_eval")
            base_score -= 40
        if re.search(r"range\(.{0,10}1000", code_snippet):
            issues.append("Loop besar terdeteksi")
            suggestions.append("Optimasi dengan generator")
            base_score -= 30

        quality_score = max(0, min(base_score, 100))
        image_path = self.generate_heatmap(code_snippet, quality_score, issues)
        status = "Kode bersih" if prediction == 0 and not issues else "Potensi masalah"
        return {
            "status": status,
            "quality_score": quality_score,
            "issues": issues if issues else ["Tidak ada masalah"],
            "suggestions": suggestions if suggestions else ["Kode sudah baik"],
            "visualization": f"/static/{os.path.basename(image_path)}"
        }