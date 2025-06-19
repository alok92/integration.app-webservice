# Webhook Service
This is a simple FastAPI service that accepts and processes webhook payloads with a 5-second delay.

---

## Features

- `POST /webhook`: Accepts arbitrary JSON payloads, stores them with status `"unprocessed"`, and marks them as `"processed"` after 5 seconds.
- `GET /webhooks`: Lists all received payloads in reverse chronological order with their statuses.

---

## 🚀 Deploying to Render

This project uses Render's **native GitHub auto-deploy**.

### Steps:

1. Push this code to a **public GitHub repository**.
2. Go to [https://dashboard.render.com/new](https://dashboard.render.com/new).
3. Choose **Web Service** and connect your repo.
4. Select:
   - Environment: `Docker`
   - Region: your closest region
5. Render will auto-deploy on every push to `main`.

---

## ⚙️ Terraform (Optional, Future Use)

- Terraform files are included in the `terraform/` folder for IAC extensibility.
- Currently **not used** for deployment to keep things simple.

---

## 📦 Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
