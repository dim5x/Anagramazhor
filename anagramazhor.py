import os
import time
from random import randint, seed, shuffle
from flask import Flask, g, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

LIST_OF_WORDS = []
ENCODING = 'cp1251'
PATH_TO_FILE = r'C:\Users\dim5x\PycharmProjects\Anagramazhor\word_rus_8_tolk_cM3.txt'
# PATH_TO_FILE = r'/home/dim5x/mysite/word_rus_8_tolk_cM3.txt'


@app.before_request
def before_request():
    global LIST_OF_WORDS
    g.request_start_time = time.time()
    with open(PATH_TO_FILE, 'r', encoding=ENCODING) as f:
        for string in f:
            LIST_OF_WORDS.append(string)
    g.request_time = lambda: f'{(time.time() - g.request_start_time):.2f}'


def get_word(list_of_words: list) -> tuple:
    """
    Получить слово из словаря.

    Random: Если не указан инициализатор, будет использован механизм генерации, предоставляемый ОС.
    Если такой механизм недоступен, используется текущее системное время.
    """
    seed()
    random_string = randint(0, 7732)
    word, description = list_of_words[random_string].split('^')
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
    palindrome = ''
    if request.method == 'POST':

        if request.form['btn'] == "С т а р т":
            session['word'], session['description'] = get_word(LIST_OF_WORDS)
            shuffle_word = get_shuffle_word(session['word'])
            return render_template('anagramazhor.html', shuffle_word=shuffle_word)

        elif request.form['btn'] == 'Проверка':
            answer = request.form['check_field'].upper()
            word = session['word'].upper()
            if answer == word:
                shuffle_word = "Правильно!"
            else:
                if set(word).issubset(answer):
                    shuffle_word = 'Да!'
                    palindrome = 'А ещё это может быть: ' + word + '<br>'
                else:
                    shuffle_word = "Нет! " + word.upper()
            return render_template('anagramazhor.html',
                                   shuffle_word=shuffle_word, description=palindrome + session['description'])
    else:
        return render_template('anagramazhor.html')


if __name__ == '__main__':
    app.run(debug=False)
