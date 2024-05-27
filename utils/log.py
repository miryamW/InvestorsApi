import logging
from functools import wraps
from fastapi import Request
from typing import Callable

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def log(func: Callable) -> Callable:
    """
    Decorator function to log information about function calls and their return values.

    Parameters:
    - func (Callable): The function to be decorated.

    Returns:
    - Callable: The wrapper function that adds logging functionality.
    """

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        """
        Wrapper function that logs function calls and their return values.

        Parameters:
        - request (Request): The FastAPI request object.
        - *args: Positional arguments passed to the decorated function.
        - **kwargs: Keyword arguments passed to the decorated function.

        Returns:
        - Any: The return value of the decorated function.
        """
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
