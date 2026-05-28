## 🪟 Approach 2: Basic Sliding Window

### 🧠 Intuition
Generating permutations is far too slow. Instead of caring about the *exact order* of the words, we only care about their *frequencies*. If our target list has two "foo"s and one "bar", any window in the main string that also has exactly two "foo"s and one "bar" is a valid match!

### ⚙️ Logic
1. Count the exact frequencies of the **`words`** in the target words array and store them in a dictionary.
2. Slide a window of size $M$ across the string, moving 1 character at a time.
3. At each step, chop the current window into smaller word-sized chunks ($L$).
4. Count the frequencies of these chunks.
5. If the window's frequency dictionary matches the target frequency dictionary perfectly, record the index.

### 💻 Pseudocode
```
function basic_sliding_window(s, words):
    target_counts = count_frequencies(words)
    window_length = length(words) * length(words[0])
    word_length = length(words[0])
    results = []
    
    for i from 0 to length(s) - window_length:
        current_window_counts = empty dictionary
        
        for j from i to i + window_length step word_length:
            chunk = s[j : j + word_length]
            current_window_counts[chunk] += 1
            
        if current_window_counts == target_counts:
            results.append(i)
            
    return results
```

### ⏱️ Complexity
- Time Complexity: $O(N \cdot M)$. For every single character in the string ($N$), we are iterating over the entire window size ($M$) to rebuild the frequency dictionary from scratch.

- Space Complexity: $O(K)$. We only store frequency maps of the unique words, which takes linear space based on the number of words.
---
