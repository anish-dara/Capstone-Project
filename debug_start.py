print("Step 1: Starting debug...")

try:
    print("Step 2: Testing imports...")
    import uvicorn
    print("✓ uvicorn imported")
    
    from fastapi import FastAPI
    print("✓ FastAPI imported")
    
    print("Step 3: Creating app...")
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {"status": "working"}
    
    print("Step 4: Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")