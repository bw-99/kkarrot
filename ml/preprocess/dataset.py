from argparse import Namespace
from logging import getLogger

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

logger = getLogger(__name__)


class AmazonDataset(Dataset):
    """
    Spec :
        - user_id: torch.LongTensor
        - asin: torch.LongTensor
        - parent_asin: torch.LongTensor
        - rating: torch.LongTensor
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__()

        self.user_id = np.asarray([x.astype(np.int32) for x in data["user_id"]])
        self.asin = np.asarray([x.astype(np.int32) for x in data["asin"]])
        self.parent_asin = np.asarray([x.astype(np.int32) for x in data["parent_asin"]])
        self.rating = np.asarray([x.astype(np.float16) for x in data["rating"]])

    def __getitem__(self, idx: int) -> list[torch.Tensor]:
        user_id = torch.LongTensor(self.user_id[idx])
        
        ctx_asin = torch.LongTensor(self.asin[idx][:-1])
        ctx_parent_asin = torch.LongTensor(self.parent_asin[idx][:-1])
        ctx_rating = torch.LongTensor(self.rating[idx][:-1])

        target_asin = torch.LongTensor(self.asin[idx][-1])
        target_parent_asin = torch.LongTensor(self.parent_asin[idx][-1])
        target_rating = torch.LongTensor(self.rating[idx][-1])

        return [
            user_id,
            ctx_asin,
            ctx_parent_asin,
            ctx_rating,
            target_asin,
            target_parent_asin,
            target_rating,
        ]

    def __len__(self):
        return len(self.rating)
