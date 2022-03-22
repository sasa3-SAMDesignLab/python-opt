from crypt import methods
from urllib import response
from flask import Flask, make_response, request
from jinja2 import StrictUndefined
import pandas as pd

from problem import CarGroupProblem

app = Flask(__name__)


def preprocess(request):
    students = request.files['students']
    cars = request.files['cars']
    students_df = pd.read_csv(students)
    cars_df = pd.read_csv(cars)
    return students_df, cars_df


def postprocess(solution_df):
    solution_csv = solution_df.to_csv(index=False)
    response = make_response()
    response.data = solution_csv
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/api', methods=['POST'])
def solve():
    students_df, cars_df = preprocess(request)
    solution_df = CarGroupProblem(students_df, cars_df).solve()
    response = postprocess(solution_df)
    return response
