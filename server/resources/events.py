from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.Event import Event
from server.helpers import response
from server import cur, conn

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title must be a string')
parser.add_argument('description', type=str, help='Description must be a string')
parser.add_argument('max_participant', type=int, help='Max participant must be a number')


class CreateEvent(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']
        user_id = get_jwt_identity()['id']

        event = Event(_title=title, _description=description,
            _max_participant=max_participant, _started_at=started_at, _user_id=user_id)
        result = event.save()

        if result is False:
            return response({
                'errors': event.getErrors()
            }, 401)

        return response({
            'message': 'Event successfully created!'
        })


class UpdateEvent(Resource):
    @jwt_required
    def post(self, event_id):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']
        user_id = get_jwt_identity()['id']

        event = Event(_id=event_id, _title=title, _description=description,
            _max_participant=max_participant, _started_at=started_at, _user_id=user_id)
        result = event.update()

        if result is False:
            return response({
                'errors': event.getErrors()
            }, 401)
        return response({
            'message': 'Event successfully updated!'
        })


class DeleteEvent(Resource):
    @jwt_required
    def post(self, event_id):
        event = Event(_id=event_id, _user_id=get_jwt_identity()['id'])
        event.delete()

        return response({
            'message': "Comment deleted successfully"
        })


class GetEvent(Resource):
    def get(self, event_id):
        event = Event().get(id=event_id)
        return response({
            'Event': event
        })


class GetEvents(Resource):
    def get(self):
        events = Event().all()
        return response({
            'events': events
        })

