import scrapy


class Spider(scrapy.Spider):
    name = "gol"
    start_urls = ['https://gol.gg/game/stats/{}/page-game/'.format(i) for i in range(1, 53426)]
    
    def parse(self, response):
        blue_side = response.css("div.col-sm-6")[0]
        blue_side_name = blue_side.css("a::text").get()
        blue_side_result = blue_side.css("div.col-12.blue-line-header::text")[1].get()
        blue_side_result = blue_side_result.replace(' ','').replace('-','')
        red_side = response.css("div.col-sm-6")[1]
        red_side_name = red_side.css("a::text").get()
        red_side_result = red_side.css("div.col-12.red-line-header::text")[1].get()
        red_side_result = red_side_result.replace(' ','').replace('-','')
        players = response.xpath('//td[@style="white-space:nowrap"]/a/text()').getall()
        players_blue = players[:5]
        players_red = players[5:]
        date = response.css("div.col-12.col-sm-5::text").get()[:10]
        tournament = response.css("div.col-12.col-sm-7")
        tournament_name = tournament.css("a::text").get()
        yield {
            "date": date,
            "tournament_name": tournament_name,
            "blue_side_team": blue_side_name,
            "blue_side_result": blue_side_result,
            "red_side_team": red_side_name,
            "red_side_result": red_side_result,
            "players_blue": players_blue,
            "players_red": players_red
        }