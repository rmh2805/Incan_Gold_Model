from GameModel import GameModel
from FileOut import FileOut


# ========================================<Print Helpers>========================================= #
def banner():
    return "#==============================================================================#\n" + \
           "#============================<Incan Gold Predictor>============================#\n" + \
           "#==============================================================================#\n"


def roundBanner(n):
    return "#==============================================================================#\n" + \
           "#==================================<Round " + str(n) + ">===================================#\n" + \
           "#==============================================================================#\n"


def turnBanner(n):
    return "#===============<Turn " + str(n) + ">===============#\n"


def scores(playerList: list, playerScores: dict):
    longestName = 0
    for player in playerList:
        if len(player) > longestName:
            longestName = len(player)

        if len(str(playerScores[player])) > longestName:
            longestName = len(str(playerScores[player]))

    toReturn = ''
    for i in range(0, len(playerList)):
        if i != 0:
            toReturn += ' '
        toReturn += '| '

        player = str(playerList[i])
        toReturn += centerPad(player, longestName)
    toReturn += '|\n'

    for i in range(0, len(playerList)):
        if i != 0:
            toReturn += '='
        toReturn += '+='

        for j in range(0, longestName):
            toReturn += '='
    toReturn += "+\n"

    for i in range(0, len(playerList)):
        if i != 0:
            toReturn += ' '
        toReturn += '| '

        player = str(playerList[i])
        toReturn += centerPad(str(playerScores[player]), longestName)
    toReturn += '|\n'
    return toReturn


def bank(game: GameModel):
    toReturn = "Money in the bank:\n"
    toReturn += scores(game.getPlayers(), game.getBank())
    return toReturn


def pocket(game: GameModel):
    return "Money in pocket:\n" + scores(game.getActivePlayers(), game.getPocket())


# =========================================<Math Helpers>========================================= #
def gcf(a: int, b: int, f=-1):
    if a < 0 or b < 0:
        return gcf(int(abs(a)), int(abs(b)))

    if a < b:
        return gcf(b, a)

    if f == -1:
        return gcf(a, b, b)

    if f == 1:
        return 1

    if a % f == 0 and b % f == 0:
        return f

    return gcf(a, b, f - 1)


def simplifyFraction(fraction: tuple):
    if len(fraction) != 2 or fraction[1] == 0:
        return None

    if fraction[0] == 0:
        return fraction[0], fraction[1]

    if fraction[1] < 0:
        fraction = (-fraction[0], -fraction[1])

    d = gcf(fraction[0], fraction[1])

    return int(fraction[0] / d), int(fraction[1] / d)


# =========================================<Misc Helpers>========================================= #
def centerPad(val: str, size: int):
    toReturn = ''
    for j in range(0, int((size - len(val)) / 2)):
        toReturn += ' '
    toReturn += val
    for j in range(0, int((size - len(val)) / 2 + .5)):
        toReturn += ' '

    return toReturn


def getPlayerNames(prompt: str, fp=None):
    players = []
    player = input(prompt).strip()
    if fp is not None:
        fp.filePrint(player + '\n')
    while player:
        players.append(player)
        for ch in prompt:
            print(' ', end='')
            if fp is not None:
                fp.filePrint(' ', end='')
        player = input().strip()
    if fp is not None:
        fp.filePrint(player + '\n')

    return players


# ======================================<Main Functionality>====================================== #
def main():
    print(banner())

    # ==============================<Game Setup>============================== #
    # Player name entry
    name = input("Please enter your name: ").strip()
    while not name:
        name = input("Please enter your name: ").strip()

    players = list()
    players.append(name)
    players += getPlayerNames("Please enter opponent names, followed by a blank line: ")

    if len(players) == 1:
        print("No opponents entered, exiting out")
        exit(1)

    print("\nCreating a game with players: ", end='')
    for i in range(0, len(players)):
        if i != 0:
            print(', ', end='')

        print(players[i], end='')
        if players[i] == name:
            print(' (You)', end='')
    print('\n')

    filePath = input("Choose a filePath for output saving (blank to ignore): ").strip()
    if not filePath:
        filePath = None
    fp = FileOut(filePath)
    fp.setPlayers(players)
    fp.filePrint()

    game = GameModel(players)

    # =============================<Game Rounds>============================== #
    gameRound = 1
    while gameRound <= 1:
        fp.print()
        fp.print(roundBanner(gameRound))
        game.startRound()

        turnCounter = 1
        wasBust = False
        while not wasBust:
            fp.print(turnBanner(turnCounter))

            bustChance = simplifyFraction(game.chanceBust())

            # ======================<Print Scoreboards>======================= #
            fp.print(bank(game))
            fp.print()
            fp.print(pocket(game))
            fp.print()

            # =======================<Print Prediction>======================= #
            fp.print("Chance of a bust this round is " + str(bustChance[0]) + "/" + str(bustChance[1]) + " (" +
                     str(round(float(bustChance[0]) / bustChance[1], 1)) + ")")
            fp.print("Expected payout this turn is " + str(round(game.expectedPayout(), 1)))
            fp.print("Average value of remaining treasures is " + str(round(game.deck.avg_treasure(), 1)))
            fp.print()

            # ======================<Print Retreat Info>====================== #
            fp.print("Leftover treasure on retreat is " + str(game.getLeftover()))
            if game.artifact:
                fp.print("This round's artifact is available")
            elif game.artifactShown:
                fp.print("This round's artifact has been claimed")
            else:
                fp.print("This round's artifact is still hidden")

            fp.print()

            # ===================<Gather Round Information>=================== #
            players = getPlayerNames("Enter the names of all players who retreated: ", fp)
            game.playersRetreat(players)
            if len(game.getActivePlayers()) == 0:
                fp.print("All explorers have retreated")
                break  # Break when there are no more active players

            choice = input("What was the last card? Artifact (a), Treasure (t), or Hazard (h): ").strip()
            while len(choice) == 0 or (choice[0].upper() not in ['A', 'T', 'H']):
                choice = input("What was the last card? Artifact (a), Treasure (t), or Hazard (h): ").strip()

            if choice[0].upper() == 'A':
                game.gotArtifact()
            elif choice[0].upper() == 'T':
                choice = input("What is the value of the treasure card: ").strip()
                while len(choice) == 0 or not choice.isnumeric():
                    choice = input("What is the value of the treasure card: ").strip()
                game.gotTreasure(int(choice))
            elif choice[0].upper() == 'H':
                choice = input("What was the type of the hazard" + str(game.hazardTypes) + ": ").strip()
                while choice not in game.hazardTypes:
                    choice = input("What was the type of the hazard" + str(game.hazardTypes) + ": ").strip()
                wasBust = game.isBust(choice)

            turnCounter += 1

        fp.print("===<ROUND END>===")
        gameRound += 1

    fp.close()


if __name__ == '__main__':
    main()
