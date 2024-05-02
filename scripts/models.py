import os

from dotenv import load_dotenv
from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"))
    time = Column(DateTime)
    link = Column(String)
    text = Column(String)
    source = Column(String)
    hashtags = Column(ARRAY(String), nullable=True)
    mentions = Column(ARRAY(String), nullable=True)
    retweeting = Column(String, nullable=True)
    quoting = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    cleaned_text = Column(String, nullable=True)
    tokens = Column(ARRAY(String), nullable=True)


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    chamber = Column(String)
    party = Column(String)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True)
    handle = Column(String)
    account_type = Column(String)
    prev_handles = Column(ARRAY(String))
    member_id = Column(Integer, ForeignKey("members.id"))


if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
