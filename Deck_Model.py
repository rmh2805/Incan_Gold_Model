class Diamont_Deck_Count:
    defCounts = {'h_snake': 3,
                 'h_spider': 3,
                 'h_fire': 3,
                 'h_cave-in': 3,
                 'h_mummy': 3,
                 't_1': 1,
                 't_2': 1,
                 't_3': 1,
                 't_4': 1,
                 't_5': 2,
                 't_7': 2,
                 't_9': 1,
                 't_11': 2,
                 't_13': 1,
                 't_14': 1,
                 't_15': 1,
                 't_17': 1,
                 'a': 1}

    def __init__(self):
        self.counts = None
        self.nCards = None
        self.init_deck()

    def init_deck(self):
        self.nCards = 0
        self.counts = self.defCounts.copy()

        self.nCards = 0
        for key in self.counts:
            self.nCards += self.counts[key]

    # =========================<Deck Modifications>========================== #
    def remCard(self, cardType):
        if cardType in self.counts and self.counts[cardType] > 0:
            self.counts[cardType] -= 1
            self.nCards -= 1

    def remHazard(self, hazardType):
        self.remCard('h_' + hazardType)

    def remTreasure(self, tValue: int):
        self.remCard('t_' + str(tValue))

    def remArtifact(self):
        self.remCard('a')

    def addCard(self, cardType):
        if cardType not in self.counts:
            self.counts[cardType] = 0

        self.counts[cardType] += 1
        self.nCards += 1

    def addArtifact(self):
        self.addCard('a')

    def addHazard(self, hazardType):
        self.addCard('h_' + hazardType)

    def addTreasure(self, tValue: int):
        if isinstance(tValue, int):
            self.addCard('t_' + str(tValue))

    # =============================<Member Info>============================== #
    def getCardTypes(self):
        return list(self.counts)

    def getHazardTypes(self):
        hazards = list()
        for key in self.counts:
            if key[0:2] == 'h_':
                hazards.append(key[2:])
        return hazards

    # ===========================<Deck Statistics>============================ #
    def avg_treasure(self):
        tot = 0
        count = 0
        for key in self.counts:
            if key[0:2] == 't_':
                tot += int(key[2:]) * self.counts[key]
                count += self.counts[key]
        return float(tot) / count

    def avg_payout(self):
        tot = 0
        count = 0
        for key in self.counts:
            count += self.counts[key]
            if key[0:2] == 't_':
                tot += int(key[2:])

        return float(tot) / count

    def getDeckCount(self):
        return self.nCards

    def getCardCount(self, cardType):
        return self.counts[cardType]

    def getHazardCount(self, hazardType):
        return self.getCardCount('h_' + hazardType)


def printFrequencies(counts):
    nCards = counts.getDeckCount()
    cardTypes = counts.getCardTypes()

    hazardCount = 0
    for key in cardTypes:
        val = counts.getCardCount(key)
        freq = float(val) / nCards
        print(str(key) + ' Frequency: ' + str(val) + '/' + str(nCards) + ' (' + str(round(freq, 2)) + ')')

    print('\nHazard Frequency: ' + str(hazardCount) + '/' + str(nCards) + ' (' + str(
        round(float(hazardCount) / nCards, 2)) + ')')
    print(counts.avg_payout())
    print(counts.avg_treasure())


def main():
    counts = Diamont_Deck_Count()
    cardTypes = counts.getCardTypes()

    printFrequencies(counts)


if __name__ == '__main__':
    main()
