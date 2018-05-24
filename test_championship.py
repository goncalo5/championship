#!/usr/bin/python
import unittest
import championship


class TestChampionship(unittest.TestCase):

    def setUp(self):
        self.values = ["a", "b", "c"]

    def test_create_points(self):
        result = championship.create_points(self.values)
        self.assertEqual(result, {"a": 0, "b": 0, "c": 0})
        self.assertEqual(len(result), len(self.values))

    def test_generate_random_matches(self):
        result = championship.generate_random_matches(self.values)
        self.assertEqual(len(result), len(self.values))

    def test_generate_1round_swiss_system_matches(self):
        points = {"a": 0, "b": 0, "c": 0}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [("a", "b")])

        points = {"a": 0, "b": 0, "c": 0, "d": 0}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [("a", "b"), ("c", "d")])

        points = {"a": 0, "b": 1, "c": 2}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [("c", "b")])

        points = {"a": 1, "b": 4, "c": 3, "d": 0}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [("b", "c"), ("a", "d")])

        points = {"a": 0}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [])

        points = {}
        result = championship.generate_1round_swiss_system_matches(points)
        self.assertEqual(result, [])

    # def test_swiss_system_matches(self):
    #     points = {"a": 0, "b": 0}
    #     result = championship.swiss_system_matches(points)
    #     expected = [[("a", 3), ("b", 0)], [("b", 3), ("a", 0)], [("a", 1), ("b", 1)]]
    #     self.assertIn(result, expected)

    # def test_dispute_one_match(self):
    #     result = championship.dispute_one_match(["a", "b"])
    #     self.assertIn(result, [0, 1, 2])

    def test_add_points(self):
        choises = ["a", "b"]
        answer = 1
        points = {"a": 0, "b": 0, "c": 3}
        result = championship.add_points(choises, points, answer)
        self.assertEqual(result, {"a": 3, "b": 0, "c": 3})

        choises = ["a", "b"]
        answer = 0
        points = {"a": 0, "b": 0, "c": 3}
        result = championship.add_points(choises, points, answer)
        self.assertEqual(result, {"a": 1, "b": 1, "c": 3})

        choises = ["a", "c"]
        answer = 2
        points = {"a": 0, "b": 0, "c": 3}
        result = championship.add_points(choises, points, answer)
        self.assertEqual(result, {"a": 0, "b": 0, "c": 6})

        choises = ["a", "c"]
        answer = "2"
        points = {"a": 0, "b": 0, "c": 3}
        result = championship.add_points(choises, points, answer)
        self.assertEqual(result, {"a": 0, "b": 0, "c": 6})

        choises = ["a", "c"]
        answer = 2
        points = [("a", 6), ("b", 3), ("c", 0)]  # ordered
        result = championship.add_points(choises, points, answer)
        self.assertEqual(result, {"a": 6, "b": 3, "c": 3})

        choises = "c"
        points = [("a", 6), ("b", 3), ("c", 0)]  # ordered
        result = championship.add_points(choises, points)
        self.assertEqual(result, {"a": 6, "b": 3, "c": 3})

        choises = "ghi"
        points = [("abc", 6), ("def", 3), ("ghi", 0)]  # ordered
        result = championship.add_points(choises, points)
        self.assertEqual(result, {"abc": 6, "def": 3, "ghi": 3})

    # def test_dispute_all_matches(self):
    #     matches = [("a", "c"), ("b", "c"), ("a", "b")]
    #     points = {"a": 0, "b": 0, "c": 0}
    #     result = championship.dispute_all_matches(matches, points)
    #     self.assertIsInstance(result, dict)
    #     self.assertEqual(len(result), len(matches))

    def test_order_points(self):
        result = championship.order_points({"a": 3, "b": 0, "c": 6})
        self.assertEqual(result, [("c", 6), ("a", 3), ("b", 0)])

        result = championship.order_points({"a": 3})
        self.assertEqual(result, [("a", 3)])

        result = championship.order_points({})
        self.assertEqual(result, [])

    def test_formated_results(self):
        ordered_points = [("c", 6), ("a", 3), ("b", 0)]
        result = championship.formated_results(ordered_points, "{} {}")
        self.assertEqual(result, "c 6\na 3\nb 0\n")

        result = championship.formated_results(ordered_points, "{}  ({} pts)")
        self.assertEqual(result, "c  (6 pts)\na  (3 pts)\nb  (0 pts)\n")

if __name__ == '__main__':
    unittest.main()
