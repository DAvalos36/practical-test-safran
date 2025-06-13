from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Question, Answer

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")
    seed()

def seed():

    session = get_db_session()

    currentUsers = session.query(User).count()
    
    if currentUsers > 0:
        return

    try:
        user = User(name="María González", username="maria123", password="password123")
        session.add(user)
        session.commit()

        question = Question(
            question="¿De qué color es el cielo?",
            user_id=user.id
        )
        session.add(question)
        session.commit()

        respuestas = [
            {"answer": "Rojo", "prediction": 0.1},
            {"answer": "Verde", "prediction": 0.05},
            {"answer": "Azul", "prediction": 0.85},
        ]

        for resp_data in respuestas:
            answer = Answer(
                answer=resp_data["answer"],
                prediction=resp_data["prediction"],
                question_id=question.id
            )
            session.add(answer)

        session.commit()
        print("Seed guardada exitosamente")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print("Tablas eliminadas")
