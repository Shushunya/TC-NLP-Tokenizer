# Formal Definition of the Enhanced FSA Tokenizer

## 1. Finite State Automaton (FSA) 5-Tuple

The enhanced tokenizer with complete email recognition is formally defined as a **Deterministic Finite Automaton (DFA)**:

**M = (Q, Σ, δ, q₀, F)**

Where:
- **Q** = Set of states
- **Σ** = Input alphabet
- **δ** = Transition function
- **q₀** = Initial state
- **F** = Set of accept/final states

---

## 2. Components Definition

### 2.1 Set of States (Q)

**Q = {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈}**

Where each state represents:
- **q₀** = START (initial state)
- **q₁** = IN_WORD (processing alphabetic characters)
- **q₂** = IN_NUMBER (processing numeric characters)
- **q₃** = IN_PUNCTUATION (processing punctuation marks)
- **q₄** = IN_WHITESPACE (processing whitespace - tokens not saved)
- **q₅** = IN_EMAIL_LOCAL (processing email local part before @)
- **q₆** = IN_EMAIL_AT (just read @ symbol)
- **q₇** = IN_EMAIL_DOMAIN (processing email domain after @)
- **q₈** = IN_DECIMAL (processing decimal numbers)

### 2.2 Input Alphabet (Σ)

The input alphabet consists of character classes:

**Σ = {ALPHA, DIGIT, SPACE, PUNCT, AT, DOT}**

Where:
- **ALPHA** = {a-z, A-Z} (alphabetic characters)
- **DIGIT** = {0-9} (numeric digits)
- **SPACE** = {' ', '\t', '\n', '\r'} (whitespace characters)
- **PUNCT** = {!, ?, ,, ;, :, -, _, etc.} (punctuation marks, excluding @ and .)
- **AT** = {@} (at symbol - email separator)
- **DOT** = {.} (period/dot - used in decimals, emails, and punctuation)

### 2.3 Initial State (q₀)

**q₀ = START**

The automaton always begins in the START state.

### 2.4 Set of Final/Accept States (F)

**F = {q₁, q₂, q₃, q₅, q₇, q₈}**

These states indicate that a valid token has been recognized:
- **q₁** (IN_WORD) → Token type: WORD
- **q₂** (IN_NUMBER) → Token type: NUMBER
- **q₃** (IN_PUNCTUATION) → Token type: PUNCTUATION
- **q₅** (IN_EMAIL_LOCAL) → Token type: EMAIL (partial - local part with dots)
- **q₇** (IN_EMAIL_DOMAIN) → Token type: EMAIL (complete email address)
- **q₈** (IN_DECIMAL) → Token type: NUMBER (decimal number)

**Note:** q₀ (START), q₄ (IN_WHITESPACE), and q₆ (IN_EMAIL_AT) are **not** accept states because:
- q₀: No token has been formed yet
- q₄: Whitespace is a delimiter, not a token
- q₆: Just read @, email is incomplete

---

## 3. Transition Function (δ)

The transition function **δ: Q × Σ → Q** is defined by the following complete transition table:

### 3.1 Complete Transition Table

