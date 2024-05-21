from fastapi import FastAPI

from utils.middleware import add_trace_and_session_id
from utils.settings import Settings
from utils.logging_config import simple_logger
from routes import insurance_routes

# Load settings
settings = Settings()
app = FastAPI()

# Add the middleware
app.middleware("http")(add_trace_and_session_id)

# Set the logger in the app state
app.state.logger = simple_logger

# Add the Router
app.include_router(insurance_routes.router, prefix="/api", tags=["insurance"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

