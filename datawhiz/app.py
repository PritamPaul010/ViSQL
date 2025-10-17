from fastapi import FastAPI

app = FastAPI(title= 'DataWhiz - Minimal')

@app.get('/')
async def root():
    return {"message": "Welcome to Datawhiz"}

@app.get('/health')
async def health():
    """
        Health check endpoint.
        Returns basic status to verify the app is running.
        """
    return {"status": "ok"}

