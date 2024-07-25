import torch
from ml.model import *
from torch_geometric.data import HeteroData
from torch_geometric.loader import LinkNeighborLoader
import pandas as pd

RETRIEVE_TOPK = 500
NUM_NEI1, NUM_NEI2 = 100, 50

def retrieve(model:TTRecommender, user_id, item_id_lst):
    user_lst = torch.repeat_interleave(torch.tensor([user_id]), item_id_lst.shape[0])
    with torch.no_grad():
        preds = model(user_lst.cuda(), item_id_lst)
        pred_idx = torch.argsort(preds, descending=True)[:RETRIEVE_TOPK].cpu()
    return pred_idx

def link_prediction(model:LinkPrediction, user_id, item_id_lst, graph:HeteroData):
    edge_label_index = torch.stack([
        torch.repeat_interleave(torch.tensor([user_id]), item_id_lst.shape[0]),
        item_id_lst
    ])

    data_loader = LinkNeighborLoader(
        data=graph,
        num_neighbors=[NUM_NEI1, NUM_NEI2],
        edge_label_index=(("user", "rates", "item"), edge_label_index),
        batch_size=3 * 1024,
        shuffle=False,
    )

    scores = []
    for sampled_data in data_loader:
        with torch.no_grad():
            scores.append(model(sampled_data.cuda()).cpu().squeeze())
    scores = torch.cat(scores)
    scores = (scores-scores.min())/(scores.max()-scores.min())
    return scores

def corresponding_popularity(item_id_lst, meta_df):
    rating_numbers = torch.LongTensor(pd.merge(
        pd.DataFrame(item_id_lst, columns=['item_id']), 
        meta_df, on='item_id', how='left')["rating_number"])
    rating_numbers = (rating_numbers-rating_numbers.min())/(rating_numbers.max()-rating_numbers.min())
    return rating_numbers