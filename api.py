import os

from flask import Flask
from flask_restful import reqparse, abort, Resource, Api

from utils import getTVPrograms, getCurrentDate, formatDate, convertStr2Date
from database import db_session

app = Flask(__name__)
api = Api(app)


TV_PROGRAMS = {}


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
        current_date = formatDate(getCurrentDate())
        TV_PROGRAMS = getTVPrograms(current_date)
        return TV_PROGRAMS

    def post(self):
        args = parser.parse_args()
        program_id = int(max(TV_PROGRAMS.keys())) + 1
        program_id = '{}'.format(program_id)
        TV_PROGRAMS[program_id] = {'title': args['title'], 'time': args['time']}
        return TV_PROGRAMS[program_id], 201

class ProgramListByDate(Resource):
    def get(self, program_date):
        program_date = convertStr2Date(program_date)
        print(program_date)
        TV_PROGRAMS = getTVPrograms(program_date)
        return TV_PROGRAMS



##
## Actually setup the Api resource routing here
##
api.add_resource(ProgramList, '/programs')
api.add_resource(ProgramListByDate, '/programs/<program_date>')
api.add_resource(Program, '/program/<program_id>')

@app.route("/")
def index():
    return "<h1>Welcome to NorHaak Labs</h1>"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)



