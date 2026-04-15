from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page
from core.services import tmdb


PROVIDER_STRIP = ["Netflix", "Prime Video", "Disney+", "Crunchyroll", "Apple TV+"]


@cache_page(60 * 15)
def home(request: HttpRequest) -> HttpResponse:
    trending_movies = tmdb.get_trending("movie")
    trending_tv = tmdb.get_trending("tv")
    anime = tmdb.get_anime()
    return render(request, "core/home.html", {
        "trending_movies": trending_movies.get("results", [])[:10],
        "trending_tv": trending_tv.get("results", [])[:10],
        "anime": anime.get("results", [])[:10],
        "providers_strip": PROVIDER_STRIP,
    })


@cache_page(60 * 5)
def search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))
    results = {}
    if query:
        results = tmdb.search_multi(query, page=page)

    # HTMX partial: return only the results grid fragment
    if request.htmx:
        return render(request, "partials/search_results.html", {
            "results": results.get("results", []),
            "query": query,
            "total": results.get("total_results", 0),
        })

    return render(request, "core/search.html", {
        "results": results.get("results", []),
        "query": query,
        "total": results.get("total_results", 0),
        "total_pages": results.get("total_pages", 0),
        "page": page,
    })


@cache_page(60 * 15)
def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = tmdb.get_movie(movie_id)
    providers_data = tmdb.get_watch_providers(movie_id, "movie")
    region_data = providers_data.get("results", {}).get("US", {})
    return render(request, "core/detail.html", {
        "item": movie,
        "media_type": "movie",
        "providers": region_data,
        "justwatch_link": region_data.get("link", ""),
        "poster_url": tmdb.image_url(movie.get("poster_path"), "w500"),
        "backdrop_url": tmdb.image_url(movie.get("backdrop_path"), "original"),
    })


@cache_page(60 * 15)
def tv_detail(request: HttpRequest, tv_id: int) -> HttpResponse:
    show = tmdb.get_tv(tv_id)
    providers_data = tmdb.get_watch_providers(tv_id, "tv")
    region_data = providers_data.get("results", {}).get("US", {})
    return render(request, "core/detail.html", {
        "item": show,
        "media_type": "tv",
        "providers": region_data,
        "justwatch_link": region_data.get("link", ""),
        "poster_url": tmdb.image_url(show.get("poster_path"), "w500"),
        "backdrop_url": tmdb.image_url(show.get("backdrop_path"), "original"),
    })


@cache_page(60 * 15)
def popular(request: HttpRequest) -> HttpResponse:
    media_type = request.GET.get("type", "movie")
    page = int(request.GET.get("page", 1))
    data = tmdb.get_popular(media_type, page=page)
    genres = tmdb.get_genres(media_type)

    if request.htmx:
        return render(request, "partials/card_grid.html", {
            "items": data.get("results", []),
            "media_type": media_type,
        })

    return render(request, "core/popular.html", {
        "items": data.get("results", []),
        "media_type": media_type,
        "genres": genres,
        "page": page,
        "total_pages": data.get("total_pages", 1),
    })


@cache_page(60 * 15)
def browse_genre(request: HttpRequest, genre_id: int) -> HttpResponse:
    media_type = request.GET.get("type", "movie")
    page = int(request.GET.get("page", 1))
    data = tmdb.get_by_genre(genre_id, media_type, page=page)
    genres = tmdb.get_genres(media_type)

    return render(request, "core/genre.html", {
        "items": data.get("results", []),
        "media_type": media_type,
        "genres": genres,
        "genre_id": genre_id,
        "page": page,
        "total_pages": data.get("total_pages", 1),
    })

@cache_page(60 * 5)
def library(request: HttpRequest) -> HttpResponse:
    sort = request.GET.get("sort", "popularity")
    year = request.GET.get("year", "")
    letter = request.GET.get("letter", "")
    media_type = request.GET.get("type", "movie")
    
    data = tmdb.get_library_items(sort=sort, year=year, letter=letter, media_type=media_type)
    
    context = {
        "items": data.get("results", []),
        "sort": sort,
        "year": year,
        "letter": letter,
        "type": media_type,
    }
    
    if request.htmx:
        return render(request, "partials/library_grid.html", context)
        
    return render(request, "core/library.html", context)

