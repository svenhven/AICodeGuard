from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class CodeAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base")

    def analyze(self, code_snippet):
        inputs = self.tokenizer(code_snippet, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
        return "Potensi bug" if prediction == 1 else "Kode bersih"

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    sample_code = "def add(a, b): return a + b"
    print(analyzer.analyze(sample_code))