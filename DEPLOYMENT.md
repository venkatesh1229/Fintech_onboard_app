# Deployment Guide — Fintech Onboard App

This project can be deployed for free using:
- Backend on **Render** (free Python web service)
- Database on **PlanetScale** (free MySQL-compatible database)
- Frontend on **Netlify** (free static site hosting)

## 1. Backend: Render

1. Sign up or log in to Render: https://render.com
2. Create a new **Web Service** or connect your GitHub repo.
3. Select the `backend` directory as the service root.
4. Use the following service settings:
   - Environment: `Python`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python run.py`
5. Add environment variables in Render:
   - `DATABASE_URL` — your PlanetScale connection string
   - `SECRET_KEY` — a strong random secret
   - `APP_HOST` = `0.0.0.0`
   - `APP_PORT` = `8000`
   - `APP_RELOAD` = `false`

### Render config files included
- `backend/render.yaml`
- `backend/Procfile`

## 2. Database: PlanetScale

1. Create a free PlanetScale database account: https://planetscale.com
2. Create a new database and deploy the initial branch.
3. Create a password and connection string for the `main` branch.
4. Copy the connection string and set it as Render env var:
   - `DATABASE_URL=mysql+pymysql://<username>:<password>@<host>/<database>`

> Note: The backend app now uses `backend/app/config.py` and `backend/app/database.py` to read `DATABASE_URL` from environment.

## 3. Frontend: Netlify

1. Sign up or log in to Netlify: https://app.netlify.com
2. Create a new site from your GitHub repo.
3. Set the publish directory to `frontend/build`.
4. Add Netlify build environment variables:
   - `REACT_APP_API_URL=https://<your-render-backend-url>/api`
5. If you build locally, ensure `frontend/.env.example` is used as a template.

### Netlify config included
- `frontend/netlify.toml`

## 4. Local testing

### Backend
```powershell
cd backend
python run.py
```
Browse: `http://127.0.0.1:8000/docs`

### Frontend
If you have the frontend source, build and serve the static app:
```powershell
cd frontend
npm install
npm run build
```
Then deploy the `frontend/build` folder.

## 5. Notes and compatibility

- The backend now reads `DATABASE_URL` from env and can use MySQL or SQLite.
- The frontend uses `REACT_APP_API_URL` at build time to point to the deployed API.
- Uploaded files are served from `/uploads`. Free hosts may not preserve files across restarts.
