from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to library api project"}

if __name__ == "__main__":
    uvicorn.run(app)