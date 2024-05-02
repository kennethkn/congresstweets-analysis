import json
import logging
import os

from dotenv import load_dotenv
from models import Account, Member
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_DIR = "../data/"
VALID_CHAMBERS = ["house", "senate"]
VALID_PARTIES = ["D", "R"]

engine = create_engine(DATABASE_URL)

with open(os.path.join(DATA_DIR, "members.json")) as f:
    data = json.load(f)

with Session(engine) as session:
    for member_data in data:
        if member_data["type"] != "member":
            continue
        member_fields = {
            "name": member_data["name"],
            "chamber": (member_data["chamber"] if member_data["chamber"] in VALID_CHAMBERS else None),
            "party": (member_data["party"] if member_data["party"] in VALID_PARTIES else None),
        }
        member = Member(**member_fields)
        session.add(member)
        session.flush()  # Assign an ID to the member

        for account_data in member_data["accounts"]:
            try:
                prev_names = account_data["prev_names"][0].values()
            except:
                prev_names = account_data.get("prev_names")

            account_fields = {
                "id": account_data["id"],
                "handle": account_data["screen_name"],
                "account_type": account_data["account_type"],
                "prev_handles": prev_names,
            }
            account = Account(member_id=member.id, **account_fields)
            session.add(account)

    session.commit()
    logger.info("Members and accounts inserted successfully")
