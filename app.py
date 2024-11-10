from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/lessons')
def lessons_json():
    from uni_lessons_scraper import get_lessons
    events = get_lessons(False)
    return events


if __name__ == "__main__":
    app.run()
