# [Substring with Concatenation of All Words 🧩](https://leetcode.com/problems/substring-with-concatenation-of-all-words/description/?envType=study-plan-v2&envId=top-interview-150)

Welcome to a string puzzle where the goal is to spot perfect word blends inside a longer text. ✨

### 🔍 What the problem asks

You are given:
- a string `s` 📝
- an array of words `words` 📚

Every word in `words` has the same length.

A substring of `s` is valid when it is made by concatenating every word from `words` exactly once, one after another, with no extra letters or spaces inserted.

That means the words can appear in any order, as long as the substring is a complete permutation of the list.

### 💡 Why it’s interesting

Think of `words` as puzzle pieces 🧩. The challenge is to find every place in `s` where those pieces fit together perfectly in a row.

For example, if `words = ["ab", "cd", "ef"]`, these joined strings are valid:
- `abcdef` ✅
- `abefcd` ✅
- `cdabef` ✅
- `cdefab` ✅
- `efabcd` ✅
- `efcdab` ✅

But `acdbef` is not valid because the pieces are not aligned to form a full permutation of the original list. ❌

### 🎯 What to return

Return all starting indices in `s` where a valid concatenated substring begins.

The output order does not matter — just collect every valid starting position.

### 📌 Examples

- `s = "barfoothefoobarman"`, `words = ["foo","bar"]`
  - Output: `[0, 9]`
  - Explanation: the substrings starting at 0 and 9 are `barfoo` and `foobar`.

- `s = "wordgoodgoodgoodbestword"`, `words = ["word","good","best","word"]`
  - Output: `[]`
  - Explanation: no substring contains every word exactly once.

- `s = "barfoofoobarthefoobarman"`, `words = ["bar","foo","the"]`
  - Output: `[6, 9, 12]`
  - Explanation: each index marks the start of a valid concatenation.

### ⚙️ Constraints

- `1 <= s.length <= 10^4` 🔢
- `1 <= words.length <= 5000` 📏
- `1 <= words[i].length <= 30` 🔤
- `s` and `words[i]` contain only lowercase English letters 🇬🇧

### 🛣️ Approaches
| Approach | ⚙️ Core Mechanism | ⏱️ Time Complexity | 💾 Space Complexity | ✅ Biggest Pro | ❌ Biggest Con | 🏆 Viability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[1. Brute Force](docs/brute-force.md)** | Generate all exact permutations; slide window 1 character at a time. | $O(K! \cdot (K + N) \cdot M)$ | $O(K! \cdot M)$ | Easy to conceptualize and write the base logic. | Factorial scaling will instantly crash on larger inputs. | ❌ Fails (TLE/MLE) |
| **[2. Basic Window](docs/basic-sliding-window.md)** | Compare word frequencies; slide window 1 character at a time, rebuilding dictionary every step. | $O(N \cdot M)$ | $O(K)$ | Bypasses the need for factorial permutation generation. | Rebuilding the frequency map from scratch every single character is extremely slow. | ⚠️ Sub-optimal (Barely passes) |
| **[3. Staggered Window](docs/staggered-sliding-window.md)** | Jump by whole words using multiple starting offsets; dynamically update a single dictionary. | $O(N)$ | $O(K)$ | Processes every character essentially twice; highly scalable and fast. | The offset and inner loop logic is tricky to understand and implement initially. | ✅ Optimal |

**Variable Key:**
* $N$ = Length of the main string `s`
* $K$ = Total number of words in the `words` array
* $L$ = Length of each individual word
* $M$ = Total length of the concatenated string ($K \times L$)
---
