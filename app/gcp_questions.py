import pandas as pd
import numpy as np
from os import system
import time

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from starlette.status import HTTP_404_NOT_FOUND


app = FastAPI()

#create Post class Model
class Answer(BaseModel):
    id: int
    answer: int


def make_questions():

    df = pd.read_json("/Users/ezequielmelillan/Desktop/GCP/certifications/associate.json") 
    n = np.random.randint(len(df))
    return df.iloc[n], n


def get_question(id):
    df = pd.read_json("/Users/ezequielmelillan/Desktop/GCP/certifications/associate.json") 
    question = df.iloc[id]
    return question


#MAIN ENDPOINT
@app.get("/")
def root():
    return {"message": "Welcome to GCP-PRACTICE"}

#MAIN ENDPOINT
@app.get("/question")
def question():
    question, id  = make_questions()
    return {"ID" : id,
            "question": question['question_content'],
            "options": question['question_options']}

@app.post("/answer")
def answer(post:Answer):
    id, answer = post.id, post.answer-1
    question = get_question(id)
    idx_correct = question['is_answer'].index(True)

    result = "INCORRECT"
    if answer == idx_correct:
        result = "CORRECT"

    return {
            "Result" : result,
            "Question": question['question_content'],
            "Options": question['question_options'],
            "User_answer": question['question_options'][answer],
            "Correct_Answer" : question['question_options'][idx_correct],
            "Explanation" : question['explanation']
            }