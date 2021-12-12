
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from time import sleep

import pandas as pd


class AudibleWebScraper():
    def __init__(self):
        self.driver = webdriver.Firefox()
        
        self.REVIEWS_PER_PAGE = 10
        
        self.search_url             = 'https://www.audible.com/search?keywords={}&ref=a_search_t1_header_search'
        self.override_country       = '&overrideBaseCountry=true&overrideBaseCountry=true&ipRedirectOverride=true'
        self.first_result_xpath     = "//div[contains(@data-widget,'productList')]/li[1]//li[1]//a"
        self.first_result_box_xpath = "//div[contains(@data-widget,'productList')]/li[1]/div/div[1]/div/div[2]/div/div"
        self.review_list_xpath_fmt  = "//div[contains(@class,'ReviewsTab{0}')]"
        self.more_reviews_xpath     = "//span[contains(@class,'showMoreReviews')]"
        self.review_xpath_fmt       = "//div[contains(@class,'{0}reviews{1}')]/p[1]"
        
        
    def searchAudiobook(self, book_title):
        return self.getBookEntry(book_title.replace(' ', '+'))
        
    def getBookEntry(self, book_title):
        try:
            self.driver.get(self.search_url.format(book_title) + self.override_country)
        except NoSuchElementException:
            return None
        
        first_result = self.driver.find_element_by_xpath(self.first_result_box_xpath)
        book_metadata = self.getBookMetadata(first_result.text.split('\n'))
        
        book_link = self.driver.find_element_by_xpath(self.first_result_xpath)
        book_link.click()
        
        book_reviews = self.getBookReviews()
        book_metadata.update(book_reviews)
        
        return book_metadata
        
    
    def getBookMetadata(self, data):
        book_data = {}
        for i, field in enumerate(data):
            if i == 0: 
                book_data['title'] = field
            elif field.startswith('By: '):
                book_data['author'] = field.replace('By: ', '').split(',')[0]
            elif field.startswith('Narrated by: '):
                book_data['narrator'] = field.replace('Narrated by: ', '')
            elif field.startswith('Length: '):
                book_data['runtime'] = self.getRuntime(field)
            elif field.startswith('Release date: '):
                book_data['date'] = field.replace('Release date: ', '')
            elif field.startswith('Language: '):
                book_data['language'] = field.replace('Language: ', '')
            elif 'stars' in field:
                book_data['rating'] = float(field.split(' ')[0])
            elif 'ratings' in field:
                book_data['no_ratings'] = int(field.split(' ')[0].replace(',', ''))
                
        price_txt = self.driver.find_element_by_id("buybox-regular-price-0").text
        book_data['price'] = float(price_txt.split(': ')[-1].replace('$', ''))
        return book_data


    def getBookReviews(self, num_pages = 5):
        # Expand review list
        local_num_pages = 1
        try:
            for _ in range(num_pages):
                more_reviews = self.driver.find_element_by_xpath(self.more_reviews_xpath)
                if more_reviews:
                    more_reviews.click()
                    local_num_pages += 1
                    sleep(1)
                else:
                    break
            local_num_pages -= 1
        except NoSuchElementException:
            pass
        
        max_review_count = num_pages * self.REVIEWS_PER_PAGE
        reviews_label = [f'review_{i+1}' for i in range(max_review_count)]
        reviews_loc = 'US'
        
        review_list = self.driver.find_element_by_xpath(self.review_list_xpath_fmt.format(reviews_loc))
        if not review_list:
            reviews_loc = 'UK'
            review_list = self.driver.find_element_by_xpath(self.review_list_xpath_fmt.format(reviews_loc))
            if not review_list:
                return dict(zip(reviews_label, [''] * max_review_count))
        
        reviews = []
        for page in range(local_num_pages):
            current_page_reviews = review_list.find_elements_by_xpath(self.review_xpath_fmt.format(reviews_loc, page))
            for rev in current_page_reviews:
                reviews.append(rev.text)
                
        padding = max_review_count - len(reviews)
        reviews += [''] * padding
        return dict(zip(reviews_label, reviews))
            
            
    def getRuntime(self, raw_duration):
        time = [int(s) for s in raw_duration.split() if s.isdigit()]
        return time[0] + time[1] / 60.0
    
    
    def constructDatabase(self, booklist):
        num   = 100
        db    = []
        
        for i, book_title in enumerate(booklist):
            book = self.searchAudiobook(book_title)
            if book:
                db.append(book)
            
            if (i+1) % num == 0:
                pd.DataFrame(db).to_csv(f'audible_data_{i//num}.csv', index=False)
                db = []
        
        pd.DataFrame(db).to_csv(f'audible_data_{len(booklist)//num}.csv', index=False)
    

if __name__ == '__main__':
    # books = [
    #     'Crime and punishement',
    #     'Go tell the bees that I am gone',
    #     'Harry Potter and the Half-Blood Prince (Harry Potter #6)'
    # ]
    
    kaggle_db = pd.read_csv('Audible_Dataset_final.csv')
    books = kaggle_db['Book Title']
    
    bot = AudibleWebScraper()
    bot.constructDatabase(books)
    