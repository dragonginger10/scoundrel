from collections.abc import Generator

from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.css.query import DOMQuery
from textual.widgets import Button, Digits, Footer, Header, Log, Static

from scoundrel.cards.card import Card
from scoundrel.cards.deck import Deck
from scoundrel.tui.room import CardWidget, Room
from scoundrel.tui.weapon import WeaponSlot


class Scoundrel(App):

    CSS_PATH = "scoundrel.tcss"

    def __init__(self) -> None:
        self.ran: bool = False
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with HorizontalGroup():
            with VerticalGroup(classes="field decks"):
                yield Log()
                yield WeaponSlot()
            with VerticalGroup(classes="field play"):
                with HorizontalGroup(classes="game-controls"):
                    yield Button("New Game")
                    yield Button("Run", id="run")
                    yield Digits("20", id="health")
                yield Room()
        yield Footer()

    @on(Button.Pressed, "#run")
    def runner(self, event: Button.Pressed) -> None:
        room: Room = self.query_one("Room", Room)
        deck: Deck = room.deck
        slots: DOMQuery[CardWidget] = self.query(CardWidget)
        cards: list[Card] = [c.card for c in slots]
        new_cards: Generator[Card] = deck.run(cards)
        for c in slots:
            c.new_card(next(new_cards))
            room.cards = 4

        self.ran = True
        event.button.disabled = True
