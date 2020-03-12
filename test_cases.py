import unittest
import math
import itertools
# mine:
import championship


class TestChampionship(unittest.TestCase):

    def test_add_a_team(self):
        self.assertEqual(championship.add_a_team(["a", "b", "c"], "d"), ["a", "b", "c", "d"])
        self.assertEqual(championship.add_a_team([], "a"), ["a"])
        self.assertEqual(championship.add_a_team(["a"], ""), ["a"])
        self.assertEqual(championship.add_a_team(["a"], []), ["a"])
        with self.assertRaises(Exception):
            championship.add_a_team([], ["a", "b"])

    def test_create_matches(self):
        self.assertEqual(championship.create_matches(["a", "b", "c", "d"]), [["a", "b"], ["c", "d"]])
        self.assertEqual(championship.create_matches(["a", "b"]), [["a", "b"]])
        self.assertEqual(championship.create_matches(["a", "b", "c"]), [["a", "b"], ["c"]])
        with self.assertRaises(Exception):
            championship.create_matches([])
        with self.assertRaises(Exception):
            championship.create_matches(["a"])
        with self.assertRaises(Exception):
            championship.create_matches(["a", {}])
        with self.assertRaises(Exception):
            championship.create_matches(["a", 2])

    def test_create_random_matches(self):
        l = ["a", "b", "c", "d"]
        res = championship.create_random_matches(l)
        self.assertEqual(len(res), math.ceil(len(l) / 2))
        self.assertIn(res[0][1],l)
        self.assertEqual(sorted(itertools.chain(*l)), l)

    def test_matches_after_results(self):
        self.assertEqual(championship.teams_after_results([["a", "b"], ["c", "d"]], [1, 0]), ["b", "c"])
        self.assertEqual(championship.teams_after_results([["a", "b"], ["c"]], [0]), ["a", "c"])
        self.assertEqual(championship.teams_after_results([["a", "b"]], [1]), ["b"])
        self.assertEqual(championship.teams_after_results([["a", "b"], ["c", "d"], ["e"]], [0, 1]), ["a", "d", "e"])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a", "b"], ["c", "d"]], [2, 0])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a", "b"], ["c", "d"]], [1])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a", "b"], ["c", "d"]], [1, 1, 0])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a"], ["c", "d"]], [0, 1])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a", "b"], ["c"]], [1, 0])
        with self.assertRaises(Exception):
            championship.teams_after_results([["a", "b"], ["c", "d"], ["e", "f"]], [1, 0])

    def test_check_if_match_exists(self):
        # True:
        self.assertTrue(championship.check_if_match_exists([["a", "b"]], 0))
        self.assertTrue(championship.check_if_match_exists([["a", "b"], ["c", "d"]], 0))
        self.assertTrue(championship.check_if_match_exists([["a", "b"], ["c", "d"]], 1))
        # False:
        self.assertFalse(championship.check_if_match_exists([["a", "b"], ["c", "d"]], 2))
        self.assertFalse(championship.check_if_match_exists([["a", "b"], ["c", "d"]], 5))
        self.assertFalse(championship.check_if_match_exists([["a", "b"]], 1))
        self.assertFalse(championship.check_if_match_exists([], 0))
        with self.assertRaises(Exception):
            championship.check_if_match_exists([["a", "b"], ["c", "d"]], "string")

    def test_check_if_it_is_the_winner(self):
        self.assertTrue(championship.check_if_it_is_the_winner(["a"]))
        self.assertFalse(championship.check_if_it_is_the_winner(["a", "b"]))
        with self.assertRaises(Exception):
            championship.check_if_it_is_the_winner([])

    def test_check_if_the_teams_are_fine(self):
        self.assertTrue(championship.check_if_the_teams_are_fine(["a", "b"]))
        self.assertTrue(championship.check_if_the_teams_are_fine(["a", "b", "c"]))
        self.assertFalse(championship.check_if_the_teams_are_fine([]))
        self.assertFalse(championship.check_if_the_teams_are_fine(["a"]))
        self.assertFalse(championship.check_if_the_teams_are_fine([["a"]]))

    def test_calc_new_match(self):
        # test easiest method
        matches = [["a", "b"], ["c", "d"]]
        match_i = 0
        results = [1]
        list_of_teams = ["a", "b", "c", "d"]
        new_match, new_matches, new_match_i, new_results, new_list_of_teams =\
            championship.calc_new_match(matches, match_i, results, list_of_teams)
        self.assertEqual(sorted(new_match), matches[1])
        self.assertEqual(new_matches, matches)
        self.assertEqual(new_match_i, 1)
        self.assertEqual(new_results, results)
        self.assertEqual(new_list_of_teams, list_of_teams)
        # test next level
        matches = [["a", "b"], ["c", "d"]]
        match_i = 1
        results = [1, 0]
        list_of_teams = ["a", "b", "c", "d"]
        new_match, new_matches, new_match_i, new_results, new_list_of_teams =\
            championship.calc_new_match(matches, match_i, results, list_of_teams)
        self.assertEqual(sorted(new_match), ["b", "c"])
        self.assertEqual(sorted(new_matches[0]), ["b", "c"])
        self.assertEqual(new_match_i, 0)
        self.assertEqual(new_results, [])
        self.assertEqual(sorted(new_list_of_teams), ["b", "c"])
        # test winner
        matches = [["a", "b"]]
        match_i = 0
        results = [1]
        list_of_teams = ["a", "b"]
        new_match, new_matches, new_match_i, new_results, new_list_of_teams =\
            championship.calc_new_match(matches, match_i, results, list_of_teams)
        self.assertEqual(new_match, None)
        self.assertEqual(new_matches, [])
        self.assertEqual(new_match_i, 0)
        self.assertEqual(new_results, [])
        self.assertEqual(new_list_of_teams, ["b"])



if __name__ == '__main__':
    unittest.main()