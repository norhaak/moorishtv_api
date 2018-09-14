from flask import Flask
from flask_restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

"""
TV_PROGRAMS = {
    '1': {'title': '', 'time': ''},
    '2': {'title': '', 'time': ''},
    '3': {'title': '', 'time': ''},
    '4': {'title': '', 'time': ''},
    '5': {'title': '', 'time': ''},
    '6': {'title': '', 'time': ''},
    '7': {'title': '', 'time': ''},
    '8': {'title': '', 'time': ''},
}
"""

def getTVPrograms(qty):
    programs = {}
    for i in range(1, qty):
        title = "title_{}".format(i)
        time = "time_{}".format(i)
        program = { title: time }
        programs[str(i)] = program
    return programs

TV_PROGRAMS = getTVPrograms(10)

def abort_if_program_doesnt_exist(program_id):
    if program_id not in TV_PROGRAMS:
        abort(404, message="Program {} doesn't exist.".format(program_id))

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('time')

# Program
# shows a single program item and lets you delete a program item
class Program(Resource):
    def get(self, program_id):
        abort_if_program_doesnt_exist(program_id)
        return TV_PROGRAMS[program_id]

    def delete(self, program_id):
        abort_if_program_doesnt_exist(program_id)
        del TV_PROGRAMS[program_id]
        return '', 204

    def put(self, program_id):
        args = parser.parse_args()
        title = args['title']
        time = args['time']
        program = {'title': title, 'time': time}
        program_id = len(TV_PROGRAMS.keys()) + 1
        TV_PROGRAMS[program_id] = program
        return program, 201

# ProgramList
# shows a list of all programs, and lets you POST to add new programs
class ProgramList(Resource):
    def get(self):
        return TV_PROGRAMS

    def post(self):
        args = parser.parse_args()
        program_id = int(max(TV_PROGRAMS.keys())) + 1
        program_id = '{}'.format(program_id)
        TV_PROGRAMS[program_id] = {'title': args['title'], 'time': args['time']}
        return TV_PROGRAMS[program_id], 201



##
## Actually setup the Api resource routing here
##
api.add_resource(ProgramList, '/programs')
api.add_resource(Program, '/programs/<program_id>')

"""
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
"""

if __name__ == '__main__':
    app.run(debug=True)



