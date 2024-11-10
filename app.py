from flask import Flask
app = Flask(__name__)

@app.route('/lessons')
def hello_world():
    from uni_lessons_scraper import get_lessons
    events = get_lessons(False)
    return events


if __name__ == "__main__":
    app.run()
