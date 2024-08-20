
maxes = {
    "red": 12,
    "green": 13,
    "blue": 14
}
ans = 0
with open("puzzle2/input.txt") as input:
    games = input.read().split("\n")
    for game in games:
        game_possible = True
        game_name = game.split(":")[0]
        game_info = game.split(":")[1].strip().split(";")
        total_balls = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for show in game_info:
            balls = [x.strip().split(" ") for x in show.split(",")]
            for ball in balls:
                total_balls[ball[1]] += int(ball[0])
                if int(ball[0]) > maxes[ball[1]]:
                    game_possible = False
        #for key, value in total_balls.items():
            #if maxes[key] < value:
            #    game_possible = False
        if game_possible:
            ans += int(game_name.split(" ")[1])

print(ans)