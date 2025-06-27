class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def exists(self, name: str) -> bool:
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False

    def declare(self, name, type_):
        if name in self.scopes[-1]:
            raise Exception(f"❌ Variable '{name}' already declared in this scope.")
        self.scopes[-1][name] = type_

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"❌ Variable '{name}' is not declared.")

    def current_scope(self):
        return self.scopes[-1]
