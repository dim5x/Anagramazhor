from random import randint, shuffle, seed
from flask import Flask, render_template, request, g
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

word = ''
tolk = ''


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


def get_word():
    """ Если не указан инициализатор, будет использован механизм генерации, предоставляемый ОС.
    Если такой механизм недоступен, используется текущее системное время."""
    seed()
    r = randint(1, 7732)
    count = 0
    with open(r'C:\Users\dim5x\PycharmProjects\untitled1\word_rus_8_tolk.txt', 'r', encoding='cp1251') as f:
        # with open(r'/home/dim5x/mysite/word_rus_8_tolk.txt', 'r', encoding='cp1251') as f:
        for row in f:
            count += 1
            if r == count:
                word, tolk = row.split('***')

    return word.upper().strip(), tolk


def get_sh_word(s):
    sh = list(s.strip())
    while True:
        shuffle(sh)
        if sh != list(s):
            break

    return '  '.join(sh).upper()


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    global word
    global tolk
    if request.method == 'POST':
        if request.form['btn'] == "С т а р т":
            word, tolk = get_word()
            if 'искомое слово отсутствует' in tolk:
                tolk = ''
            shuffle_word = get_sh_word(word)

            return render_template('index.html', word=word, shuffle_word=shuffle_word)

        elif request.form['btn'] == 'Проверка':
            answer = request.form['check_field'].upper()
            if answer == word:
                shuffle_word = "Правильно!"
            else:
                shuffle_word = "Нет! " + word

            return render_template('index.html', shuffle_word=shuffle_word, tolk=tolk)
    else:

        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
