from flask import request
from dao.model.movie import MovieSchema
from implemented import movie_service
from flask_restx import Namespace, Resource, fields


movie_ns = Namespace('movies', description='Movies operations')


@movie_ns.route('/')
class MoviesView(Resource):
    @movie_ns.doc('list_movies')
    def get(self):
        status = request.args.get("status")
        page = int(request.args.get("page", 0))
        filters = {
        "status": status,
        "page": page,
                  }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

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
