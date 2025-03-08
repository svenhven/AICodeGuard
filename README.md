# AICodeGuard 2.0
AI-powered code review bot yang cerdas dan visual untuk GitHub. Didukung CodeBERT, memberikan analisis mendalam, skor kualitas, saran perbaikan, dan **heatmap interaktif**.

![Heatmap Example](https://via.placeholder.com/800x400.png?text=Heatmap+Kualitas+Kode)  
*Heatmap kualitas kode dengan anotasi baris*

## Fitur
- **Analisis AI**: Deteksi bug, keamanan, dan efisiensi dengan CodeBERT.
- **Visualisasi**: Heatmap skor kualitas per baris kode.
- **Output Kaya**: Status, skor, issues, saran dalam JSON.
- **GitHub Integration**: Review PR otomatis via GitHub Actions.

## Contoh Output
```json
{
  "analysis": {
    "status": "Kode bersih",
    "quality_score": 94.15,
    "issues": ["Tidak ada masalah"],
    "suggestions": ["Kode sudah baik"],
    "visualization": "/static/4c01b511-4c0e-4fb0-af43-c8696271d6af.png"
  },
  "metadata": {
    "model": "CodeBERT",
    "version": "2.0.0",
    "processed_at": "2025-03-08"
  }
}