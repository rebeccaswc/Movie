from flask import request, render_template
import urllib.request as url_request
import ssl
import json

from urllib.parse import quote

from datetime import datetime,timedelta

from config import API_KEY

def get_query(data):
    result = []
    for key in data:
        if not data[key]: continue
        result.append(f'{key}={data[key]}')
    return "&".join(result)

def get_movies_data(movie_type):
    allMovies = []
    selected_condition, splited_condition, is_order_reversed, selected_number = get_request_parameters()

    for page in range(1, (selected_number // 20) + 1):
        if movie_type == "upcoming":
            today = datetime.today()
            formatted_date = today.strftime("%Y-%m-%d")
            query = get_query({
            "primary_release_date.gte" : formatted_date,
            "sorted_by" : "primary_release_date.asc",
            "language": "zh-TW",
            "page": page,
            "api_key": API_KEY,
            })
            src = f"https://api.themoviedb.org/3/discover/movie?{query}"
        elif movie_type == "top_rated":
            today = datetime.today()
            thirty_years_ago = today - timedelta(days=30*365)
            formatted_date = thirty_years_ago.strftime("%Y-%m-%d")
            query = get_query({
            "sorted_by" : 'vote_average.desc',
            "primary_release_date.gte" : formatted_date,           
            "language": "zh-TW",
            "page": page,
            "api_key": API_KEY,
            })
            src = f"https://api.themoviedb.org/3/discover/movie?{query}"

        else :
            query = get_query({
            "page": page,
            "language": "zh-TW",
            "api_key": API_KEY,
            })
            src = f"https://api.themoviedb.org/3/movie/{movie_type}?{query}"
        context = ssl._create_unverified_context()

        try:
            with url_request.urlopen(src, context=context) as response:
                data = json.load(response)
                movies = data.get("results", [])
                allMovies.extend(movies)
        except Exception as e:
            print(f"Error fetching movies data from the API: {e}")

    if movie_type == "top_rated":
        allMovies = sorted(allMovies, key=lambda x: x['vote_average'], reverse=True)
    elif movie_type == "upcoming":
        allMovies = sorted(allMovies, key=lambda x: x['release_date'], reverse=False)
    elif selected_condition != 'none':
        allMovies = sorted(allMovies, key=lambda x: x[splited_condition], reverse=is_order_reversed)

    return allMovies, selected_condition, selected_number

def get_20_movie_data():
    popular = []
    now_playing = []
    upcoming = []
    top_rated = []
    allMovies = [popular, now_playing, upcoming, top_rated]
    conditions = ['popular', 'now_playing', 'upcoming', 'top_rated']

    for i in range(len(conditions)):
        for page in range(1, 2):
            if conditions[i] == "upcoming":
                today = datetime.today()
                formatted_date = today.strftime("%Y-%m-%d")
                query = get_query({
                "primary_release_date.gte" : formatted_date,
                "sorted_by" : "primary_release_date.asc",
                "language": "zh-TW",
                "page": page,
                "api_key": API_KEY,
                })
                src = f"https://api.themoviedb.org/3/discover/movie?{query}"
            elif conditions[i] == "top_rated":
                today = datetime.today()
                thirty_years_ago = today - timedelta(days=30*365)
                formatted_date = thirty_years_ago.strftime("%Y-%m-%d")
                query = get_query({
                "primary_release_date.gte" : formatted_date,
                "sorted_by" : 'vote_average.desc',
                "language": "zh-TW",
                "page": page,
                "api_key": API_KEY,
                })
                src = f"https://api.themoviedb.org/3/discover/movie?{query}"
            else :
                query = get_query({
                    "page": page,
                    "language": "zh-TW",
                    "api_key": API_KEY,
                })
                src = f"https://api.themoviedb.org/3/movie/{conditions[i]}?{query}"
            context = ssl._create_unverified_context()
            
            try:
                with url_request.urlopen(src, context=context) as response:
                    data = json.load(response)
                    movies = data.get("results", [])
                    if conditions[i] == "top_rated":
                        movies = sorted(movies, key=lambda x: x['vote_average'], reverse=True)
                    elif conditions[i] == "upcoming":
                        movies = sorted(movies, key=lambda x: x['release_date'], reverse=False)

                    allMovies[i].extend(movies)

            except Exception as e:
                print(f"Error fetching 20 movies data from the API: {e}")

    return allMovies

def search_movies_data(searchTerm):
    allMovies = []
    selected_condition, splited_condition, is_order_reversed, selected_number, selected_year, selected_region = get_search_request_parameters()
    print(searchTerm)

    for page in range(1, (selected_number // 20) + 1):
        encoded_search_term = quote(searchTerm, safe='')
        query = get_query({
            "query": encoded_search_term,
            "page": page,
            "api_key": API_KEY,
            "sort_by": splited_condition,
            "language": "zh-TW",
            "region": selected_region,
            "primary_release_year": selected_year,
        })
        src = f"https://api.themoviedb.org/3/search/movie?{query}"
        context = ssl._create_unverified_context()

        try:
            with url_request.urlopen(src, context=context) as response:
                data = json.load(response)
                movies = data.get("results", [])
                # 新增中文標題進movie名為alternative_title的key
                # for movie in movies:
                #     alternative_title = get_alternative_title(movie.get('id'))
                #     print(alternative_title)
                #     movie['alternative_title'] = alternative_title or movie['original_title']
                allMovies.extend(movies)
        except Exception as e:
            print(f"Error fetching search movies data from the API: {e}")

    if selected_condition != 'none':
        allMovies = sorted(allMovies, key=lambda x: x[splited_condition], reverse=is_order_reversed)

    return allMovies, selected_condition, selected_number, selected_year, selected_region

def discover_movies_data():
    allMovies = []
    selected_condition, splited_condition, is_order_reversed, selected_number, selected_genres, selected_year ,selected_region= get_discover_request_parameters()

    for page in range(1, (selected_number // 20) + 1):
        query = get_query({
            "with_genres": selected_genres,
            "primary_release_year": selected_year,
            "region":selected_region,
            "page": page,
            "api_key": API_KEY,
            "sort_by": splited_condition,
            "language": "zh-TW"
        })
        src = f"https://api.themoviedb.org/3/discover/movie?{query}"
        context = ssl._create_unverified_context()

        try:
            with url_request.urlopen(src, context=context) as response:
                data = json.load(response)
                movies = data.get("results", [])
                # 新增中文標題進movie名為alternative_title的key
                # for movie in movies:
                #     alternative_title = get_alternative_title(movie.get('id'))
                #     print(alternative_title)
                #     movie['alternative_title'] = alternative_title or movie['original_title']
                allMovies.extend(movies)
        except Exception as e:
            print(f"Error fetching search movies data from the API: {e}")


    if selected_condition != 'none':
        allMovies = sorted(allMovies, key=lambda x: x[splited_condition], reverse=is_order_reversed)

    return allMovies, selected_condition, selected_number, selected_genres, selected_year,selected_region

def search_movie_data(movieId):
    movie = None
    alternative_title = get_alternative_title(movieId)
    casts = get_casts_data(movieId)

    encoded_search_term = quote(movieId, safe='')
    src = f"https://api.themoviedb.org/3/movie/{encoded_search_term}?language=zh-TW&api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            movie = json.load(response)
            movie['alternative_title'] = alternative_title or movie['original_title']
            movie['casts'] = casts
            if not movie['overview']:
                src = f"https://api.themoviedb.org/3/movie/{encoded_search_term}?api_key={API_KEY}"
                context = ssl._create_unverified_context()
                try:
                    with url_request.urlopen(src, context=context) as response:
                        movie = json.load(response)
                        movie['alternative_title'] = alternative_title or movie['original_title']
                        movie['casts'] = casts

                except Exception as e:
                    print(f"Error fetching movie data from the API: {e}")

    except Exception as e:
        print(f"Error fetching movie data from the API: {e}")

    return movie


def get_casts_data(movieId):
    casts = None

    encoded_search_term = quote(str(movieId), safe='')
    src = f"https://api.themoviedb.org/3/movie/{encoded_search_term}/credits?api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            data = json.load(response)
            casts = data.get("cast", [])
    except Exception as e:
        print(f"Error fetching casts data from the API: {e}")

    return casts

def get_cast_data(castId):
    cast = None
    images_paths = get_cast_images_paths_data(castId)
    movie_credits = get_cast_movie_credits_data(castId)

    encoded_search_term = quote(str(castId), safe='')
    src = f"https://api.themoviedb.org/3/person/{encoded_search_term}?api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            cast = json.load(response)
            cast['images_paths'] = images_paths
            cast['movie_credits'] = movie_credits
            
    except Exception as e:
        print(f"Error fetching cast data from the API: {e}")

    return cast

def get_request_parameters():
    selected_condition = 'none'
    splited_condition = 'popularity'
    is_order_reversed = True
    selected_number = 100

    if request.method == 'POST':

        selected_condition = request.form['condition']
        selected_number = int(request.form['number'])

        if selected_condition != 'none':
            splited_condition = selected_condition.split('.')[0]
            is_order_reversed = selected_condition.split('.')[1] == 'desc'

    return selected_condition, splited_condition, is_order_reversed, selected_number

def get_search_request_parameters():
    selected_condition = 'none'
    splited_condition = 'popularity'
    is_order_reversed = True
    selected_number = 100
    selected_year = 'none'
    selected_region = 'none'

    if request.method == 'POST':
        selected_condition = request.form['condition']
        selected_number = int(request.form['number'])
        selected_year = request.form['years']
        selected_region = request.form['region']
        if selected_condition != 'none':
            splited_condition = selected_condition.split('.')[0]
            is_order_reversed = selected_condition.split('.')[1] == 'desc'

    return selected_condition, splited_condition, is_order_reversed, selected_number, selected_year, selected_region

def get_discover_request_parameters():
    selected_condition = 'none'
    splited_condition = 'popularity'
    is_order_reversed = True
    selected_number = 100
    selected_genres = None
    selected_year = 2023
    selected_region = None

    if request.method == 'POST':

        selected_condition = request .form['condition']
        selected_number = int(request.form['number'])
        selected_genres = request.form['genres']
        selected_year = request.form['years']
        selected_region = request.form['region']

        if selected_condition != 'none':
            splited_condition = selected_condition.split('.')[0]
            is_order_reversed = selected_condition.split('.')[1] == 'desc'
        

    return selected_condition, splited_condition, is_order_reversed, selected_number, selected_genres, selected_year,selected_region

def get_alternative_title(movieId):
    title = None

    encoded_search_term = quote(str(movieId), safe='')
    src = f"https://api.themoviedb.org/3/movie/{encoded_search_term}/alternative_titles?api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            titles_data = json.load(response)
            titles = titles_data.get('titles', [])

            # Check if 'TW' exists in the alternative titles
            title_info = next((t for t in titles if t.get('iso_3166_1') == 'TW'), None)
            if title_info:
                title = title_info.get('title')
            else:
                # If 'TW' doesn't exist, check for 'HK'
                title_info = next((t for t in titles if t.get('iso_3166_1') == 'HK'), None)
                if title_info:
                    title = title_info.get('title')
                else:
                    # If 'HK' doesn't exist, check for 'CN'
                    title_info = next((t for t in titles if t.get('iso_3166_1') == 'CN'), None)
                    if title_info:
                        title = title_info.get('title')
    except Exception as e:
        print(f"Error fetching alternative title data from the API: {e}")

    return title

def get_cast_movie_credits_data(castId):
    movie_credits = None

    encoded_search_term = quote(str(castId), safe='')
    src = f"https://api.themoviedb.org/3/person/{encoded_search_term}/movie_credits?api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            data = json.load(response)
            movie_credits = data.get("cast", [])
    except Exception as e:
        print(f"Error fetching cast movie credits data from the API: {e}")

    return movie_credits

def get_cast_images_paths_data(castId):
    images_paths = None

    encoded_search_term = quote(str(castId), safe='')
    src = f"https://api.themoviedb.org/3/person/{encoded_search_term}/images?api_key={API_KEY}"
    # 取得該人物的所有電影海報
    # src = f"https://api.themoviedb.org/3/person/{encoded_search_term}/tagged_images?api_key={API_KEY}"
    context = ssl._create_unverified_context()

    try:
        with url_request.urlopen(src, context=context) as response:
            data = json.load(response)
            profiles = data.get("profiles", [])
            images_paths = [profile.get("file_path") for profile in profiles]   
            # data = json.load(response)
            # results = data.get("results", [])
            # images_paths = [result.get("file_path") for result in results]   
    except Exception as e:
        print(f"Error fetching cast movie credits data from the API: {e}")

    return images_paths