import logging
from functools import wraps
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Callable

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def log(func: Callable):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Log the request method and path
        logging.info(f"Request: {request.method} {request.url.path}")

        # Log the function call with arguments
        logging.info(f"Calling function '{func.__name__}' with arguments: {args} and keyword arguments: {kwargs}")

        # Execute the function and capture the return value
        result = await func(request, *args, **kwargs)

        # Log the return value
        logging.info(f"Function '{func.__name__}' returned: {result}")

        return result

    return wrapper
