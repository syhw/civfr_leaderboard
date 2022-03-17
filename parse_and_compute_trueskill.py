from collections import defaultdict
from trueskill import TrueSkill, rate_1vs1, quality_1vs1

env = TrueSkill(draw_probability=0.001)

players = defaultdict(env.create_rating)
matches = []

p1 = None
p2 = None

with open("1v1.txt") as rf:
    for line in rf:
        line = line.replace('(CivFR)', 'CivFR')
        line = line.replace('The ', 'The')
        line = line.replace('Jack The', 'JackThe')
        if 'victoire' in line and '@' in line:
            ls = line.split('@')
            p1 = ls[1].split()[0].split('#')[0].split('(')[0]
            if len(ls) > 2:
                p2 = ls[2].split()[0].split('#')[0].split('(')[0]
            else:
                continue
            if len(ls) > 3:
                print('This line mentions more than 2 players, splitting on "victoire"')
                print(line)
                ls = line.split('victoire')
                left, right = ls[0], ls[1]
                p1 = left.split('@')[-1].split()[0].split('#')[0].split('(')[0]
                p2 = right.split('@')[-1].split()[0].split('#')[0].split('(')[0]
        if p1 is not None and p2 is None and '@' in line:
            ls = line.split('@')
            p2 = ls[1].split()[0].split('#')[0].split('(')[0]
        if p1 is not None and p2 is not None:
            new_p1_rating, new_p2_rating = rate_1vs1(players[p1], players[p2])
            players[p1] = new_p1_rating
            players[p2] = new_p2_rating
            matches.append((p1, p2))
            p1 = None
            p2 = None

#print(players)

players_list = [(k, v) for k, v in players.items()]
leaderboard = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
for player, rating in leaderboard:
    print(f'{player}: {env.expose(rating)}')

print("=================")
print("Example for how to use it for getting a probability of a balanced match:")
for p1, p2 in [('CivFRMalm', 'Snippy'), ('Lege', 'CivFRMalm')]:
    print(f'{p1} rating {env.expose(players[p1]):0.1f}, {p2} rating {env.expose(players[p2]):0.1f}, {p1} vs. {p2} draw chance {quality_1vs1(players[p1], players[p2]):0.2f}')

from random import shuffle

for n in range(10):
    shuffle(matches)
    env = TrueSkill(draw_probability=0.001)
    players = defaultdict(env.create_rating)
    for (p1, p2) in matches:
        new_p1_rating, new_p2_rating = rate_1vs1(players[p1], players[p2])
        players[p1] = new_p1_rating
        players[p2] = new_p2_rating
    players_list = [(k, v) for k, v in players.items()]
    leaderboard = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
    with open(f'leaderboard_{n}.txt', 'w') as wf:
        for player, rating in leaderboard:
            wf.write(f'{player}: {env.expose(rating)}\n')

