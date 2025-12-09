"""
Finite State Automaton-Based Tokenizer
Theory of Computation Project - NLP Application
"""


class FSATokenizer:
    """
    A tokenizer implemented as a Finite State Automaton (FSA)
    Demonstrates state transitions for text processing
    """

    # Define states
    START = "START"
    IN_WORD = "IN_WORD"
    IN_NUMBER = "IN_NUMBER"
    IN_PUNCTUATION = "IN_PUNCTUATION"
    IN_WHITESPACE = "IN_WHITESPACE"
    IN_EMAIL = "IN_EMAIL"
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
        """
        self.transitions = {
            # From START state
            (self.START, "ALPHA"): (self.IN_WORD, "append"),
            (self.START, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.START, "PUNCT"): (self.IN_PUNCTUATION, "append"),
            (self.START, "SPACE"): (self.IN_WHITESPACE, "ignore"),
            (self.START, "AT"): (self.IN_PUNCTUATION, "append"),
            # From IN_WORD state
            (self.IN_WORD, "ALPHA"): (self.IN_WORD, "append"),
            (self.IN_WORD, "DIGIT"): (self.IN_NUMBER, "save_and_append"),
            (self.IN_WORD, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_WORD, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_WORD, "AT"): (self.IN_EMAIL, "append"),  # email detection
            # From IN_NUMBER state
            (self.IN_NUMBER, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.IN_NUMBER, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_NUMBER, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_NUMBER, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_NUMBER, "DOT"): (self.IN_DECIMAL, "append"),  # decimal numbers
            # From IN_DECIMAL state (for decimal numbers)
            (self.IN_DECIMAL, "DIGIT"): (self.IN_DECIMAL, "append"),
            (self.IN_DECIMAL, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_DECIMAL, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_DECIMAL, "SPACE"): (self.IN_WHITESPACE, "save"),
            # From IN_PUNCTUATION state
            (self.IN_PUNCTUATION, "ALPHA"): (self.IN_WORD, "save_and_append"),
            (self.IN_PUNCTUATION, "DIGIT"): (self.IN_NUMBER, "save_and_append"),
            (self.IN_PUNCTUATION, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
            (self.IN_PUNCTUATION, "SPACE"): (self.IN_WHITESPACE, "save"),
            # From IN_WHITESPACE state
            (self.IN_WHITESPACE, "ALPHA"): (self.IN_WORD, "append"),
            (self.IN_WHITESPACE, "DIGIT"): (self.IN_NUMBER, "append"),
            (self.IN_WHITESPACE, "PUNCT"): (self.IN_PUNCTUATION, "append"),
            (self.IN_WHITESPACE, "SPACE"): (self.IN_WHITESPACE, "ignore"),
            # From IN_EMAIL state
            (self.IN_EMAIL, "ALPHA"): (self.IN_EMAIL, "append"),
            (self.IN_EMAIL, "DIGIT"): (self.IN_EMAIL, "append"),
            (self.IN_EMAIL, "DOT"): (self.IN_EMAIL, "append"),
            (self.IN_EMAIL, "SPACE"): (self.IN_WHITESPACE, "save"),
            (self.IN_EMAIL, "PUNCT"): (self.IN_PUNCTUATION, "save_and_append"),
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

    def save_token(self):
        """Save the current token and determine its type"""
        if self.current_token:
            self.tokens.append(self.current_token)

            # Determine token type based on state
            if self.state == self.IN_WORD:
                token_type = "WORD"
            elif self.state in [self.IN_NUMBER, self.IN_DECIMAL]:
                token_type = "NUMBER"
            elif self.state == self.IN_PUNCTUATION:
                token_type = "PUNCTUATION"
            elif self.state == self.IN_EMAIL:
                token_type = "EMAIL"
            else:
                token_type = "OTHER"

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
        print("  - IN_EMAIL: Processing email addresses")
        print("  - IN_WHITESPACE: Processing spaces (tokens not saved)")

        print("\nKey Transitions:")
        print("  START --[letter]--> IN_WORD")
        print("  START --[digit]--> IN_NUMBER")
        print("  IN_WORD --[letter]--> IN_WORD (stay)")
        print("  IN_WORD --[@]--> IN_EMAIL")
        print("  IN_NUMBER --[digit]--> IN_NUMBER (stay)")
        print("  IN_NUMBER --[.]--> IN_DECIMAL")
        print("  * --[space]--> Save token, go to IN_WHITESPACE")
        print()


# ===== DEMONSTRATION AND TESTING =====


def demonstrate_tokenizer():
    """Demonstrate the FSA tokenizer with various examples"""

    tokenizer = FSATokenizer()

    # Print the state diagram
    tokenizer.print_state_diagram()

    # Test cases
    test_cases = [
        "Hello world!",
        "The price is $49.99 today.",
        "Contact me at user@example.com for details.",
        "Python3 is great! Version 3.11 rocks.",
        "I scored 95.5 on the test, wow!!!",
        "Don't forget: meeting@3pm tomorrow.",
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
