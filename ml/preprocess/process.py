import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
from ml.preprocess.util import pad_sequence
from ml.name import UNK_TOKEN, MIN_SEQ_LEN, MAX_SEQ_LEN, PAD_TOKEN, SEQUENCE_PATH

logger = logging.getLogger(__name__)

def _build_sequence_data(df: pd.DataFrame) -> pd.DataFrame:
    data: np.ndarray = df.to_numpy()

    userid_lst = []
    asin_lst, parent_asin_lst, rating_lst, is_train_lst = [], [], [], []

    for i in tqdm(range(len(data)), desc="build sequence dataset", total=len(data)):
        train_i: np.ndarray = data[i]
        asin_t, parent_asin_t, rating_t, is_train_t = [np.array(x) for x in train_i[:4]]

        # 최소 2개는 돼야 input, output으로 구성 가능하다.
        if len(asin_t) <= 1:  
            continue
        
        target_indices = np.arange(len(asin_t)).flatten()

        if len(target_indices) == 0:
            continue

        for target_idx in target_indices:
            if asin_t[target_idx] == UNK_TOKEN:
                continue

            non_leakage_idx = np.arange(target_idx)
            valid_idx = np.concatenate([non_leakage_idx[-MAX_SEQ_LEN :], np.array([target_idx])])

            is_target_train = train_i[-1][target_idx]

            # min_seq_len 추가 체크
            if len(valid_idx) < MIN_SEQ_LEN:
                continue

            # 각 sequence의 길이는 max_seq_len + 1 (label)이 된다.
            if len(valid_idx) <= MAX_SEQ_LEN:
                pad_length = MAX_SEQ_LEN - len(valid_idx) + 1
                asin_lst.append(pad_sequence(asin_t[valid_idx], pad_length, PAD_TOKEN))
                parent_asin_lst.append(pad_sequence(parent_asin_t[valid_idx], pad_length, PAD_TOKEN))
                # rating의 경우 해당 유저의 평균 rating으로 채운다.
                rating_lst.append(pad_sequence(rating_t[valid_idx], pad_length, rating_t[valid_idx].mean()))
            else:
                asin_lst.append(asin_t[valid_idx])
                parent_asin_lst.append(parent_asin_t[valid_idx])
                rating_lst.append(rating_t[valid_idx])

            is_train_lst.append(is_target_train)
            userid_lst.append(df.index[i])

    logger.info(f"  - the size of total dataset: {len(is_train_lst)}")

    return pd.DataFrame(
        {
            "user_id": userid_lst,
            "asin": asin_lst,
            "parent_asin": parent_asin_lst,
            "rating": rating_lst,
            "is_train": is_train_lst,
        }
    )

def build_sequence_data(df: pd.DataFrame) -> pd.DataFrame:
    if SEQUENCE_PATH.exists():
        return pd.read_parquet(SEQUENCE_PATH)
    
    df["is_train"] = True
    df.loc[df.sample(frac=0.1).index, "is_train"] = False

    features: list[str] = ["asin", "parent_asin", "rating"] + ["is_train"]
    df = df.sort_values(by="timestamp", ascending=True)
    df = df.groupby("user_id")[features].agg(list)
    
    sequence_df = _build_sequence_data(df)
    sequence_df.to_parquet(SEQUENCE_PATH)
    return sequence_df
