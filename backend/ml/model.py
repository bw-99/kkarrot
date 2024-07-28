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
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=1, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_items)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.gru(x)
        x = self.relu(x[:, -1, :])
        x = self.fc(x)
        return x
    

class TailNet(nn.Module):
    def __init__(self, num_items, embedding_dim, hidden_dim, head_mapping_lst):
        super(TailNet, self).__init__()
        self.head_mapping_lst = head_mapping_lst
        
        self.head_idx = self.head_mapping_lst == 1
        self.tail_idx = self.head_mapping_lst == 0

        self.hidden_dim = hidden_dim
        self.embedding = nn.Embedding(num_items, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=2, batch_first=True)
        
        self.attn_key = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.attn_query = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.attn_fc = nn.Linear(hidden_dim, 1, bias=True)
        self.last_fc = nn.Linear(hidden_dim*2, num_items)
        
        self.adjust_attn_key = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.adjust_attn_query = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.adjust_attn_fc = nn.Linear(hidden_dim, 1, bias=True)
        self.adjust_last_fc = nn.Linear(hidden_dim*2, 1)

    def forward(self, item_idx):
        x = self.embedding(item_idx)
        item_emb, _ = self.gru(x)
        # head_indiciators, tail_indicators = is_head==1, is_head==0
        
        # * rectification factors
        item_types= self.head_mapping_lst[item_idx].view(item_idx.shape[0], item_idx.shape[1], 1)
        item_types = item_types.repeat(1, 1, self.hidden_dim)

        adjust_item_emb = item_emb + item_types
        adjust_last_item_emb = adjust_item_emb[:, -1, :].unsqueeze(dim=1)
        adjust_attention = self.adjust_attn_fc(F.tanh(self.adjust_attn_key(adjust_item_emb) + self.adjust_attn_query(adjust_last_item_emb)))
        adjust_global_session_emb = (adjust_item_emb * adjust_attention).sum(dim=1)
        adjust_local_session_emb = adjust_last_item_emb.view(item_idx.shape[0], -1)
        r_head = F.sigmoid(self.adjust_last_fc(torch.cat([adjust_global_session_emb, adjust_local_session_emb], dim=1)))
        r_tail = 1-r_head

        # * preference estimation
        last_item_emb = item_emb[:, -1, :].unsqueeze(dim=1)
        attention = self.attn_fc(F.tanh(self.attn_key(item_emb) + self.attn_query(last_item_emb)))
        global_session_emb = (item_emb * attention).sum(dim=1)
        local_session_emb = last_item_emb.view(item_idx.shape[0], -1)
        predicted_score = self.last_fc(torch.cat([global_session_emb, local_session_emb], dim=1))
        predicted_score[:, self.head_idx] *= r_head
        predicted_score[:, self.tail_idx] *= r_tail

        # ! * adjust r_head and r_tail to long, tail item
        predicted_score = F.softmax(predicted_score, dim=1)

        return predicted_score