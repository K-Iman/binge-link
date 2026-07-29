# BingeLink 🎬 — Legal Movie & TV Show Discovery Platform

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.9+-336699?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![TMDB API](https://img.shields.io/badge/TMDB-v3_API-01B4E4?style=for-the-badge&logo=themoviedb&logoColor=white)](https://www.themoviedb.org/)

**BingeLink** is a modern, high-performance entertainment discovery platform designed to help users instantly find where movies, TV shows, and anime series are available for legal streaming, rent, or purchase across official providers such as **Netflix**, **Amazon Prime Video**, **Disney+**, **Crunchyroll**, and **Apple TV+**.

> **Note**: BingeLink is NOT a streaming provider or host. It is an official discovery search engine that indexes legal availability, embeds official YouTube trailers, and directs users to verified platforms.

---

## ✨ Features

- 🍿 **Embedded Official YouTube Trailers**: High-definition YouTube trailer embeds directly on detail pages with full-screen theater support.
- 🎬 **Cinematic Content Hubs**: Full-bleed ambient backdrops, cast & crew spotlights, runtime info, rating badges, and "You May Also Like" recommendation grids.
- ⚡ **Real-Time HTMX Autocomplete**: Instant search dropdown previews titles, year, and rating without page reloads.
- 🌐 **Provider Availability Matrix**: Categorized subscription, rent, and buy availability with direct official provider links and a *"Search the Web"* fallback engine.
- 🎯 **Responsive Grid System**: 6-tier responsive grid system (2 columns on mobile up to 6 columns on desktop) for seamless browsing.
- 🔌 **Dual-Mode TMDB Engine**: Operates seamlessly in offline **Mock Mode** (with rich built-in fixture datasets) or **Live API Mode** when a TMDB API key is provided.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Django 5.0 (Python 3.11+) |
| **Frontend Dynamic Engine** | HTMX 1.9 (Declarative AJAX & dynamic DOM partials) |
| **Styling & UI System** | Tailwind CSS CDN + Custom CSS Design System (`bingelink.css`) |
| **Data Provider API** | TMDB (The Movie Database API v3) + JustWatch Integration |
| **Fonts & Icons** | Plus Jakarta Sans, Inter, Heroicons |

---

## 📂 Project Architecture

```text
binge-link/
├── bingelink/            # Django Project Configuration
│   ├── settings.py       # Core settings, static files, TMDB environment variables
│   ├── urls.py           # Root URL routing
│   └── wsgi.py           # WSGI entry point
├── core/                 # Core Discovery App
│   ├── services/
│   │   └── tmdb.py       # Dual-mode TMDB API service layer & fixture mocks
│   ├── templatetags/
│   │   └── bingelink_tags.py # Custom template filters (tmdb_image, rating_class, etc.)
│   ├── urls.py           # Core routes (home, search, detail, popular, library, genre)
│   └── views.py          # View logic & HTMX partial handlers
├── static/
│   └── css/
│       └── bingelink.css # Custom design system tokens, glassmorphism, & card animations
├── templates/
│   ├── core/             # Full page templates (home, detail, search, popular, library, genre)
│   └── partials/         # HTMX fragments (media_card, search_results, library_grid)
├── manage.py             # Django CLI runner
└── README.md             # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.11+** installed on your system.
- **Git** for repository management.

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/K-Iman/binge-link.git
   cd binge-link
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install django requests
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the local development server**:
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**:
   Navigate to `http://127.0.0.1:8000/` in your web browser.

---

## 🔑 Environment Configuration

BingeLink supports dual-mode operation out of the box. If no `TMDB_API_KEY` is specified, the application automatically runs in **Mock Mode** using built-in offline movie and TV fixtures.

To connect BingeLink to live real-time TMDB data:

1. Obtain an API Key from [The Movie Database (TMDB)](https://www.themoviedb.org/settings/api).
2. Set environment variables or update `bingelink/settings.py`:

```python
# bingelink/settings.py
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "YOUR_TMDB_API_KEY_HERE")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
```

---

## ⚖️ Legal & Attributions

- **Data Attribution**: Metadata, images, backdrops, and cast info provided by [The Movie Database (TMDB)](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.
- **Provider Information**: Streaming availability data indexed via JustWatch.
- **Legal Compliance**: BingeLink strictly indexes official streaming options and does not host, upload, or distribute copyrighted video files.

---

## 📄 License

This project is licensed under the **MIT License**.