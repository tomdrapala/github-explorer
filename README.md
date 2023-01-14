# Github Explorer

Simple application that shows a list of GitHub repositories owned by a user.<br>
Application requires providing valid GitHub username.<br>
The frontend is prepared using [Vue.js](https://vuejs.org/) and the backend using [FastAPI](https://fastapi.tiangolo.com/).

<br>

# Installation

## 1. Backend

Backend requires having installed [python3](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installation/) and few libraries listed in `backend/requirements.txt`.<br>To avoid clashes with potentially allready installed libraries it is recommended to use virtual environment (such as [venv](https://docs.python.org/3/library/venv.html)).<br>

### Steps:
- being in the main app folder (`github-explorer`) run below commands to create and activate environment
```
python3 -m venv {environment-name}
```
Environment activation on Linux/Mac:
```
source {environment-name}/bin/activate
```
Environment activation on Windows:
```
{environment-name}\Scripts\activate.bat
```

- install requirements
```
pip install -r backend/requirements.txt
```
- start local server
```
uvicorn backend.main:app
```
- if you wish to enter changes in the source code and have them reflected on the server add `--reload` to uvicorn command
```
uvicorn backend.main:app --reload
```
<br>

## 2. Frontend

Frontend requires installation of [Node.js](https://nodejs.org/en/download/).

### Steps:
- starting from main project directory change location to `frontend/vue-app/`
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

With both backend and frontend servers running main application page is available at: http://127.0.0.1:8080/ <br>
To list user repositories just provide a valid username and click `fetch` or press `enter`.<br><br>
API endpoints used by the app (in this case a single endpoint) can be viewed at: http://127.0.0.1:8000/docs
