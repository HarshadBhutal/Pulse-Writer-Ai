
# Pulse Writer AI ✍️

**Pulse Writer AI** is an AI-powered, scheduler-driven news aggregation and blog generation platform. It automatically collects trending topics from free RSS and web sources, aggregates 3-5 related articles per topic, and generates a unified, human-readable news blog using a local LLM (**LLaMA 3.2 via Ollama**). The system extracts information from the web, stores content in a **SQLite** database using **SQLModel**, and removes outdated topics through automated timestamp-based cleanup.

---
<img width="1861" height="913" alt="image" src="https://github.com/user-attachments/assets/8566122f-6a68-4be1-b3f6-6a913e9ce9ed" />



# Articles Written By AI

<img width="1893" height="904" alt="image" src="https://github.com/user-attachments/assets/a1e8fc85-a58b-493f-a01d-32d650a0be45" />


## 💻 Hardware Requirements

To run this platform effectively, your system must meet the following minimum specifications:

* **GPU:** Dedicated Graphics Card with at least **4GB VRAM**.
* **Storage:** Sufficient space for the LLaMA 3.2 model weights and the growing SQLite database.

---

## 🛠️ Infrastructure Setup

Before running the application, set up the following components in your environment.

### 1. Ollama (AI Engine)

* **Download:** [ollama.com/download](https://ollama.com/download)
* **Setup Model:** Open your **Command Prompt (CMD)** and run:
```cmd
ollama pull llama3.2

```


* **Run Model:** To start the model before using the app:
```cmd
ollama run llama3.2

```


* **Stop Model:** To free up your 4GB GPU memory after you are finished using the app, run:
```cmd
ollama stop llama3.2

```



### 2. SQLite (Database)

* **Download:** [sqlite.org/download.html](https://www.sqlite.org/download.html)
* **Setup:** Download the "sqlite-tools" and ensure `sqlite3` is available in your CMD environment.

---

## 🚀 Installation & Execution (CMD)

Perform the following steps in the **Command Prompt (CMD)**:

### Phase 1: Environment Preparation

```cmd
:: 1. Create a virtual environment
python -m venv .venv

:: 2. Activate the virtual environment
.venv\Scripts\activate

:: 3. Install required dependencies
pip install -r requirements.txt

```

### Phase 2: Database Initialization

The application uses **SQLModel** to handle the database.

* The system **automatically creates** and initializes the `data.db` file in the backend folder.
* No manual setup is required for the database file or tables.

### Phase 3: Launch the Scheduler & Server

Navigate to the backend folder and start the server. This will initiate the **10-minute scheduler** immediately.

```cmd
cd backend
fastapi dev main.py

```
---

## ⚠️ Important: Stopping the Scheduler

The scraper heartbeat is a background job that runs every 10 minutes.

* **VS Code Users:** If you leave VS Code running in the background, the terminal process stays active. This means the scheduler will **continue to run every 10 minutes** even if you aren't actively using the editor.
* **To stop the app completely:** You **must** use `Ctrl+C` in the terminal to kill the process. Simply minimizing or leaving VS Code open will keep the scraper active.

---
---

## ⏱️ Orchestration Logic

The system heartbeat is a background job that runs every 10 minutes:

```python
# scheduler logic inside main.py
scheduler.add_job(func=fetch_trending_topics, trigger="interval", minutes=10, id="scraper_job")

```

*You can modify the `minutes` value in `main.py` to change how often the web extraction runs.*

---

## 📖 API Documentation

Manage your generated content via:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

---

