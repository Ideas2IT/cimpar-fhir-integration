from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import sys
import os
from os.path import abspath, dirname, join
import logging
from logging.handlers import TimedRotatingFileHandler

# Define the root path of your project
root_path = abspath(dirname(__file__))

# Ensure the integration_pipeline directory is in sys.path
integration_pipeline_path = join(root_path, 'integration-pipeline')
sys.path.insert(0, integration_pipeline_path)

from utils.middleware import add_trace_and_session_id, origins
from utils.settings import Settings
from utils.logging_config import simple_logger
from utils.config import Logs
from routes import (insurance_routes, integration_pipeline_router, authentication_router, patient_routes,
                    encounter_routes, medication_routes, condition_allergy_routes)

# Load settings
settings = Settings()

app = FastAPI(docs_url="/documentation")
if os.environ.get("ENVIRONMENT").upper() == "PRODUCTION":
    app = FastAPI(docs_url=None)


# Add the middleware
app.middleware("http")(add_trace_and_session_id)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the logger in the app state
app.state.logger = simple_logger

# Add the Router
app.include_router(insurance_routes.router, prefix="/api", tags=["INSURANCE"])
app.include_router(patient_routes.router, prefix="/api", tags=["PATIENT"])
app.include_router(encounter_routes.router, prefix="/api", tags=["ENCOUNTER"])
app.include_router(medication_routes.router, prefix="/api", tags=["MEDICATION"])
app.include_router(authentication_router.router, prefix="/api", tags=["AUTHENTICATION"])
app.include_router(condition_allergy_routes.router, prefix="/api", tags=["ALLERGY_CONDITION"])
app.include_router(integration_pipeline_router.router, prefix="/HL7v2", tags=["AIDBOX_INTEGRATION"])


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


def custom_openapi():
    env_name = os.environ.get("APP_DOC_ENVIRONMENT")
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=env_name,
        version="1.0.0",
        description="Cimpar development API documentation for integrating and testing in the development environment",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

