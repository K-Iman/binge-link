"""
BingeLink — TMDB Service Layer
================================
Dual-mode design:
  MOCK MODE  — TMDB_API_KEY is blank → returns hardcoded fixture data
  LIVE MODE  — TMDB_API_KEY present  → hits real TMDB endpoints

Views NEVER import `requests` directly. All external data flows through here.
"""
import logging
from typing import Optional, List, Dict, Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _is_live() -> bool:
    return bool(getattr(settings, "TMDB_API_KEY", None))


def _get(endpoint: str, params: dict = None) -> dict:
    """Make an authenticated GET request to the TMDB API."""
    base = getattr(settings, "TMDB_BASE_URL", "https://api.themoviedb.org/3")
    url = f"{base}{endpoint}"
    default_params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    if params:
        default_params.update(params)
    try:
        resp = requests.get(url, params=default_params, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        logger.error("TMDB request failed: %s", exc)
        return {}


# ─── Mock Data Fixtures ───────────────────────────────────────────────────────

MOCK_MOVIES = [
    {
        "id": 550,
        "title": "Fight Club",
        "media_type": "movie",
        "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
        "poster_path": None,
        "backdrop_path": None,
        "release_date": "1999-10-15",
        "vote_average": 8.4,
        "vote_count": 26280,
        "genre_ids": [18, 53, 35],
        "popularity": 73.5,
    },
    {
        "id": 13,
        "title": "Forrest Gump",
        "media_type": "movie",
        "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events. Along the way he has never been shy about showing his true love for his childhood sweetheart.",
        "poster_path": None,
        "backdrop_path": None,
        "release_date": "1994-06-23",
        "vote_average": 8.5,
        "vote_count": 24831,
        "genre_ids": [18, 35, 10749],
        "popularity": 80.1,
    },
    {
        "id": 278,
        "title": "The Shawshank Redemption",
        "media_type": "movie",
        "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank State Penitentiary.",
        "poster_path": None,
        "backdrop_path": None,
        "release_date": "1994-09-23",
        "vote_average": 8.7,
        "vote_count": 24000,
        "genre_ids": [18, 80],
        "popularity": 92.0,
    },
    {
        "id": 238,
        "title": "The Godfather",
        "media_type": "movie",
        "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family.",
        "poster_path": None,
        "backdrop_path": None,
        "release_date": "1972-03-14",
        "vote_average": 8.7,
        "vote_count": 18900,
        "genre_ids": [18, 80],
        "popularity": 88.3,
    },
    {
        "id": 157336,
        "title": "Interstellar",
        "media_type": "movie",
        "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel.",
        "poster_path": None,
        "backdrop_path": None,
        "release_date": "2014-11-05",
        "vote_average": 8.4,
        "vote_count": 32000,
        "genre_ids": [12, 18, 878],
        "popularity": 110.0,
    },
]

MOCK_TV = [
    {
        "id": 1396,
        "name": "Breaking Bad",
        "title": "Breaking Bad",
        "media_type": "tv",
        "overview": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2008-01-20",
        "vote_average": 8.9,
        "vote_count": 12900,
        "genre_ids": [18, 80],
        "popularity": 120.0,
    },
    {
        "id": 1399,
        "name": "Game of Thrones",
        "title": "Game of Thrones",
        "media_type": "tv",
        "overview": "Seven noble families fight for control of the mythical land of Westeros.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2011-04-17",
        "vote_average": 8.4,
        "vote_count": 21500,
        "genre_ids": [10765, 18, 10759],
        "popularity": 150.0,
    },
    {
        "id": 66732,
        "name": "Stranger Things",
        "title": "Stranger Things",
        "media_type": "tv",
        "overview": "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2016-07-15",
        "vote_average": 8.6,
        "vote_count": 14800,
        "genre_ids": [10765, 9648, 18],
        "popularity": 145.0,
    },
    {
        "id": 1668,
        "name": "Friends",
        "title": "Friends",
        "media_type": "tv",
        "overview": "Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "1994-09-22",
        "vote_average": 8.4,
        "vote_count": 7200,
        "genre_ids": [35],
        "popularity": 68.0,
    },
    {
        "id": 60735,
        "name": "The Flash",
        "title": "The Flash",
        "media_type": "tv",
        "overview": "After a particle accelerator causes a freak storm, CSI Investigator Barry Allen is struck by lightning and falls into a coma.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2014-10-07",
        "vote_average": 7.7,
        "vote_count": 5400,
        "genre_ids": [10765, 18, 10759],
        "popularity": 82.0,
    },
]

MOCK_ANIME = [
    {
        "id": 31911,
        "name": "Fullmetal Alchemist: Brotherhood",
        "title": "Fullmetal Alchemist: Brotherhood",
        "media_type": "tv",
        "overview": "Two brothers use alchemy to try to resurrect their deceased mother, only to lose parts of themselves in the attempt.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2009-04-05",
        "vote_average": 9.1,
        "vote_count": 7300,
        "genre_ids": [16, 10765, 18, 10759],
        "popularity": 95.0,
    },
    {
        "id": 46260,
        "name": "Attack on Titan",
        "title": "Attack on Titan",
        "media_type": "tv",
        "overview": "After his hometown is destroyed and his mother is killed, young Eren Yeager vows to cleanse the earth of the giant humanoid Titans.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2013-04-07",
        "vote_average": 8.7,
        "vote_count": 9800,
        "genre_ids": [16, 10765, 10759],
        "popularity": 170.0,
    },
    {
        "id": 37854,
        "name": "One Piece",
        "title": "One Piece",
        "media_type": "tv",
        "overview": "Years ago, the fearsome Pirate King, Gol D. Roger was executed leaving a huge pile of treasure and the famous \"One Piece\" behind.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "1999-10-20",
        "vote_average": 8.7,
        "vote_count": 4100,
        "genre_ids": [16, 10765, 10759],
        "popularity": 130.0,
    },
    {
        "id": 65930,
        "name": "My Hero Academia",
        "title": "My Hero Academia",
        "media_type": "tv",
        "overview": "A superhero-loving boy without any powers is determined to enroll in a prestigious hero academy.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2016-04-03",
        "vote_average": 8.4,
        "vote_count": 5300,
        "genre_ids": [16, 10765, 10759],
        "popularity": 110.0,
    },
    {
        "id": 85937,
        "name": "Demon Slayer: Kimetsu no Yaiba",
        "title": "Demon Slayer",
        "media_type": "tv",
        "overview": "A family is attacked by demons and only two members survive — Tanjiro and his sister Nezuko, who is turning into a demon slowly.",
        "poster_path": None,
        "backdrop_path": None,
        "first_air_date": "2019-04-06",
        "vote_average": 8.7,
        "vote_count": 6800,
        "genre_ids": [16, 10765, 10759],
        "popularity": 160.0,
    },
]

MOCK_PROVIDERS = {
    "results": {
        "US": {
            "link": "https://www.justwatch.com/",
            "flatrate": [
                {
                    "provider_id": 8,
                    "provider_name": "Netflix",
                    "logo_path": "/t2yyOv40HZeVlLjYsCsPHnWLk4W.jpg",
                    "display_priority": 1,
                },
                {
                    "provider_id": 9,
                    "provider_name": "Amazon Prime Video",
                    "logo_path": "/emthp39XA2YScoYL1p0sdbAH2WA.jpg",
                    "display_priority": 2,
                },
                {
                    "provider_id": 337,
                    "provider_name": "Disney Plus",
                    "logo_path": "/7rwgEs15tFwyR9NPQ5vpzxTj19Q.jpg",
                    "display_priority": 3,
                },
            ],
        }
    }
}


def _mock_detail(item: dict, media_type: str) -> dict:
    """Enrich a mock result item with detail-level fields."""
    return {
        **item,
        "media_type": media_type,
        "tagline": "A classic you should not miss.",
        "runtime": 120 if media_type == "movie" else None,
        "number_of_seasons": None if media_type == "movie" else 3,
        "number_of_episodes": None if media_type == "movie" else 30,
        "genres": [{"id": gid, "name": _genre_name(gid)} for gid in item.get("genre_ids", [])],
        "production_companies": [{"name": "Fictional Studios", "logo_path": None}],
        "spoken_languages": [{"english_name": "English"}],
        "status": "Released" if media_type == "movie" else "Ended",
        "homepage": "",
    }


def _genre_name(gid: int) -> str:
    genres = {
        28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
        80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
        14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
        9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
        10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
        10759: "Action & Adventure", 10762: "Kids", 10763: "News",
        10764: "Reality", 10765: "Sci-Fi & Fantasy", 10766: "Soap",
        10767: "Talk", 10768: "War & Politics",
    }
    return genres.get(gid, "Unknown")


# ─── Public API ───────────────────────────────────────────────────────────────

def search_multi(query: str, page: int = 1) -> dict:
    """Search movies + TV shows. Returns TMDB-shaped response dict."""
    if not query.strip():
        return {"results": [], "total_results": 0, "total_pages": 0, "page": 1}

    if not _is_live():
        q = query.lower()
        all_items = MOCK_MOVIES + MOCK_TV + MOCK_ANIME
        results = [
            item for item in all_items
            if q in item.get("title", "").lower() or q in item.get("name", "").lower()
        ]
        if not results:
            results = all_items[:6]
        return {"results": results, "total_results": len(results), "total_pages": 1, "page": 1}

    data = _get("/search/multi", {"query": query, "page": page, "include_adult": "false"})
    data["results"] = [
        r for r in data.get("results", [])
        if r.get("media_type") in ("movie", "tv")
    ]
    return data


def get_movie(movie_id: int) -> dict:
    """Fetch full movie details."""
    if not _is_live():
        match = next((m for m in MOCK_MOVIES if m["id"] == movie_id), MOCK_MOVIES[0])
        return _mock_detail(match, "movie")
    return _get(f"/movie/{movie_id}", {"append_to_response": "credits,videos"})


def get_tv(tv_id: int) -> dict:
    """Fetch full TV show / anime details."""
    if not _is_live():
        all_tv = MOCK_TV + MOCK_ANIME
        match = next((t for t in all_tv if t["id"] == tv_id), MOCK_TV[0])
        return _mock_detail(match, "tv")
    return _get(f"/tv/{tv_id}", {"append_to_response": "credits,videos"})


def get_videos(content_id: int, media_type: str = "movie") -> dict:
    """Fetch video trailers for a movie or TV show."""
    if not _is_live():
        return {
            "results": [
                {
                    "id": "mock_trailer_1",
                    "iso_639_1": "en",
                    "iso_3166_1": "US",
                    "name": "Official Trailer",
                    "key": "dQw4w9WgXcQ",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Trailer",
                    "official": True,
                }
            ]
        }
    return _get(f"/{media_type}/{content_id}/videos")


def select_best_trailer(videos_data: dict) -> Optional[dict]:
    """Select the best YouTube trailer from a TMDB videos response dict."""
    results = videos_data.get("results", [])
    if not results:
        return None

    # Filter for YouTube videos
    yt_videos = [v for v in results if v.get("site") == "YouTube"]
    if not yt_videos:
        return None

    # 1. Official Trailers
    official_trailers = [
        v for v in yt_videos
        if v.get("type") == "Trailer" and (v.get("official") or "official" in v.get("name", "").lower())
    ]
    if official_trailers:
        return official_trailers[0]

    # 2. Any Trailer
    trailers = [v for v in yt_videos if v.get("type") == "Trailer"]
    if trailers:
        return trailers[0]

    # 3. Teasers or fallback
    teasers = [v for v in yt_videos if v.get("type") == "Teaser"]
    if teasers:
        return teasers[0]

    return yt_videos[0]


def get_credits(content_id: int, media_type: str = "movie") -> dict:
    """Fetch credits (cast & crew) for a movie or TV show."""
    if not _is_live():
        return {
            "cast": [
                {"id": 1, "name": "Edward Norton", "character": "The Narrator", "profile_path": None},
                {"id": 2, "name": "Brad Pitt", "character": "Tyler Durden", "profile_path": None},
                {"id": 3, "name": "Helena Bonham Carter", "character": "Marla Singer", "profile_path": None},
                {"id": 4, "name": "Meat Loaf", "character": "Robert 'Bob' Paulson", "profile_path": None},
                {"id": 5, "name": "Jared Leto", "character": "Angel Face", "profile_path": None},
            ]
        }
    return _get(f"/{media_type}/{content_id}/credits")


def get_similar(content_id: int, media_type: str = "movie", page: int = 1) -> dict:
    """Fetch similar titles."""
    if not _is_live():
        return {"results": MOCK_MOVIES if media_type == "movie" else MOCK_TV, "page": 1, "total_pages": 1}
    return _get(f"/{media_type}/{content_id}/similar", {"page": page})


def get_recommendations(content_id: int, media_type: str = "movie", page: int = 1) -> dict:
    """Fetch recommended titles."""
    if not _is_live():
        return {"results": MOCK_MOVIES if media_type == "movie" else MOCK_TV, "page": 1, "total_pages": 1}
    return _get(f"/{media_type}/{content_id}/recommendations", {"page": page})


def get_top_rated(media_type: str = "movie", page: int = 1) -> dict:
    """Fetch top rated movies or TV shows."""
    if not _is_live():
        return {"results": MOCK_MOVIES if media_type == "movie" else MOCK_TV, "page": 1, "total_pages": 1}
    return _get(f"/{media_type}/top_rated", {"page": page})


def get_watch_providers(content_id: int, media_type: str = "region_US", region: str = "US") -> dict:
    """Returns streaming provider data for given content."""
    if not _is_live():
        return MOCK_PROVIDERS

    data = _get(f"/{media_type}/{content_id}/watch/providers")
    return data


def get_trending(media_type: str = "all", time_window: str = "week", page: int = 1) -> dict:
    """Fetch trending content. media_type: 'all' | 'movie' | 'tv'"""
    if not _is_live():
        if media_type == "movie":
            return {"results": MOCK_MOVIES, "page": 1, "total_pages": 1}
        elif media_type == "tv":
            return {"results": MOCK_TV, "page": 1, "total_pages": 1}
        else:
            return {"results": MOCK_MOVIES + MOCK_TV, "page": 1, "total_pages": 1}

    return _get(f"/trending/{media_type}/{time_window}", {"page": page})


def get_popular(media_type: str = "movie", page: int = 1) -> dict:
    """Fetch popular movies or TV shows."""
    if not _is_live():
        if media_type == "tv":
            return {"results": MOCK_TV, "page": 1, "total_pages": 1}
        return {"results": MOCK_MOVIES, "page": 1, "total_pages": 1}

    return _get(f"/{media_type}/popular", {"page": page})


def get_anime(page: int = 1) -> dict:
    """Fetch anime (TV genre 16 = Animation, filtered to Japanese origin)."""
    if not _is_live():
        return {"results": MOCK_ANIME, "page": 1, "total_pages": 1}

    return _get(
        "/discover/tv",
        {
            "with_genres": "16",
            "with_original_language": "ja",
            "sort_by": "popularity.desc",
            "page": page,
        },
    )


def get_genres(media_type: str = "movie") -> list:
    """Return genre list for movies or TV."""
    if not _is_live():
        return [
            {"id": 28, "name": "Action"}, {"id": 35, "name": "Comedy"},
            {"id": 18, "name": "Drama"}, {"id": 878, "name": "Science Fiction"},
            {"id": 27, "name": "Horror"}, {"id": 10749, "name": "Romance"},
            {"id": 16, "name": "Animation"}, {"id": 80, "name": "Crime"},
            {"id": 14, "name": "Fantasy"}, {"id": 9648, "name": "Mystery"},
        ]
    data = _get(f"/genre/{media_type}/list")
    return data.get("genres", [])


def get_by_genre(genre_id: int, media_type: str = "movie", page: int = 1) -> dict:
    """Discover content by genre."""
    if not _is_live():
        all_items = MOCK_MOVIES if media_type == "movie" else MOCK_TV + MOCK_ANIME
        filtered = [i for i in all_items if genre_id in i.get("genre_ids", [])]
        return {"results": filtered or all_items, "page": 1, "total_pages": 1}

    return _get(
        f"/discover/{media_type}",
        {"with_genres": genre_id, "sort_by": "popularity.desc", "page": page},
    )


def get_library_items(sort: str = "popularity", year: str = "", letter: str = "", media_type: str = "movie") -> dict:
    """Fetch and filter library items."""
    sort_map = {
        "popularity": "popularity.desc",
        "rating": "vote_average.desc",
        "release_date": "first_air_date.desc" if media_type == "tv" else "primary_release_date.desc",
    }
    tmdb_sort = sort_map.get(sort, "popularity.desc")

    if not _is_live():
        if media_type == "movie":
            base_items = MOCK_MOVIES
        elif media_type == "anime":
            base_items = MOCK_ANIME
        else:
            base_items = MOCK_TV

        if sort == "rating":
            base_items = sorted(base_items, key=lambda x: x.get("vote_average", 0), reverse=True)
        elif sort == "release_date":
            date_key = "first_air_date" if media_type in ("tv", "anime") else "release_date"
            base_items = sorted(base_items, key=lambda x: x.get(date_key, ""), reverse=True)
        else:
            base_items = sorted(base_items, key=lambda x: x.get("popularity", 0), reverse=True)

        results = []
        for item in base_items:
            title = item.get("title") or item.get("name") or ""
            date_val = item.get("release_date") or item.get("first_air_date") or ""
            
            if year and year not in date_val:
                continue
                
            if letter:
                if letter.upper() == "#":
                    if title and not title[0].isalpha():
                        pass
                    else:
                        continue
                elif title and title[0].upper() != letter.upper():
                    continue
                    
            results.append(item)
            
        return {"results": results, "page": 1, "total_pages": 1}

    params = {"sort_by": tmdb_sort, "page": 1}
    api_type = "tv" if media_type in ("tv", "anime") else "movie"
    if media_type == "anime":
        params["with_genres"] = "16"
        params["with_original_language"] = "ja"
        
    date_param = "first_air_date_year" if api_type == "tv" else "primary_release_year"
    if year:
        params[date_param] = year

    data = _get(f"/discover/{api_type}", params)
    
    if letter and data.get("results"):
        filtered = []
        for item in data.get("results"):
            title = item.get("title") or item.get("name") or ""
            if letter.upper() == "#":
                if title and not title[0].isalpha():
                    filtered.append(item)
            elif title and title[0].upper() == letter.upper():
                filtered.append(item)
        data["results"] = filtered

    return data


def image_url(path: Optional[str], size: str = "w500") -> Optional[str]:
    """Build a full TMDB image URL. Returns None for missing paths."""
    if not path:
        return None
    base = getattr(settings, "TMDB_IMAGE_BASE_URL", "https://image.tmdb.org/t/p")
    return f"{base}/{size}{path}"
