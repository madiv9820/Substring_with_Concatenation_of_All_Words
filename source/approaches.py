from typing import List, Counter, DefaultDict, Set
from collections import Counter, defaultdict

class Approaches:
    
    # ---------------------------------------------------------
    # 🔄 HELPER FUNCTION FOR APPROACH 1
    # ---------------------------------------------------------
    def __permutate(self, current_idx: int, valid_combinations: Set[str]) -> None:
        # 🧵 Base case: If we've swapped our way to the end, 
        # join the words together and save the full string!
        if current_idx == len(self._words):
            valid_combinations.add(''.join(word for word in self._words))
            return
        
        # 🔀 Recursive backtracking to generate EVERY possible arrangement (permutation)!
        for swap_idx in range(current_idx, len(self._words)):
            # 🔄 Swap current element with the element at the index
            self._words[swap_idx], self._words[current_idx] = self._words[current_idx], self._words[swap_idx]
            
            # 🤿 Dive deeper! Recursively generate permutations for the remaining elements
            self.__permutate(current_idx + 1, valid_combinations)
            
            # 🔙 Backtrack: Swap back to restore the original list order for the next loop iteration
            self._words[swap_idx], self._words[current_idx] = self._words[current_idx], self._words[swap_idx]

    # ---------------------------------------------------------
    # 💥 APPROACH 1: BRUTE FORCE (The "Try Everything" Method) 💥
    # ---------------------------------------------------------
    def approach_01_brute_force(self) -> List[int]:
        result_indices: List[int] = []

        # 1️⃣ Generate every possible concatenated string combination
        valid_combinations: Set[str] = set()
        self.__permutate(0, valid_combinations)

        # 2️⃣ Calculate the exact window size we need to check in the main string 📏
        num_words: int = len(self._words)
        word_length: int = len(self._words[0])
        string_length: int = len(self._s)
        total_window_length: int = num_words * word_length

        window_start: int = 0
        window_end: int = total_window_length - 1

        # 3️⃣ Slide a window of the exact total length across the string... 
        # moving a painfully slow 1 character at a time! 🐌
        while window_end < string_length:
            # 🎯 If the chunk inside our window matches ANY of our permutations, save the index!
            current_substring = self._s[window_start : window_end + 1]
            if current_substring in valid_combinations:
                result_indices.append(window_start)

            # ➡️ Shift the window forward by 1 character
            window_start += 1
            window_end += 1
        
        return result_indices

    # ---------------------------------------------------------
    # 🪟 APPROACH 2: BASIC SLIDING WINDOW (Character by Character) 🪟
    # ---------------------------------------------------------
    def approach_02_sliding_window(self) -> List[int]:        
        result_indices: List[int] = []

        num_words: int = len(self._words)
        word_length: int = len(self._words[0])
        string_length: int = len(self._s)
        total_window_length: int = num_words * word_length

        window_start: int = 0
        window_end: int = total_window_length - 1

        # 🎯 The target frequencies of words we are hunting for!
        target_word_freqs: Counter = Counter(self._words)
        current_window_freqs: DefaultDict = defaultdict(int)

        # 🐢 Slide a window across the string, moving just ONE character at a time...
        while window_end < string_length:

            # ✂️ Break the current window into word-sized chunks and count 'em up!
            for index in range(window_start, window_end + 1, word_length):
                current_word = self._s[index : index + word_length]
                current_window_freqs[current_word] += 1

            # 🎉 If the frequencies in our window perfectly match our target, it's a valid substring!
            if current_window_freqs == target_word_freqs:
                result_indices.append(window_start)

            # 🧹 Clear the dictionary so we can rebuild it from scratch next loop (very inefficient!)
            current_window_freqs.clear()
            
            # ➡️ Shift the window forward by 1 character
            window_start += 1
            window_end += 1

        return result_indices
    
    # ---------------------------------------------------------
    # 🚀 APPROACH 3: STAGGERED SLIDING WINDOW (The Optimized Word-Jumper!) 🚀
    # ---------------------------------------------------------
    def approach_03_staggered_sliding_window(self) -> List[int]:
        result_indices: List[int] = []

        num_words: int = len(self._words)
        word_length: int = len(self._words[0])
        string_length: int = len(self._s)

        # 🎯 Target frequencies (What are we looking for?)
        target_word_freqs: Counter = Counter(self._words)

        # 🏁 1. OUTER LOOP: Determine the starting offset. 
        # We only need to run this 'word_length' times to cover every possible starting index!
        for offset in range(word_length):
            window_start: int = offset
            matched_words_count: int = 0
            current_window_freqs: DefaultDict = defaultdict(int)

            # 🦘 2. INNER LOOP: Slide the right boundary forward by WHOLE words, not single characters!
            for window_end in range(window_start, string_length - word_length + 1, word_length):
                
                # 📥 Grab the incoming word on the right side of the window
                incoming_word: str = self._s[window_end : window_end + word_length]
                
                # ✨ Case A: The word is part of our target list!
                if incoming_word in target_word_freqs:
                    current_window_freqs[incoming_word] += 1
                    matched_words_count += 1

                    # 🗜️ Shrink time! If we collected too many of this specific word, we must 
                    # shrink the window from the left until we drop the extra copy!
                    while current_window_freqs[incoming_word] > target_word_freqs[incoming_word]:
                        outgoing_word: str = self._s[window_start : window_start + word_length]
                        current_window_freqs[outgoing_word] -= 1
                        matched_words_count -= 1
                        window_start += word_length  # ➡️ Move left boundary forward by a whole word
                    
                    # 🏆 MATCH FOUND! We collected the exact total number of valid words!
                    if matched_words_count == num_words:
                        result_indices.append(window_start)
                
                # 🚨 Case B: The word is NOT in our target list (Garbage word!) 🗑️
                else:
                    # 💥 This breaks any potential valid sequence. 
                    # Reset all trackers and jump the left boundary entirely past this garbage word!
                    current_window_freqs.clear()
                    matched_words_count = 0
                    window_start = window_end + word_length

        return result_indices
    