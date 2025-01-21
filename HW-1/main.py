
# Задание 1.

# Найдите ошибку в коде:
# from flask import Flask
# app = Flask(__name__)
# @app.route('')
# def home():
#  return 'Hello, World!'
# if __name__ == '__main__':
#  app.run()

# Ответ: должно бить так @app.route('/')


# Задание 2.

from flask import Flask

app = Flask(__name__)

@app.route('/')
def simple_hallo():
    return "Hello, Flask!"

@app.route('/user/<name>')
def hallo_name(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)