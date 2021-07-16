"""Parse FAQ from website https://designing-the-future.org ."""
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import config


def get_data():
    """Get data."""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    url = 'https://designing-the-future.org/the-venus-project-faq/'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    titles = soup.find("div", class_="wk-accordion").find_all('h3', 'toggler')
    questions = []
    answers = []

    for title in titles:
        title = title.find("a").text.strip()
        questions.append(title)

    contents = soup.find(
        "div", class_="wk-accordion").find_all('div', 'content')
    for content in contents:
        answers.append(content.text.strip())

    IDS = []
    values = []
    for i, (a, b) in enumerate(zip(questions, answers), start=1):
        IDS.append(i)
        values.append(f'({i},"{a}","{b}")')

    # Создать list с ID's по количеству вопросов
    dump = json.dumps(IDS)
    # Создать подключение к db
    base = sqlite3.connect(config.DB_NAME)
    cur = base.cursor()
    # Удалить таблицу, если уже существует
    base.execute('DROP TABLE IF EXISTS answer_ids')
    base.commit()
    # Создать таблицу
    base.execute('CREATE TABLE IF NOT EXISTS answer_ids(`count` TEXT)')
    base.commit()
    # Записать list в db
    cur.execute(f'INSERT INTO `answer_ids`(`count`) VALUES ("{dump}")')
    # cur.execute(f'UPDATE answer_ids SET `count`="{dump}ь"')
    base.commit()

    # Удалить старую таблицу faq в db
    base.execute('DROP TABLE IF EXISTS faq')
    base.commit()
    # Создать таблицу faq
    base.execute('CREATE TABLE IF NOT EXISTS faq(\
        id INT,\
        q TEXT,\
        a TEXT\
     )')
    base.commit()
    # Составить SQL запрос с данными списков
    values = ','.join(values)
    # print(values)
    cur.execute(f'INSERT INTO faq(id, q, a) VALUES {values}')
    base.commit()


def main():
    """Run main."""
    get_data()


if __name__ == "__main__":
    main()