| Current State (q) | Input (σ) | Next State δ(q, σ) | Action |
|-------------------|-----------|-------------------|---------|
| **q₀ (START)** | ALPHA | q₁ (IN_WORD) | Append character |
| q₀ | DIGIT | q₂ (IN_NUMBER) | Append character |
| q₀ | SPACE | q₄ (IN_WHITESPACE) | Ignore |
| q₀ | PUNCT | q₃ (IN_PUNCTUATION) | Append character |
| q₀ | AT | q₃ (IN_PUNCTUATION) | Append character |
| q₀ | DOT | q₃ (IN_PUNCTUATION) | Append character |
| **q₁ (IN_WORD)** | ALPHA | q₁ (IN_WORD) | Append character |
| q₁ | DIGIT | q₁ (IN_WORD) | Append character |
| q₁ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₁ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₁ | AT | q₆ (IN_EMAIL_AT) | Append character |
| q₁ | DOT | q₅ (IN_EMAIL_LOCAL) | Append character |
| **q₂ (IN_NUMBER)** | DIGIT | q₂ (IN_NUMBER) | Append character |
| q₂ | ALPHA | q₁ (IN_WORD) | Save token, append |
| q₂ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₂ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₂ | DOT | q₈ (IN_DECIMAL) | Append character |
| q₂ | AT | q₃ (IN_PUNCTUATION) | Save token, append |
| **q₃ (IN_PUNCTUATION)** | ALPHA | q₁ (IN_WORD) | Save token, append |
| q₃ | DIGIT | q₂ (IN_NUMBER) | Save token, append |
| q₃ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₃ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₃ | AT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₃ | DOT | q₃ (IN_PUNCTUATION) | Save token, append |
| **q₄ (IN_WHITESPACE)** | ALPHA | q₁ (IN_WORD) | Append character |
| q₄ | DIGIT | q₂ (IN_NUMBER) | Append character |
| q₄ | SPACE | q₄ (IN_WHITESPACE) | Ignore |
| q₄ | PUNCT | q₃ (IN_PUNCTUATION) | Append character |
| q₄ | AT | q₃ (IN_PUNCTUATION) | Append character |
| q₄ | DOT | q₃ (IN_PUNCTUATION) | Append character |
| **q₅ (IN_EMAIL_LOCAL)** | ALPHA | q₅ (IN_EMAIL_LOCAL) | Append character |
| q₅ | DIGIT | q₅ (IN_EMAIL_LOCAL) | Append character |
| q₅ | DOT | q₅ (IN_EMAIL_LOCAL) | Append character |
| q₅ | AT | q₆ (IN_EMAIL_AT) | Append character |
| q₅ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₅ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| **q₆ (IN_EMAIL_AT)** | ALPHA | q₇ (IN_EMAIL_DOMAIN) | Append character |
| q₆ | DIGIT | q₇ (IN_EMAIL_DOMAIN) | Append character |
| q₆ | DOT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₆ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₆ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₆ | AT | q₃ (IN_PUNCTUATION) | Save token, append |
| **q₇ (IN_EMAIL_DOMAIN)** | ALPHA | q₇ (IN_EMAIL_DOMAIN) | Append character |
| q₇ | DIGIT | q₇ (IN_EMAIL_DOMAIN) | Append character |
| q₇ | DOT | q₇ (IN_EMAIL_DOMAIN) | Append character |
| q₇ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₇ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₇ | AT | q₃ (IN_PUNCTUATION) | Save token, append |
| **q₈ (IN_DECIMAL)** | DIGIT | q₈ (IN_DECIMAL) | Append character |
| q₈ | ALPHA | q₁ (IN_WORD) | Save token, append |
| q₈ | PUNCT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₈ | SPACE | q₄ (IN_WHITESPACE) | Save token |
| q₈ | DOT | q₃ (IN_PUNCTUATION) | Save token, append |
| q₈ | AT | q₃ (IN_PUNCTUATION) | Save token, append |

### 3.2 Transition Function in Mathematical Notation

**From q₀ (START):**
- δ(q₀, ALPHA) = q₁
- δ(q₀, DIGIT) = q₂
- δ(q₀, SPACE) = q₄
- δ(q₀, PUNCT) = q₃
- δ(q₀, AT) = q₃
- δ(q₀, DOT) = q₃

**From q₁ (IN_WORD):**
- δ(q₁, ALPHA) = q₁
- δ(q₁, DIGIT) = q₁
- δ(q₁, SPACE) = q₄
- δ(q₁, PUNCT) = q₃
- δ(q₁, AT) = q₆
- δ(q₁, DOT) = q₅

**From q₂ (IN_NUMBER):**
- δ(q₂, DIGIT) = q₂
- δ(q₂, ALPHA) = q₁
- δ(q₂, SPACE) = q₄
- δ(q₂, PUNCT) = q₃
- δ(q₂, DOT) = q₈
- δ(q₂, AT) = q₃

