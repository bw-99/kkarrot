import pandas as pd
from torch_geometric.data import HeteroData
import torch

ALPHA = 0.7
WINDOW_SIZE = 3

# * load data
meta_df = pd.read_pickle("data/processed/item_meta.pkl")
ITEM_ID_LST = torch.LongTensor(meta_df["item_id"].to_list()).cuda()
RATING_LST = torch.LongTensor(meta_df["rating_number"].to_list())
graph = torch.load("data/processed/graph.pkl")
graph = HeteroData().from_dict(graph)