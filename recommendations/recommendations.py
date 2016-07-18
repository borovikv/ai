from collections import defaultdict
from math import sqrt

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.028,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5},
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}


def sim_distance(prefs, person1, person2):
    si = get_same_items(prefs, person1, person2)

    if not len(si):
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])

    return 1 / (1 + sqrt(sum_of_squares))


def get_same_items(prefs, person1, person2):
    return {item: 1 for item in prefs[person1] if item in prefs[person2]}


def sim_pearson(prefs, p1, p2):
    si = get_same_items(prefs, p1, p2)

    n = len(si)
    if not n:
        return 0

    sum1 = sum(prefs[p1][item] for item in si)
    sum2 = sum(prefs[p2][item] for item in si)

    sum1Sq = sum(pow(prefs[p1][item], 2) for item in si)
    sum2Sq = sum(pow(prefs[p2][item], 2) for item in si)

    pSum = sum(prefs[p1][item] * prefs[p2][item] for item in si)

    # Pearson coefficient
    num = pSum - (sum1 * sum2) / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if not den:
        return 0

    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    result = scores[-n:]
    result.reverse()
    return result

def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = defaultdict(int)
    simSums = defaultdict(int)

    for other in prefs.keys() - {person}:
        sim = similarity(prefs, person, other)

        if sim <= 0:
            continue

        for item in prefs[other]:

            if item not in prefs[person] or prefs[person][item] == 0:
                totals[item] += prefs[other][item] * sim
                simSums[item] += sim

    print(simSums)
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

# print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
# print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))

# print(top_matches(critics, 'Toby', n=3))
# print(top_matches(critics, 'Toby', n=3, similarity=sim_distance))
print(get_recommendations(critics, 'Toby'))
# print(get_recommendations(critics, 'Toby', similarity=sim_distance))

