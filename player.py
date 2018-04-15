import itertools

from card import Card


class Player:
    def __init__(self, name, user, hand=(), chips=10000):
        self.name = name
        self.chips = chips
        self.dealer = False
        self.hand = list(hand)
        self.state = 0
        # 1 SEEN 2 PACKED
        self.user = user

    def see(self):
        self.state = 1
        return [str(i) for i in self.hand]

    def pack(self):
        self.state = 2

    def __gt__(self, other):
        return self.get_score() > other.get_score()

    def __eq__(self, other):
        return self.get_score() == other.get_score()

    def get_type(self):
        self.hand.sort(key=lambda i: i.num)
        if self.hand[0] == self.hand[1] == self.hand[2]:
            return 100000
        if self.hand[0].kind == self.hand[1].kind == self.hand[2].kind:
            if self.hand[0].num + 2 == self.hand[1].num + 1 == self.hand[2].num:
                return 10000
            return 1000
        if self.hand[0].num + 2 == self.hand[1].num + 1 == self.hand[2].num:
            return 100
        if self.hand[0] == self.hand[1] or self.hand[1] == self.hand[2]:
            return 10
        return 1

    def get_score(self):
        score = self.hand[0].num + self.hand[1].num + self.hand[2].num
        return score * self.get_type()

    def sort_hand(self):
        self.hand.sort(key=lambda i: i.num)


class AIPlayer(Player):
    def loss_rate(self):
        cards = []
        for kind in range(4):
            for num in range(13):
                cards.append(Card(kind, num))
        for i in self.hand:
            cards.remove(i)
        all = 18424
        loss = 0
        for hand in itertools.combinations(cards, 3):
            if not self.get_score() > Player("", hand).get_score():
                loss += 1
        return loss / all
