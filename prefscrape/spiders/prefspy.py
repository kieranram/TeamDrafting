import scrapy
import pandas as pd
from scrapy import Selector

class prefspy(scrapy.Spider):
    name = 'prefspy'

    draftdf = pd.DataFrame(columns = ['Year', 'AV', 'G', 'PB', 'TM', 'Number', 'Pos'])

    start_urls = ['https://www.pro-football-reference.com/draft/']
        #draft > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(7)
#team_draft > tbody:nth-child(4) > tr:nth-child(1) > th:nth-child(1) > a:nth-child(1)
    def parse(self, response):
        teams = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den',
                'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'sdg', 'ram', 'mia', 'min',
                'nwe', 'nor', 'nyg', 'nyj', 'rai', 'phi', 'pit', 'sfo', 'sea', 'tam',
                'oti', 'was']
        meta = {}
        for team in teams:
            meta['Team'] = team
            link = 'https://www.pro-football-reference.com/teams/' + team + '/draft.htm'
            print(link)
            yield scrapy.Request(link, meta = meta, callback = self.teampage)

    def teampage(self, response):
        year = 2015
        players = response.css('#draft > tbody:nth-child(4) > tr')
        playerinfo = {'Year' : 0, 'Number' : 0, 'AV' : 0, 'G' : 0, 'PB' : 0, 'TM' : '', 'Pos' : '', 'Round' : 0}
        playerinfo['TM'] = response.meta['Team']
        for player in players:
            infoget = Selector(text = player.extract(), type = 'html')

            numbercand = infoget.css('td:nth-child(4)::text').extract_first()
            if numbercand:
                playerinfo['Number'] = numbercand
            else:
                pass

            ycand = infoget.css('th:nth-child(1) > a:nth-child(1)::text').extract_first()
            if ycand:
                playerinfo['Year'] = int(ycand)
            else:
                continue



            position = infoget.css('td:nth-child(5)::text').extract_first()
            if position:
                playerinfo['Pos'] = position

            rnd = infoget.css('td:nth-child(2)::text').extract_first()
            if rnd:
                playerinfo['Round'] = int(rnd)

            avcand = infoget.css('td:nth-child(10)::text').extract_first()
            if avcand:
                playerinfo['AV'] = int(avcand)
            else:
                playerinfo['AV'] = 0

            gcand = infoget.css('td:nth-child(11)::text').extract_first()
            if gcand:
                playerinfo['G'] = int(gcand)
            else:
                playerinfo['G'] = 0

            pbcand = infoget.css('td:nth-child(8)::text').extract_first()
            if pbcand:
                playerinfo['PB'] = int(pbcand)
            else:
                playerinfo['PB'] = 0

            self.draftdf = self.draftdf.append(pd.Series(playerinfo), ignore_index = True)

    def closed(self, reason):
        self.draftdf.set_index('Number').to_csv('posandround.csv')
