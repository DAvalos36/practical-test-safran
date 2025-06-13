from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    username = Column(Text)
    password = Column(Text)

    # Relación uno a muchos con questions
    questions = relationship("Question", back_populates="user", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    question = Column(Text)

    # Relaciones
    user = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE', onupdate='CASCADE'))
    answer = Column(Text)
    prediction = Column(Numeric)

    # Relación con question
    question = relationship("Question", back_populates="answers")