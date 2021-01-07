import scrapy
from selenium import webdriver
import time
import seriesname as sn
from urllib.parse import urljoin
from urllib.parse import urlparse

class Browser:
    def __init__(self, link):
        self.link = link
        self.browser = webdriver.Chrome()
        Browser.goIMDb(self)
        Browser.getTVSeries(self)
        Browser.getEpisodeGuide(self)
        Browser.getSeasonInfo(self)
    
    def goIMDb(self):
        self.browser.get(self.link)
        time.sleep(5)
        Browser.searchSeries(self)

    def getTVSeries(self):
        self.browser.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/table/tbody/tr[1]/td[2]/a").click()
        time.sleep(5)

    def getEpisodeGuide(self):
        self.browser.find_element_by_xpath("//*[@id=\"title-overview-widget\"]/div[1]/div[3]/a/div").click()
        time.sleep(5)

    def getSeasonInfo(self):
        Browser.loadPreviousSeasons(self)
        seriesInfo = self.browser.find_elements_by_css_selector(".list_item")
        for info in seriesInfo:
            print(info.text)

    def searchSeries(self):
        seriesName = self.browser.find_element_by_name("q")
        seriesName.send_keys(sn.seriesName)

        searchButton = self.browser.find_element_by_css_selector("#suggestion-search-button")
        searchButton.click()
        time.sleep(5)
    
    def loadPreviousSeasons(self):
        jsCommand = """
        page = document.querySelector("#load_previous_episodes");
        page.click();
        """
        endToPage = self.browser.execute_script(jsCommand)
        while True:
            end = endToPage
            time.sleep(1)
            endToPage = self.browser.execute_script(jsCommand)
        
        