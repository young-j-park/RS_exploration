
from typing import List

import numpy as np


class RandomAgent:
    def __init__(self, num_users: int, num_candidates: int, slate_size: int):
        self.num_users = num_users
        self.num_candidates = num_candidates
        self.slate_size = slate_size

    def update_policy(self, obs: np.ndarray):
        pass

    def select_action(
            self,
            available_doc_ids: List[int]
    ):
        recs = [
            np.random.choice(
                np.arange(self.num_candidates),
                self.slate_size,
                replace=False
            )
            for _ in range(self.num_users)
        ]
        return np.array(recs)


