from collections.abc import Generator

from loguru import logger
from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.css.query import DOMQuery
from textual.widgets import Button, Digits

from scoundrel.cards.deck import Card, Deck, Hand
from scoundrel.tui.cardWidget import CardWidget
from scoundrel.tui.weapon import WeaponSlot


class Scoundrel(App):

    CSS_PATH = "scoundrel.tcss"

    def __init__(self) -> None:
        self.ran: bool = False
        self.deck: Deck = Deck()
        self.life: str = "20"
        self.slots: int = 4
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with HorizontalGroup(id="game-controls"):
            yield Button("New Game", id="new-game")
            yield Button("Run", id="run")
            yield Digits(self.life, id="health") # TODO: Make this work with int
        self.deck.shuffle()
        room: Generator[Card] = self.deck.draw(self.slots)
        with HorizontalGroup(id="room"):
            for card in room:
                logger.debug(card)
                yield CardWidget(card, self.deck)
        # with HorizontalGroup(id="weapons"):
        yield WeaponSlot()

    def on_button_pressed(self) -> None:
        self.weapon_check()
        if self.slots == 1:
            self.next_room()

    @on(Button.Pressed, "#run")
    def runner(self) -> None:
        slots: DOMQuery[CardWidget] = self.query(CardWidget)
        cards: Hand = [c.card for c in slots if c.card is not None]
        new_cards: Generator[Card] = self.deck.run(cards)
        for c in slots:
            c.new_card(next(new_cards))

        self.toggle_run()

    @on(Button.Pressed, "#new-game")
    async def new_game(self) -> None:
        self.deck = Deck()
        await self.recompose()


    def next_room(self) -> None:
        slots: DOMQuery[CardWidget] = self.query(CardWidget)
        required: int = sum(slot.beat for slot in slots)
        cards: Generator[Card] = self.deck.draw(required)
        for slot in slots:
            if slot.beat:
                self.slots = 4
                slot.new_card(next(cards))

    def toggle_run(self) -> None:
        button: Button = self.query_one("#run", Button)
        self.ran: bool = not self.ran
        button.disabled = not button.disabled

    def change_life(self, amount: int) -> None:
        digit: Digits = self.screen.query_one("#health", Digits)
        current: int = int(self.life)
        self.life = str(current - amount)
        digit.update(self.life)

    def weapon_check(self) -> None:
        weapon: WeaponSlot = self.query_one(WeaponSlot)
        slots = self.query(CardWidget)
        for slot in slots:
            if slot.card is None:
                continue
            attack: Button = slot.query_one("#attack", Button)
            if weapon.has_weapon() and weapon.can_hit(slot.card):
                attack.remove_class("hidden")
