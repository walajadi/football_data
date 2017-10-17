
import requests
from bs4 import BeautifulSoup
import re
import time

URLS_BY_LEAGUE = {
    'ligue1': 'https://www.lequipe.fr/Football/FootballResultat54959.html',
}


class Scrapper:

    HOST = 'https://www.lequipe.fr'

    def run(self):
        for day_table_link in self.get_all_tables_per_season_per_league():
            time.sleep(10) # be kind with lequipe.fr
            print('*' * 88)
            for game_data in self.get_games_data(day_table_link):
                print(game_data)

    @staticmethod
    def get_all_tables_per_season_per_league(league=None):
        """ extract result for a given league. If not given, extract all the leagues."""

        # if league:
        #   URLS_BY_LEAGUE = {league : URLS_BY_LEAGUE.get(league)}

        for league, league_url in URLS_BY_LEAGUE.items():
            # extract league

            main_req = requests.get(league_url)

            # get all games of the season.
            if main_req:
                soup = BeautifulSoup(main_req.content, 'html')

                # get all games tables
                all_games = soup.findAll('select')[0].select('option')
                all_games_urls = [game['value'] for game in all_games]

                for day_game_url in all_games_urls:
                    yield day_game_url

    def get_games_data(self, day_link):
        """ pick games infos  """

        # pick day / journee / jornada
        url = '{}{}'.format(self.HOST, day_link)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html')
        games = soup.select('.ligne')
        day_number_el = games[0]
        game_day = re.findall('[0-9]+', day_number_el.text)[0]

        # pick games infos : teams (host / away), score, link to game details
        for game_el in games[1:]:
            home_team_el = game_el.select_one('.equipeDom')
            home_team = home_team_el.text
            away_team_el = game_el.select_one('.equipeExt')
            away_team = away_team_el.text
            score_el = game_el.select_one('.score')
            score = score_el.text.strip()
            game_record_link = score_el.find('a', href=True)['href']
            game_hour_el = game_el.select_one('.heure')
            game_hour = game_hour_el.text.strip()

            game_record_data = self.get_game_record(game_record_link)

            game_record_data.update({
                'home_team': home_team,
                'away_team': away_team,
                'score': score,
                'home_team': home_team,
                'home_team': home_team,
                'game_day': game_day,
                'game_hour': game_hour
            })
            yield game_record_data

    def get_game_record(cls, details_link):
        """get record game infos """
        url = '{}{}'.format(cls.HOST, details_link)
        game_record_data = {}

        return {}
