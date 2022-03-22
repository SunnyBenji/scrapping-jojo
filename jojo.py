import requests
from bs4 import BeautifulSoup
import  pandas as pd
import time

# Do the same with https://stacker.com/stories/1587/100-best-movies-all-time

class JojoScraper(object):

    def __init__(self):
        self.pages = [
            r'https://jjba.fandom.com',
            r'https://jjba.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages'
        ]
        self.characters_link = []
        self.characters_link_first_part = []
        self.characters_link_second_part = []
        self.characters = []
        self.get_characters_link(5)
        self.lim1 = None
        self.lim2 = None

    def get_request(self, url):
        return requests.get(url).text

    def get_soup(self, url):
        return BeautifulSoup(self.get_request(url), 'html.parser')

    def get_characters_link(self, lim=None):
        if type(lim) == int:
            if lim > 195:
                self.lim1 = 195
            else: 
                self.lim1 = lim
            self.lim2 = lim - self.lim1
        
        self.get_charactereLink_first_part(self.lim1)
        self.get_charactereLink_second_part(self.lim2)
        self.characters_link = self.characters_link_first_part + self.characters_link_second_part

    def get_charactereLink_first_part(self, lim1):
        categories = self.get_soup(self.pages[1]).find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        if (type(lim1) != int):
            for category in categories:
                characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
                for character in characters:
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link_first_part.append(link) 
        elif (len(self.characters_link_first_part) < lim1 ) :
            for category in categories:
                if(len(self.characters_link_first_part) < lim1) :
                    characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
                    for character in characters:
                        if(len(self.characters_link_first_part) < lim1):
                            link = character.a.get('href')
                            if link.find(':') == -1:
                                self.characters_link_first_part.append(link) 
                        else:
                            break
                else:
                    break

    def get_charactereLink_second_part(self, lim2):
        categories = self.get_soup(self.pages[1]+'?from=Squalo').find(class_='category-page__members').find_all(class_='category-page__members-wrapper')
        if (type(lim2) != int ):
            for category in categories:
                characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
                for character in characters:
                    link = character.a.get('href')
                    if link.find(':') == -1:
                        self.characters_link_second_part.append(link)
        elif (len(self.characters_link_second_part) < lim2 ) :
            for category in categories:
                if(len(self.characters_link_second_part) < lim2) :
                    characters = category.find(class_='category-page__members-for-char').find_all(class_='category-page__member')
                    for character in characters:
                        if(len(self.characters_link_second_part) < lim2) :
                            link = character.a.get('href')
                            if link.find(':') == -1:
                                self.characters_link_second_part.append(link)
                        else:
                            break
                else: 
                    break;


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
    start = time.perf_counter()
    characters = JojoScraper().get_characters()
    end = time.perf_counter()
    print(end - start)
    dataFrame = pd.DataFrame(characters).fillna('No data')
    dataFrame.to_excel("jojo's charactere data.xlsx", sheet_name="jojo_charaters",encoding='utf-8', index=False)
    print(dataFrame)


   