# Github Explorer

Simple application that shows a list of GitHub repositories owned by a user.<br>
The frontend is built with [Vue.js](https://vuejs.org/) and the backend with [FastAPI](https://fastapi.tiangolo.com/).

<br>

# Installation

## 1. Backend

Backend requires having installed [python3](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installation/) and few libraries listed in `backend/requirements.txt`.<br>
To avoid clashes with potentially already installed libraries it is recommended to use a virtual environment. There are various options but for this instruction I chose [venv](https://docs.python.org/3/library/venv.html) as it is part of Python’s standard library.<br>

### Steps:
- from the main app directory (`github-explorer/`) run below command in your terminal to create environment
```
python3 -m venv {environment-name}
```
- activate environment
```bash
# on Linux/Mac
source {environment-name}/bin/activate

# on Windows
{environment-name}\Scripts\activate.bat
```

- install required libraries
```
pip install -r backend/requirements.txt
```
- start local server
```
uvicorn backend.main:app
```
<br>

## 2. Frontend

Frontend requires installation of [Node.js](https://nodejs.org/en/download/) (with npm).

### Steps:
- in the new terminal tab, starting from the main project directory move to `frontend/vue-app/`
```
cd frontend/vue-app/
```
- install required packages
```
npm install
```
- start local server
```
npm run serve
```
<br>

# Usage

With both backend and frontend servers running main application page should be available at: http://127.0.0.1:8080/ <br>
To get a list of user repositories just provide a valid GitHub username and click `fetch`.<br><br>
API swagger docs can be viewed at: http://127.0.0.1:8000/docs
