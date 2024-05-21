from fastapi import Request
import uuid
from contextvars import ContextVar

# Context variables for storing trace_id and session_id
trace_id_var = ContextVar('trace_id', default='N/A')
session_id_var = ContextVar('session_id', default='N/A')


async def add_trace_and_session_id(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    session_id = request.headers.get('X-Session-ID', 'N/A')

    # Set the trace_id and session_id in context variables
    trace_id_var.set(trace_id)
    session_id_var.set(session_id)

    # Process the request
    response = await call_next(request)

    # Add trace_id and session_id to the response headers (optional)
    response.headers['X-Trace-ID'] = trace_id
    response.headers['X-Session-ID'] = session_id

    return response

