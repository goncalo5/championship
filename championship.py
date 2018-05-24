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


class System(object):
    """Common to all Systems"""
    def __init__(self, values):
        super(System, self).__init__()
        self.values = values
        self.n = len(self.values)
        self.points = {}
        self.create_points()

    def create_points(self):
        for value in self.values:
            self.points[value] = 0
        return self.points

    def dispute_all_matches(self, matches):
        self.all_results = []
        for match in matches:
            result = self.dispute_one_match(match)
            self.all_results.append(result)
            self.add_points(choises=match, answer=result)

    def dispute_one_match(self, choises):
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

    def order_points(self):
        if isinstance(self.points, dict):
            self.points = self.points.items()
        self.points = sorted(self.points)
        self.points = sorted(self.points, key=lambda x: -x[1])

    def add_points(self, choises, answer=None):
        # print "choises: ", choises
        # print "points: ", points
        if isinstance(choises, str):  # in the case of odd numbers, it still wins points
            if isinstance(self.points, list):
                self.points = OrderedDict(self.points)
            self.points[choises] += 3
            return dict(self.points)
        # print "answer: ", answer
        answer = int(answer)
        if answer == 0:
            self.points[choises[0]] += 1
            self.points[choises[1]] += 1
        else:
            if isinstance(self.points, list):
                self.points = OrderedDict(self.points)
            self.points[choises[answer - 1]] += 3
        self.points = dict(self.points)

    # presentation:
    def formated_results(self, msg="{}   ({} points)"):
        formated = ""
        print "self.points", self.points
        for key, value in self.points:
            formated += msg.format(key, value) + "\n"
        return formated


class KnockoutSystem(System):
    """Knockout system"""
    def __init__(self, values=[]):
        super(KnockoutSystem, self).__init__(values)
        self.name = "Knockout"
        self.n_matches = int(self.n - 1)
        # ceil(log2 n) * floor(n / 2)
        print "self.n", self.n, "self.values", self.values
        self.n_rounds = int(math.ceil(math.log(self.n, 2)))
        self.left = list(self.values)

    def eliminate_all_losers(self):
        print "self.left", self.left
        all_losers = []
        print "self.all_results", self.all_results
        for i, result in enumerate(self.all_results):
            if result:  # result != 0
                all_losers.append(self.left[result % 2 + i * 2])
        print "all_losers", all_losers
        for loser in all_losers:
            self.left.remove(loser)
        print "self.left", self.left

    def generate_1round_matches(self, random_matches=True):
        print "generate_1round_matches"
        if random_matches:
            random.shuffle(self.left)
        self.order_points()
        is_odd = len(self.left) % 2
        matches = []
        for i in xrange(0, len(self.left) - is_odd, 2):
            matches.append((self.left[i], self.left[i + 1]))
        if is_odd:
            self.add_points(choises=points[-1][0])
        return matches

    def generate_matches(self):
        print "generate_matches"
        for round_i in xrange(self.n_rounds):
            matches = self.generate_1round_matches(self.left)
            self.dispute_all_matches(matches)
            self.eliminate_all_losers()
            print "self.all_results", self.all_results
            self.order_points()


class LeagueSystem(System):
    """League system"""
    def __init__(self, values=[]):
        super(LeagueSystem, self).__init__(values)
        self.name = "League"
        self.n_matches = int(math.factorial(self.n)/(2 * math.factorial(self.n - 2)))

    def generate_random_matches(self):
        matches = []
        for i in xrange(self.n):
            for j in xrange(i):
                matches.append((self.values[i], self.values[j]))
        random.shuffle(matches)
        return matches
    # print generate_random_matches(["a", "b", "c"])


class SwissSystem(System):
    """docstring for swiss"""
    def __init__(self, values=[]):
        super(SwissSystem, self).__init__(values)
        self.name = "Swiss"
        self.n_matches = int(math.ceil(math.log(self.n, 2)) * math.floor(self.n / 2))

    def generate_1round_swiss_system_matches(self):
        self.order_points()
        is_odd = self.n % 2
        matches = []
        for i in xrange(0, self.n - is_odd, 2):
            matches.append((self.points[i][0], self.points[i + 1][0]))
        if is_odd:
            self.add_points(choises=self.points[-1][0])
        return matches

    def swiss_system_matches(self):
        # ceil(log2 n) * floor(n / 2)
        n_rounds = int(math.ceil(math.log(self.n, 2)))
        for round_i in xrange(n_rounds):
            matches = self.generate_1round_swiss_system_matches()
            self.dispute_all_matches(matches)
            self.order_points()


class Run(object):
    """Run the script"""
    def __init__(self):

        clear_screen()
        args = get_args()
        values = get_values(args)
        if "" in values:
            values.remove("")
        print "values: ", values
        # points = create_points(values)
        self.values = values

        self.league_system = LeagueSystem(values=self.values)
        self.swiss_system = SwissSystem(values=self.values)
        self.knockout_system = KnockoutSystem(values=self.values)
        self.all_championships = [self.knockout_system, self.league_system, self.swiss_system]
        self.formated_menu()
        while True:
            print self.msg
            option = raw_input("what tournament do you want? ").lower()
            self.handle_the_options(option)

    def formated_menu(self):
        self.msg = ""
        for championship in self.all_championships:
            self.msg += "(%s)%s (%s matches), " % \
                (championship.name[0], championship.name[1:], championship.n_matches)
        self.msg += "... (Q)uit"

    def handle_the_options(self, option):
        if option in ["l", "league"]:
            self.league_system = LeagueSystem(values=self.values)
            matches = self.league_system.generate_random_matches()
            # print "matches: ", matches
            self.league_system.dispute_all_matches(matches)
            self.league_system.order_points()
            print self.league_system.formated_results()
        elif option in ["s", "swiss system"]:
            self.swiss_system = SwissSystem(values=self.values)
            self.swiss_system.swiss_system_matches()
            self.swiss_system.points
            print self.swiss_system.formated_results()
        elif option in ["k", "knockout"]:
            self.knockout_system = KnockoutSystem(values=self.values)
            self.knockout_system.generate_matches()

            # while len(self.values) > 1:
            #     random.shuffle(self.values)
            #     self.values = self.chose_the_bests()
            #     print self.values
            # print "\n\n", self.values[0]
        elif option in ["q", "quit"]:
            sys.exit(0)
        else:
            print "\n\nplease insert:"

    def chose_the_bests(self):
        # print values
        n = len(self.values)
        for i in xrange(0, n, 2):
            # print self.values, i
            try:
                answer = None
                while not answer:
                    answer = self.ask([self.values[i], self.values[i + 1]])
                    print "eliminated: ", answer
                if answer in ["q", "quit"]:
                    print "bye"
                    return
                else:
                    self.values.remove(answer)
            except IndexError:
                pass
        return self.values

    def ask(self, choises):
        skip = 0
        while True:
            print "\n\nWhat do you perfer?  ({} to skip)".format(skip)
            answer = raw_input("1 - {}  vs  2 - {}   ".format(choises[0], choises[1]))
            if answer in ["q", "quit"]:
                sys.exit(0)
            try:
                answer = int(answer)
                break
            except ValueError:
                print "please select {}, 1 or 2".format(skip)
                continue
        convert = {1: 1, 2: 0}
        # print "answer: ", answer
        if answer in [skip, 1, 2]:
            return choises[convert[answer]]
        else:
            print "\nplease insert {} to skip, if you don't know what is the better".format(skip)
            print "or 1 for {} or 2 for {}\n\n\n".format(choises[0], choises[1])
    # print ask(["goncalo", "ana"])


if __name__ == '__main__':
    Run()

#
# END
#
