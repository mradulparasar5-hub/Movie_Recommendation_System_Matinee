import html

import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Matinee | Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (Matinee design system)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root{
  --bg:#0B1424; --surface:#13203A; --surface-2:#1B2B49; --ink:#EAF0F8; --muted:#9AA9C2;
  --line:#26385A; --accent:#FF6B86; --accent-ink:#1A0A10; --match:#4FE0C8;
  --display:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;
  --body:"DM Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
}

/* ---------- base ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"]{
  background:var(--bg) !important; color:var(--ink); font-family:var(--body);
}
[data-testid="stHeader"]{ background:transparent !important; }
#MainMenu, footer{ visibility:hidden; }
.block-container{ padding-top:1.2rem; padding-bottom:3rem; max-width:1320px; }
p, li, label, span, div{ font-family:var(--body); }
h1,h2,h3,h4,h5{ font-family:var(--display) !important; color:var(--ink) !important; letter-spacing:-.01em; }
hr{ border-color:var(--line) !important; }
a{ color:var(--accent); }

/* ---------- brand bar ---------- */
.brandbar{ display:flex; align-items:center; gap:12px; padding:6px 0 18px; border-bottom:1px solid var(--line); margin-bottom:22px; }
.brandbar svg{ color:var(--accent); flex:none; }
.brand{ font-family:var(--display); font-weight:800; font-size:1.55rem; letter-spacing:-.02em; color:var(--ink); }
.tag{ margin-left:auto; color:var(--muted); font-size:.92rem; }

/* ---------- hero (home) ---------- */
.hero-title{ font-family:var(--display); font-weight:800; font-size:clamp(2rem,4.4vw,3.4rem); line-height:1.05; letter-spacing:-.03em; margin:6px 0 10px; color:var(--ink); }
.hero-sub{ color:var(--muted); font-size:1.05rem; max-width:60ch; margin:0 0 18px; }

/* ---------- section titles ---------- */
.sec{ display:flex; align-items:baseline; justify-content:space-between; gap:12px; margin:26px 0 14px; }
.sec h3{ margin:0 !important; font-size:1.5rem !important; }
.sec p{ margin:0; color:var(--muted); font-size:.92rem; }
.small-muted{ color:var(--muted); font-size:.92rem; }

