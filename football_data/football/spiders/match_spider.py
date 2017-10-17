from scrapy import Item, Field, Rule, LinkExtractor


 
class MatchItem(Item):
  country = Field()
  league = Field()
  date = Field()
  home_team = Field()
  away_team = Field()
  home_goals1 = Field()
  home_goals2 = Field()
  away_goals1 = Field()
  away_goals2 = Field()


 class MatchSpider(CrawlSpider):
  name = 'soccer'
  start_urls = ['http://www.stat-football.com/en/']

rules = (
   Rule(LinkExtractor(restrict_css="ul#menuA > li:not(.f11.t0.tar)"), follow=True), # LEVEL 1
   Rule(LinkExtractor(restrict_css="td.im34.p0612 > nobr:nth-of-type(4)"), callback="populate_item") # LEVEL 2
)

league = response.css("h1.f6.nw::text").extract_first()
country = response.css("td.im34.p0612.t0.vat > a > strong::text").extract_first()

elements = response.css("td.s14 > pre::text, td.s14 > pre > a::text, td.s14 > pre > span::text").extract()
for i in range(0, len(elements)-2):
  if ".201" in elements[i]:
    match = MatchItem()
 
    match["league"] = league
 
    match["country"] = country
    match["date"] = elements[i]
    match["home_team"] = elements[i+1]
    match["away_team"] = elements[i+1]
    match["home_goals1"] = elements[i+2]
    match["home_goals2"] = elements[i+2]
    match["away_goals1"] = elements[i+2]
    match["away_goals2"] = elements[i+2]


elements = response.css("td.s14 > pre::text, td.s14 > pre > a::text, td.s14 > pre > span::text").extract()
for i in range(0, len(elements)-2):
  if ".201" in elements[i]:
    match = MatchItem()
 
    match["league"] = league
 
    match["country"] = country
    match["date"] = elements[i]
    match["home_team"] = elements[i+1]
    match["away_team"] = elements[i+1]
    match["home_goals1"] = elements[i+2]
    match["home_goals2"] = elements[i+2]
    match["away_goals1"] = elements[i+2]
    match["away_goals2"] = elements[i+2]


def populate_item(self, response):
  league = response.css("h1.f6.nw::text").extract_first()
  country = response.css("td.im34.p0612.t0.vat > a > strong::text").extract_first()
  elements = response.css("td.s14 > pre::text, td.s14 > pre > a::text, td.s14 > pre > span::text").extract()
  for i in range(0, len(elements)-2):
    if ".201" in elements[i]:
      match = MatchItem()
      match["league"] = league
      match["country"] = country
      match["date"] = elements[i]
      match["home_team"] = elements[i+1]
      match["away_team"] = elements[i+1]
      match["home_goals1"] = elements[i+2]
      match["home_goals2"] = elements[i+2]
      match["away_goals1"] = elements[i+2]
      match["away_goals2"] = elements[i+2]
      yield match
