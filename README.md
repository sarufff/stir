# Stir

A full-stack recipe app that matches your pantry against real recipes and, eventually, generates new ones when nothing fits.

## What it does

- Users create an account and log in (JWT-based auth).
- Users maintain a personal ingredient pantry.
- The app returns recipes based on what's in that pantry.

## Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React (Vite), Axios
- **Auth:** JWT, bcrypt password hashing

## Status

The backend and frontend are working end-to-end: signup/login, pantry CRUD, and recipe lookup (currently via the Spoonacular API).

In progress, under `ml-experiments/`:
- A retrieval pipeline over a 2M+ recipe dataset (Hugging Face) that matches pantry ingredients against real recipes by ingredient overlap, using custom text-parsing and ingredient-normalization logic. This will replace the Spoonacular call as the primary matching engine.
- A LoRA fine-tune of Qwen 7B to generate a novel recipe as a fallback when no dataset match scores well — combining retrieval accuracy with generative flexibility.

## Project layout

```
main.py             FastAPI app and routes
models.py            SQLAlchemy models
schemas.py           Pydantic schemas
auth.py               JWT auth and password hashing
database.py          DB session/engine setup
frontend/            React app
ml-experiments/      Recipe retrieval pipeline (data cleaning, ingredient matching)
```

## Running locally

Backend:
```
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```

Requires a `.env` file with `SPOONACULAR_API_KEY` set.
