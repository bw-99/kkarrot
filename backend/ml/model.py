import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv, to_hetero
from torch import Tensor
from torch_geometric.data import HeteroData
import torch_geometric.transforms as T

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = GATv2Conv(hidden_channels, hidden_channels, add_self_loops=False)
        self.conv2 = GATv2Conv(hidden_channels, hidden_channels, add_self_loops=False)
    def forward(self, x: Tensor, edge_index: Tensor):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x


class LinkPrediction(torch.nn.Module):
    def __init__(self, hidden_channels, num_user, num_item):
        super().__init__()
        self.user_emb = nn.Sequential(
            nn.Embedding(num_user, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        self.item_emb = nn.Sequential(
            nn.Embedding(num_item, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )

        self.classifier = nn.Linear(hidden_channels*2, 1)
        self.gnn = GNN(hidden_channels)
        self.gnn = to_hetero(self.gnn, metadata=(['user', 'item'], [('user', 'rates', 'item'), ('item', 'rev_rates', 'user')]))
        
    def forward(self, data: HeteroData):
        x_dict = {
          "user": self.user_emb(data["user"].node_id),
          "item": self.item_emb(data["item"].node_id),
        } 
        x_dict = self.gnn(x_dict, data.edge_index_dict)
        pref_embed = torch.cat([x_dict["user"][data["user", "rates", "item"].edge_label_index[0]],
            x_dict["item"][data["user", "rates", "item"].edge_label_index[1]]], dim=1)

        pred = self.classifier(pref_embed)
        return pred
    

class TTRecommender(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim):
        super(TTRecommender, self).__init__()
        self.item_embedding = nn.Sequential(
            nn.Embedding(num_items, embedding_dim), 
        )
        self.user_embedding = nn.Sequential(
            nn.Embedding(num_users, embedding_dim), 
        )

    def forward(self, user_idx, item_idx):
        user_emb = self.user_embedding(user_idx)
        item_emb = self.item_embedding(item_idx)

        return (user_emb * item_emb).sum(dim=-1)
    

class GRURecommender(nn.Module):
    def __init__(self, num_items, embedding_dim, hidden_dim):
        super(GRURecommender, self).__init__()
        self.embedding = nn.Embedding(num_items, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_items)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.gru(x)
        x = self.relu(x[:, -1, :])
        x = self.fc(x)
        return x