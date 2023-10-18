import scrapy


class Spider(scrapy.Spider):
    name = "srs"
    start_urls = ['https://gol.gg/game/stats/{}/page-summary/'.format(i) for i in range(1, 53426)]
    
    def parse(self, response):
        blue_side = response.css('div.col-4.col-sm-5')
        blue_side_name = blue_side.css("a::text").get()
        red_side = response.css('div.col-4.col-sm-5')[1]
        red_side_name = red_side.css("a::text").get()
        rows = response.css('div.row.pb-1')
        n_games = len(rows.css('h1::text').getall()) // 3
        blue_side_wins = []
        for i in range(0, 3 * n_games, 3):
            if rows.css('h1::text')[i].get() == 'WIN':
                blue_side_wins.append(rows.css('h1::text')[i].get())
        wins = len(blue_side_wins)
        players_blue_place = response.css("div.col-12.col-sm-6.pb-4")[2]
        players_blue = players_blue_place.css("a::text").getall()
        players_red_place = response.css("div.col-12.col-sm-6.pb-4")[3]
        players_red = players_red_place.css("a::text").getall()
        date = response.css("div.col-12.col-sm-5::text").get()[:10]
        tournament = response.css("div.col-12.col-sm-7")
        tournament_name = tournament.css("a::text").get()
        yield {
            "date": date,
            "tournament_name": tournament_name,
            "blue_side_team": blue_side_name,
            "red_side_team": red_side_name,
            "blue_side_wins": wins,
            "n_games": n_games,
            "players_blue": players_blue,
            "players_red": players_red
        }