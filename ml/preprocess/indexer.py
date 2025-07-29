import json
import pandas as pd
import numpy as np
from ml.name import INTERACTION_PATH, META_PATH, N_SPECIAL_TOKENS, CONTENTS_INDEXER_PATH, UNK_TOKEN, USERS_INDEXER_PATH, CATEGORY_INDEXER_PATH, RATING_SCALER_PATH, AVG_RATING_SCALER_PATH, RATING_NUMBER_SCALER_PATH, PRICE_SCALER_PATH
from sklearn.preprocessing import MultiLabelBinarizer
import pickle
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

def save_indexer(indexer: dict, fpath: str):
    json.dump(indexer, open(fpath, "w"))
    
def indexing(df: pd.DataFrame, meta_df: pd.DataFrame):
    # contents indexing
    total_contents = set(df["asin"].unique()) | set(meta_df["parent_asin"].unique())
    contents_indexer = {
        c: idx for idx, c in enumerate(total_contents, start=N_SPECIAL_TOKENS)
    }
    save_indexer(contents_indexer, CONTENTS_INDEXER_PATH)

    # users indexing
    users_indexer = {
        u: idx for idx, u in enumerate(df["user_id"].unique(), start=N_SPECIAL_TOKENS)
    }
    save_indexer(users_indexer, USERS_INDEXER_PATH)

    df["user_id"] = df["user_id"].map(users_indexer).fillna(UNK_TOKEN).astype(int)
    df["parent_asin"] = df["parent_asin"].map(contents_indexer).fillna(UNK_TOKEN).astype(int)
    meta_df["parent_asin"] = meta_df["parent_asin"].map(contents_indexer).fillna(UNK_TOKEN).astype(int)

    # category indexing
    # TODO: 시간이 많이 걸린다. 최적화 필요.
    categories_list = meta_df['categories'].tolist()
    mlb = MultiLabelBinarizer(sparse_output=False)
    multi_hot = mlb.fit_transform(categories_list)
    multi_hot_df = pd.DataFrame(multi_hot, columns=mlb.classes_, index=meta_df.index)
    meta_df["categories"] = list(multi_hot_df.values)
    with open(CATEGORY_INDEXER_PATH, "wb") as f:
        pickle.dump(mlb, f)

    return df, meta_df

def _scalarize(df: pd.DataFrame, col: str, save_path: str) -> np.ndarray:
    scaler = StandardScaler()
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].mean())
    values = scaler.fit_transform(df[col].values.reshape(-1, 1))
    with open(save_path, "wb") as f:
        pickle.dump(scaler, f)
    return values

def scalarize(df: pd.DataFrame, meta_df: pd.DataFrame):
    df["rating"] = _scalarize(df, "rating", RATING_SCALER_PATH)
    meta_df["average_rating"] = _scalarize(meta_df, "average_rating", AVG_RATING_SCALER_PATH)
    meta_df["rating_number"] = _scalarize(meta_df, "rating_number", RATING_NUMBER_SCALER_PATH)
    meta_df["price"] = _scalarize(meta_df, "price", PRICE_SCALER_PATH)
    return df, meta_df


def indexing_and_scalarize(df: pd.DataFrame, meta_df: pd.DataFrame):
    if INTERACTION_PATH.exists() and META_PATH.exists():
        df = pd.read_parquet(INTERACTION_PATH)
        meta_df = pd.read_parquet(META_PATH)
        return df, meta_df

    # 유저가 10개 이상의 아이템을 구매한 경우만 남긴다.
    prev_rows = len(df)
    count_df = df.groupby("user_id").agg({"parent_asin": "count"}).reset_index()
    df = df[df["user_id"].isin(count_df[count_df["parent_asin"] >= 10]["user_id"])].reset_index(drop=True)
    logger.info(f"filtered rows (%): {(1 - len(df)/prev_rows) * 100:.2f}")
    logger.info(f"total users: {len(df['user_id'].unique())}")

    # 아이템이 10개 이상의 유저가 구매한 경우만 남긴다.
    prev_rows = len(df)
    count_df = df.groupby("asin").agg({"user_id": "count"}).reset_index()
    df = df[df["asin"].isin(count_df[count_df["user_id"] >= 10]["asin"])].reset_index(drop=True)
    logger.info(f"filtered rows (%): {(1 - len(df)/prev_rows) * 100:.2f}")
    logger.info(f"total items: {len(df['asin'].unique())}")

    logger.info(f"total interactions: {len(df)}")

    # 공통으로 사용된 카테고리만 남긴다.
    unique_categories = set(df["parent_asin"].unique()) & set(meta_df["parent_asin"].unique())
    df = df[df["parent_asin"].isin(unique_categories)].reset_index(drop=True)
    meta_df = meta_df[meta_df["parent_asin"].isin(unique_categories)].reset_index(drop=True)
    logger.info(f"unique_categories: {len(unique_categories)}")

    df, meta_df = indexing(df, meta_df)
    df, meta_df = scalarize(df, meta_df)

    df.to_parquet(INTERACTION_PATH)
    meta_df.to_parquet(META_PATH)
    return df, meta_df