from typing import List
from .approaches import Approaches

# 🪟 This file is the LeetCode-facing entrypoint for the substring problem.
# Right now it only contains a scaffold, and the full sliding-window
# implementation still needs to be added.
class Solution(Approaches):
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        # 🪟 Sliding-window logic will collect every valid starting index.
        # 🚧 For now, this remains a scaffold until the full matcher is added.
        self._s = s
        self._words = words

        # ans1 = self.approach_01_brute_force()
        # ans2 = self.approach_02_sliding_window()
        ans3 = self.approach_03_staggered_sliding_window()
        
        return ans3
        