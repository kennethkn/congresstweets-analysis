import json
import logging
import os

from dotenv import load_dotenv
from models import Account, Tweet
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_DIR = "../data/tweets"

engine = create_engine(DATABASE_URL)

cum_loaded = 0
cum_skipped = 0
cum_errors = 0
added_ids = set()
error_logs = dict()

json_files = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".json")])

with Session(engine) as session:
    account_ids = set(id[0] for id in session.query(Account.id).distinct().all())

    for j in json_files:
        with open(j) as f:
            data = json.load(f)

            skipped = 0
            errors = 0
            for tweet_data in data:
                try:
                    if tweet_data["user_id"] not in account_ids or tweet_data["id"] in added_ids:
                        skipped += 1
                        continue
                    tweet_fields = {
                        "id": tweet_data["id"],
                        "account_id": tweet_data["user_id"],
                        "time": tweet_data["time"],
                        "link": tweet_data["link"],
                        "text": tweet_data["text"],
                        "source": tweet_data["source"],
                    }
                    tweet = Tweet(**tweet_fields)
                    session.add(tweet)
                    added_ids.add(tweet_data["id"])
                except Exception as e:
                    logger.error(f"Error loading tweet: {e}")
                    error_logs[j] = e
                    errors += 1
                    continue
            logger.info(f"Loaded {(loaded:=len(data)-skipped-errors)} tweets from {j}, skipped {skipped} tweets (posted by non-member accounts or are duplicates), encountered {errors} error(s)")
            cum_loaded += loaded
            cum_skipped += skipped
            cum_errors += errors

    logger.info(f"Loaded a total of {cum_loaded} tweets, skipped {cum_skipped} tweets (posted by non-member accounts or are duplicates), encountered {cum_errors} error(s). Printing error logs for reference. ===>")
    for f, e in error_logs.items():
        logger.error(f"Error in {f}: {e}")
    logger.info("=== End of error logs ===")

    try:
        session.commit()
        logger.info("Successfully committed tweets to the database.")
    except Exception as e:
        logger.error(f"Error committing to database: {e}")
