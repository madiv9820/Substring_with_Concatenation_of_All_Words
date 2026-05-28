## 🚀 Approach 3: Staggered Sliding Window (Optimal)

### 🧠 Intuition
Moving by 1 character is inefficient because we end up recalculating the exact same words over and over. Since all valid words have the exact same length, we should jump by whole words! To ensure we don't accidentally skip the correct starting index, we run our whole-word jumps multiple times using different starting "offsets".

### ⚙️ Logic
1. Create an **Outer Loop (Offset)** that runs $L$ times. This ensures every possible starting index is covered.
2. Create an **Inner Loop (Right Pointer)** that jumps forward by $L$ (whole words) instead of 1 character.
3. Maintain a running dictionary of word counts. When a valid word enters the window on the right, add it to the count.
4. If a word's count exceeds what we need, move the **Left Pointer** forward (by whole words) to shrink the window and drop the excess.
5. If a garbage word is found (not in our target list), clear the current dictionary and immediately jump the Left Pointer past it.
6. If the number of valid matched words equals $K$, record the index.

### 💻 Pseudocode
```
function staggered_sliding_window(s, words):
    target_counts = count_frequencies(words)
    word_length = length(words[0])
    results = []
    
    for offset from 0 to word_length - 1:
        left = offset
        current_counts = empty dictionary
        words_matched = 0
        
        for right from offset to length(s) step word_length:
            incoming_word = s[right : right + word_length]
            
            if incoming_word is in target_counts:
                current_counts[incoming_word] += 1
                words_matched += 1
                
                while current_counts[incoming_word] > target_counts[incoming_word]:
                    outgoing_word = s[left : left + word_length]
                    current_counts[outgoing_word] -= 1
                    words_matched -= 1
                    left += word_length
                    
                if words_matched == total_words:
                    results.append(left)
            else:
                current_counts.clear()
                words_matched = 0
                left = right + word_length
                
    return results
```

### ⏱️ Complexity
- Time Complexity: $O(N)$. Because the inner loop jumps by **`word_length`** and the outer loop runs **`word_length`** times, every single character in the string is processed exactly twice (once when the right pointer expands over it, once when the left pointer shrinks past it). Hash map operations are $O(1)$.

- Space Complexity: $O(K)$. We maintain hash maps for the target frequencies and the current window frequencies, which scale with the number of unique words.
---
