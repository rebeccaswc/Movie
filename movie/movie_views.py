from flask import Blueprint, render_template, request
from movie_utils import get_movies_data
from movie_utils import get_20_movie_data
from movie_utils import search_movies_data
from movie_utils import search_movie_data
from movie_utils import get_cast_data
from movie_utils import discover_movies_data
from data import regions



movie_blueprint = Blueprint('movies', __name__)


@movie_blueprint.route('/')
@movie_blueprint.route('/home')
def index():
    condition_chinese = ['熱門電影', '現正熱映', '即將上映', '好評電影']
    allMovies = get_20_movie_data()
    return render_template("index.html", data=allMovies, condition_chinese = condition_chinese )

@movie_blueprint.route('/movie/<movie_type>', methods=['GET', 'POST'])
def get_movies(movie_type):
    allMovies, selected_condition, selected_number= get_movies_data(movie_type)
    return render_template('movie_list.html', movie_type=movie_type, data=allMovies, selected_condition=selected_condition, selected_number=selected_number)


@movie_blueprint.route('/movie-search/', methods=['GET', 'POST'])
def search_page():
    year_options = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"]
    allMovies, selected_condition, selected_number, selected_year, selected_region = search_movies_data(None)
    return render_template('movie_search.html', data=allMovies, selected_condition=selected_condition, selected_number=selected_number, year_options=year_options, selected_year=selected_year, selected_region=selected_region, region_options=regions)

@movie_blueprint.route('/movie-search/<string:searchTerm>', methods=['GET', 'POST'])
def search_movies(searchTerm):
    year_options = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"]
    allMovies, selected_condition, selected_number, selected_year, selected_region = search_movies_data(searchTerm=searchTerm)
    return render_template('movie_search.html', searchTerm = searchTerm, data=allMovies, selected_condition=selected_condition, selected_number=selected_number, year_options=year_options, selected_year=selected_year, selected_region=selected_region, region_options=regions)

@movie_blueprint.route('/movie-discover/', methods=['GET', 'POST'])
def discover_movies():
    year_options = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"]
    allMovies, selected_condition, selected_number, selected_genres, selected_year, selected_region = discover_movies_data()

    return render_template('movie_discover.html', data=allMovies, selected_condition=selected_condition, selected_number=selected_number, selected_genres=selected_genres, year_options=year_options, selected_year=selected_year, selected_region=selected_region, region_options=regions)

@movie_blueprint.route('/movie/readmore/<string:movieId>', methods=['GET', 'POST'])
def search_movie(movieId):
    movie = search_movie_data(movieId)
    return render_template('movie_readmore.html', movie = movie)

@movie_blueprint.route('/cast/<string:castId>', methods=['GET', 'POST'])
def get_cast(castId):
    cast = get_cast_data(castId)
    return render_template('movie_cast.html', cast = cast)
 