**From q₃ (IN_PUNCTUATION):**
- δ(q₃, ALPHA) = q₁
- δ(q₃, DIGIT) = q₂
- δ(q₃, SPACE) = q₄
- δ(q₃, PUNCT) = q₃
- δ(q₃, AT) = q₃
- δ(q₃, DOT) = q₃

**From q₄ (IN_WHITESPACE):**
- δ(q₄, ALPHA) = q₁
- δ(q₄, DIGIT) = q₂
- δ(q₄, SPACE) = q₄
- δ(q₄, PUNCT) = q₃
- δ(q₄, AT) = q₃
- δ(q₄, DOT) = q₃

**From q₅ (IN_EMAIL_LOCAL):**
- δ(q₅, ALPHA) = q₅
- δ(q₅, DIGIT) = q₅
- δ(q₅, DOT) = q₅
- δ(q₅, AT) = q₆
- δ(q₅, SPACE) = q₄
- δ(q₅, PUNCT) = q₃

**From q₆ (IN_EMAIL_AT):**
- δ(q₆, ALPHA) = q₇
- δ(q₆, DIGIT) = q₇
- δ(q₆, DOT) = q₃
- δ(q₆, SPACE) = q₄
- δ(q₆, PUNCT) = q₃
- δ(q₆, AT) = q₃

**From q₇ (IN_EMAIL_DOMAIN):**
- δ(q₇, ALPHA) = q₇
- δ(q₇, DIGIT) = q₇
- δ(q₇, DOT) = q₇
- δ(q₇, SPACE) = q₄
- δ(q₇, PUNCT) = q₃
- δ(q₇, AT) = q₃

**From q₈ (IN_DECIMAL):**
- δ(q₈, DIGIT) = q₈
- δ(q₈, ALPHA) = q₁
- δ(q₈, PUNCT) = q₃
- δ(q₈, SPACE) = q₄
- δ(q₈, DOT) = q₃
- δ(q₈, AT) = q₃

---

## 4. Email Recognition State Machine

### 4.1 Email Recognition Flow

The FSA recognizes emails through the following state sequence:

**Simple email (user@domain.com):**
```
q₀ → q₁ → q₁ → q₁ → q₁ → q₆ → q₇ → q₇ → q₇ → q₇ → q₇ → q₇ → q₇ → q₇ → q₇ → q₇
START  u    s    e    r    @    d    o    m    a    i    n    .    c    o    m
```

**Email with dots (john.doe@example.org):**
```
q₀ → q₁ → q₁ → q₁ → q₁ → q₅ → q₅ → q₅ → q₅ → q₆ → q₇ → q₇ → ...
START  j    o    h    n    .    d    o    e    @    e    x    ...
```

### 4.2 Key Design Decisions

1. **Dots in different contexts:**
   - q₁ + DOT → q₅ (dots in email local part: "john.doe")
   - q₂ + DOT → q₈ (dots in numbers: "3.14")
   - q₃ + DOT → q₃ (dots as punctuation: sentence ending)

2. **Email validation:**
   - q₆ (IN_EMAIL_AT) is NOT an accept state (incomplete email)
   - q₇ (IN_EMAIL_DOMAIN) IS an accept state (complete email)
   - This ensures "@" alone is not recognized as an email

3. **Alphanumeric support:**
   - q₁ + DIGIT → q₁ (allows "user123@...")
   - q₇ + DIGIT → q₇ (allows "...@domain2.com")

---

## 5. Token Recognition and Acceptance

### 5.1 Acceptance Condition

A token is **accepted** when:
1. The automaton transitions from an accept state (q ∈ F) to another state, OR
2. The input string ends while the automaton is in an accept state

### 5.2 Token Type Mapping

When a token is accepted from state q ∈ F:

| State | Token Type | Example |
|-------|-----------|---------|
| q₁ (IN_WORD) | WORD | "hello", "Python3" |
| q₂ (IN_NUMBER) | NUMBER | "123", "2024" |
| q₃ (IN_PUNCTUATION) | PUNCTUATION | ".", "!", "," |
| q₅ (IN_EMAIL_LOCAL) | EMAIL | "john.doe" (partial) |
| q₇ (IN_EMAIL_DOMAIN) | EMAIL | "user@example.com" |
| q₈ (IN_DECIMAL) | NUMBER | "3.14", "99.99" |

