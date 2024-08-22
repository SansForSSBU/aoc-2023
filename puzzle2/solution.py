
maxes = {
    "red": 12,
    "green": 13,
    "blue": 14
}
pt1_ans = 0
pt2_ans = 0
with open("puzzle2/input.txt") as input:
    games = input.read().split("\n")
    for game in games:
        game_possible = True
        game_name = game.split(":")[0]
        game_info = game.split(":")[1].strip().split(";")
        max_balls = {
            "red": 0,
            "green": 0,
            "blue": 0
        }

        for show in game_info:
            balls = [x.strip().split(" ") for x in show.split(",")]
            for ball in balls:
                if int(ball[0]) > maxes[ball[1]]:
                    game_possible = False
                max_balls[ball[1]] = max(max_balls[ball[1]], int(ball[0]))

        if game_possible:
            pt1_ans += int(game_name.split(" ")[1])
        
        power = 1
        for k, v in max_balls.items():
            power = power * v
        pt2_ans += power

print("Part 1:", pt1_ans)
print("Part 2:", pt2_ans)