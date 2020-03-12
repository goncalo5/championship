#:kivy `1.10.1`
# kivy:
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy import properties as kp
# mine:
import championship


class MainScreenManager(ScreenManager):
    pass


class ChampionShipApp(App):
    list_of_teams = kp.ListProperty()
    matches = kp.ListProperty()
    match_i = kp.NumericProperty()
    team1 = kp.StringProperty("team1")
    team2 = kp.StringProperty("team2")
    results = kp.ListProperty()

    def build(self):
        self.main_screen_manager = MainScreenManager()
        return self.main_screen_manager

    def press_next(self, team_input):
        print("press_next()", team_input.text)
        self.list_of_teams = championship.add_a_team(self.list_of_teams, team_input.text)
        team_input.text = ""

    def press_done(self, team_input):
        print("press_done()", team_input.text)
        self.list_of_teams = championship.add_a_team(self.list_of_teams, team_input.text)
        if not championship.check_if_the_teams_are_fine(self.list_of_teams):
            return
        self.matches = championship.create_random_matches(self.list_of_teams)
        self.team1, self.team2 = self.matches[self.match_i]
        self.main_screen_manager.current = "choosing_team_screen"

    def press_option(self, option_n):
        print("press_option()", option_n)
        self.results.append(option_n)
        print("self.matches: %s, self.match_i: %s, self.results: %s, self.list_of_teams: %s" % 
            (self.matches, self.match_i, self.results, self.list_of_teams))
        self.match, self.matches, self.match_i, self.results, self.list_of_teams =\
            championship.calc_new_match(self.matches, self.match_i, self.results, self.list_of_teams)
        print("self.match: %s, self.matches: %s, self.match_i: %s, self.results: %s, self.list_of_teams: %s" % 
            (self.match, self.matches, self.match_i, self.results, self.list_of_teams))
        if self.match:
            self.team1, self.team2 = self.match
        else:
            # CHAMPIONSHIP OVER:
            self.main_screen_manager.current = "winner_screen"


if __name__ == '__main__':
    ChampionShipApp().run()