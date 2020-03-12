import random


def add_a_team(list_of_teams, new_team):
    if not new_team:
        return list_of_teams
    if not isinstance(new_team, str):
        raise Exception("%s is not a string" % new_team)
    list_of_teams.append(new_team)
    return list_of_teams


def create_matches(list_of_teams):
    if len(list_of_teams) < 2:
        raise Exception("not enough teams")
    matches = []
    match = []
    for i, team in enumerate(list_of_teams):
        if not isinstance(team, str):
            raise Exception("%s is not a string" % team)
        if not i % 2:
            match = [team]
        elif i % 2:
            match.append(team)
            matches.append(match)
            match = []
    if match:
        matches.append(match)
    return matches


# print(create_matches(["a", "b"]))


def create_random_matches(list_of_teams):
    list_of_teams = list_of_teams.copy()
    random.shuffle(list_of_teams)
    matches = create_matches(list_of_teams)
    return matches


def teams_after_results(matches, results):
    if len(matches) < len(results):
        raise Exception("len(matches)=%s < len(results)=%s" % (len(matches), len(results)))
    if len(matches[-1]) == 1 and len(matches) == len(results):
        raise Exception("len(matches)=%s == len(results)=%s when last len(match)=1" % (len(matches), len(results)))
    if len(matches[-1]) == 2 and len(matches) != len(results):
        raise Exception("len(matches)=%s != len(results)=%s when last len(match)=2" % (len(matches), len(results)))
    if len(matches) == len(results) + 1:
        results.append(0)
    list_of_teams = []
    for i, (match, result) in enumerate(zip(matches, results)):
        # print(i, (match, result))
        if len(match) == 2:
            list_of_teams.append(match[result])
        else:
            if i == len(matches) - 1:
                # last lonely match
                list_of_teams.append(match[0])
                break
            else:
                raise Exception("%s is not a pair match" % match)
    return list_of_teams

# print(teams_after_results([["a", "b"], ["c"]], [0]))


def check_if_match_exists(matches, index):
    if len(matches) <= index:
        return False
    return True


def check_if_it_is_the_winner(list_of_teams):
    if not list_of_teams:
        raise Exception("doesnt have any team")
    if len(list_of_teams) == 1:
        return True
    return False


def check_if_the_teams_are_fine(list_of_teams):
    for team in list_of_teams:
        if not isinstance(team, str):
            return False
    if len(list_of_teams) < 2:
        return False
    return True


def calc_new_match(matches, match_i, results, list_of_teams):
    new_match_i = match_i + 1
    if len(matches) > new_match_i:
        new_list_of_teams = list_of_teams
        new_matches = matches
        new_results = results
        new_match = matches[new_match_i]
    else:
        # new level
        new_list_of_teams = teams_after_results(matches, results)
        if check_if_it_is_the_winner(new_list_of_teams):
            new_match = None
            new_matches = []
            new_match_i = 0
            new_results = []
        else:
            new_matches = create_random_matches(new_list_of_teams)
            new_match_i = 0
            new_results = []
            new_match = new_matches[0]
    
    return new_match, new_matches, new_match_i, new_results, new_list_of_teams
