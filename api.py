import os

from flask import Flask
from flask_restful import reqparse, abort, Resource, Api

from utils import getTVPrograms, getCurrentDate

app = Flask(__name__)
api = Api(app)

LAST_UPDATE = None
TV_PROGRAMS = getTVPrograms(LAST_UPDATE)
LAST_UPDATE = getCurrentDate()

def abort_if_program_doesnt_exist(program_id):
    if int(program_id) > len(TV_PROGRAMS["programs"]):
        abort(404, message="Program {} doesn't exist.".format(program_id))

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('time')

# Program
# shows a single program item and lets you delete a program item
class Program(Resource):
    def get(self, program_id):
        abort_if_program_doesnt_exist(program_id)
        return TV_PROGRAMS["programs"][int(program_id)]

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

class HelloWorld(Resource):
    def get(self):
        return "<h1>Welcome to NorHaak Labs</h1>"

api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)



