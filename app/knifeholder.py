import random


cv = {
    "A": 14,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13
}


class Card:
    def __init__(self, s, v):
        self.suit = s
        self.value = v
        self.owner = ""
        self.state = "deck"



def show_cards(cards, p):
    for c in cards:
        if c.owner == p:
            print(c.suit + " " + c.value)


def deal(cards, players):
    for i, p in enumerate(players):
        for c in range(int(i*(len(cards)/4)), int((i+1)*(len(cards)/4))):
            cards[c].owner = p
            cards[c].state = "hand"
    return cards


def get_solo(players, rami):
    for p in [players[(players.index(rami) + 1) % 4], players[(players.index(rami) +3) % 4]]:
        if random.randint(0, 10) == 0:
            return p
    return ""


def send_cards(cards, players):
    print("cards sent!!")


def get_showcards(cards, players, starter):
    showcards = []
    for p in players[starter:] + players[:starter]:
        for c in cards:
            if c.owner == p:
                showcards.append(c)
                break
    return showcards


def choose_game(cards):
    for c in cards:
        if c.suit in ["diamond", "heart"]:  #remember to add support for fake cards later!!!!!!!!!!!
            return c.owner
    return ""


def create_deck():
    cards = []
    for i, s in enumerate(["diamond", "spade", "heart", "club"]):
        for v in cv.keys():
            cards.append(Card(s, v))
    return cards


def get_player_cards(cards, p, state):
    p_cards = []
    for c in cards:
        if c.owner == p:
            if state == c.state or not state:
                p_cards.append(c)
    return p_cards


def get_card(cards, player, suit):
    p_cards = get_player_cards(cards, player, "hand")
    card = p_cards[0]
    for c in p_cards:
        if c.suit == suit or not suit:
            card = c
            break
    card.state = "table"
    return card


def play_hand(rami, cards, players, starter):
    if rami:
        print("Rami by " + rami)

    tiks = {}
    for p in players:
        tiks[p] = 0
    if rami:
        starter = (players.index(rami) + 3) % 4
    for tik in range(13):
        tablecards = []
        suit = ""
        for i in range(4):
            tablecards.append(get_card(cards, players[(starter+i) % 4], suit))
            suit = tablecards[0].suit
        largest = tablecards[0]
        for c in tablecards[1:]:
            if c.suit == tablecards[0].suit and cv[c.value] > cv[largest.value]:
                largest = c
        tiks[largest.owner] += 1

        starter = players.index(largest.owner)

    #stupid code with hardcodings

    pair1 = tiks[players[0]]+tiks[players[2]]
    pair2 = tiks[players[1]]+tiks[players[3]]
    pair1_points = 0
    pair2_points = 0
    if rami:
        if pair1 > pair2:
            double = 1
            if rami in [players[1], players[3]]:
                double = 2
            pair1_points = (pair1-6)*4 * double
            print("Winners: " + players[0] + " & " + players[2] + ". + " + str(pair1_points) + " points")
        else:
            double = 1
            if rami in [players[0], players[2]]:
                double = 2
            pair2_points = (pair2-6)*4 * double
            print("Winners: " + players[1] + " & " + players[3] + ". + " + str(pair2_points) + " points")
    else:
        if pair1 < pair2:
            pair1_points = (pair2-6)*4
            print("Winners: " + players[0] + "& " + players[2] + ". + " + str(pair1_points) + " points")
        else:
            pair2_points = (pair1-6)*4
            print("Winners: " + players[1] + " & " + players[3] + ". + " + str(pair2_points) + " points")

    return pair1_points, pair2_points


def play_solohand(rami, cards, players, solo):
    print("Rami by " + rami)
    print("Solo by " + solo)

    starter = 0

    for tik in range(13):
        tablecards = []
        suit = ""
        for i in range(2):
            tablecards.append(get_card(cards, players[(starter+i*2) % 4], suit))
            suit = tablecards[0].suit

        tablecards.append(get_card(cards, solo, suit))

        largest = tablecards[0]
        for c in tablecards[1:]:
            if c.suit == tablecards[0].suit and cv[c.value] > cv[largest.value]:
                largest = c
        if largest.owner == solo:
            if solo in [players[0], players[2]]:
                print("Winners: " + players[1] + " & " + players[3] + ". + 24 points, on tik " + str(tik+1))
                return 0, 24
            else:
                print("Winners: " + players[0] + " & " + players[2] + ". + 24 points, on tik " + str(tik+1))
                return 24, 0

        starter = players.index(largest.owner)

    if solo in [players[0], players[2]]:
        print("Winners: " + players[0] + " & " + players[2] + ". + 24 points")
        return 24, 0
    else:
        print("Winners: " + players[1] + " & " + players[3] + ". + 24 points")
        return 0, 24



def main():
    players = ["jsloth", "glukoosi", "kannadan", "megatron"]
    starter = 0
    pair1p = 0
    pair2p = 0
    i = 1
    while True:
        cards = create_deck()
        random.shuffle(cards)
        cards = deal(cards, players)
        send_cards(cards, players)
        # wait for cards to come
        rami = choose_game(get_showcards(cards, players, starter))
        solo = ""
        if rami:
            solo = get_solo(players, rami)
        if solo:
            cv["A"] = 1
            p1p, p2p = play_solohand(rami, cards, players, solo)
        else:
            cv["A"] = 14
            p1p, p2p = play_hand(rami, cards, players, starter)
        pair1p += p1p
        pair2p += p2p
        if pair1p > 0 and pair2p > 0:
            pair1p = 0
            pair2p = 0
        elif pair1p >= 52:
            print("Pair 1: " + players[0] + " & " + players[2] + " won the game on round " + str(i) + "!")
            break
        elif pair2p >= 52:
            print("Pair 2: " + players[1] + " & " + players[3] + " won the game on round " + str(i) + "!")
            break

        starter = (starter + 1) % 4
        i += 1



if __name__ == '__main__':
    main()