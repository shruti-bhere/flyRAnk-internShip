from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message" : "hello from my first backend!"
    }

@app.get("/about")
def about():
    return {
        "name": "Shruti Suresh Bhere",
        "role": "Ai backend Enginnering Intern",
        "skills": [
            "Python",
            "FastAPI",
            "RestAPI",
            "RAG"
        ]

    }
        