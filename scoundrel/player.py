from scoundrel.cards.card import Card


class Player:
    def __init__(self) -> None:
        self.health: int = 20
        self.weapon: Card | None = None
        
    def set_weapon(self, card: Card) -> None:
        self.weapon = card