/* ---------- inputs ---------- */
.stTextInput label p, .stSelectbox label p, .stSlider label p{ color:var(--muted) !important; font-weight:500; }
.stTextInput [data-baseweb="input"], .stTextInput [data-baseweb="base-input"]{
  background:var(--surface) !important; border-radius:999px !important; border:1px solid var(--line) !important;
}
.stTextInput input{ color:var(--ink) !important; padding:0.7rem 1.1rem !important; font-family:var(--body) !important; }
.stTextInput input::placeholder{ color:var(--muted) !important; opacity:1; }
.stTextInput [data-baseweb="input"]:focus-within{ border-color:var(--accent) !important; box-shadow:0 0 0 1px var(--accent); }
.stSelectbox [data-baseweb="select"] > div{
  background:var(--surface) !important; border:1px solid var(--line) !important; border-radius:14px !important; color:var(--ink) !important;
}
.stSelectbox [data-baseweb="select"] *{ color:var(--ink) !important; }
[data-baseweb="popover"] ul, [data-baseweb="menu"]{ background:var(--surface) !important; border:1px solid var(--line); border-radius:12px; }
[data-baseweb="popover"] li{ color:var(--ink) !important; background:transparent !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"]{ background:var(--surface-2) !important; }
.stSlider [role="slider"]{ background:var(--accent) !important; box-shadow:none !important; }
.stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"],
.stSlider [data-testid="stThumbValue"]{ color:var(--muted) !important; }

/* ---------- buttons ---------- */
.stButton > button{
  width:100%; border-radius:999px; border:1px solid var(--line); background:var(--surface); color:var(--ink);
  font-family:var(--body); font-weight:700; padding:.45rem 1rem; transition:background .15s, border-color .15s;
}
.stButton > button:hover{ background:var(--surface-2); border-color:var(--accent); color:var(--ink); }
.stButton > button:focus-visible{ outline:3px solid var(--accent); outline-offset:2px; }
.stButton > button:active{ background:var(--accent); color:var(--accent-ink); border-color:var(--accent); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{ background:var(--surface) !important; border-right:1px solid var(--line); }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3{ font-size:1.15rem !important; }

/* ---------- posters + cards ---------- */
[data-testid="stImage"] img{ border-radius:14px; box-shadow:0 10px 26px rgba(0,0,0,.4); transition:transform .2s; }
[data-testid="stImage"] img:hover{ transform:translateY(-3px); }
.movie-title{
  font-family:var(--display); font-weight:700; font-size:.98rem; line-height:1.2rem; height:2.4rem;
  overflow:hidden; color:var(--ink); margin:2px 0 14px;
}
[data-testid="stVerticalBlockBorderWrapper"]{ background:var(--surface); border:1px solid var(--line) !important; border-radius:20px; }

/* ---------- details ---------- */
.detail-title{ font-family:var(--display); font-weight:800; font-size:clamp(2rem,4vw,3.2rem); line-height:1.04; letter-spacing:-.03em; margin:0 0 10px; color:var(--ink); }
.pills{ display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 6px; }
.pill{ padding:4px 14px; border-radius:999px; border:1px solid var(--line); background:var(--surface-2); color:var(--ink); font-size:.86rem; }
.meta-line{ color:var(--muted); font-size:.95rem; }
.ov-head{ font-family:var(--display); font-weight:700; font-size:1.2rem; margin:18px 0 6px; color:var(--ink); }

/* ---------- alerts ---------- */
[data-testid="stAlert"]{ border-radius:14px; background:var(--surface); border:1px solid var(--line); color:var(--ink); }
[data-testid="stCaptionContainer"]{ color:var(--muted); }

@media (max-width:640px){
  .tag{ display:none; }
  .block-container{ padding-left:1rem; padding-right:1rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


# =============================
# UI HELPERS (presentation only)
# =============================
def section_title(title: str, sub: str = ""):
    sub_html = f"<p>{html.escape(sub)}</p>" if sub else ""
    st.markdown(
        f"<div class='sec'><h3>{html.escape(title)}</h3>{sub_html}</div>",
        unsafe_allow_html=True,
    )


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("View details", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{html.escape(str(title))}</div>",
                    unsafe_allow_html=True,
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### Home feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        format_func=lambda x: x.replace("_", " ").title(),
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.markdown(
    """
<div class='brandbar'>
  <svg width="32" height="32" viewBox="0 0 28 28" fill="none" aria-hidden="true">
    <rect x="3" y="5" width="22" height="18" rx="3" stroke="currentColor" stroke-width="2.4"/>
    <path d="M11 10.5v7l6-3.5z" fill="currentColor"/>
  </svg>
  <span class='brand'>Matinee</span>
  <span class='tag'>Movie recommendations</span>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    st.markdown(
        "<div class='hero-title'>Find something worth watching tonight</div>"
        "<div class='hero-sub'>Search any movie, open it, and get similar picks "
        "based on its story and its genre.</div>",
        unsafe_allow_html=True,
    )

    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                section_title("Results", f"{len(cards)} movies for “{typed.strip()}”")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    section_title(home_category.replace("_", " ").title(), "Straight from TMDB")

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        section_title("Movie details")
    with b:
        if st.button("← Back to Home"):
            goto_home()

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")

    with left:
        with st.container(border=True):
            if data.get("poster_url"):
                st.image(data["poster_url"], use_container_width=True)
            else:
                st.write("🖼️ No poster")

    with right:
        with st.container(border=True):
            release = data.get("release_date") or "-"
            genre_names = [g["name"] for g in data.get("genres", [])]
            pills = (
                "".join(f"<span class='pill'>{html.escape(g)}</span>" for g in genre_names)
                or "<span class='meta-line'>-</span>"
            )
            st.markdown(
                f"<div class='detail-title'>{html.escape(data.get('title',''))}</div>"
                f"<div class='meta-line'>Release: {html.escape(str(release))}</div>"
                f"<div class='pills'>{pills}</div>"
                f"<div class='ov-head'>Overview</div>",
                unsafe_allow_html=True,
            )
            st.write(data.get("overview") or "No overview available.")

    if data.get("backdrop_url"):
        section_title("Backdrop")
        st.image(data["backdrop_url"], use_container_width=True)
    st.divider()
    section_title("Recommendations", "Picked by story similarity and by genre")

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            section_title("Similar movies", "Matched by plot and keywords (TF-IDF)")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            section_title("More like this", "Popular movies in the same genre")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")