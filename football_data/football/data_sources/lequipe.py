
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
        for day_table_link in self.get_all_url_tables():
            time.sleep(10)  # be kind with lequipe.fr
            print('*' * 88)
            for game_data in self._get_games_data(day_table_link):
                print(game_data)

    @staticmethod
    def get_all_url_tables(league=None):
        """ 
        extract result for a given league. If not given, extract all the leagues.
        yield url representing a weeklyy table for all the season.    
        """
        # if league:
        #   URLS_BY_LEAGUE = {league : URLS_BY_LEAGUE.get(league)}

        for league, league_url in URLS_BY_LEAGUE.items():
            # extract league

            main_req = requests.get(league_url)

            # get all games of the season.
            if main_req:
                soup = BeautifulSoup(main_req.content, , 'html.parser')

                # get all games tables
                all_games = soup.findAll('select')[0].select('option')
                all_games_urls = [game['value'] for game in all_games]

                for day_game_url in all_games_urls:
                    yield day_game_url
            else:
                raise Exception('{} is not responding'.format(league_url))

    def _get_games_data(self, day_link):
        """ pick games data for each game, organized on weekly basis  """
        url = '{}{}'.format(self.HOST, day_link)
        res = requests.get(url)
        if not res:
            raise Exception('{} is not responding'.format(url))
        soup = BeautifulSoup(res.content, , 'html.parser')
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
                'score': score,
                'game_day': game_day,
                'game_hour': game_hour
            })
            yield game_record_data

    @classmethod
    def get_game_record(cls, details_link):
        """get record game infos"""
        url = '{}{}'.format(cls.HOST, details_link)
        print('Current url : {}'.format(url))
        game_record_data = {}

        res = requests.get(url)

        if not res:
            raise Exception('{} is not responding'.format(url))

        soup = BeautifulSoup(res.content, 'html.parser')

        home_team_el = soup.find('div', {'id': 'EqDom'})

        away_team_el = soup.find('div', {'id': 'EqExt'})

        home_team_name = home_team_el.select_one('.equipe').text.strip()
        away_team_name = away_team_el.select_one('.equipe').text.strip()

        home_yellow_cards_el = home_team_el.select_one('.cjaune')
        if home_yellow_cards_el is not None:
            home_yellow_cards = home_yellow_cards_el.findAll('div')[0].text
            # home_yellow_cards = home_yellow_cards_el[0].findAll('div')
        else:
            home_yellow_cards = ''

        away_yellow_cards_el = away_team_el.select_one('.cjaune')
        if away_yellow_cards_el:
            away_yellow_cards = away_yellow_cards_el.findAll('div')[0].text
        else:
            away_yellow_cards = ''

        home_red_cards_el = home_team_el.select_one('.crouge')
        if home_red_cards_el:
            home_red_cards = home_red_cards_el.findAll('div')[0].text
        else:
            home_red_cards = ''

        away_red_cards_el = away_team_el.select_one('.cjrouge')
        if away_red_cards_el:
            away_red_cards = away_red_cards_el.findAll('div')[0].text
        else:
            away_red_cards = ''

        home_scorers = [el.text for el in home_team_el.select('.buteur')]
        away_scorers = [el.text for el in away_team_el.select('.buteur')]

        additional_infos = soup.select_one('.info_match_sup').text
        city, arena, fan_number = re.split('; |, |\*|\n', additional_infos)
        return {
            'away_team': {
                'name': away_team_name,
                'scorers': away_scorers,
                'red_cards': away_red_cards,
                'yellow_cards': away_yellow_cards,
            },
            'home_team': {
                'name': home_team_name,
                'scorers': home_scorers,
                'red_cards': home_yellow_cards,
                'yellow_cards': home_yellow_cards
            },
            'city': city.strip(),
            'arena': arena.strip(),
            'fan_number': fan_number.strip()

        }
        return game_record_data
