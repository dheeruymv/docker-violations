'''
Created on 19-Sep-2021

@author: deerakum
'''

import plotly.graph_objects as go


class Generator:
    def __init__(self, violations):
        self._violations = violations

    def generate_report(self):
        line_nos, violations, recommendations = self._prepare_for_report()
        fig = go.Figure(data=[
            go.Table(header=dict(
                values=['Line Number', 'Violation', 'Recommendation'],
                fill_color='lightskyblue'),
                     cells=dict(
                         values=[line_nos, violations, recommendations]))
        ])
        fig.show()

    def _prepare_for_report(self):
        line_nos, violations, recommendations = [], [], []
        for violation in self._violations:
            line_nos.append(violation['Line #'])
            violations.append(violation['Violation'])
            recommendations.append(violation['Recommendation'])
        return line_nos, violations, recommendations
