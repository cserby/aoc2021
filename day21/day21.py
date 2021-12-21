from itertools import zip_longest


def die(start=0):
    die_rolls = 0
    die_state = start
    while True:
        die_rolls += 1
        yield (die_state + 1, die_rolls)
        die_state = (die_state + 1) % 100


def three_die_rolls(die_iter):
    return zip_longest(*([iter(die_iter)] * 3))


def score(ps):
    (_, score) = ps
    return score


def step(ps, die3_iter):
    (field, score) = ps
    steps = sum(rolled for (rolled, _) in next(die3_iter))
    field = ((field + steps - 1) % 10) + 1
    score += field
    return (field, score)


def player_stats(die_iter, player_starts):
    player_stats = player_starts
    die3_iter = three_die_rolls(die_iter)
    while all(score(ps) < 1000 for ps in player_stats):
        player_stats = tuple(step(ps, die3_iter) for ps in player_stats)
        yield player_stats


def part1(player_starts):
    die_iter = die()
    end_stats = list(player_stats(die_iter, player_starts))[-2:]
    (_, roll_count) = next(die_iter)
    ((_, player1_score_end), _) = end_stats[-1]
    if player1_score_end >= 1000:
        (_, (_, player2_score_before_end)) = end_stats[-2]
        return (roll_count - 4) * player2_score_before_end
    else:
        ((_, player1_score_end), _) = end_stats[-1]
        return (roll_count - 1) * player1_score_end


sample_starts = ((4, 0), (8, 0))
input_starts = ((5, 0), (9, 0))
print(f"Part1: {part1(input_starts)}")
