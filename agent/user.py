
import torch
import torch.nn as nn

from config.config import PAD_IDX


class UserModel(nn.Module):
    def __init__(
            self,
            num_candidates: int,
            emb_dim: int,
            aggregate: str,
    ):
        super(UserModel, self).__init__()
        self.num_candidates = num_candidates
        self.item_emb = nn.Embedding(num_candidates+1, emb_dim, PAD_IDX+1)
        if aggregate == 'mean':
            self.aggregate_fn = {
                'pos': lambda x: torch.mean(x, dim=1),
                'neg': lambda x: torch.mean(x, dim=1)
            }
        elif aggregate == 'gru':
            self.gru_layer_pos = nn.GRU(
                input_size=emb_dim,
                hidden_size=emb_dim,
                num_layers=2,
                batch_first=True,
                dropout=0.1,
                bidirectional=False
            )
#             self.gru_layer_neg = nn.GRU(
#                 input_size=emb_dim,
#                 hidden_size=emb_dim,
#                 num_layers=2,
#                 batch_first=True,
#                 dropout=0.1,
#                 bidirectional=False
#             )
            self.aggregate_fn = {
                'pos': lambda x: self.gru_layer_pos(x)[0][:, -1],
#                 'neg': lambda x: self.gru_layer_neg(x)[0][:, -1]
            }

    def forward(self, state):
        """
        Args:
            state: (N, 2, W)

        Returns:
            emb: (N, 2*D)

        """
        state += 1
        emb_p = self.item_emb(state[:, 0, :])
        return self.aggregate_fn['pos'](emb_p)
#         emb_n = self.item_emb(state[:, 1, :])
#         emb = torch.cat(
#             [self.aggregate_fn['pos'](emb_p), self.aggregate_fn['neg'](emb_n)], dim=1
#         )
#         return emb
