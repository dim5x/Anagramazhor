import os
import sys
import time
from random import randint, shuffle, seed
from flask_frozen import Freezer
from flask import Flask, render_template, request, g, session

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SECRET_KEY'] = 'SECRET_KEY'
freezer = Freezer(app)
LIST_OF_WORDS = []
PATH_TO_FILE = r'C:\Users\dim5x\PycharmProjects\Anagramazhor\word_rus_8_tolk_cM3.txt'
# PATH_TO_FILE = r'/home/dim5x/mysite/word_rus_8_tolk_cM3.txt'
ENCODING = 'cp1251'


@app.before_request
def before_request():
    global LIST_OF_WORDS
    g.request_start_time = time.time()
    with open(PATH_TO_FILE, 'r', encoding=ENCODING) as f:
        for string in f:
            LIST_OF_WORDS.append(string)
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


def get_word(list_of_words: list) -> tuple:
    """
    Получить слово из словаря.

    Random: Если не указан инициализатор, будет использован механизм генерации, предоставляемый ОС.
    Если такой механизм недоступен, используется текущее системное время.
    """
    seed()
    random_string = randint(0, 7732)
    word, tolk = list_of_words[random_string].split('^')
    return word, tolk


def get_shuffle_word(s: str) -> str:
    """Перемешиваем буквы в слове до тех пор пока точно не совпадут с изначальным порядком."""
    sh = list(s)
    while True:
        shuffle(sh)
        if sh != list(s):
            break
    return '  '.join(sh).upper()


# def find_answer(answer: str) -> bool:
#     """О"""
#     for string in LIST_OF_WORDS:
#         if string.split('^')[0] == answer:
#             return True
#     return False


@app.route('/', methods=['POST', 'GET'])
def anagramazhor():
    palindrom = ''
    if request.method == 'POST':

        if request.form['btn'] == "С т а р т":
            session['word'], session['tolk'] = get_word(LIST_OF_WORDS)
            shuffle_word = get_shuffle_word(session['word'])
            return render_template('anagramazhor.html', shuffle_word=shuffle_word)

        elif request.form['btn'] == 'Проверка':
            answer = request.form['check_field'].upper()
            word = session['word']
            if answer == word:
                shuffle_word = "Правильно!"
            else:
                if set(word).issubset(answer):
                    shuffle_word = 'Да!'
                    palindrom = 'А ещё это может быть: ' + word + '<br>'
                else:
                    shuffle_word = "Нет! " + word.upper()
            return render_template('anagramazhor.html', shuffle_word=shuffle_word, tolk=palindrom + session['tolk'])
    else:
        return render_template('anagramazhor.html')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=False)
