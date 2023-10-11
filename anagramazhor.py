import os
import random
import time
from random import seed, shuffle
from flask import Flask, g, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# app.config['SECRET_KEY'] = 'SECRET_KEY'

DICT_OF_WORDS = {}
ENCODING = 'cp1251'
PATH_TO_FILE = r'C:\Users\dim5x\PycharmProjects\Anagramazhor\word_rus_8_tolk_cM3.txt'
# PATH_TO_FILE = r'/home/dim5x/mysite/word_rus_8_tolk_cM3.txt'


@app.before_request
def before_request():
    g.request_start_time = time.time()
    with open(PATH_TO_FILE, 'r', encoding=ENCODING) as file:
        for string in file:
            word, description = string.split('^')
            DICT_OF_WORDS[word] = description
    g.request_time = lambda: f'{(time.time() - g.request_start_time):.2f}'


def get_word() -> tuple:
    """
    Получить слово из словаря.

    Random: Если не указан инициализатор, будет использован механизм генерации, предоставляемый ОС.
    Если такой механизм недоступен, используется текущее системное время.
    """
    seed()
    word, description = random.choice(list(DICT_OF_WORDS.items()))
    return word, description


def get_shuffle_word(s: str) -> str:
    """Перемешиваем буквы в слове до тех пор пока точно не совпадут с изначальным порядком."""
    sh = list(s)
    while True:
        shuffle(sh)
        if sh != list(s):
            break
    return '  '.join(sh).upper()


@app.route('/', methods=['POST', 'GET'])
def anagramazhor():
    description = ''
    if request.method == 'POST':

        if request.form['btn'] == "С т а р т":
            session['word'], session['description'] = get_word()
            shuffle_word = get_shuffle_word(session['word'])
            return render_template('anagramazhor.html', shuffle_word=shuffle_word)

        elif request.form['btn'] == 'Проверка':
            answer = request.form['check_field'].upper()
            word = session['word'].upper()
            if answer == word:
                shuffle_word = "Правильно!"
                description = session['description']
            else:
                if sorted(word) == sorted(answer) and answer in DICT_OF_WORDS:
                    shuffle_word = 'Да!'
                    palindrome = f"А ещё это может быть: {word}  <br> {session['description']}"
                    description = f'{DICT_OF_WORDS[answer]} <br> {palindrome}'
                else:
                    shuffle_word = "Нет! " + word.upper()
                    description = session['description']
            return render_template('anagramazhor.html',
                                   shuffle_word=shuffle_word, description=description)
    else:
        return render_template('anagramazhor.html')


if __name__ == '__main__':
    app.run(debug=False)
