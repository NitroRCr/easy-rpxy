from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import aiohttp
from typing import Optional, Dict, Any
import os

app = FastAPI()

ALLOWED_PREFIXES = os.getenv("ALLOWED_PREFIXES", "").split(",")

class ProxyRequest(BaseModel):
    method: str
    url: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[Any] = None

@app.post("/proxy")
async def proxy(request: ProxyRequest):
    if not any(request.url.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise HTTPException(status_code=403, detail="URL not allowed")
    
    kwargs = {
        'method': request.method,
        'url': request.url,
        'headers': request.headers or {}
    }
    
    if request.body is not None:
        if isinstance(request.body, (dict, list)):
            kwargs['json'] = request.body
        else:
            kwargs['data'] = request.body

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(**kwargs) as response:
                content = await response.read()
                
                return Response(content=content, status_code=response.status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
