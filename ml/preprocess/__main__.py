import logging
from ml.preprocess.indexer import indexing_and_scalarize
from ml.preprocess.downloader import load_data
from ml.preprocess.process import build_sequence_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    df, meta_df = load_data()
    df, meta_df = indexing_and_scalarize(df, meta_df)
    sequence_df = build_sequence_data(df)




