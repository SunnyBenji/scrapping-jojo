from typing import Tuple
import requests
from bs4 import BeautifulSoup
import  pandas as pd

# Do the same with https://stacker.com/stories/1587/100-best-movies-all-time

class JojoScraper(object):

    def __init__(self):
        self.pages = [
            r'https://jjba.fandom.com',
            r'https://jjba.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages'
        ]
        self.characters_link = []
        self.characters = []
        self.get_characters_link(4)

    def get_request(self, url):
        return requests.get(url).text

    def get_soup(self, url):
        return BeautifulSoup(self.get_request(url), 'html.parser')

    def get_characters_link(self, lim=None):
        if type(lim) == int:
            if lim > 195:
                lim1 = 195
            else: 
                lim1 = lim
            lim2 = lim - lim1
        else:
            lim1 = None
            lim2 = None
        self.get_charactereLink_first_part(lim1)
        self.get_charactereLink_second_part(lim2)

    def get_charactereLink_first_part(self, lim1):
        categories = self.get_soup(self.pages[1]).find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        for category in categories:
            characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
            for character in characters:
                if (type(lim1) != int):
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link.append(link)
                elif (len(self.characters_link) < lim1 ) :
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link.append(link)

    def get_charactereLink_second_part(self, lim2):
        categories = self.get_soup(self.pages[1]+'?from=Squalo').find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        links = 0
        for category in categories:
            characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
            for character in characters:
                if (type(lim2) != int ):
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link.append(link)
                elif ((195+links) - len(self.characters_link) >= 0  and ((195+links) - len(self.characters_link) < lim2)) :
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link.append(link)
                        links += 1

    def get_characters(self):
        for character_link in self.characters_link:
            page = self.get_soup(self.pages[0]+character_link)
            informations_group = page.find_all(class_='pi-group')
            character_info = {}
            for informations in informations_group:
                contents = informations.find_all(class_='pi-data')
                for content in contents:
                    character_info[content.find(class_='pi-secondary-font').get_text()] = content.find(class_='pi-font').get_text()
            self.characters.append(character_info)
        return self.characters

if __name__ == "__main__":
    characters = JojoScraper().get_characters()
    dataFrame = pd.DataFrame(characters).fillna('No data')
    dataFrame.to_excel("jojo's charactere data.xlsx", sheet_name="jojo_charaters",encoding='utf-8', index=False)
    print(dataFrame)


   