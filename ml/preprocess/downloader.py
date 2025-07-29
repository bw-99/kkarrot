import json
from tqdm import tqdm
import pandas as pd
from datasets import load_dataset
import logging

from ml.name import RAW_INTERACTION_PATH, RAW_META_PATH
from ml.preprocess.util import load_cache

logger = logging.getLogger(__name__)

def download_interaction_data():
    rate_lst, asin_lst, parent_asin_lst, use_id_lst, timestamp_lst = [], [], [], [], []
    with open("data/Electronics.jsonl", 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            obj = json.loads(line)
            rate_lst.append(obj["rating"])
            asin_lst.append(obj["asin"])
            parent_asin_lst.append(obj["parent_asin"])
            use_id_lst.append(obj["user_id"])
            timestamp_lst.append(obj["timestamp"])

    logger.info(f"len(data): {len(rate_lst)}")

    df = pd.DataFrame({
        "rating": rate_lst,
        "asin": asin_lst,
        "parent_asin": parent_asin_lst,
        "user_id": use_id_lst,
        "timestamp": timestamp_lst
    })
    return df

def download_meta_data():
    dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_meta_Electronics", split="full", trust_remote_code=False)
    meta_json = [{
        "title": item["title"],
        "categories": item["categories"],
        "main_category": item["main_category"],
        "average_rating": item["average_rating"],
        "description": item["description"],
        "images": item["images"]["thumb"][0] if item["images"]["thumb"] else None,
        "price": item["price"],
        "parent_asin": item["parent_asin"],
        "rating_number": item["rating_number"],
    } for item in tqdm(dataset)]
    meta_df = pd.DataFrame(meta_json)
    return meta_df


def load_data():
    df = load_cache(
        fpath=RAW_INTERACTION_PATH,
        read=True,
        write=True,
        func=download_interaction_data
    )
    logger.info(f"\n{df.head()}")

    meta_df = load_cache(
        fpath=RAW_META_PATH,
        read=True,
        write=True,
        func=download_meta_data
    )
    logger.info(f"\n{meta_df.head()}")

    return df, meta_df