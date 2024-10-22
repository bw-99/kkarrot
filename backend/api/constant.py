import pandas as pd
from torch_geometric.data import HeteroData
import torch
from flask import session

ALPHA = 0.7
WINDOW_SIZE = 5
FETCH_UNIT = 4*3*2

# * load data
NUM_USER, NUM_ITEM = 5_000, 30_000
meta_df = pd.read_pickle("data/processed/item_meta.pkl")
ITEM_ID_LST = torch.LongTensor(meta_df["item_id"].to_list()).cuda()
RATING_LST = torch.LongTensor(meta_df["rating_number"].to_list())
longtail_df = pd.read_pickle("data/processed/longtail_indicator.pkl")
longtail_df = longtail_df.sort_values("item_id").reset_index(drop=True)
LONGTAIL_INDICATOR = torch.tensor(longtail_df["is_head"].tolist()).long().cuda()

graph = torch.load("data/processed/graph.pkl")
graph = HeteroData().from_dict(graph)


user_history = {}
