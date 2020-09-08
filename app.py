from flask import Flask
from flask import render_template, url_for, request, redirect
app = Flask(__name__)

@app.route('/api/covid', methods=["POST","OPTIONS","GET"])
def contact():
    if request.method == 'POST':
        print(request.form['submit_button'])
        if request.form['submit_button'] == 'nuevo_caso':
            print("got it!")
            return render_template('index.html')
        elif request.form['submit_button'] == 'recuperado':
            return render_template('index.html')
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    print("Starting DevOps Tools")
    app.run(host='127.0.0.1', port=8080, debug=True)
