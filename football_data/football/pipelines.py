# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FootballPipeline(object):
    def process_item(self, item, spider):
        return item


class CleaningPipeline(object):

	def process_item(self, item, spider):
		item["league"] = self.clean_league(item)
		item["date"] = self.clean_date(item)
		item["home_team"] = self.clean_home_team(item)
		item["away_team"] = self.clean_away_team(item)
		item["home_goals1"] = self.clean_home_goals1(item)
		item["home_goals2"] = self.clean_home_goals2(item)
		item["away_goals1"] = self.clean_away_goals1(item)
		item["away_goals2"] = self.clean_away_goals2(item)
		return item

	def clean_league(self, item):
		value = item[“league”]
		return value[value.index(" "):value.index("(")].strip()

	def clean_date(self, item):
		value = item[“date”]
		date_str = value[value.index(".") - 2:].strip()
		date = datetime.strptime(date_str, "%d.%m.%Y")
		return date.strftime("%Y-%m-%d")

	def clean_home_team(self, item):
		value = item[“home_team”]
		return value[:value.index(u"—")].strip()

	def clean_away_team(self, item):
		value = item[“away_team”]
		return value[value.index(u"—") + 1:].strip()

	def clean_home_goals1(self, item):
		value = item[“home_goals1”]
		goals = value[value.index("(") + 1:value.index(")")]
		return int(goals[:goals.index(":")])

	def clean_away_goals1(self, item):
		value = item[“away_goals1”]
		goals = value[value.index("(")+1:value.index(")")]
		return int(goals[goals.index(":")+1:])

	def clean_home_goals2(self, item):
		home_goals1 = item[“home_goals1”]
		value = item[“home_goals2”]
		result = value[:value.index("(")]
		home_goals_full = int(result[:result.index(":")].strip())
		return home_goals_full-home_goals1

	def clean_away_goals2(self, item):
		value = item[“away_goals2”]
		away_goals1 = item[“away_goals1”]
		result = value[:value.index("(")]
		away_goals_full = int(result[result.index(":")+1:].strip())
		return away_goals_full - away_goals1