---

## 6. Extended Transition Function (δ*)

The extended transition function **δ*: Q × Σ* → Q** processes strings:

**δ*(q, ε) = ε** (base case: empty string)  
**δ*(q, wa) = δ(δ*(q, w), a)** where w ∈ Σ*, a ∈ Σ

This allows the automaton to process entire input strings character by character.

---

## 7. Language Accepted by the FSA

The language **L(M)** accepted by this automaton consists of all valid sequences of tokens:

**L(M) = {w ∈ Σ* | δ*(q₀, w) ∈ F}**

This FSA recognizes:
- **Words**: sequences of alphabetic and alphanumeric characters
- **Numbers**: sequences of digits, optionally with one decimal point
- **Punctuation**: individual punctuation marks including dots
- **Email addresses**: patterns matching local@domain format with dots allowed
- **Mixed sequences**: separated by whitespace

---

## 8. Properties of This FSA

### 8.1 Deterministic
- For every state q ∈ Q and every input symbol σ ∈ Σ, there is **exactly one** next state δ(q, σ)
- No ε-transitions (empty transitions)
- Therefore, this is a **DFA** (Deterministic Finite Automaton)

### 8.2 Complete
- The transition function δ is defined for **all** combinations of (q, σ) where q ∈ Q and σ ∈ Σ
- Total transitions: 54 (9 states × 6 input symbols)
- No undefined transitions

### 8.3 Context-Sensitive Dot Handling
- The same input character (DOT) leads to different states depending on context:
  - From q₁ (word) → q₅ (email local)
  - From q₂ (number) → q₈ (decimal)
  - From q₃ (punctuation) → q₃ (stay in punctuation)

### 8.4 Token Separation
- Whitespace acts as a natural delimiter
- Transitions between different token types trigger token saves
- Self-loops accumulate characters for the same token

---

## 9. Example Traces

### 9.1 Simple Email: "user@mail.com"

| Step | Input | Type | Current | Next | Buffer | Action |
|------|-------|------|---------|------|--------|--------|
| 0 | - | - | q₀ | - | "" | Initialize |
| 1 | u | ALPHA | q₀ | q₁ | "u" | Append |
| 2 | s | ALPHA | q₁ | q₁ | "us" | Append |
| 3 | e | ALPHA | q₁ | q₁ | "use" | Append |
| 4 | r | ALPHA | q₁ | q₁ | "user" | Append |
| 5 | @ | AT | q₁ | q₆ | "user@" | Append |
| 6 | m | ALPHA | q₆ | q₇ | "user@m" | Append |
| 7 | a | ALPHA | q₇ | q₇ | "user@ma" | Append |
| 8 | i | ALPHA | q₇ | q₇ | "user@mai" | Append |
| 9 | l | ALPHA | q₇ | q₇ | "user@mail" | Append |
| 10 | . | DOT | q₇ | q₇ | "user@mail." | Append |
| 11 | c | ALPHA | q₇ | q₇ | "user@mail.c" | Append |
| 12 | o | ALPHA | q₇ | q₇ | "user@mail.co" | Append |
| 13 | m | ALPHA | q₇ | q₇ | "user@mail.com" | Append |
| 14 | (end) | - | q₇ | - | - | Save "user@mail.com" (EMAIL) |

**Output:** [("user@mail.com", EMAIL)]

### 9.2 Decimal Number: "Price: $49.99"

