#!/usr/bin/python
import argparse
import sys
import os
import math
import random
from collections import OrderedDict


def clear_screen():
        if os.name == "nt":
            os.system("cls")  # windows
        else:
            os.system("clear")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('values', nargs="*")
    parser.add_argument(
        '-r', '--reverse', action='store_true', help="print the values below")
    args = parser.parse_args()
    return args


def get_values(args):
    if len(args.values) > 0:
        try:
            with open(args.values[0], 'r') as f:
                values = f.read()
                values = values.split("\n")
        except IOError:
            values = args.values
    else:
        values = sys.stdin.read().split("\n")
    return values


def ask(choises):
    skip = 0
    while True:
        print "\n\nWhat do you perfer?  ({} to skip)".format(skip)
        answer = raw_input("1 - {}  vs  2 - {}   ".format(choises[0], choises[1]))
        if answer in ["q", "quit"]:
            return answer
        try:
            answer = int(answer)
        except ValueError:
            print "please select {}, 1 or 2".format(skip)
            continue
    convert = {1: 1, 2: 0}
    if answer in [skip, 1, 2]:
        return choises[convert[answer]]
    else:
        print "\nplease insert {} to skip, if you don't know what is the better".format(skip)
        print "or 1 for {} or 2 for {}\n\n\n".format(choises[0], choises[1])
# print ask(["goncalo", "ana"])


def chose_the_bests(values):
    n = len(values)
    for i in xrange(0, n, 2):
        # print values
        try:
            answer = None
            while not answer:
                answer = ask([values[i], values[i + 1]])
                print "answer: ", answer
            if answer in ["q", "quit"]:
                print "bye"
                return
            else:
                values.remove(answer)
        except IndexError:
            pass
    return values


def create_points(values):
    points = {}
    for value in values:
        points[value] = 0
    return points


def generate_random_matches(values):
    n = len(values)
    matches = []
    for i in xrange(n):
        for j in xrange(i):
            matches.append((values[i], values[j]))
    random.shuffle(matches)
    return matches
# print generate_random_matches(["a", "b", "c"])


def generate_1round_swiss_system_matches(points):
    points = order_points(points)
    is_odd = len(points) % 2
    n = len(points) - is_odd
    matches = []
    for i in xrange(0, n, 2):
        matches.append((points[i][0], points[i + 1][0]))
    if is_odd:
        points = add_points(choises=points[-1][0], points=points)
    return matches


def swiss_system_matches(points):
    # ceil(log2 n) * floor(n / 2)
    n_rounds = int(math.ceil(math.log(len(points), 2)))
    for round_i in xrange(n_rounds):
        matches = generate_1round_swiss_system_matches(points)
        points = dispute_all_matches(matches, points)
        points = order_points(points)
    return points


def dispute_one_match(choises):
    skip = 0
    while True:
        print "\n\nWhat do you perfer?  ({} to skip)".format(skip)
        answer = raw_input("1 - {}  vs  2 - {}   ".format(choises[0], choises[1]))
        try:
            answer = int(answer)
        except ValueError:
            print "\nplease insert a number\n"
            continue
        if answer in [skip, 1, 2]:
            break
        else:
            print "\nplease insert {} to skip, if you don't know what is the better".format(skip)
            print "or 1 for {} or 2 for {}\n\n\n".format(choises[0], choises[1])
    return answer
# print match(["goncalo", "ana"])


def add_points(choises, points, answer=None):
    if len(choises) == 1:  # in the case of odd numbers, it still wins points
        if isinstance(points, list):
            points = OrderedDict(points)
        points[choises] += 3
        return dict(points)
    answer = int(answer)
    if answer == 0:
        points[choises[0]] += 1
        points[choises[1]] += 1
    else:
        if isinstance(points, list):
            points = OrderedDict(points)
        points[choises[answer - 1]] += 3
    return dict(points)


def dispute_all_matches(matches, points):
    for match in matches:
        result = dispute_one_match(match)
        points = add_points(choises=match, points=points, answer=result)
    return points


def order_points(points):
    if isinstance(points, dict):
        points = points.items()
    # sort keys:
    points = sorted(points)
    # return sorted values
    return sorted(points, key=lambda x: -x[1])


# presentation:
def formated_results(ordered_points, msg="{}   ({} points)"):
    formated = ""
    for key, value in ordered_points:
        formated += msg.format(key, value) + "\n"
    return formated


def formated_menu(n):
    msg = "championship ({} matches), swiss system ({} matches), league ({} matches)"
    n_championship_matches = int(math.factorial(n)/(2 * math.factorial(n - 2)))
    n_swiss_system_matches = int(math.ceil(math.log(n, 2)) * math.floor(n / 2))
    n_league_matches = int(n - 1)
    return msg.format(n_championship_matches, n_swiss_system_matches, n_league_matches)


def handle_the_options(option, values, points):
    if option in ["c", "championship"]:
        matches = generate_random_matches(values)
        # print "matches: ", matches
        points = dispute_all_matches(matches, points)
        # print "points: ", points
        points = order_points(points)
        print formated_results(points)
    elif option in ["s", "swiss system"]:
        points = swiss_system_matches(points)
        print formated_results(points)
    elif option in ["l", "league"]:
        while len(values) > 1:
            random.shuffle(values)
            values = chose_the_bests(values)
            # print values
        print "\n\n", values[0]
    elif option in ["q", "quit"]:
        sys.exit(0)
    else:
        print "\n\nplease insert:"
        print "(c) for championship,(s) for swiss system, or (l) for league\n"


def run():
    clear_screen()
    args = get_args()
    values = get_values(args)
    if "" in values:
        values.remove("")
    # print "values: ", values
    points = create_points(values)
    # print "points: ", points
    n = len(points)
    while True:
        print formated_menu(n)
        option = raw_input("what tournament do you want? ").lower()
        handle_the_options(option, values, points)

if __name__ == '__main__':
    run()
