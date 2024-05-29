def parse(tokens):
    i = 0

    def match(token):
        nonlocal i
        if i < len(tokens) and tokens[i] == token:
            i += 1
        else:
            raise SyntaxError(f"Expected {token}, got {tokens[i]}")

    def stmt():
        nonlocal i
        if i < len(tokens) and tokens[i] == 'if':
            open_stmt()
        else:
            matched_stmt()

    def matched_stmt():
        nonlocal i
        if i < len(tokens) and tokens[i] == 'if':
            match('if')
            expr()
            match('then')
            matched_stmt()
            match('else')
            matched_stmt()
        elif i < len(tokens) and tokens[i] == 'other':
            match('other')
        else:
            raise SyntaxError(f"Unexpected token in matched_stmt: {tokens[i]}")

    def open_stmt():
        nonlocal i
        if i < len(tokens) and tokens[i] == 'if':
            match('if')
            expr()
            match('then')
            stmt()
            if i < len(tokens) and tokens[i] == 'else':
                match('else')
                stmt()
        else:
            raise SyntaxError(f"Unexpected token in open_stmt: {tokens[i]}")

    def expr():
        nonlocal i
        if i < len(tokens) and tokens[i] == 'expr':
            match('expr')
        else:
            raise SyntaxError(f"Unexpected token in expr: {tokens[i]}")

    stmt()
    if i < len(tokens):
        raise SyntaxError(f"Unexpected token at the end: {tokens[i]}")

# Example usage:
tokens = ['if', 'expr', 'then', 'expr', 'then', 'other', 'else', 'other']
parse(tokens)  # This should parse successfully
