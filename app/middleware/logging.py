import time
import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logger.addHandler(handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            
            status_code = 500
            logger.error(f"CRITICAL ERROR: {str(e)}")
            raise e  
        finally:
            process_time = time.time() - start_time
            
            log_data = {
                "method": request.method,
                "url": str(request.url.path),
                "status_code": status_code,
                "execution_time": f"{process_time:.4f}s"
            }
            
            logger.info(json.dumps(log_data))
            
        return response