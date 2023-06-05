import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

import time

# Selenium imports

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["newyork.craigslist.org"]
    # start_urls = ["https://newyork.craigslist.org/search/egr#search=1~thumb~0~0"]

    def start_requests(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # self.driver.get("https://newyork.craigslist.org/search/egr#search=1~thumb~0~0")
        self.driver.get("https://newyork.craigslist.org/search/edu#search=1~thumb~0~0")
        

        # create a scrapy selector object that has the page source of target url
        sel = Selector(text=self.driver.page_source)

        job_urls = sel.xpath("//a[@class='titlestring']/@href").extract()

        for joburl in job_urls:
            yield Request(joburl,callback=self.parse)

        # implement the click of Next button functionality using selenium

       
        while True:

            try:
                 # locator of the next button
                next_button = self.driver.find_element(By.XPATH , "//button[@class='bd-button cl-next-page icon-only']")
                time.sleep(3)
                self.logger.info("Waiting for 3 seconds...")
                
                # next_button.click()             # click on next button

                self.driver.execute_script("arguments[0].click();" , next_button)

                sel = Selector(text=self.driver.page_source)

                job_urls = sel.xpath("//a[@class='titlestring']/@href").extract()

                for joburl in job_urls:
                    yield Request(joburl,callback=self.parse)

            except NoSuchElementException:
                self.logger.info("No more NEXT button to click...")
                self.driver.close()
                break

    def parse(self, response):

        # Logic to fetch data points like job title, compensation, etc
        pass
