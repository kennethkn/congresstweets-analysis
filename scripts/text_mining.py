import html
import logging
import os
import re
import time

import nltk
from dotenv import load_dotenv
from models import Tweet
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BATCH_SIZE = 20000
LOG_EVERY = 5000
TWITTER_URL_PATTERN = re.compile(r"https://t.co/\w+")
URL_PATTERN = re.compile(r"https?://\S+")
HASHTAG_PATTERN = re.compile(r"#\w+")
MENTION_PATTERN = re.compile(r"@\w+")
RETWEET_PATTERN = re.compile(r"RT @\w+")
QUOTE_TWEET_PATTERN = re.compile(r"QT @\w+")

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
cool_session = scoped_session(session_factory)

nrow = session.query(Tweet).count()
for i, (id, text) in enumerate(cool_session.query(Tweet.id, Tweet.text).yield_per(BATCH_SIZE)):
    # logger.info(f"===> Processing tweet {id}:\n'''{text}'''")

    # Extract hashtags and tags
    hashtags = HASHTAG_PATTERN.findall(text)
    retweeting = RETWEET_PATTERN.match(text)
    quoting = QUOTE_TWEET_PATTERN.search(text)
    if retweeting:
        retweeting = retweeting[0][3:]
    if quoting:
        quoting = quoting[0][3:]
    text = RETWEET_PATTERN.sub("", text)
    text = QUOTE_TWEET_PATTERN.sub("", text)
    mentions = MENTION_PATTERN.findall(text)  # Goes after RETWEET_PATTERN and QUOTE_TWEET_PATTERN

    # logger.info(f"Hashtags: {hashtags}")
    # logger.info(f"Mentions: {mentions}")
    # logger.info(f"Retweeting: {retweeting}")
    # logger.info(f"Quoting: {quoting}")

    # Clean text
    text = TWITTER_URL_PATTERN.sub("", text)  # Goes before URL_PATTERN
    text = URL_PATTERN.sub("", text)
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = text.strip()
    text = html.unescape(text)
    # logger.info(f"Cleaned text: {text}")

    # Tokenize
    tokens = nltk.word_tokenize(text)
    # logger.info(f"Tokens: {tokens}")
    tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in stopwords.words("english")]
    # logger.info(f"Tokens: {tokens}")

    # Sentiment
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    # logger.info(f"Sentiment: {sentiment}")

    row = session.get(Tweet, id)
    row.hashtags = hashtags
    row.mentions = mentions
    row.retweeting = retweeting
    row.quoting = quoting
    row.tokens = tokens
    row.cleaned_text = text
    row.sentiment_score = sentiment["compound"]

    if i % LOG_EVERY == 0:
        logger.info(f"{i}/{nrow}")
    if i % BATCH_SIZE == 0 and i > 0:
        try:
            session.commit()
            logger.info(f"Committed at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            logger.error(f"Error committing batch {i/BATCH_SIZE}, ie. row {i-BATCH_SIZE}-{i}. ID of last row in batch: {id}. ErrorMsg: {e}")

logger.info(f"{nrow}/{nrow}")
try:
    session.commit()
    logger.info("Committed the last batch.")
except Exception as e:
    logger.error(f"Error committing the last batch: {e}")
