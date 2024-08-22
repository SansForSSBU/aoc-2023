from math import pow

lines = []
with open("puzzle4/input.txt") as input:
    lines = input.read().split("\n")



cards = [line.split(":")[1].strip().split("|") for line in lines]
for card in cards:
    card[0] = list(filter(lambda a: a!='', card[0].strip().split(" ")))
    card[1] = list(filter(lambda a: a!='', card[1].strip().split(" ")))

def get_matches(card):
    matches = 0
    for n in card[0]:
        if n in card[1]:
            matches += 1
    return matches

def score_matches(matches):
    if matches == 0:
        return 0
    return pow(2, (matches-1))

def score_card(card):
    matches = get_matches(card)
    return score_matches(matches)

def solve_pt1():
    score = 0
    for card in cards:
        score += score_card(card)
    return int(score)

card_dict = {}
for i, line in enumerate(lines):
    card_dict[int(line.split(":")[0].split(" ")[-1])] = get_matches(cards[i])

def solve_pt2():
    my_cards = {}
    for i in card_dict.keys():
        my_cards[i] = 1
    for i in range(1, len(my_cards) + 1):
        cards_won = card_dict[i]
        for j in range(i+1, i+cards_won+1):
            my_cards[j] += my_cards[i]

    return sum(my_cards.values())

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())