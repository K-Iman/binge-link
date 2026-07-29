import urllib.parse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page
from core.services import tmdb


PROVIDER_STRIP = ["Netflix", "Prime Video", "Disney+", "Crunchyroll", "Apple TV+"]


@cache_page(60 * 15)
def home(request: HttpRequest) -> HttpResponse:
    trending_movies_data = tmdb.get_trending("movie")
    trending_tv_data = tmdb.get_trending("tv")
    anime_data = tmdb.get_anime()
    top_rated_data = tmdb.get_top_rated("movie")
    trending_today_data = tmdb.get_trending("all", time_window="day")

    trending_movies = trending_movies_data.get("results", [])[:12]
    trending_tv = trending_tv_data.get("results", [])[:12]
    anime = anime_data.get("results", [])[:12]
    top_rated_movies = top_rated_data.get("results", [])[:12]
    trending_today = trending_today_data.get("results", [])[:12]

    # Select top trending item as Hero Spotlight
    hero_item = trending_movies[0] if trending_movies else (trending_tv[0] if trending_tv else None)
    hero_backdrop_url = tmdb.image_url(hero_item.get("backdrop_path"), "original") if hero_item else None

    return render(request, "core/home.html", {
        "hero_item": hero_item,
        "hero_backdrop_url": hero_backdrop_url,
        "trending_movies": trending_movies,
        "trending_tv": trending_tv,
        "anime": anime,
        "top_rated_movies": top_rated_movies,
        "trending_today": trending_today,
        "providers_strip": PROVIDER_STRIP,
    })


def search(request: HttpRequest) -> HttpResponse:
    """Dynamic multi-search view for movies, TV shows, and anime."""
    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))
    partial_type = request.GET.get("partial", "")
    
    results = {}
    if query:
        results = tmdb.search_multi(query, page=page)

    context = {
        "results": results.get("results", []),
        "query": query,
        "total": results.get("total_results", 0),
        "total_pages": results.get("total_pages", 0),
        "page": page,
    }

    # HTMX partial: compact autocomplete dropdown list
    if request.htmx and partial_type == "dropdown":
        return render(request, "partials/search_dropdown.html", context)

    # HTMX partial: full search page results grid
    if request.htmx:
        return render(request, "partials/search_results.html", context)

    # Full page request
    return render(request, "core/search.html", context)


@cache_page(60 * 15)
def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = tmdb.get_movie(movie_id)
    providers_data = tmdb.get_watch_providers(movie_id, "movie")
    region_data = providers_data.get("results", {}).get("US", {})

    # Fetch videos & select primary trailer
    videos_data = tmdb.get_videos(movie_id, "movie")
    if not videos_data.get("results") and isinstance(movie.get("videos"), dict):
        videos_data = movie["videos"]
    trailer = tmdb.select_best_trailer(videos_data)

    # Fetch cast credits
    credits_data = tmdb.get_credits(movie_id, "movie")
    if not credits_data.get("cast") and isinstance(movie.get("credits"), dict):
        credits_data = movie["credits"]
    cast = credits_data.get("cast", [])[:10]

    # Fetch similar & recommended titles
    similar_data = tmdb.get_similar(movie_id, "movie")
    recs_data = tmdb.get_recommendations(movie_id, "movie")

    raw_items = similar_data.get("results", []) + recs_data.get("results", [])
    seen_ids = set()
    similar_items = []
    for item in raw_items:
        if item.get("id") != movie_id and item.get("id") not in seen_ids:
            seen_ids.add(item["id"])
            similar_items.append(item)
            if len(similar_items) >= 12:
                break

    # Build Google search fallback link
    title_str = movie.get("title", "")
    release_year = (movie.get("release_date") or "")[:4]
    search_query = f"{title_str} {release_year} watch online streaming".strip()
    google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

    return render(request, "core/detail.html", {
        "item": movie,
        "media_type": "movie",
        "providers": region_data,
        "justwatch_link": region_data.get("link", ""),
        "poster_url": tmdb.image_url(movie.get("poster_path"), "w500"),
        "backdrop_url": tmdb.image_url(movie.get("backdrop_path"), "original"),
        "trailer": trailer,
        "cast": cast,
        "similar_items": similar_items,
        "google_search_url": google_search_url,
    })


@cache_page(60 * 15)
def tv_detail(request: HttpRequest, tv_id: int) -> HttpResponse:
    show = tmdb.get_tv(tv_id)
    providers_data = tmdb.get_watch_providers(tv_id, "tv")
    region_data = providers_data.get("results", {}).get("US", {})

    # Fetch videos & select primary trailer
    videos_data = tmdb.get_videos(tv_id, "tv")
    if not videos_data.get("results") and isinstance(show.get("videos"), dict):
        videos_data = show["videos"]
    trailer = tmdb.select_best_trailer(videos_data)

    # Fetch cast credits
    credits_data = tmdb.get_credits(tv_id, "tv")
    if not credits_data.get("cast") and isinstance(show.get("credits"), dict):
        credits_data = show["credits"]
    cast = credits_data.get("cast", [])[:10]

    # Fetch similar & recommended titles
    similar_data = tmdb.get_similar(tv_id, "tv")
    recs_data = tmdb.get_recommendations(tv_id, "tv")

    raw_items = similar_data.get("results", []) + recs_data.get("results", [])
    seen_ids = set()
    similar_items = []
    for item in raw_items:
        if item.get("id") != tv_id and item.get("id") not in seen_ids:
            seen_ids.add(item["id"])
            similar_items.append(item)
            if len(similar_items) >= 12:
                break

    # Build Google search fallback link
    title_str = show.get("name") or show.get("title") or ""
    first_air = (show.get("first_air_date") or "")[:4]
    search_query = f"{title_str} {first_air} watch online streaming".strip()
    google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

    return render(request, "core/detail.html", {
        "item": show,
        "media_type": "tv",
        "providers": region_data,
        "justwatch_link": region_data.get("link", ""),
        "poster_url": tmdb.image_url(show.get("poster_path"), "w500"),
        "backdrop_url": tmdb.image_url(show.get("backdrop_path"), "original"),
        "trailer": trailer,
        "cast": cast,
        "similar_items": similar_items,
        "google_search_url": google_search_url,
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
