import random

from card import Card


class Board:
    def __init__(self, players, min_chips=100, max_chips=3000):
        assert (2 <= len(players) <= 6)
        self.players = players
        self.min = min_chips
        self.max = max_chips
        self.chips = 0
        self.current_chips = 0
        self.cards = []
        self.shuffle()
        random.choice(players).dealer = True
        index = 0
        while not self.players[index].dealer:
            index += 1
        self.dealer = self.players[index]
        self.players = self.players[index:] + self.players[:index]
        self.current = 0

    def shuffle(self):
        self.cards = []
        for kind in range(4):
            for num in range(13):
                self.cards.append(Card(kind, num))

    def deal(self, player):
        card = random.choice(self.cards)
        self.cards.remove(card)
        player.hand.append(card)

    def deal_all(self):
        for i in range(3):
            for player in self.players:
                self.deal(player)
        print("Cards left {}".format(len(self.cards)))
        for player in self.players:
            self.chips += self.min
            player.chips -= self.min
        self.current_chips = self.min

    def __repr__(self):
        result = ""
        for player in self.players:
            result += "{} {} {}\n".format(player.name, player.dealer, player.hand)
        return result

    def check(self):
        winner = None
        left = []
        for player in self.players:
            if player.state != 2:
                left.append(player)
        for i in range(len(left)):
            if winner is not None:
                if not winner > left[i]:
                    winner = left[i]
            else:
                winner = left[i]
        return winner
