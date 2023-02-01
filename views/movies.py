from flask import request
from flask_restx import Resource, Namespace
from jsonschema.cli import parser
from flask_restx import Namespace, Resource, fields, reqparse
from dao.model.movie import MovieSchema
from implemented import movie_service
from flask_restx import Namespace, Resource, fields
from service.movie import MovieService

movie_ns = Namespace('movies', description='Movies operations')

# movie_model = movie_ns.model('Movie', {
#     'id': fields.Integer(readOnly=True, description='The movie identifier'),
#     'name': fields.String(required=True, description='The movie name'),
#     # ... other fields ...
# })

@movie_ns.route('/')
class MoviesView(Resource):
    @movie_ns.doc('list_movies')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=False)
        args = parser.parse_args()

        status = args.get('status')
        if status and status == 'new':
            return sorted(MovieService.get_movies(), key=lambda x: x['release_date'], reverse=True)
        else:
            return MovieService.get_movies()

# class MoviesView(Resource):
#     def get(self):
#         director = request.args.get("director_id")
#         genre = request.args.get("genre_id")
#         year = request.args.get("year")
#         filters = {
#             "director_id": director,
#             "genre_id": genre,
#             "year": year,
#         }
#         all_movies = movie_service.get_all(filters)
#         res = MovieSchema(many=True).dump(all_movies)
#         return res, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
