import json

from flask import Flask, render_template

with open("data.json", "r", encoding="utf-8") as f:
    f = f.read()
    data = json.loads(f)

meta = data["meta"]
promo = data["promo"]
departures = data["departures"]
tours = data["tours"]

for key in tours:
    tours[key]['url'] = key  # используем id тура, в качестве url

app = Flask(__name__)


@app.context_processor
def inject_departures():
    return dict(departures=departures)


@app.route('/')
def main():
    return render_template('index.html', promo=promo, tours=tours.values())


@app.route('/from/<direction>')
def from_direction(direction):
    depart_tour = {}  # Отфильтрованный список туров
    for tour_id in tours.keys():
        if tours[tour_id]["departure"] == direction:
            depart_tour[tour_id] = tours[tour_id]
    return render_template('direction.html', tours=depart_tour.values(), direction=direction)


@app.route('/tours/<id>')
def toursid(id):
    tour = tours.get(id)
    if tour:
        return render_template('tour.html', tours=tour)
    else:
        return page_not_found(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
