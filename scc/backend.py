from flask import Flask,render_template

app = Flask('scc')


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
