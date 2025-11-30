## Project Setup Guide (Using `uv`)

This project uses `uv` for Python dependency and environment management. If you want to run it on your machine, follow these steps:

---

### **Installation Steps**

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/Bention99/techport_nasa_projects.git
cd techport_nasa_projects
```

#### 2️⃣ Create a virtual environment

```bash
uv venv
```

#### 3️⃣ Install all dependencies

```bash
uv sync
```

---

That's it — the project is ready to run! 🎉

---

### If you don't have `uv` installed

You can install it with one command:

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows PowerShell

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Run

After installation run:

```bash
uv run main.py
```