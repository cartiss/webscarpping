import requests
import re
from bs4 import BeautifulSoup

class Habr_preview():

    def __init__(self, website_link, keywords):
        self.post_link = website_link
        self.keywords = keywords


    def make_bs4_soup(self, post_link):
        response = requests.get(post_link)

        if not response.ok:
            raise Exception('something went wrong :(')

        soup = BeautifulSoup(response.text, 'html.parser')

        return soup


    def search_keywords_in_text(self, text):
        sorted_text_list = re.findall(r'[А-Яа-яЁё]*[\w]*', text)
        for item in sorted_text_list:
            for keyword in self.keywords:
                if item.lower() == keyword.lower():
                    return True
                else:
                    return False


    def print_result(self, date, title, link):
        print(date + ' - ' + title + ' - ' + link)


    def search_keywords_in_open_post(self, link):
        article = self.make_bs4_soup(link).find(class_='tm-page-article__content_inner')
        texts = article.find(id="post-content-body").find_all('p')
        subtitles = article.find(id="post-content-body").find_all('h3')
        items_list_li = article.find(id="post-content-body").find_all('li')
        quotes = article.find(id="post-content-body").find_all('blockquote')
        title = article.find(class_='tm-article-snippet__title').find('span').text
        date = article.find(class_='tm-article-snippet__meta').find(
            class_='tm-article-snippet__datetime-published').find('time').text

        for text in texts:
            if self.search_keywords_in_text(text.text):
                self.print_result(date, link, title)
                return

        for subtitle in subtitles:
            if self.search_keywords_in_text(subtitle.text):
                self.print_result(date, link, title)
                return

        for item_list_li in items_list_li:
            if self.search_keywords_in_text(item_list_li.text):
                self.print_result(date, link, title)
                return

        for quote in quotes:
            if self.search_keywords_in_text(quote.text):
                self.print_result(date, link, title)
                return


    def search_keywords_in_preview(self):
        articles = self.make_bs4_soup(self.post_link).find_all(class_='tm-articles-list__item')
        for article in articles:
            is_searched = False
            tags_span = article.find(class_='tm-article-snippet__hubs').find_all(class_='tm-article-snippet__hubs-item')
            description_paragraphs = article.find(class_='article-formatted-body').find_all('p')
            title = article.find(class_='tm-article-snippet__title').find('span').text
            date = article.find(class_='tm-article-snippet__meta').find(
                class_='tm-article-snippet__datetime-published').find(
                'time').text
            link = article.find(class_='tm-article-snippet__readmore')['href']

            if self.search_keywords_in_text(title):
                self.print_result(date, 'https://habr.com' + link, title)
                continue

            for tag_span in tags_span:
                tag = tag_span.find('span').text
                if self.search_keywords_in_text(tag):
                    self.print_result(date, 'https://habr.com' + link, title)
                    is_searched = True
                    break

            if is_searched:
                continue

            for description_paragraph in description_paragraphs:
                paragraph = description_paragraph.text
                if self.search_keywords_in_text(paragraph):
                    self.print_result(date, 'https://habr.com' + link, title)
                    is_searched = True
                    break

            if is_searched:
                continue

            self.search_keywords_in_open_post('https://habr.com' + link)


if __name__ == '__main__':
    KEYWORDS = input('Введите через пробел ключевые слова: ').split(' ')
    LINK = 'https://habr.com/ru/all/'
    habr = Habr_preview(LINK, KEYWORDS)
    habr.search_keywords_in_preview()