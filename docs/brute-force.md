## 💥 Approach 1: The Brute Force Method

### 🧠 Intuition
The most straightforward way to solve this is to ask: *"What are all the possible valid combinations of these words?"* If we can generate every single valid concatenated string, we can simply scan the main string and see if any of those combinations appear.

### ⚙️ Logic
1. Use recursive backtracking to generate every possible permutation of the **`words`** array.
2. Join each permutation into a single long string and store them in a Set for fast $O(1)$ lookups.
3. Slide a fixed-length window (size $M$) across the main string **`s`**, moving exactly 1 character at a time.
4. If the chunk of text inside the window exists in our Set of permutations, record the starting index.

### 💻 Pseudocode
```
function brute_force(s, words):
    valid_combinations = set()
    generate_all_permutations(words, valid_combinations)
    
    window_length = length(words) * length(words[0])
    results = []
    
    for i from 0 to length(s) - window_length:
        current_chunk = s[i : i + window_length]
        if current_chunk exists in valid_combinations:
            results.append(i)
            
    return results
```

### ⏱️ Complexity
- Time Complexity: $O(K! \cdot (K + N) \cdot M)$. Generating permutations takes factorial time $O(K!)$. Slicing and hashing the string during the window slide takes $O(N \cdot M)$. This will cause a Time Limit Exceeded (TLE) error for large arrays.

- Space Complexity: $O(K! \cdot M)$. We must store every single permutation in memory, which scales factorially.
---
