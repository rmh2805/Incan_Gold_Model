from GameModel import GameModel

# ========================================<Print Helpers>========================================= #
def printBanner():
    print("#==============================================================================#")
    print("#============================<Incan Gold Predictor>============================#")
    print("#==============================================================================#")


def printRoundBanner(n):
    print('\n')
    print("#==============================================================================#")
    print("#==================================<Round " + str(n) + ">===================================#")
    print("#==============================================================================#")


def printTurnBanner(n):
    print()
    print("#===============<Turn " + str(n) + ">===============#")


def printScores(playerList: list, playerScores: dict):
    longestName = 0
    for player in playerList:
        if len(player) > longestName:
            longestName = len(player)

        if len(str(playerScores[player])) > longestName:
            longestName = len(str(playerScores[player]))

    for i in range(0, len(playerList)):
        if i != 0:
            print(' ', end='')
        print('| ', end='')

        player = str(playerList[i])
        printCenterPad(player, longestName)
    print('|')

    for i in range(0, len(playerList)):
        if i != 0:
            print('=', end='')
        print('+=', end='')

        for j in range(0, longestName):
            print('=', end='')
    print("+")

    for i in range(0, len(playerList)):
        if i != 0:
            print(' ', end='')
        print('| ', end='')

        player = str(playerList[i])
        printCenterPad(str(playerScores[player]), longestName)
    print('|')


def printBank(game: GameModel):
    print("Money in the bank:")
    printScores(game.getPlayers(), game.getBank())


def printPocket(game: GameModel):
    print("Money in pocket:")
    printScores(game.getActivePlayers(), game.getPocket())


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
def printCenterPad(val: str, size: int):
    for j in range(0, int((size - len(val)) / 2)):
        print(' ', end='')
    print(val, end='')
    for j in range(0, int((size - len(val)) / 2 + .5)):
        print(' ', end='')


def getPlayerNames(prompt: str):
    players = []
    player = input(prompt).strip()

    while player:
        players.append(player)
        for ch in prompt:
            print(' ', end='')
        player = input().strip()

    return players


# ======================================<Main Functionality>====================================== #
def main():
    printBanner()

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

    game = GameModel(players)

    # =============================<Game Rounds>============================== #
    gameRound = 1
    while gameRound <= 5:
        printRoundBanner(gameRound)
        game.startRound()

        turnCounter = 1
        wasBust = False
        while not wasBust:
            printTurnBanner(turnCounter)

            bustChance = simplifyFraction(game.chanceBust())

            printBank(game)
            print()
            printPocket(game)

            print()
            print("Chance of a bust this round is " + str(bustChance[0]) + "/" + str(bustChance[1]) + " (" +
                  str(round(float(bustChance[0]) / bustChance[1], 2)) + ")")
            print("Expected payout this round is " + str(round(game.expectedPayout())))
            print("Leftover treasure on retreat is " + str(game.getLeftover()))
            if game.artifact:
                print("This round's artifact is available")
            elif game.artifactShown:
                print("This round's artifact has been claimed")
            else:
                print("This round's artifact is still hidden")

            print()

            # ===================<Gather Round Information>=================== #
            players = getPlayerNames("Enter the names of all players who retreated: ")
            game.playersRetreat(players)
            if len(game.getActivePlayers()) == 0:
                print("All explorers have retreated")
                break   # Break when there are no more active players

            choice = input("What was the last turn? Artifact (a), Treasure (t), or Hazard (h): ").strip()
            while len(choice) == 0 or (choice[0].upper() not in ['A', 'T', 'H']):
                choice = input("What was the last turn? Artifact (a), Treasure (t), or Hazard (h): ").strip()

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

        print("===<ROUND END>===")
        gameRound += 1


if __name__ == '__main__':
    main()
