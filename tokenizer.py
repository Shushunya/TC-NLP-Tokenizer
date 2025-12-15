"""
Finite State Automaton-Based Tokenizer
Theory of Computation Project - NLP Application
Enhanced Version with Strict Email Recognition
"""


class FSATokenizer:
    """
    A tokenizer implemented as a Finite State Automaton (FSA)
    Demonstrates state transitions for text processing
    Now requires proper domain format (must have TLD like .com, .org, etc.)
    """

    # Define states as constants
    START = "START"
    IN_WORD = "IN_WORD"
    IN_NUMBER = "IN_NUMBER"
    IN_PUNCTUATION = "IN_PUNCTUATION"
    IN_WHITESPACE = "IN_WHITESPACE"
    IN_EMAIL_LOCAL = "IN_EMAIL_LOCAL"
    IN_EMAIL_AT = "IN_EMAIL_AT"
    IN_EMAIL_DOMAIN = "IN_EMAIL_DOMAIN"
    IN_EMAIL_DOMAIN_DOT = "IN_EMAIL_DOMAIN_DOT"
    IN_EMAIL_TLD = "IN_EMAIL_TLD"
    IN_DECIMAL = "IN_DECIMAL"

    def __init__(self):
        self.state = self.START
        self.current_token = ""
        self.tokens = []
        self.token_types = []

        # Define state transition table
        self.setup_transitions()

    def setup_transitions(self):
        """
        Define the state transition table for the FSA
        Format: {(current_state, input_type): (next_state, action)}

        Email recognition now requires:
        local@domain.tld format (e.g., user@mail.com)
        """
        self.transitions = {
            # From START state
            (self.START, "ALPHA"): (self.IN_WORD, "append"),
            (self.START, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.START, "PUNCT"): (self.IN_PUNCTUATION, "append"),
            (self.START, "SPACE"): (self.IN_WHITESPACE, "ignore"),
            (self.START, "AT"): (self.IN_PUNCTUATION, "append"),
            (self.START, "DOT"): (self.IN_PUNCTUATION, "append"),
            # From IN_WORD state
            (self.IN_WORD, "ALPHA"): (self.IN_WORD, "append"),
            (self.IN_WORD, "DIGIT"): (self.IN_WORD, "append"),
            (self.IN_WORD, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_WORD, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_WORD, "AT"): (self.IN_EMAIL_AT, "append"),
            (self.IN_WORD, "DOT"): (self.IN_EMAIL_LOCAL, "append"),
            # From IN_EMAIL_LOCAL state (word with dots, before @)
            (self.IN_EMAIL_LOCAL, "ALPHA"): (self.IN_EMAIL_LOCAL, "append"),
            (self.IN_EMAIL_LOCAL, "DIGIT"): (self.IN_EMAIL_LOCAL, "append"),
            (self.IN_EMAIL_LOCAL, "DOT"): (self.IN_EMAIL_LOCAL, "append"),
            (self.IN_EMAIL_LOCAL, "AT"): (self.IN_EMAIL_AT, "append"),
            (self.IN_EMAIL_LOCAL, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_EMAIL_LOCAL, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_EMAIL_AT state (after @ symbol) - NOT AN ACCEPT STATE
            (self.IN_EMAIL_AT, "ALPHA"): (self.IN_EMAIL_DOMAIN, "append"),
            (self.IN_EMAIL_AT, "DIGIT"): (self.IN_EMAIL_DOMAIN, "append"),
            (self.IN_EMAIL_AT, "DOT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_EMAIL_AT, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_EMAIL_AT, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_EMAIL_AT, "AT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_EMAIL_DOMAIN state (domain part, before dot) - NOT AN ACCEPT STATE
            (self.IN_EMAIL_DOMAIN, "ALPHA"): (self.IN_EMAIL_DOMAIN, "append"),
            (self.IN_EMAIL_DOMAIN, "DIGIT"): (self.IN_EMAIL_DOMAIN, "append"),
            (self.IN_EMAIL_DOMAIN, "DOT"): (self.IN_EMAIL_DOMAIN_DOT, "append"),
            (self.IN_EMAIL_DOMAIN, "SPACE"): (
                self.IN_WHITESPACE,
                "save_as_word",
            ),  # Invalid email
            (self.IN_EMAIL_DOMAIN, "PUNCT"): (
                self.IN_PUNCTUATION,
                "save_as_word_and_append",
            ),
            (self.IN_EMAIL_DOMAIN, "AT"): (
                self.IN_PUNCTUATION,
                "save_as_word_and_append",
            ),
            # From IN_EMAIL_DOMAIN_DOT state (just read dot in domain) - NOT AN ACCEPT STATE
            (self.IN_EMAIL_DOMAIN_DOT, "ALPHA"): (self.IN_EMAIL_TLD, "append"),
            (self.IN_EMAIL_DOMAIN_DOT, "DIGIT"): (self.IN_EMAIL_TLD, "append"),
            (self.IN_EMAIL_DOMAIN_DOT, "DOT"): (self.IN_EMAIL_DOMAIN_DOT, "append"),
            (self.IN_EMAIL_DOMAIN_DOT, "SPACE"): (self.IN_WHITESPACE, "save_as_word"),
            (self.IN_EMAIL_DOMAIN_DOT, "PUNCT"): (
                self.IN_PUNCTUATION,
                "save_as_word_and_append",
            ),
            (self.IN_EMAIL_DOMAIN_DOT, "AT"): (
                self.IN_PUNCTUATION,
                "save_as_word_and_append",
            ),
            # From IN_EMAIL_TLD state (top-level domain like .com) - THIS IS AN ACCEPT STATE
            (self.IN_EMAIL_TLD, "ALPHA"): (self.IN_EMAIL_TLD, "append"),
            (self.IN_EMAIL_TLD, "DIGIT"): (self.IN_EMAIL_TLD, "append"),
            (self.IN_EMAIL_TLD, "DOT"): (
                self.IN_EMAIL_DOMAIN_DOT,
                "append",
            ),  # Allow .co.uk
            (self.IN_EMAIL_TLD, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_EMAIL_TLD, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_EMAIL_TLD, "AT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_NUMBER state
            (self.IN_NUMBER, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.IN_NUMBER, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_NUMBER, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_NUMBER, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_NUMBER, "DOT"): (self.IN_DECIMAL, "append"),
            (self.IN_NUMBER, "AT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_DECIMAL state (for decimal numbers)
            (self.IN_DECIMAL, "DIGIT"): (self.IN_DECIMAL, "append"),
            (self.IN_DECIMAL, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_DECIMAL, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_DECIMAL, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_DECIMAL, "DOT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_DECIMAL, "AT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_PUNCTUATION state
            (self.IN_PUNCTUATION, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_PUNCTUATION, "DIGIT"): (self.IN_NUMBER, "save_and_append"),
            (self.IN_PUNCTUATION, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_PUNCTUATION, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_PUNCTUATION, "AT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_PUNCTUATION, "DOT"): (self.IN_PUNCTUATION, "save_and_append"),
            # From IN_WHITESPACE state
            (self.IN_WHITESPACE, "ALPHA"): (self.IN_WORD, "append"),
            (self.IN_WHITESPACE, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.IN_WHITESPACE, "PUNCT"): (self.IN_PUNCTUATION, "append"),
            (self.IN_WHITESPACE, "SPACE"): (self.IN_WHITESPACE, "ignore"),
            (self.IN_WHITESPACE, "AT"): (self.IN_PUNCTUATION, "append"),
            (self.IN_WHITESPACE, "DOT"): (self.IN_PUNCTUATION, "append"),
        }

    def classify_char(self, char):
        """Classify a character into input types for the FSA"""
        if char.isalpha():
            return "ALPHA"
        elif char.isdigit():
            return "DIGIT"
        elif char.isspace():
            return "SPACE"
        elif char == "@":
            return "AT"
        elif char == ".":
            return "DOT"
        else:
            return "PUNCT"

    def save_token(self, force_type=None):
        """Save the current token and determine its type"""
        if self.current_token:
            self.tokens.append(self.current_token)

            # Determine token type based on state or forced type
            if force_type:
                token_type = force_type
            elif self.state == self.IN_WORD:
                token_type = "WORD"
            elif self.state in [self.IN_NUMBER, self.IN_DECIMAL]:
                token_type = "NUMBER"
            elif self.state == self.IN_PUNCTUATION:
                token_type = "PUNCTUATION"
            elif self.state in [self.IN_EMAIL_LOCAL, self.IN_EMAIL_TLD]:
                token_type = "EMAIL"
            else:
                # States that are not valid accept states for email
                token_type = "WORD"

            self.token_types.append(token_type)
            self.current_token = ""

    def process_transition(self, char, action):
        """Execute the action specified by the transition"""
        if action == "append":
            self.current_token += char
        elif action == "save":
            self.save_token()
        elif action == "save_and_append":
            self.save_token()
            self.current_token += char
        elif action == "save_as_word":
            # Force save as WORD (invalid email)
            self.save_token(force_type="WORD")
        elif action == "save_as_word_and_append":
            # Force save as WORD and start new token
            self.save_token(force_type="WORD")
            self.current_token += char
        elif action == "ignore":
            pass  # Do nothing for whitespace

    def tokenize(self, text):
        """
        Tokenize the input text using the FSA
        Returns a list of tokens and their types
        """
        self.state = self.START
        self.current_token = ""
        self.tokens = []
        self.token_types = []

        for char in text:
            char_type = self.classify_char(char)

            # Look up transition in the table
            transition_key = (self.state, char_type)

            if transition_key in self.transitions:
                next_state, action = self.transitions[transition_key]
                self.process_transition(char, action)
                self.state = next_state
            else:
                # Handle unexpected transitions
                # Save current token and start fresh
                self.save_token()
                self.state = self.START

                # Process the character again from START state
                char_type = self.classify_char(char)
                if (self.START, char_type) in self.transitions:
                    next_state, action = self.transitions[(self.START, char_type)]
                    self.process_transition(char, action)
                    self.state = next_state

        # Save any remaining token
        self.save_token()

        return list(zip(self.tokens, self.token_types))

    def print_state_diagram(self):
        """Print a text representation of the FSA state diagram"""
        print("\n=== FSA STATE DIAGRAM ===")
        print("\nStates:")
        print("  - START: Initial state")
        print("  - IN_WORD: Processing alphabetic characters")
        print("  - IN_NUMBER: Processing digits")
        print("  - IN_DECIMAL: Processing decimal numbers")
        print("  - IN_PUNCTUATION: Processing punctuation")
        print("  - IN_EMAIL_LOCAL: Processing local part of email (before @)")
        print("  - IN_EMAIL_AT: Just read @ symbol (NOT ACCEPT)")
        print("  - IN_EMAIL_DOMAIN: Processing domain before dot (NOT ACCEPT)")
        print("  - IN_EMAIL_DOMAIN_DOT: Just read dot in domain (NOT ACCEPT)")
        print(
            "  - IN_EMAIL_TLD: Processing top-level domain (.com, .org, etc.) (ACCEPT)"
        )
        print("  - IN_WHITESPACE: Processing spaces (tokens not saved)")

        print("\nEmail Recognition Flow:")
        print("  user@mail     -> IN_EMAIL_DOMAIN (NOT VALID - no TLD)")
        print("  user@mail.    -> IN_EMAIL_DOMAIN_DOT (NOT VALID - incomplete)")
        print("  user@mail.com -> IN_EMAIL_TLD (VALID - complete email)")

        print("\nKey Transitions:")
        print("  START --[letter]--> IN_WORD")
        print("  START --[digit]--> IN_NUMBER")
        print("  IN_WORD --[letter/digit]--> IN_WORD (stay)")
        print("  IN_WORD --[.]--> IN_EMAIL_LOCAL (dot in local part)")
        print("  IN_WORD --[@]--> IN_EMAIL_AT")
        print("  IN_EMAIL_LOCAL --[@]--> IN_EMAIL_AT")
        print("  IN_EMAIL_AT --[letter/digit]--> IN_EMAIL_DOMAIN")
        print("  IN_EMAIL_DOMAIN --[.]--> IN_EMAIL_DOMAIN_DOT")
        print("  IN_EMAIL_DOMAIN_DOT --[letter/digit]--> IN_EMAIL_TLD")
        print("  IN_EMAIL_TLD --[.]--> IN_EMAIL_DOMAIN_DOT (allows .co.uk)")
        print("  IN_NUMBER --[digit]--> IN_NUMBER (stay)")
        print("  IN_NUMBER --[.]--> IN_DECIMAL")
        print("  * --[space]--> Save token, go to IN_WHITESPACE")
        print()

    def print_formal_definition(self):
        """Print the formal definition of the FSA"""
        print("\n=== FORMAL DEFINITION OF FSA ===")
        print("\nM = (Q, Σ, δ, q₀, F)")
        print("\nQ (States):")
        print("  Q = {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈, q₉, q₁₀}")
        print("  q₀ = START")
        print("  q₁ = IN_WORD")
        print("  q₂ = IN_NUMBER")
        print("  q₃ = IN_PUNCTUATION")
        print("  q₄ = IN_WHITESPACE")
        print("  q₅ = IN_EMAIL_LOCAL")
        print("  q₆ = IN_EMAIL_AT (NOT ACCEPT)")
        print("  q₇ = IN_EMAIL_DOMAIN (NOT ACCEPT)")
        print("  q₈ = IN_EMAIL_DOMAIN_DOT (NOT ACCEPT)")
        print("  q₉ = IN_EMAIL_TLD (ACCEPT)")
        print("  q₁₀ = IN_DECIMAL")

        print("\nΣ (Input Alphabet):")
        print("  Σ = {ALPHA, DIGIT, SPACE, PUNCT, AT, DOT}")

        print("\nq₀ (Initial State):")
        print("  q₀ = START")

        print("\nF (Final/Accept States):")
        print("  F = {q₁, q₂, q₃, q₅, q₉, q₁₀}")
        print("  q₁ → WORD tokens")
        print("  q₂ → NUMBER tokens")
        print("  q₃ → PUNCTUATION tokens")
        print("  q₅ → EMAIL tokens (partial with dots)")
        print("  q₉ → EMAIL tokens (complete with TLD)")
        print("  q₁₀ → NUMBER tokens (decimal)")
        print("\n  IMPORTANT: q₆, q₇, q₈ are NOT accept states")
        print("  This ensures emails MUST have proper domain.tld format")

        print("\nδ (Transition Function):")
        print("  Total transitions: " + str(len(self.transitions)))
        print("  See transition table for complete definition")
        print()


# ===== DEMONSTRATION AND TESTING =====


def demonstrate_tokenizer():
    """Demonstrate the FSA tokenizer with various examples"""

    tokenizer = FSATokenizer()

    # Print the state diagram
    # tokenizer.print_state_diagram()

    # Print formal definition
    # tokenizer.print_formal_definition()

    # Test cases
    test_cases = [
        "Hello world!",
        "The price is $49.99 today.",
        "Contact me at user@example.com for details.",
        "Email john.doe@company.org now!",
        "Invalid: email@ee should be WORD not EMAIL",
        "Valid: test@mail.pt is EMAIL",
        "Python3 is great! Version 3.11 rocks.",
        "I scored 95.5 on the test, wow!!!",
        "My email is alice.smith@sub.domain.edu, thanks.",
        "Send to bob123@mail.co.uk immediately.",
        "Visit site.com or email info@site.com",
        "Numbers: 3.14, 2.718, and 1.414 are important.",
    ]

    print("=== TOKENIZATION EXAMPLES ===\n")

    for i, text in enumerate(test_cases, 1):
        print(f'Example {i}: "{text}"')
        result = tokenizer.tokenize(text)

        print("Tokens:")
        for token, token_type in result:
            print(f"  '{token}' -> {token_type}")
        print()

    # Statistical summary
    print("=== STATISTICS ===")
    all_results = [tokenizer.tokenize(text) for text in test_cases]
    total_tokens = sum(len(result) for result in all_results)

    token_type_counts = {}
    for result in all_results:
        for _, token_type in result:
            token_type_counts[token_type] = token_type_counts.get(token_type, 0) + 1

    print(f"Total tokens processed: {total_tokens}")
    print("\nToken type distribution:")
    for token_type, count in sorted(token_type_counts.items()):
        percentage = (count / total_tokens) * 100
        print(f"  {token_type}: {count} ({percentage:.1f}%)")

    # Test email recognition specifically with STRICT validation
    print("\n=== STRICT EMAIL RECOGNITION TEST ===")
    email_tests = [
        ("exam@ua.pt", True),
        ("john.doe@company.org", True),
        ("alice_smith@sub.domain.edu", True),
        ("bob123@mail.co.uk", True),
        ("info@site.com", True),
        ("first.last@domain.net", True),
        ("email@ee", False),  # Should be WORD - no TLD
        ("test@", False),  # Should be WORD - incomplete
        ("@domain.com", False),  # Should be PUNCT + WORD
        ("user@domain", False),  # Should be WORD - no TLD
    ]

    print("Testing strict email validation (must have domain.tld):")
    for email, should_be_email in email_tests:
        result = tokenizer.tokenize(email)
        tokens = [token for token, _ in result]
        types = [t_type for _, t_type in result]
        is_email = "EMAIL" in types
        status = "\t" if is_email == should_be_email else "-" * 8
        expected = "EMAIL" if should_be_email else "WORD/OTHER"
        print(
            f"{status} {email:30} -> {str(result[0]) if result else 'EMPTY':30} (expected: {expected})"
        )
        # Added str(...) around result[0]


# ===== MAIN EXECUTION =====

if __name__ == "__main__":
    demonstrate_tokenizer()

    # Interactive mode
    print("\n=== INTERACTIVE MODE ===")
    print("Enter text to tokenize (or 'quit' to exit):\n")

    tokenizer = FSATokenizer()

    while True:
        user_input = input("> ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        if user_input.strip():
            result = tokenizer.tokenize(user_input)
            print("\nTokens:")
            for token, token_type in result:
                print(f"  '{token}' -> {token_type}")
            print()
