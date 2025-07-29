from pathlib import Path

DATA_PATH = Path("data")
RAW_PATH = DATA_PATH / "raw"
PROCESSED_PATH = DATA_PATH / "processed"
INDEXER_PATH = DATA_PATH / "indexer"
SCALER_PATH = DATA_PATH / "scaler"

RAW_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
INDEXER_PATH.mkdir(parents=True, exist_ok=True)
SCALER_PATH.mkdir(parents=True, exist_ok=True)

RAW_INTERACTION_PATH = RAW_PATH / "interaction.parquet"
RAW_META_PATH = RAW_PATH / "meta.parquet"

INTERACTION_PATH = PROCESSED_PATH / "interaction.parquet"
META_PATH = PROCESSED_PATH / "meta.parquet"
SEQUENCE_PATH = PROCESSED_PATH / "sequence.parquet"

CONTENTS_INDEXER_PATH = INDEXER_PATH / "contents_indexer.json"
USERS_INDEXER_PATH = INDEXER_PATH / "users_indexer.json"
CATEGORY_INDEXER_PATH = INDEXER_PATH / "category_indexer.pkl"

RATING_SCALER_PATH = SCALER_PATH / "rating_scaler.pkl"
AVG_RATING_SCALER_PATH = SCALER_PATH / "avg_rating_scaler.pkl"
RATING_NUMBER_SCALER_PATH = SCALER_PATH / "rating_number_scaler.pkl"
PRICE_SCALER_PATH = SCALER_PATH / "price_scaler.pkl"

PAD_TOKEN = 0
UNK_TOKEN = 1
N_SPECIAL_TOKENS = 2

MIN_SEQ_LEN = 3
MAX_SEQ_LEN = 50