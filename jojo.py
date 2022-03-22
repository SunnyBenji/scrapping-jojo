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
        self.get_characters_link()

    def get_request(self, url):
        return requests.get(url).text

    def get_soup(self, url):
        return BeautifulSoup(self.get_request(url), 'html.parser')

    def get_characters_link(self):
        self.get_charactereLink_first_part()
        self.get_charactereLink_second_part()

    def get_charactereLink_first_part(self):
        categories = self.get_soup(self.pages[1]).find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        for category in categories:
            characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
            for character in characters:
                link = character.a.get('href')
                if link.find(':') == -1:
                    self.characters_link.append(link)

    def get_charactereLink_second_part(self):
        categories = self.get_soup(self.pages[1]+'?from=Squalo').find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        for category in categories:
            characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
            for character in characters:
                link = character.a.get('href')
                self.characters_link.append(link)

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
    print(pd.DataFrame(characters))


   