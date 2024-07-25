import torch
from ml.model import *


def load_twotower(save_path="parameters/twotower.pth"):
    data = torch.load(save_path)
    model = TTRecommender(
        num_items=data["num_items"],
        num_users=data["num_users"],
        embedding_dim=data["embedding_dim"],
    )
    model.load_state_dict(data["state_dict"])
    return model


def load_linkprediction(save_path="parameters/linkprediction.pth"):
    data = torch.load(save_path)
    model = LinkPrediction(
        num_item=data["num_item"],
        num_user=data["num_user"],
        hidden_channels=data["hidden_channels"],
    )
    model.load_state_dict(data["state_dict"])
    return model


def load_session(save_path="parameters/session.pth"):
    data = torch.load(save_path)
    model = GRURecommender(
        num_items=data["num_items"],
        embedding_dim=data["embedding_dim"],
        hidden_dim=data["hidden_dim"],
    )
    model.load_state_dict(data["state_dict"])
    return model