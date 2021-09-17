from random import randint, shuffle, seed
from flask import Flask, render_template, request, g, make_response, session
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


# word = ''
# tolk = ''


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


def get_word():
    """ Если не указан инициализатор, будет использован механизм генерации, предоставляемый ОС.
    Если такой механизм недоступен, используется текущее системное время."""
    seed()
    r = randint(0, 7732)
    count = 0
    # with open(r'C:\Users\dim5x\PycharmProjects\Anagramazhor\word_rus_8_tolk_cM3.txt', 'r', encoding='cp1251') as f:
    # with open('word_rus_8_tolk_c.txt', 'r', encoding='cp1251') as f:
    with open(r'/home/dim5x/mysite/word_rus_8_tolk_cM3.txt', 'r', encoding='cp1251') as f:
        for row in f:
            count += 1
            if r == count:
                word, tolk = row.split('^')

    return word.upper().strip(), tolk


def get_shuffle_word(s):
    sh = list(s)
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
            shuffle_word = get_shuffle_word(word)
            session['word'] = word
            # res = make_response(render_template('index.html', shuffle_word=shuffle_word, word=word))
            # res.set_cookie(key='word', value=word)
            return render_template('anagramazhor.html', shuffle_word=shuffle_word, word=word)

        elif request.form['btn'] == 'Проверка':
            answer = request.form['check_field'].upper()
            word = session['word']
            if answer == word:
                shuffle_word = "Правильно!"
            else:
                shuffle_word = "Нет! " + word

            return render_template('anagramazhor.html', shuffle_word=shuffle_word, tolk=tolk)
    else:

        return render_template('anagramazhor.html')


if __name__ == '__main__':
    app.run(debug=False)
