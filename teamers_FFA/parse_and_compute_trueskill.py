import sys
from collections import defaultdict
from trueskill import TrueSkill

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

env = TrueSkill(draw_probability=0.001)

players = defaultdict(env.create_rating)
players_teamer = defaultdict(env.create_rating)
players_ffa = defaultdict(env.create_rating)
matches = []

nbugs = 0
bot_parsing_failed = 0
parsing_skipped = 0
draw_matches_skipped = 0
parsing_report = False
gametype = None
names = [[] for _ in range(12)]

def reset():
    global parsing_report 
    parsing_report = False
    global gametype
    gametype = None
    global names
    names = [[] for _ in range(12)]

with open("report.txt") as rf:
    for i, line in enumerate(rf):
        ### substitutions for some names
        line = line.replace('(CivFR)', 'CivFR')
        line = line.replace('The ', 'The')
        line = line.replace('Jack The', 'JackThe')
        if 'ReportParser' in line:
            if parsing_report == True:
                nbugs += 1
                reset()
            parsing_report = True
        if 'En attente de validation' in line or 'Le report ne contient aucun joueur' in line or 'données invalides' in line or 'pas le même nombre de joueur' in line or "Aucun joueur n'est présent dans le report" in line or "Le report ne contient pas le type de partie" in line or "Le report contient un nombre de joueurs suspect" in line:
            bot_parsing_failed += 1
            reset()
        if 'Report valid' in line:
            names = [x for x in names if x != []]
            ranks = range(len(names))
            p = [[e for e in map(lambda x: players[x], nl)] for nl in names]
            if (len(p) > 1):
                tmp = env.rate(p, ranks=ranks)
                for tn, team in enumerate(tmp):
                    for pn, player in enumerate(team):
                        players[names[tn][pn]] = player
                if gametype == "teamer":
                    p_t = [[e for e in map(lambda x: players_teamer[x], nl)] for nl in names]
                    tmp = env.rate(p_t, ranks=ranks)
                    for tn, team in enumerate(tmp):
                        for pn, player in enumerate(team):
                            players_teamer[names[tn][pn]] = player
                elif gametype == "ffa":
                    p_f = [[e for e in map(lambda x: players_ffa[x], nl)] for nl in names]
                    tmp = env.rate(p_f, ranks=ranks)
                    for tn, team in enumerate(tmp):
                        for pn, player in enumerate(team):
                            players_ffa[names[tn][pn]] = player
            else:
                draw_matches_skipped += 1
            matches.append(names)
            reset()

        if parsing_report:
            if 'gametype' in line.lower():
                gametype = line.split(':')[1].strip().split(' ')[0].lower()
            if '@' in line:
                ls = line.split(':')
                try:
                    idx = int(ls[0]) - 1
                    names[idx].append(ls[1].strip().split(' ')[0].rstrip('\n'))
                except:
                    eprint(names)
                    eprint(ls)
                    eprint(f'line: {i}')
                    parsing_skipped += 1
                    reset()


players_list = [(k, v) for k, v in players.items()]
leaderboard = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
print(f'Number of bugs that we know of: {nbugs}')
print(f'Number of matches that we failed to parse: {parsing_skipped}, that the bot failed to parse: {bot_parsing_failed}')
print(f'Number of draw matches that we ignored: {draw_matches_skipped}.')
print(f'Number of matches counted: {len(matches)}.')
print("\n=================")
with open('leaderboard_global.txt', 'w') as wf:
    for player, rating in leaderboard:
        wf.write(f'{player}: {env.expose(rating):0.2f} ({rating.mu:0.2f}, {rating.sigma:0.2f})\n')
players_list = [(k, v) for k, v in players_teamer.items()]
leaderboard_teamer = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
with open('leaderboard_teamer.txt', 'w') as wf:
    for player, rating in leaderboard_teamer:
        wf.write(f'{player}: {env.expose(rating):0.2f} ({rating.mu:0.2f}, {rating.sigma:0.2f})\n')
players_list = [(k, v) for k, v in players_ffa.items()]
leaderboard_ffa = sorted(players_list, key=lambda x: env.expose(x[1]), reverse=True)
with open('leaderboard_ffa.txt', 'w') as wf:
    for player, rating in leaderboard_ffa:
        wf.write(f'{player}: {env.expose(rating):0.2f} ({rating.mu:0.2f}, {rating.sigma:0.2f})\n')

