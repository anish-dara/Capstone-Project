print("Starting diagnosis...")

try:
    print("1. Testing basic Python...")
    import sys
    print(f"Python version: {sys.version}")
    
    print("2. Testing FastAPI import...")
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
    
    print("3. Testing uvicorn import...")
    import uvicorn
    print("Uvicorn imported successfully")
    
    print("4. Creating basic FastAPI app...")
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {"status": "working"}
    
    print("5. Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()