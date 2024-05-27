from fastapi import FastAPI
import sys
from os.path import abspath, dirname, join

# Define the root path of your project
root_path = abspath(dirname(__file__))

# Ensure the integration_pipeline directory is in sys.path
integration_pipeline_path = join(root_path, 'integration-pipeline')
sys.path.insert(0, integration_pipeline_path)

from utils.middleware import add_trace_and_session_id
from utils.settings import Settings
from utils.logging_config import simple_logger
from routes import insurance_routes, integration_pipeline_router

# Load settings
settings = Settings()
app = FastAPI()

# Add the middleware
app.middleware("http")(add_trace_and_session_id)

# Set the logger in the app state
app.state.logger = simple_logger

# Add the Router
app.include_router(insurance_routes.router, prefix="/api", tags=["insurance"])

# Integration pipeline routes are added into the below router
app.include_router(integration_pipeline_router.router, prefix="/HL7v2", tags=["hl7wrapper"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

