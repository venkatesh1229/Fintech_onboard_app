# Deployment Guide — Fintech Onboard App

This project can be deployed using:
- Backend on **Render** (free Python web service) — uses local JSON file storage
- Frontend on **Netlify** (free static site hosting)

> **Note:** Database removed! The app now stores all data in local JSON files (`data/db.json`). No external database required.

## 1. Backend: Render

1. Sign up or log in to Render: https://render.com
2. Create a new **Web Service** or connect your GitHub repo.
3. Select the `backend` directory as the service root.
4. Use the following service settings:
   - Environment: `Python`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python run.py`
5. Add environment variables in Render:
   - `SECRET_KEY` — a strong random secret (e.g., `openssl rand -hex 32`)
   - `APP_HOST` = `0.0.0.0`
   - `APP_PORT` = `8000`
   - `APP_RELOAD` = `false`

### Render config files included
- `backend/render.yaml`
- `backend/Procfile`

> **Important:** The app stores data in `data/db.json` which persists in the Render filesystem. On free tier, files are lost on service restart. For production, consider adding persistent disk storage or switching to a real database backend.

## 2. Frontend: Netlify

1. Sign up or log in to Netlify: https://app.netlify.com
2. Create a new site from your GitHub repo.
3. Set the publish directory to `frontend/build`.
4. Add Netlify build environment variables:
   - `REACT_APP_API_URL=https://<your-render-backend-url>/api`
5. If you build locally, ensure `frontend/.env.example` is used as a template.

### Netlify config included
- `frontend/netlify.toml`

## 3. Local testing

### Backend
```powershell
cd backend
pip install -r requirements.txt
python run.py
```
Browse: `http://127.0.0.1:8000/docs`

Data is stored in `backend/data/db.json`. Default admin credentials:
- Email: `admin@example.com`
- Password: `admin123`

### Frontend
If you have the frontend source, build and serve the static app:
```powershell
cd frontend
npm install
npm run build
```
Then deploy the `frontend/build` folder.

## 4. Notes and limitations

- **Data Storage:** All merchant accounts, applications, and documents are stored in `data/db.json` as plain JSON.
- **Persistence:** On free hosting (Render), the JSON file is lost when the service restarts. For production use, add proper database persistence.
- **Security:** Uploaded files are served from `/uploads`. Ensure proper file handling and virus scanning in production.
- **Scalability:** JSON storage is not suitable for high-traffic applications. Migrate to a real database (MySQL, PostgreSQL) for production.
- **Concurrency:** Basic file-level locking is used, but production deployments need robust transaction handling.

## 5. Upgrading to a real database

To add back MySQL/PostgreSQL support:

1. Install SQLAlchemy: `pip install sqlalchemy pymysql`
2. Update `app/database.py` with proper SQLAlchemy engine setup
3. Rewrite routes to use SQLAlchemy ORM instead of `app/storage.py`
4. Set `DATABASE_URL` environment variable in Render
