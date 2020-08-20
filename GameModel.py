from Deck_Model import Diamont_Deck_Count


class GameModel:
    def __init__(self, players: list):
        # ==========================<General State>=========================== #
        self.deck = Diamont_Deck_Count()
        self.players = players.copy()
        self.hazardTypes = self.deck.getHazardTypes()
        self.clearedTraps = list()

        self.artifactsClaimed = 0

        self.bank = dict()
        self.artifacts = dict()
        for player in self.players:
            self.bank[player] = 0
            self.artifacts[player] = 0

        # =======================<Allocate Round State>======================= #
        self.primedHazards = list()
        self.activePlayers = list()
        self.roundScore = dict()
        self.leftover = 0
        self.artifact = False
        self.artifactShown = False

    def startRound(self):
        self.primedHazards = list()
        self.activePlayers = self.players.copy()

        self.deck.init_deck()
        for hazard in self.clearedTraps:
            self.deck.remHazard(hazard)

        self.roundScore = dict()
        for player in self.players:
            self.roundScore[player] = 0

        self.leftover = 0
        self.artifact = False
        self.artifactShown = False

    def chanceBust(self):
        hCount = 0
        for hazard in self.primedHazards:
            hCount += self.deck.getHazardCount(hazard)

        return hCount, self.deck.getDeckCount()

    def expectedPayout(self):
        return self.deck.avg_payout() / len(self.activePlayers)

    def gotTreasure(self, val):
        self.deck.remTreasure(val)

        self.leftover += val % len(self.activePlayers)
        for player in self.activePlayers:
            self.roundScore[player] += int(val / len(self.activePlayers))

    def gotArtifact(self):
        self.deck.remArtifact()
        self.artifact = True
        self.artifactShown = True

    def isBust(self, hazardType: str) -> bool:
        if hazardType not in self.hazardTypes:
            return False

        if hazardType in self.primedHazards:
            self.clearedTraps.append(hazardType)
            return True

        self.deck.remHazard(hazardType)
        self.primedHazards.append(hazardType)
        return False

    def getBank(self):
        return self.bank.copy()

    def getPocket(self):
        return self.roundScore.copy()

    def getPlayers(self):
        return self.players.copy()

    def getActivePlayers(self):
        return self.activePlayers.copy()

    def getLeftover(self):
        return self.leftover

    def playersRetreat(self, players: list):
        for player in players:
            if player not in self.players:
                players.remove(player)

        if len(players) == 0:
            return

        payout = int(self.leftover / len(players))
        self.leftover = self.leftover % len(players)

        if len(players) == 1 and self.artifact:
            self.artifacts[players[0]] += 1

            self.artifact = False
            self.artifactsClaimed += 1
            if self.artifact <= 3:
                payout += 5
            else:
                payout += 10

        for player in players:
            self.bank[player] += payout + self.roundScore[player]
            self.roundScore.pop(player)
            self.activePlayers.remove(player)
