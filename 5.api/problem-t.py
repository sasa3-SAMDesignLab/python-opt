import pandas as pd
import pulp


class CarGroupProblem():
    def __init__(self, students_df, cars_df, name='ClubCarProblem'):
        self.students_df = students_df
        self.cars_df = cars_df
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        prob = pulp.LpProblem(self.name, pulp.LpMinimize)

        S = self.students_df['student_id'].to_list()
        C = self.cars_df['car_id'].to_list()
        G = [1, 2, 3, 4]
        SC = [(s, c) for s in S for c in C]
        S_license = self.students_df[self.students_df['license']
                                     == 1]['student_id']
        S_g = {
            g: self.students_df[self.students_df['grade'] == g]['student_id'] for g in G}
        S_male = self.students_df[self.students_df['gender']
                                  == 0]['student_id']
        S_female = self.students_df[self.students_df['gender']
                                    == 1]['student_id']

        U = self.cars_df['capacity'].to_list()

        x = pulp.LpVariable.dicts('x', SC, cat='Binary')

        for s in S:
            prob += pulp.lpSum([x[s, c] for c in C]) == 1

        for c in C:
            prob += pulp.lpSum([x[s, c] for s in S]) <= U[c]

        for c in C:
            prob += pulp.lpSum([x[s, c] for s in S_license]) >= 1

        for c in C:
            for g in G:
                prob += pulp.lpSum([x[s, c] for s in S_g[g]]) >= 1

        for c in C:
            prob += pulp.lpSum([x[s, c] for s in S_male]) >= 1

        for c in C:
            prob += pulp.lpSum([x[s, c] for s in S_female]) >= 1

        return {'prob': prob, 'variable': {'x': x}, 'list': {'S': S, 'C': C}}

    def solve(self):
        status = self.prob['prob'].solve()

        x = self.prob['variable']['x']
        S = self.prob['list']['S']
        C = self.prob['list']['C']
        car2students = {c: [s for s in S if x[s, c].value() == 1] for c in C}
        student2car = {s: c for c, ss in car2students.items() for s in ss}
        solution_df = pd.DataFrame(list(student2car.items()), columns=[
                                   'student_id', 'car_id'])

        return solution_df


if __name__ == '__main__':
    students_df = pd.read_csv('resource/students.csv')
    cars_df = pd.read_csv('resource/cars.csv')

    prob = CarGroupProblem(students_df, cars_df)

    solution_df = prob.solve()

    print('Solution: \n', solution_df)
