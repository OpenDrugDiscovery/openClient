import os 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

api_app = FastAPI(title="Api App")

@api_app.get("/log")
def log():
    """Return the content of the manager log file"""
    fname = os.path.join(ROOT_DIR, "manager.log")
    with open(fname, "r") as fd:
        res = fd.read()
    return res


app = FastAPI(title="Main App")

app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="static", html=True), name="static")