from fastapi import FastAPI
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from utils.settings import Settings
from utils.config import Logs
from routes import insurance_routes, patient_routes, encounter_routes, medication_routes

# Load settings
settings = Settings()
app = FastAPI()

app.include_router(insurance_routes.router, prefix="/api", tags=["insurance"])
app.include_router(patient_routes.router, prefix="/api", tags=["patient"])
app.include_router(encounter_routes.router, prefix="/api", tags=["encounter"])
app.include_router(medication_routes.router, prefix="/api", tags=["medication"])


log_path = os.path.join(os.getcwd(), Logs.TAIL_PATH)
simple_logger = logging.getLogger("log")
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_formatter = logging.Formatter(
    '%(asctime)s - %(pathname)20s:%(lineno)4s - %(funcName)20s() - %(levelname)s ## %(message)s')
handler = TimedRotatingFileHandler(log_path + "/" + Logs.FILE_NAME,
                                   when="d",
                                   interval=1,
                                   backupCount=10)
handler.setFormatter(log_formatter)
if not len(simple_logger.handlers):
    simple_logger.addHandler(handler)
simple_logger.setLevel(logging.DEBUG)

app.state.logger = simple_logger


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)