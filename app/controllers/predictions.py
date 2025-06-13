from typing import List

from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
# from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError

from ..schemas.auth import UserRegistrationInput
from ..models.models import Question, Answer, User
from ..database import get_db_session
from ..schemas.prediction import PredictionOutput, PredictionAnswerOutput

router2 = APIRouter()


@router2.get("/predictions", response_model=List[PredictionOutput])
def predictions(id: int):
    db = get_db_session()
    try:
        user = db.query(User).get(id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario {id} no encontrado")

        questions = db.query(Question).filter(Question.user_id == id).all()

        predictions_output = []

        for question in questions:
            answers = db.query(Answer).filter(Answer.question_id == question.id).all()

            prediction_answers = []
            for answer in answers:
                prediction_answer = PredictionAnswerOutput(
                    answer=answer.answer,
                    prediction=answer.prediction
                )
                prediction_answers.append(prediction_answer)

            prediction_output = PredictionOutput(
                id=question.id,
                question=question.question,
                predictions=prediction_answers
            )
            predictions_output.append(prediction_output)

        return predictions_output

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