| Step | Input | Type | Current | Next | Buffer | Action |
|------|-------|------|---------|------|--------|--------|
| 0-5 | Price | ALPHA | q₀→q₁ | q₁ | "Price" | Build word |
| 6 | : | PUNCT | q₁ | q₃ | ":" | Save "Price" (WORD), new token |
| 7 | (space) | SPACE | q₃ | q₄ | - | Save ":" (PUNCT) |
| 8 | $ | PUNCT | q₄ | q₃ | "$" | Append |
| 9 | 4 | DIGIT | q₃ | q₂ | "4" | Save "$" (PUNCT), new token |
| 10 | 9 | DIGIT | q₂ | q₂ | "49" | Append |
| 11 | . | DOT | q₂ | q₈ | "49." | Append |
| 12 | 9 | DIGIT | q₈ | q₈ | "49.9" | Append |
| 13 | 9 | DIGIT | q₈ | q₈ | "49.99" | Append |
| 14 | (end) | - | q₈ | - | - | Save "49.99" (NUMBER) |

**Output:** [("Price", WORD), (":", PUNCT), ("$", PUNCT), ("49.99", NUMBER)]

### 9.3 Email with Dots: "john.doe@company.org"

| Step | Input | Type | Current | Next | Buffer | Key Transition |
|------|-------|------|---------|------|--------|----------------|
| 1-4 | john | ALPHA | q₀→q₁ | q₁ | "john" | Building word |
| 5 | . | DOT | q₁ | q₅ | "john." | **Enter email local** |
| 6-8 | doe | ALPHA | q₅ | q₅ | "john.doe" | Continue in email local |
| 9 | @ | AT | q₅ | q₆ | "john.doe@" | **Enter email AT state** |
| 10-16 | company | ALPHA | q₆→q₇ | q₇ | "john.doe@company" | **Enter email domain** |
| 17 | . | DOT | q₇ | q₇ | "john.doe@company." | Stay in domain |
| 18-20 | org | ALPHA | q₇ | q₇ | "john.doe@company.org" | Complete domain |
| 21 | (end) | - | q₇ | - | - | Save "john.doe@company.org" (EMAIL) |

**Output:** [("john.doe@company.org", EMAIL)]

---

## 10. Complexity Analysis

### Time Complexity
- **O(n)** where n is the length of the input string
- Each character is processed exactly once
- State transition lookup is O(1) using hash table

### Space Complexity
- **O(m)** where m is the total length of all tokens
- Stores current token buffer and token list
- FSA structure (54 transitions) is constant O(1)

---

## 11. Comparison with Previous Version

| Feature | Previous FSA | Enhanced FSA |
|---------|-------------|--------------|
| States | 7 | 9 |
| Email Recognition | Basic | Complete (local@domain) |
| Dot Handling | Context-free | Context-sensitive |
| Email States | 1 (IN_EMAIL) | 3 (LOCAL, AT, DOMAIN) |
| Validation | Weak | Strong (@ must have domain) |
| Dots in Emails | Not supported | Fully supported |
| Accept States | 5 | 6 |

---

## 12. Relation to Theory of Computation

### 12.1 Chomsky Hierarchy
This tokenizer recognizes **Regular Languages** (Type-3 in Chomsky hierarchy)

### 12.2 Equivalence
This DFA can be equivalently represented as:
- A Regular Expression (though complex for email pattern)
- A Non-deterministic Finite Automaton (NFA)
- A Regular Grammar

### 12.3 Closure Properties
The language recognized is closed under:
- Union
- Concatenation
- Kleene star
- Intersection
- Complement

---

## 13. Summary

**Complete Formal Definition:**

**M_tokenizer = (Q, Σ, δ, q₀, F)**

Where:
- **Q = {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈}** (9 states)
- **Σ = {ALPHA, DIGIT, SPACE, PUNCT, AT, DOT}** (6 input classes)
- **δ** = As defined in the transition table (54 transitions total)
- **q₀ = q₀ (START)**
- **F = {q₁, q₂, q₃, q₅, q₇, q₈}** (6 accept states)

**Key Enhancements:**
1. Complete email recognition with local@domain structure
2. Context-sensitive dot handling (emails vs decimals vs punctuation)
3. Support for dots in email local parts (john.doe@...)
4. Strong validation (@ must be followed by domain)
5. Proper acceptance states for complete email addresses

This enhanced DFA successfully tokenizes natural language text with robust email recognition while maintaining deterministic and complete properties.