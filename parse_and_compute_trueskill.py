import sys
from collections import defaultdict
from trueskill import TrueSkill, rate_1vs1, quality_1vs1

env = TrueSkill(draw_probability=0.001)

players = defaultdict(env.create_rating)
matches = []

p1 = None
p2 = None
count_continuations = 0
count_victory_lines = 0

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

with open("1v1.txt") as rf:
    for line in rf:
        ### substitutions for some names
        line = line.replace('(CivFR)', 'CivFR')
        line = line.replace('The ', 'The')
        line = line.replace('Jack The', 'JackThe')
        if ('ictoire' in line or 'ictory' in line or ' win ' in line or ' vin ' in line) and '@' in line:
            count_victory_lines += 1
            ls = line.split('@')
            p1 = ls[1].split()[0].split('#')[0].split('(')[0]
            if len(ls) > 2:
                p2 = ls[2].split()[0].split('#')[0].split('(')[0]
            else:
                count_continuations += 1
                continue
            if len(ls) > 3:
                eprint('This line mentions more than 2 players, splitting on "ictoire"')
                eprint(line)
                ls = line.split('ictoire')
                if len(ls) < 2:
                    eprint("Failed")
                    eprint('This line mentions more than 2 players, splitting on "ictory"')
                    eprint(line)
                    ls = line.split('ictory')
                if len(ls) < 2:
                    eprint("Failed")
                    eprint('This line mentions more than 2 players, splitting on "win"')
                    eprint(line)
                    ls = line.split('win')
                if len(ls) < 2:
                    eprint("Failed")
                    continue
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


players_list = [(k, v) for k, v in players.items()]
leaderboard = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
print(f'Number of lines where we found a message of victory: {count_victory_lines}')
print(f'Number of matches counted: {len(matches)}.')
print(f'Number of matches that were reported on 2 lines: {count_continuations}')
print("\n=================")
for player, rating in leaderboard:
    print(f'{player}: {env.expose(rating)}')
print("\n=================")
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

