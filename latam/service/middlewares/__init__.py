from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def middleware_handler(request: Request, call_next):
    if request.url.path == '/status':
        return await call_next(request)
    
    if request.url.path == '/predict':
        return await call_next(request)