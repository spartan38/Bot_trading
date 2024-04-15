from api.server import app
from settings import API_HOST, API_PORT


def run():
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)