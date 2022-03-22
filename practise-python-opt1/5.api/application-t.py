from flask import Flask, make_response, redirect, render_template, request, request_tearing_down
import pandas as pd
from problem import CarGroupProblem

app = Flask(__name__)


def check_request(request):

    students = request.files['students']
    cars = request.files['cars']

    if students.filename == '':
        return False

    if cars.filename == '':
        return False

    return True


def preprocess(request):
    students = request.files['students']
    cars = request.files['cars']

    students_df = pd.read_csv(students)
    cars_df = pd.read_csv(cars)

    return students_df, cars_df


def postprocess(solution_df):
    solution_html = solution_df.to_html(header=True, index=False)
    return solution_html


@app.route('/', methods=['GET', 'POST'])
def solve():

    if request.method == 'GET':
        return render_template('index.html', solution_html=None)

    if not check_request(request):
        return redirect(request.url)

    students_df, cars_df = preprocess(request)
    solution_df = CarGroupProblem(students_df, cars_df).solve()
    solution_html = postprocess(solution_df)
    return render_template('index.html', solution_html=solution_html)


@app.route('/download', methods=['POST'])
def download():
    solution_html = request.form.get('solution_html')
    solution_df = pd.read_html(solution_html)[0]
    solution_csv = solution_df.to_csv(index=False)
    response = make_response()
    response.data = solution_csv
    response.headers['Contens-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=solution.csv'
    return response
