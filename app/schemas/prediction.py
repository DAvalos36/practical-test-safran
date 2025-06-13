from pydantic import BaseModel, Field
from typing import List


class PredictionAnswerInput(BaseModel):
    answer: str = Field(min_length=8, max_length=500)

class PredicitionInput(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    answers: List[PredictionAnswerInput] = Field(min_items=1, max_items=10)

class PredictionAnswerOutput(BaseModel):
    answer: str
    prediction: float = Field(ge=0.0, le=100.0)

class PredictionOutput(BaseModel):
    id: int
    question: str
    predictions: List[PredictionAnswerOutput]