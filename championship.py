#!/usr/bin/python
import argparse
import sys
import os
import random


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
    print "\n\nWhat do you perfer?  ({} to skip)".format(skip)
    answer = raw_input("1 - {}  vs  2 - {}   ".format(choises[0], choises[1]))
    answer = int(answer)
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


def add_points(choises, answer, points):
    if answer == 0:
        points[choises[0]] += 1
        points[choises[1]] += 1
    else:
        points[choises[answer - 1]] += 3
    return points


def dispute_all_matches(matches, points):
    for match in matches:
        result = dispute_one_match(match)
        points = add_points(match, result, points)
    return points


def order_points(points):
    return sorted(points.items(), key=lambda x: -x[1])


def formated_results(ordered_points, msg="{}   ({} points)"):
    formated = ""
    for key, value in ordered_points:
        formated += msg.format(key, value) + "\n"
    return formated


def run():
    clear_screen()
    args = get_args()
    values = get_values(args)
    # print "values: ", values

    points = create_points(values)
    # print "points: ", points
    matches = generate_random_matches(values)
    # print "matches: ", matches
    points = dispute_all_matches(matches, points)
    # print "points: ", points
    points = order_points(points)
    print formated_results(points)
    # while len(values) > 1:
    #     random.shuffle(values)
    #     values = chose_the_bests(values)
    #     # print values
    # print "\n\n", values[0]


if __name__ == '__main__':
    run()
