
lines = []
with open("puzzle7/input.txt") as input:
    lines = input.read().split("\n")

def categorise_hand(hand):
    if pt2 and "J" in hand:
        possibilities = []
        hand = hand.replace("J", "!")
        possibilities.append(categorise_hand(hand))
        for k in key.keys():
            if k == "J":
                continue
            possible_hand = hand.replace("!", k)
            possibilities.append(categorise_hand(possible_hand))
        return max(possibilities)


    occs = {}
    for letter in hand:
        occs[letter] = occs.get(letter, 0) + 1
    if len(occs.keys()) == 5:
        return 0 # High card
    elif len(occs.keys()) == 4:
        return 1 #One pair
    elif len(occs.keys()) == 3:
        if max(occs.values()) == 2:
            return 2#Two pair
        else:
            return 3#Three of a kind
    elif len(occs.keys()) == 2:
        if max(occs.values()) == 3:
            return 4#Full house
        else:
            return 5#Four of a kind
    else:
        return 6#Five of a kind

def get_strength(hand):
    strength = categorise_hand(hand) * (len(key.values()) ** 6)
    strength += key[hand[0]] * (len(key.values()) ** 5)
    strength += key[hand[1]] * (len(key.values()) ** 4)
    strength += key[hand[2]] * (len(key.values()) ** 3)
    strength += key[hand[3]] * (len(key.values()) ** 2)
    strength += key[hand[4]] * (len(key.values()) ** 1)
    return strength



games = [line.split(" ") for line in lines]
for game in games:
    game[1] = int(game[1])

def solve_pt1():
    strengths = [[get_strength(game[0]), game[1]] for game in games]
    sorted_strengths = sorted(strengths)
    winnings = 0
    for rank_minus_1, bid in enumerate([x[1] for x in sorted_strengths]):
        winnings += (rank_minus_1+1) * bid
    return winnings

def solve_pt2():
    return solve_pt1()

pt2 = False
key = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12
}
print(solve_pt1())
pt2 = True
key = {
    "J": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "Q": 10,
    "K": 11,
    "A": 12
}
print(solve_pt2())