class Money:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Money: {self.name}, {self.category}, ${self.amount}"
    