from flask import Flask, render_template, url_for
import sectiondesigner as sd

app = Flask(__name__)


@app.route('/')
def index():
    ga = sd.GA(4, 5, 9, 40, b_range=[200, 500], h_range=[200, 500])
    best, designs = ga.RunGA()
    clct = [best, designs]
    return render_template('index.html', clct=clct)


if __name__ == "__main__":
    app.run(debug=True)
