class Card:
    def __init__(self, kind, num):
        self.kind = kind
        self.num = num

    def __gt__(self, other):
        return self.num > other.num

    def __eq__(self, other):
        return self.num == other.num

    def __repr__(self):
        kinds = ["S", "H", "C", "D"]
        nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return kinds[self.kind] + nums[self.num]
