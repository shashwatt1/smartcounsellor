# 🎓 JEE College Predictor

Predict eligible colleges based on your JEE rank using JoSAA 2025 cutoff data.

---

## 📁 Project Structure

```
Project Rank/
├── backend/          # FastAPI server
│   ├── app/
│   │   ├── main.py           # App entry point
│   │   ├── routes/predict.py # POST /api/predict
│   │   ├── services/predictor.py
│   │   ├── models/schema.py
│   │   └── utils/data_loader.py
│   ├── requirements.txt
│   └── .env
├── frontend/         # Next.js app
├── data/
│   └── josaa_2025.csv        # JoSAA cutoff dataset
├── .venv/            # Python virtual environment
└── README.md
```

---

## ⚡ Quick Start

### 1. Activate Virtual Environment

```bash
# From the Project Rank root directory
source .venv/bin/activate
```

### 2. Run the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

API docs available at: **http://localhost:8000/docs**

### 3. Run the Frontend

```bash
cd frontend
npm run dev
```

Frontend available at: **http://localhost:3000**

---

## 🔌 API Reference

### `GET /`
Health check.

### `POST /api/predict`

**Request body:**
```json
{
  "rank": 5000,
  "category": "OPEN",
  "gender": "Gender-Neutral",
  "quota": "AI"
}
```

**Response:**
```json
{
  "rank": 5000,
  "category": "OPEN",
  "total_results": 12,
  "colleges": [...]
}
```

**Categories:** `OPEN`, `OBC-NCL`, `SC`, `ST`, `EWS`  
**Gender:** `Gender-Neutral`, `Female-only`  
**Quota:** `AI` (All India), `HS` (Home State)

---

## 📦 Backend Dependencies

```bash
pip install fastapi uvicorn pandas python-dotenv
```

---

## 📊 Data

Place the JoSAA 2025 cutoff CSV at `data/josaa_2025.csv`.

Expected columns:
| Column | Description |
|---|---|
| `institute` | Institution name |
| `academic_program_name` | Branch / programme |
| `quota` | AI or HS |
| `seat_type` | OPEN, OBC-NCL, SC, ST, EWS |
| `gender` | Gender-Neutral / Female-only |
| `opening_rank` | Opening rank for the round |
| `closing_rank` | Closing rank for the round |

---

## ☁️ AWS Lambda Deployment (Future)

The FastAPI backend is structured for [Mangum](https://mangum.io/) adapter:

```python
from mangum import Mangum
handler = Mangum(app)
```

---

## 🧹 Development Notes

- `data_loader.py` uses `@lru_cache` — restart the server to reload CSV data.
- Never commit `.env` or real student data to version control.
- The `data/*.csv` line in `.gitignore` is commented out by default — uncomment if the dataset is large.
