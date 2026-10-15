from scoundrel.cards import Card


class Player:
    def __init__(self, life: int) -> None:
        self.life: int = life
        self.weapon: Card | None = None
        self.durability: Card | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.life}, {self.weapon})"

    def __str__(self) -> str:
        return f"Player has {self.life} remaining"
        
    def hurt(self, damage: int) -> None:
        self.life -= damage

    def heal(self, recover: int) -> None:
        self.life += recover

    def set_weapon(self, card: Card) -> None:
        self.weapon = card
        if self.durability:
            self.durability = None

    def attack(self, card: Card) -> None:
        if self.weapon and self.durability > card:
            harm = card.damage(self.weapon)
            self.durability = card
        else:
            harm = card.damage()

        if self.durability is not None and self.durability.get_value() == 2:
            self.weapon = None
            self.durability = None

        if harm > 0:
            self.hurt(harm)

