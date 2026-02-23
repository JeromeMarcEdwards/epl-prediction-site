import marimo

__generated_with = "0.20.1"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import requests
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
    import matplotlib.patches as mpatches
    import io, base64
    from datetime import datetime
    from collections import defaultdict
    import numpy as np

    API_KEY = "7a874a538506441bbdc6b4aca3dbb648"
    HEADERS = {"X-Auth-Token": API_KEY}
    BASE    = "https://api.football-data.org/v4"
    SEASON  = 2025

    PREDICTIONS = {
        "Jerome": ["Manchester City FC", "Liverpool FC", "Chelsea FC",
                   "Arsenal FC", "Newcastle United FC", "Tottenham Hotspur FC"],
        "Erin":   ["Liverpool FC", "Arsenal FC", "Chelsea FC",
                   "Manchester City FC", "Aston Villa FC", "Tottenham Hotspur FC"],
        "Alex":   ["Liverpool FC", "Arsenal FC", "Manchester City FC",
                   "Chelsea FC", "Aston Villa FC", "Tottenham Hotspur FC"],
    }
    
    # 2024 season predictions
    PREDICTIONS_2024 = {
        "Jerome": ["Manchester City FC", "Arsenal FC", "Tottenham Hotspur FC", 
                   "Chelsea FC", "Liverpool FC", "Manchester United FC"],
        "Alex":   ["Arsenal FC", "Manchester City FC", "Liverpool FC", 
                   "Tottenham Hotspur FC", "Aston Villa FC", "Manchester United FC"],
        "Erin":   ["Manchester City FC", "Arsenal FC", "Tottenham Hotspur FC", 
                   "Liverpool FC", "Chelsea FC", "Newcastle United FC"],
    }
    
    # 2023-2024 season predictions
    PREDICTIONS_2023 = {
        "Alex":   ["Liverpool FC", "Manchester City FC", "Arsenal FC", 
                   "Chelsea FC", "Newcastle United FC", "Manchester United FC"],
        "Erin":   ["Manchester City FC", "Arsenal FC", "Newcastle United FC", 
                   "Chelsea FC", "Liverpool FC", "Manchester United FC"],
        "Jerome": ["Arsenal FC", "Newcastle United FC", "Manchester City FC", 
                   "Brighton & Hove Albion FC", "Manchester United FC", "Chelsea FC"],
    }
    COLORS = {"Jerome": "#E8A838", "Erin": "#4FC3C3", "Alex": "#E8608A"}
    T6_BON = -2
    EX_BON = -5
    BG     = "#0D1117"
    CARD   = "#161B22"
    TEXT   = "#E6EDF3"
    MUTED  = "#8B949E"

    return (
        API_KEY, BASE, BG, CARD, COLORS, EX_BON, HEADERS, MUTED, np,
        PREDICTIONS, PREDICTIONS_2024, PREDICTIONS_2023, SEASON, T6_BON, TEXT,
        base64, datetime, defaultdict, io, matplotlib, mo,
        mpatches, pe, plt, requests,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');
    body, .marimo-app, [class*="marimo"] {
        background: #0D1117 !important; color: #E6EDF3 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .hero { text-align:center; padding:36px 0 16px; border-bottom:1px solid #30363D; margin-bottom:24px; }
    .hero h1 { font-family:'Space Mono',monospace; font-size:2.1rem; font-weight:700; color:#E6EDF3; margin:0 0 8px; }
    .hero p  { color:#8B949E; font-size:0.88rem; margin:0; }
    .card { background:#161B22; border-radius:14px; padding:22px 26px; border:1px solid #30363D; margin-bottom:20px; }
    .section-title { font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:0.14em;
        text-transform:uppercase; color:#8B949E; margin-bottom:16px; padding-bottom:8px; border-bottom:1px solid #30363D; }
    .lb-row { display:flex; align-items:center; gap:14px; padding:14px 18px; border-radius:10px;
        margin-bottom:10px; border:1px solid #30363D; background:#0D1117; transition:transform 0.15s; }
    .lb-row:hover { transform:translateX(5px); }
    .lb-medal { font-size:1.7rem; min-width:36px; }
    .lb-name  { font-family:'Space Mono',monospace; font-size:1.1rem; font-weight:700; min-width:80px; }
    .lb-detail { font-size:0.76rem; color:#8B949E; display:flex; gap:14px; flex-wrap:wrap; }
    .lb-pts { margin-left:auto; font-family:'Space Mono',monospace; font-size:1.6rem; font-weight:700;
        padding:2px 18px; border-radius:999px; background:rgba(255,255,255,0.05); }
    .ptable { width:100%; border-collapse:collapse; font-size:0.84rem; }
    .ptable th { color:#8B949E; font-weight:500; padding:6px 10px; border-bottom:1px solid #30363D; text-align:left; }
    .ptable td { padding:7px 10px; border-bottom:1px solid #1c2130; }
    .ptable tr.exact td { background:#1a2e1a; color:#FFD700; }
    .ptable tr.top6  td { background:#14232b; }
    .d-good { color:#4FC3C3; font-weight:700; }
    .d-ok   { color:#FFD700; font-weight:700; }
    .d-bad  { color:#FF6B6B; font-weight:700; }
    .form-dot { display:inline-block; width:22px; height:22px; border-radius:50%;
        line-height:22px; text-align:center; font-size:0.65rem; font-weight:700; margin:0 2px; }
    .form-W { background:#1a3a1a; color:#4ade80; border:1px solid #4ade8055; }
    .form-D { background:#2a2a1a; color:#facc15; border:1px solid #facc1555; }
    .form-L { background:#3a1a1a; color:#f87171; border:1px solid #f8717155; }
    .statusbar { display:flex; justify-content:space-between; align-items:center;
        font-family:'Space Mono',monospace; font-size:0.72rem; color:#8B949E; padding:6px 4px 16px; }
    .live-dot { display:inline-block; width:7px; height:7px; border-radius:50%;
        background:#4FC3C3; animation:blink 2s ease-in-out infinite; margin-right:6px; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }
    .chart-img { width:100%; border-radius:10px; display:block; }
    .fact-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:20px; }
    .fact-card { background:#0D1117; border:1px solid #30363D; border-radius:10px; padding:16px 18px; }
    .fact-label { font-size:0.7rem; color:#8B949E; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px; }
    .fact-value { font-family:'Space Mono',monospace; font-size:1.3rem; font-weight:700; color:#E6EDF3; }
    .fact-sub   { font-size:0.76rem; color:#8B949E; margin-top:3px; }
    details summary { cursor:pointer; font-family:'Space Mono',monospace; font-size:0.7rem;
        color:#8B949E; letter-spacing:0.1em; text-transform:uppercase; padding:10px 4px; user-select:none; }
    details summary:hover { color:#E6EDF3; }
    .ssm-badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.7rem;
        font-family:'Space Mono',monospace; font-weight:700; }
    .ssm-up   { background:#1a3a1a; color:#4ade80; border:1px solid #4ade8033; }
    .ssm-down { background:#3a1a1a; color:#f87171; border:1px solid #f8717133; }
    .ssm-same { background:#1c1c2e; color:#8B949E; border:1px solid #30363D; }
    .proj-highlight { background: rgba(99,102,241,0.1); border-left: 3px solid #6366f1; padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; }
    </style>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    refresh = mo.ui.refresh(default_interval="10m")
    return (refresh,)


@app.cell(hide_code=True)
def _(BASE, COLORS, EX_BON, HEADERS, PREDICTIONS, SEASON, T6_BON,
      datetime, defaultdict, refresh, requests):
    _ = refresh

    errors = []

    def _api(path, params=None):
        try:
            r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            errors.append(f"{path} → HTTP {r.status_code}")
        except Exception as e:
            errors.append(f"{path} → {e}")
        return {}

    def _fuzzy(team, pos_dict):
        if team in pos_dict:
            return pos_dict[team]
        tl = team.lower().replace(" fc", "").strip()
        for k, v in pos_dict.items():
            kl = k.lower().replace(" fc", "").strip()
            if tl in kl or kl in tl:
                return v
            if len(set(tl.split()) & set(kl.split())) >= 2:
                return v
        return None

    def _score(picks, pos_dict):
        top6 = {t for t, p in pos_dict.items() if p <= 6}
        dt = tb = eb = 0
        bk = []
        for pr, team in enumerate(picks, 1):
            ar = _fuzzy(team, pos_dict)
            if ar is None:
                bk.append({"team": team, "pred": pr, "actual": "?", "dist": 0, "in_top6": False, "exact": False})
                continue
            dist  = abs(pr - ar)
            in_t6 = any(team.lower().replace(" fc","") in t.lower() or t.lower() in team.lower() for t in top6)
            exact = (pr == ar)
            dt += dist
            if in_t6: tb += T6_BON
            if exact: eb += EX_BON
            bk.append({"team": team, "pred": pr, "actual": ar, "dist": dist, "in_top6": in_t6, "exact": exact})
        return {"dist": dt, "top6": tb, "exact": eb, "total": dt + tb + eb, "breakdown": bk}

    # 1. Current standings
    standings_data = _api("/competitions/PL/standings", {"season": SEASON})
    current_table = []
    for _s in standings_data.get("standings", []):
        if _s.get("type") == "TOTAL":
            for _t in _s["table"]:
                current_table.append({
                    "pos": _t["position"], "name": _t["team"]["name"],
                    "pts": _t["points"], "gd": _t.get("goalDifference", 0),
                    "gf": _t["goalsFor"], "ga": _t["goalsAgainst"],
                    "played": _t["playedGames"], "won": _t["won"],
                    "draw": _t["draw"], "lost": _t["lost"],
                    "form": _t.get("form") or "",
                })
            break

    actual_pos = {t["name"]: t["pos"] for t in current_table}
    current_matchday = standings_data.get("season", {}).get("currentMatchday", "?")

    # 2. All matches
    matches_data = _api("/competitions/PL/matches", {"season": SEASON})
    all_matches  = matches_data.get("matches", [])

    gw_matches = defaultdict(list)
    for _m in all_matches:
        if _m.get("status") == "FINISHED" and _m.get("matchday"):
            gw_matches[_m["matchday"]].append(_m)

    _stats = {}
    historical = []

    def _init(n):
        if n not in _stats:
            _stats[n] = {"pts": 0, "gf": 0, "ga": 0}

    for _md in sorted(gw_matches.keys()):
        for _m in gw_matches[_md]:
            _ht = _m["homeTeam"]["name"]
            _at = _m["awayTeam"]["name"]
            _hg = _m["score"]["fullTime"].get("home")
            _ag = _m["score"]["fullTime"].get("away")
            if _hg is None or _ag is None:
                continue
            _init(_ht); _init(_at)
            _stats[_ht]["gf"] += _hg; _stats[_ht]["ga"] += _ag
            _stats[_at]["gf"] += _ag; _stats[_at]["ga"] += _hg
            if   _hg > _ag: _stats[_ht]["pts"] += 3
            elif _ag > _hg: _stats[_at]["pts"] += 3
            else:           _stats[_ht]["pts"] += 1; _stats[_at]["pts"] += 1
        _sorted = sorted(_stats.items(), key=lambda x: (-x[1]["pts"], -(x[1]["gf"]-x[1]["ga"]), -x[1]["gf"]))
        historical.append((_md, {n: i+1 for i, (n, _) in enumerate(_sorted)}))

    # 3. Top scorers
    scorers_data = _api("/competitions/PL/scorers", {"season": SEASON, "limit": 10})
    top_scorers = []
    for _sc in scorers_data.get("scorers", []):
        top_scorers.append({
            "name": _sc["player"]["name"], "team": _sc["team"]["name"],
            "goals": _sc["goals"], "assists": _sc.get("assists") or 0,
        })

    # 4. Upcoming fixtures
    upcoming = []
    for _m in all_matches:
        if _m.get("status") in ("SCHEDULED", "TIMED"):
            upcoming.append({"home": _m["homeTeam"]["name"], "away": _m["awayTeam"]["name"],
                             "date": _m.get("utcDate", ""), "md": _m.get("matchday")})
    upcoming = sorted(upcoming, key=lambda x: x["date"])[:15]

    # 5. Recent results
    recent = []
    for _m in reversed(all_matches):
        if _m.get("status") == "FINISHED":
            recent.append({"home": _m["homeTeam"]["name"], "away": _m["awayTeam"]["name"],
                           "hg": _m["score"]["fullTime"].get("home"),
                           "ag": _m["score"]["fullTime"].get("away"),
                           "md": _m.get("matchday"), "date": _m.get("utcDate", "")[:10]})
            if len(recent) == 10:
                break

    # 6. Scores
    results   = {p: _score(picks, actual_pos) for p, picks in PREDICTIONS.items()}
    ranked    = sorted(results.items(), key=lambda x: x[1]["total"])
    gw_scores = {p: [(md, _score(picks, pos)["total"]) for md, pos in historical]
                 for p, picks in PREDICTIONS.items()}

    best_md = {}
    for _p, _pts in gw_scores.items():
        if len(_pts) >= 2:
            _deltas = [(w, s - _pts[i-1][1]) for i, (w, s) in enumerate(_pts) if i > 0]
            best_md[_p] = min(_deltas, key=lambda x: x[1])

    fetched_at = datetime.now().strftime("%d %b %Y · %H:%M")

    return (
        actual_pos, all_matches, best_md, current_matchday, current_table, errors,
        fetched_at, gw_scores, historical, ranked, recent, results,
        top_scorers, upcoming,
    )


@app.cell(hide_code=True)
def _(BASE, EX_BON, HEADERS, PREDICTIONS_2024, T6_BON,
      datetime, defaultdict, requests):
    errors_2024 = []

    def _api_2024(path, params=None):
        try:
            r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            errors_2024.append(f"{path} → HTTP {r.status_code}")
        except Exception as e:
            errors_2024.append(f"{path} → {e}")
        return {}

    def _fuzzy_2024(team, pos_dict):
        if team in pos_dict:
            return pos_dict[team]
        tl = team.lower().replace(" fc", "").strip()
        for k, v in pos_dict.items():
            kl = k.lower().replace(" fc", "").strip()
            if tl in kl or kl in tl:
                return v
            if len(set(tl.split()) & set(kl.split())) >= 2:
                return v
        return None

    def _score_2024(picks, pos_dict):
        top6 = {t for t, p in pos_dict.items() if p <= 6}
        dt = tb = eb = 0
        bk = []
        for pr, team in enumerate(picks, 1):
            ar = _fuzzy_2024(team, pos_dict)
            if ar is None:
                bk.append({"team": team, "pred": pr, "actual": "?", "dist": 0, "in_top6": False, "exact": False})
                continue
            dist  = abs(pr - ar)
            in_t6 = any(team.lower().replace(" fc","") in t.lower() or t.lower() in team.lower() for t in top6)
            exact = (pr == ar)
            dt += dist
            if in_t6: tb += T6_BON
            if exact: eb += EX_BON
            bk.append({"team": team, "pred": pr, "actual": ar, "dist": dist, "in_top6": in_t6, "exact": exact})
        return {"dist": dt, "top6": tb, "exact": eb, "total": dt + tb + eb, "breakdown": bk}

    standings_data_2024 = _api_2024("/competitions/PL/standings", {"season": 2024})
    current_table_2024 = []
    for _s in standings_data_2024.get("standings", []):
        if _s.get("type") == "TOTAL":
            for _t in _s["table"]:
                current_table_2024.append({
                    "pos": _t["position"], "name": _t["team"]["name"],
                    "pts": _t["points"], "gd": _t.get("goalDifference", 0),
                    "gf": _t["goalsFor"], "ga": _t["goalsAgainst"],
                    "played": _t["playedGames"], "won": _t["won"],
                    "draw": _t["draw"], "lost": _t["lost"],
                    "form": _t.get("form") or "",
                })
            break

    actual_pos_2024 = {t["name"]: t["pos"] for t in current_table_2024}
    current_matchday_2024 = standings_data_2024.get("season", {}).get("currentMatchday", "?")

    matches_data_2024 = _api_2024("/competitions/PL/matches", {"season": 2024})
    all_matches_2024  = matches_data_2024.get("matches", [])

    gw_matches_2024 = defaultdict(list)
    for _m in all_matches_2024:
        if _m.get("status") == "FINISHED" and _m.get("matchday"):
            gw_matches_2024[_m["matchday"]].append(_m)

    _stats_2024 = {}
    historical_2024 = []

    def _init_2024(n):
        if n not in _stats_2024:
            _stats_2024[n] = {"pts": 0, "gf": 0, "ga": 0}

    for _md in sorted(gw_matches_2024.keys()):
        for _m in gw_matches_2024[_md]:
            _ht = _m["homeTeam"]["name"]
            _at = _m["awayTeam"]["name"]
            _hg = _m["score"]["fullTime"].get("home")
            _ag = _m["score"]["fullTime"].get("away")
            if _hg is None or _ag is None:
                continue
            _init_2024(_ht); _init_2024(_at)
            _stats_2024[_ht]["gf"] += _hg; _stats_2024[_ht]["ga"] += _ag
            _stats_2024[_at]["gf"] += _ag; _stats_2024[_at]["ga"] += _hg
            if   _hg > _ag: _stats_2024[_ht]["pts"] += 3
            elif _ag > _hg: _stats_2024[_at]["pts"] += 3
            else:           _stats_2024[_ht]["pts"] += 1; _stats_2024[_at]["pts"] += 1
        _sorted = sorted(_stats_2024.items(), key=lambda x: (-x[1]["pts"], -(x[1]["gf"]-x[1]["ga"]), -x[1]["gf"]))
        historical_2024.append((_md, {n: i+1 for i, (n, _) in enumerate(_sorted)}))

    results_2024   = {p: _score_2024(picks, actual_pos_2024) for p, picks in PREDICTIONS_2024.items()}
    ranked_2024    = sorted(results_2024.items(), key=lambda x: x[1]["total"])
    gw_scores_2024 = {p: [(md, _score_2024(picks, pos)["total"]) for md, pos in historical_2024]
                     for p, picks in PREDICTIONS_2024.items()}

    best_md_2024 = {}
    for _p, _pts in gw_scores_2024.items():
        if len(_pts) >= 2:
            _deltas = [(w, s - _pts[i-1][1]) for i, (w, s) in enumerate(_pts) if i > 0]
            best_md_2024[_p] = min(_deltas, key=lambda x: x[1])

    fetched_at_2024 = datetime.now().strftime("%d %b %Y · %H:%M")

    return (
        actual_pos_2024, best_md_2024, current_matchday_2024, current_table_2024, errors_2024,
        fetched_at_2024, gw_scores_2024, historical_2024, ranked_2024, results_2024,
    )


@app.cell(hide_code=True)
def _(BASE, EX_BON, HEADERS, PREDICTIONS_2023, T6_BON,
      datetime, defaultdict, requests):
    errors_2023 = []

    def _api_2023(path, params=None):
        try:
            r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            errors_2023.append(f"{path} → HTTP {r.status_code}")
        except Exception as e:
            errors_2023.append(f"{path} → {e}")
        return {}

    def _fuzzy_2023(team, pos_dict):
        if team in pos_dict:
            return pos_dict[team]
        tl = team.lower().replace(" fc", "").strip()
        for k, v in pos_dict.items():
            kl = k.lower().replace(" fc", "").strip()
            if tl in kl or kl in tl:
                return v
            if len(set(tl.split()) & set(kl.split())) >= 2:
                return v
        return None

    def _score_2023(picks, pos_dict):
        top6 = {t for t, p in pos_dict.items() if p <= 6}
        dt = tb = eb = 0
        bk = []
        for pr, team in enumerate(picks, 1):
            ar = _fuzzy_2023(team, pos_dict)
            if ar is None:
                bk.append({"team": team, "pred": pr, "actual": "?", "dist": 0, "in_top6": False, "exact": False})
                continue
            dist  = abs(pr - ar)
            in_t6 = any(team.lower().replace(" fc","") in t.lower() or t.lower() in team.lower() for t in top6)
            exact = (pr == ar)
            dt += dist
            if in_t6: tb += T6_BON
            if exact: eb += EX_BON
            bk.append({"team": team, "pred": pr, "actual": ar, "dist": dist, "in_top6": in_t6, "exact": exact})
        return {"dist": dt, "top6": tb, "exact": eb, "total": dt + tb + eb, "breakdown": bk}

    standings_data_2023 = _api_2023("/competitions/PL/standings", {"season": 2023})
    current_table_2023 = []
    for _s in standings_data_2023.get("standings", []):
        if _s.get("type") == "TOTAL":
            for _t in _s["table"]:
                current_table_2023.append({
                    "pos": _t["position"], "name": _t["team"]["name"],
                    "pts": _t["points"], "gd": _t.get("goalDifference", 0),
                    "gf": _t["goalsFor"], "ga": _t["goalsAgainst"],
                    "played": _t["playedGames"], "won": _t["won"],
                    "draw": _t["draw"], "lost": _t["lost"],
                    "form": _t.get("form") or "",
                })
            break

    actual_pos_2023 = {t["name"]: t["pos"] for t in current_table_2023}
    current_matchday_2023 = standings_data_2023.get("season", {}).get("currentMatchday", "?")

    matches_data_2023 = _api_2023("/competitions/PL/matches", {"season": 2023})
    all_matches_2023  = matches_data_2023.get("matches", [])

    gw_matches_2023 = defaultdict(list)
    for _m in all_matches_2023:
        if _m.get("status") == "FINISHED" and _m.get("matchday"):
            gw_matches_2023[_m["matchday"]].append(_m)

    _stats_2023 = {}
    historical_2023 = []

    def _init_2023(n):
        if n not in _stats_2023:
            _stats_2023[n] = {"pts": 0, "gf": 0, "ga": 0}

    for _md in sorted(gw_matches_2023.keys()):
        for _m in gw_matches_2023[_md]:
            _ht = _m["homeTeam"]["name"]
            _at = _m["awayTeam"]["name"]
            _hg = _m["score"]["fullTime"].get("home")
            _ag = _m["score"]["fullTime"].get("away")
            if _hg is None or _ag is None:
                continue
            _init_2023(_ht); _init_2023(_at)
            _stats_2023[_ht]["gf"] += _hg; _stats_2023[_ht]["ga"] += _ag
            _stats_2023[_at]["gf"] += _ag; _stats_2023[_at]["ga"] += _hg
            if   _hg > _ag: _stats_2023[_ht]["pts"] += 3
            elif _ag > _hg: _stats_2023[_at]["pts"] += 3
            else:           _stats_2023[_ht]["pts"] += 1; _stats_2023[_at]["pts"] += 1
        _sorted = sorted(_stats_2023.items(), key=lambda x: (-x[1]["pts"], -(x[1]["gf"]-x[1]["ga"]), -x[1]["gf"]))
        historical_2023.append((_md, {n: i+1 for i, (n, _) in enumerate(_sorted)}))

    results_2023   = {p: _score_2023(picks, actual_pos_2023) for p, picks in PREDICTIONS_2023.items()}
    ranked_2023    = sorted(results_2023.items(), key=lambda x: x[1]["total"])
    gw_scores_2023 = {p: [(md, _score_2023(picks, pos)["total"]) for md, pos in historical_2023]
                     for p, picks in PREDICTIONS_2023.items()}

    best_md_2023 = {}
    for _p, _pts in gw_scores_2023.items():
        if len(_pts) >= 2:
            _deltas = [(w, s - _pts[i-1][1]) for i, (w, s) in enumerate(_pts) if i > 0]
            best_md_2023[_p] = min(_deltas, key=lambda x: x[1])

    fetched_at_2023 = datetime.now().strftime("%d %b %Y · %H:%M")

    return (
        actual_pos_2023, best_md_2023, current_matchday_2023, current_table_2023, errors_2023,
        fetched_at_2023, gw_scores_2023, historical_2023, ranked_2023, results_2023,
    )


# ─── NEW: Bayesian SSM computation cell ──────────────────────────────────────
@app.cell(hide_code=True)
def _(all_matches, current_table, np, PREDICTIONS, T6_BON, EX_BON):
    """
    Bayesian State-Space Model — Gamma-Poisson conjugate filter.

    For each team i, we track latent attack α_i ~ Gamma(a_i, b_i)
    and defence δ_i ~ Gamma(c_i, d_i).

    After observing home goals H, away goals A:
      Conjugate update (mean-field):
        a_h += H,  b_h += E[1/δ_a] * exp(η)
        a_a += A,  b_a += E[1/δ_h]
        c_h += A,  d_h += E[α_a] / exp(η)
        c_a += H,  d_a += E[α_h] * exp(η)

    State evolution: multiply shape/rate by φ after each match
    (preserves mean, inflates variance → tracks time-varying form).
    """

    # ── Hyperparameters ──────────────────────────────────────────────
    PRIOR_SHAPE  = 4.0
    PRIOR_RATE   = 4.0
    PHI_WITHIN   = 0.975   # within-season forgetting factor
    ETA          = 0.26    # home advantage (log scale)
    N_SIM_SEASON = 5000    # MC simulations for season completion

    # ── Identify all teams ──────────────────────────────────────────
    ssm_teams = sorted({_t["name"] for _t in current_table})
    n_teams   = len(ssm_teams)
    _idx      = {_t: _ii for _ii, _t in enumerate(ssm_teams)}

    # ── Initialise Gamma parameters ─────────────────────────────────
    _a = np.full(n_teams, PRIOR_SHAPE)   # attack shape
    _b = np.full(n_teams, PRIOR_RATE)    # attack rate
    _c = np.full(n_teams, PRIOR_SHAPE)   # defence shape
    _d = np.full(n_teams, PRIOR_RATE)    # defence rate

    def _inv_mean(_ci, _di):
        """E[1/X] for X ~ Gamma(c, d)"""
        return _di / (_ci - 1) if _ci > 1 else _di / _ci

    def _ssm_update(_hi, _ai, _hg, _ag):
        """Conjugate mean-field update for one match."""
        _C_H = _inv_mean(_c[_ai], _d[_ai]) * np.exp(ETA)
        _C_A = _inv_mean(_c[_hi], _d[_hi])
        _D_A = (_a[_hi] / _b[_hi]) * np.exp(ETA)
        _D_H = (_a[_ai] / _b[_ai]) / np.exp(ETA)

        # Attack updates
        _a[_hi] += _hg;  _b[_hi] += _C_H
        _a[_ai] += _ag;  _b[_ai] += _C_A
        # Defence updates
        _c[_hi] += _ag;  _d[_hi] += _D_A
        _c[_ai] += _hg;  _d[_ai] += _D_H

        # Forgetting (applied to involved teams)
        for _fi in [_hi, _ai]:
            _a[_fi] *= PHI_WITHIN;  _b[_fi] *= PHI_WITHIN
            _c[_fi] *= PHI_WITHIN;  _d[_fi] *= PHI_WITHIN

    # ── Run filter over all finished 2025-26 matches ─────────────────
    _finished = sorted(
        [_m for _m in all_matches if _m.get("status") == "FINISHED"],
        key=lambda _m: _m.get("utcDate", "")
    )
    for _m in _finished:
        _hn = _m["homeTeam"]["name"]
        _an = _m["awayTeam"]["name"]
        _hg = _m["score"]["fullTime"].get("home")
        _ag = _m["score"]["fullTime"].get("away")
        if _hn in _idx and _an in _idx and _hg is not None and _ag is not None:
            _ssm_update(_idx[_hn], _idx[_an], int(_hg), int(_ag))

    # ── Remaining fixtures ───────────────────────────────────────────
    _remaining = [
        _m for _m in all_matches
        if _m.get("status") in ("SCHEDULED", "TIMED")
        and _m["homeTeam"]["name"] in _idx
        and _m["awayTeam"]["name"] in _idx
    ]
    n_remaining = len(_remaining)

    # ── Current points from actual table ────────────────────────────
    _current_pts = {}
    _current_gf  = {}
    _current_gd  = {}
    for _t in current_table:
        _current_pts[_t["name"]] = _t["pts"]
        _current_gf[_t["name"]]  = _t["gf"]
        _current_gd[_t["name"]]  = _t.get("goalDifference", 0)

    # ── Attack/defence means for rating table ────────────────────────
    ssm_ratings = {}
    for _team in ssm_teams:
        _i   = _idx[_team]
        _atk = _a[_i] / _b[_i]
        _dfc = _c[_i] / _d[_i]
        ssm_ratings[_team] = {
            "atk": round(_atk, 3),
            "def": round(_dfc, 3),
            "net": round(_atk / _dfc, 3),
            "atk_sd": round(np.sqrt(_a[_i] / _b[_i]**2), 3),
            "def_sd": round(np.sqrt(_c[_i] / _d[_i]**2), 3),
        }

    # ── Monte Carlo season completion ────────────────────────────────
    _rng = np.random.default_rng(42)

    # Pre-draw Gamma samples — shape: (N_SIM_SEASON, n_teams)
    _atk_samples = _rng.gamma(_a, 1.0 / _b, size=(N_SIM_SEASON, n_teams))
    _def_samples = _rng.gamma(_c, 1.0 / _d, size=(N_SIM_SEASON, n_teams))
    _atk_samples = np.clip(_atk_samples, 0.05, 10)
    _def_samples = np.clip(_def_samples, 0.05, 10)

    # Simulate each remaining fixture across all sims
    _sim_pts = {_t: np.full(N_SIM_SEASON, _current_pts.get(_t, 0), dtype=float) for _t in ssm_teams}
    _sim_gd  = {_t: np.full(N_SIM_SEASON, _current_gd.get(_t, 0),  dtype=float) for _t in ssm_teams}
    _sim_gf  = {_t: np.full(N_SIM_SEASON, _current_gf.get(_t, 0),  dtype=float) for _t in ssm_teams}

    for _m in _remaining:
        _hn2  = _m["homeTeam"]["name"]
        _an2  = _m["awayTeam"]["name"]
        _hi2  = _idx[_hn2]
        _ai2  = _idx[_an2]

        _lam_H = _atk_samples[:, _hi2] / _def_samples[:, _ai2] * np.exp(ETA)
        _lam_A = _atk_samples[:, _ai2] / _def_samples[:, _hi2]
        _lam_H = np.clip(_lam_H, 0.05, 10)
        _lam_A = np.clip(_lam_A, 0.05, 10)

        _hg_sim = _rng.poisson(_lam_H)
        _ag_sim = _rng.poisson(_lam_A)

        _home_win = _hg_sim > _ag_sim
        _draw     = _hg_sim == _ag_sim
        _away_win = _ag_sim > _hg_sim

        _sim_pts[_hn2] += np.where(_home_win, 3, np.where(_draw, 1, 0))
        _sim_pts[_an2] += np.where(_away_win, 3, np.where(_draw, 1, 0))
        _sim_gd[_hn2]  += (_hg_sim - _ag_sim).astype(float)
        _sim_gd[_an2]  += (_ag_sim - _hg_sim).astype(float)
        _sim_gf[_hn2]  += _hg_sim.astype(float)
        _sim_gf[_an2]  += _ag_sim.astype(float)

    # ── Final position distributions from simulations ────────────────
    _team_list = ssm_teams

    _pts_mat  = np.stack([_sim_pts[_t] for _t in _team_list], axis=1)
    _gd_mat   = np.stack([_sim_gd[_t]  for _t in _team_list], axis=1)
    _gf_mat   = np.stack([_sim_gf[_t]  for _t in _team_list], axis=1)

    _sort_key = np.stack([-_pts_mat, -_gd_mat, -_gf_mat], axis=2)

    _ranks = np.zeros((N_SIM_SEASON, n_teams), dtype=int)
    for _sim_i in range(N_SIM_SEASON):
        # Sort by points (desc), then goal difference (desc), then goals scored (desc)
        _order = np.lexsort((_sort_key[_sim_i, :, 2], _sort_key[_sim_i, :, 1], _sort_key[_sim_i, :, 0]))
        _ranks[_sim_i, _order] = np.arange(1, n_teams + 1)

    _mean_pos  = _ranks.mean(axis=0)
    _std_pos   = _ranks.std(axis=0)
    _top1_prob = (_ranks == 1).mean(axis=0)
    _top4_prob = (_ranks <= 4).mean(axis=0)
    _top6_prob = (_ranks <= 6).mean(axis=0)
    _rel_prob  = (_ranks >= 18).mean(axis=0)
    _mean_pts  = np.array([_sim_pts[_t].mean() for _t in _team_list])

    # Build predicted final table (sorted by mean_pos)
    _pred_table_order = np.argsort(_mean_pos)
    predicted_final_table = []
    for _rank_i, _ti in enumerate(_pred_table_order):
        _team = _team_list[_ti]
        _current_pos = next((_t["pos"] for _t in current_table if _t["name"] == _team), _rank_i + 1)
        predicted_final_table.append({
            "pred_pos":  _rank_i + 1,
            "curr_pos":  _current_pos,
            "name":      _team,
            "mean_pos":  round(float(_mean_pos[_ti]), 1),
            "std_pos":   round(float(_std_pos[_ti]), 1),
            "mean_pts":  round(float(_mean_pts[_ti]), 1),
            "curr_pts":  _current_pts.get(_team, 0),
            "top1_pct":  round(float(_top1_prob[_ti]) * 100, 1),
            "top4_pct":  round(float(_top4_prob[_ti]) * 100, 1),
            "top6_pct":  round(float(_top6_prob[_ti]) * 100, 1),
            "rel_pct":   round(float(_rel_prob[_ti]) * 100, 1),
        })

    # ── Predicted final positions dict (for scoring) ─────────────────
    pred_pos_dict = {_row["name"]: _row["pred_pos"] for _row in predicted_final_table}

    # ── Apply scoring formula to predicted final table ───────────────
    def _fuzzy_ssm(_team, _pos_dict):
        if _team in _pos_dict:
            return _pos_dict[_team]
        _tl = _team.lower().replace(" fc", "").strip()
        for _k, _v in _pos_dict.items():
            _kl = _k.lower().replace(" fc", "").strip()
            if _tl in _kl or _kl in _tl:
                return _v
            if len(set(_tl.split()) & set(_kl.split())) >= 2:
                return _v
        return None

    def _score_ssm(_picks, _pos_dict):
        _top6 = {_t for _t, _pp in _pos_dict.items() if _pp <= 6}
        _dt = _tb = _eb = 0
        _bk = []
        for _pr, _team in enumerate(_picks, 1):
            _ar = _fuzzy_ssm(_team, _pos_dict)
            if _ar is None:
                _bk.append({"team": _team, "pred": _pr, "proj": "?", "dist": 0, "in_top6": False, "exact": False})
                continue
            _dist  = abs(_pr - _ar)
            _in_t6 = any(_team.lower().replace(" fc","") in _t.lower() or _t.lower() in _team.lower() for _t in _top6)
            _exact = (_pr == _ar)
            _dt += _dist
            if _in_t6: _tb += T6_BON
            if _exact: _eb += EX_BON
            _bk.append({"team": _team, "pred": _pr, "proj": _ar, "dist": _dist, "in_top6": _in_t6, "exact": _exact})
        return {"dist": _dt, "top6": _tb, "exact": _eb, "total": _dt + _tb + _eb, "breakdown": _bk}

    projected_scores = {_p: _score_ssm(_picks, pred_pos_dict) for _p, _picks in PREDICTIONS.items()}
    projected_ranked = sorted(projected_scores.items(), key=lambda _x: _x[1]["total"])

    return (
        N_SIM_SEASON, n_remaining, pred_pos_dict, predicted_final_table,
        projected_ranked, projected_scores, ssm_ratings, ssm_teams,
    )


@app.cell(hide_code=True)
def _(COLORS, mo, ranked, results):
    _err_h = f" · ⚠️ {'; '.join([])}" if False else ""
    _medals = ["🥇", "🥈", "🥉"]

    def _lb_row(i, p):
        s = results[p]; c = COLORS[p]
        return f"""
        <div class="lb-row" style="border-color:{c}55">
          <span class="lb-medal">{_medals[i]}</span>
          <span class="lb-name" style="color:{c}">{p}</span>
          <span class="lb-detail">
            <span>📏 dist: <b>+{s['dist']}</b></span>
            <span>✅ top-6: <b>{s['top6']}</b></span>
            <span>🎯 exact: <b>{s['exact']}</b></span>
          </span>
          <span class="lb-pts" style="color:{c}">{s['total']}</span>
        </div>"""

    mo.Html(
        '<div class="card"><div class="section-title">🏆 Leaderboard — 2025/26 Season</div>'
        + "".join(_lb_row(i, p) for i, (p, _) in enumerate(ranked))
        + '</div>'
    )
    return


@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, TEXT, base64, gw_scores, historical, io, mo, pe, plt):
    _fig, _ax = plt.subplots(figsize=(12, 4), facecolor=BG)
    _ax.set_facecolor(CARD)
    for _sp in _ax.spines.values():
        _sp.set_edgecolor("#30363D")

    if historical:
        _all_s = [s for pts in gw_scores.values() for _, s in pts]
        _ymax  = max(_all_s) + 1
        for _p, _pts in gw_scores.items():
            _w = [w for w, _ in _pts]
            _s = [s for _, s in _pts]
            _c = COLORS[_p]
            _ax.fill_between(_w, _s, _ymax + 2, alpha=0.07, color=_c, zorder=1)
            _ax.plot(_w, _s, color=_c, lw=2.5, zorder=3, solid_capstyle="round",
                     marker="o", markersize=4, markerfacecolor=_c, markeredgewidth=0)
            _ax.plot(_w[-1], _s[-1], "o", ms=10, color=_c, zorder=5,
                     markeredgecolor=BG, markeredgewidth=2)
            _ax.text(_w[-1]+0.25, _s[-1], f" {_p}  {_s[-1]}", color=_c,
                     fontsize=9, fontfamily="monospace", va="center", fontweight="bold",
                     path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)])
        _gws = [w for w, _ in historical]
        _ax.set_xlim(min(_gws)-0.5, max(_gws)+4)
        _ax.invert_yaxis()
        _ax.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax.set_ylabel("Score  (↑ = better)", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax.text(0.01, 0.03, "↑ better", transform=_ax.transAxes, color=MUTED, fontsize=8, fontfamily="monospace")
    else:
        _ax.text(0.5, 0.5, "No finished matches yet this season",
                 ha="center", va="center", color=MUTED, fontsize=11, transform=_ax.transAxes)

    _ax.set_title("Prediction Score Evolution by Matchday — 2025/26", color=TEXT, fontsize=11, fontfamily="monospace", pad=12)
    _ax.tick_params(colors=MUTED)
    _ax.grid(color="#30363D", lw=0.6, linestyle="--", alpha=0.6, zorder=0)
    _fig.tight_layout(pad=1.5)
    _buf = io.BytesIO()
    _fig.savefig(_buf, format="png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(_fig); _buf.seek(0)
    _b64 = base64.b64encode(_buf.read()).decode()
    mo.Html(f'<div class="card"><div class="section-title">📈 Score Evolution</div>'
            f'<img class="chart-img" src="data:image/png;base64,{_b64}" /></div>')
    return


@app.cell(hide_code=True)
def _(COLORS, mo, ranked, results):
    _m2 = ["🥇", "🥈", "🥉"]

    def _rc(b): return "exact" if b["exact"] else ("top6" if b["in_top6"] else "")
    def _dc(b):
        if b["exact"]: return "d-good"
        return "d-bad" if b["dist"] > 3 else ("d-ok" if b["dist"] > 0 else "d-good")

    def _pick_card(i, p):
        c = COLORS[p]; s = results[p]
        rows = ""
        for b in s["breakdown"]:
            short = b["team"].replace(" FC","").replace(" United","").replace(" City"," C.").replace(" Hotspur","")
            rows += (f'<tr class="{_rc(b)}"><td style="color:#8B949E">{b["pred"]}</td>'
                     f'<td>{short}</td><td style="text-align:center">{b["actual"]}</td>'
                     f'<td style="text-align:center" class="{_dc(b)}">{b["dist"]}</td></tr>')
        legend = ('<tr><td colspan="4" style="padding-top:10px;font-size:0.7rem;color:#8B949E">'
                  '<span style="background:#1a2e1a;padding:2px 8px;border-radius:4px;color:#FFD700;margin-right:8px">🎯 exact (−5)</span>'
                  '<span style="background:#14232b;padding:2px 8px;border-radius:4px;color:#4FC3C3">✅ top-6 (−2)</span></td></tr>')
        return (f'<div class="card" style="border-color:{c}44">'
                f'<div class="section-title" style="color:{c}">{_m2[i]} {p} &nbsp;·&nbsp;'
                f'<span style="color:#E6EDF3;font-size:0.85rem">{s["total"]} pts</span></div>'
                f'<table class="ptable"><thead><tr><th>#</th><th>Predicted</th>'
                f'<th style="text-align:center">Actual</th><th style="text-align:center">Δ</th>'
                f'</tr></thead><tbody>{rows}{legend}</tbody></table></div>')

    mo.Html('<div class="section-title">📋 Pick-by-pick Breakdown</div>'
            '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px">'
            + "".join(_pick_card(i, p) for i, (p, _) in enumerate(ranked)) + '</div>')
    return


@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, PREDICTIONS, TEXT, base64, current_table, io, mo, mpatches, plt):
    def _form_html(form_str):
        dots = ""
        for ch in (form_str or "").replace(",", "")[-5:]:
            cls = {"W": "form-W", "D": "form-D", "L": "form-L"}.get(ch, "form-D")
            dots += f'<span class="form-dot {cls}">{ch}</span>'
        return dots

    _all_pred = {t.lower().replace(" fc","").strip() for picks in PREDICTIONS.values() for t in picks}
    def _is_pred(name):
        n = name.lower().replace(" fc","").strip()
        return any(n in p or p in n for p in _all_pred)

    rows_html = ""
    for _t in current_table:
        _pos   = _t["pos"]
        _short = _t["name"].replace(" FC","").replace(" United","").replace(" Hotspur","")
        _form  = _form_html(_t["form"])
        _hl    = "background:#1a1f2e;" if _pos <= 6 else ""
        _bold  = "font-weight:700;" if _is_pred(_t["name"]) else ""
        _pcol  = ("color:#60a5fa;" if _pos <= 4 else
                  "color:#f59e0b;" if _pos == 5 else
                  "color:#8b5cf6;" if _pos == 6 else "color:#8B949E;")
        rows_html += (f'<tr style="{_hl}"><td style="text-align:center;{_pcol}font-family:monospace;font-weight:700">{_pos}</td>'
                      f'<td style="{_bold}">{_short}</td>'
                      f'<td style="text-align:center;color:#8B949E">{_t["played"]}</td>'
                      f'<td style="text-align:center;color:#4ade80">{_t["won"]}</td>'
                      f'<td style="text-align:center;color:#facc15">{_t["draw"]}</td>'
                      f'<td style="text-align:center;color:#f87171">{_t["lost"]}</td>'
                      f'<td style="text-align:center">{_t["gd"]:+d}</td>'
                      f'<td style="text-align:center;font-family:monospace;font-weight:700;color:#E6EDF3">{_t["pts"]}</td>'
                      f'<td>{_form}</td></tr>')

    _fig2, _ax2 = plt.subplots(figsize=(10, 3.2), facecolor=BG)
    _ax2.set_facecolor(CARD)
    for _sp in _ax2.spines.values(): _sp.set_edgecolor("#30363D")
    _top10 = current_table[:10]
    _names = [t["name"].replace(" FC","").replace(" United","").replace(" Hotspur","") for t in _top10]
    _pts2  = [t["pts"] for t in _top10]
    _bc    = ["#60a5fa"]*4 + ["#f59e0b"] + ["#8b5cf6"] + ["#374151"]*4
    _bars  = _ax2.barh(_names[::-1], _pts2[::-1], color=_bc[::-1], alpha=0.85, height=0.65)
    for _bar, _p2 in zip(_bars, _pts2[::-1]):
        _ax2.text(_bar.get_width()+0.3, _bar.get_y()+_bar.get_height()/2,
                  str(_p2), va="center", color=TEXT, fontsize=9, fontfamily="monospace")
    _ax2.set_xlabel("Points", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax2.set_title("Top 10 by Points", color=TEXT, fontsize=10, fontfamily="monospace", pad=10)
    _ax2.tick_params(colors=MUTED, labelsize=8)
    _ax2.grid(axis="x", color="#30363D", lw=0.6, linestyle="--", alpha=0.6)
    _ax2.set_xlim(0, max(_pts2) + 5 if _pts2 else 10)
    _leg = [mpatches.Patch(color="#60a5fa", label="Champions League (1-4)"),
            mpatches.Patch(color="#f59e0b", label="Europa League (5)"),
            mpatches.Patch(color="#8b5cf6", label="Conference (6)")]
    _ax2.legend(handles=_leg, loc="lower right", framealpha=0.2,
                labelcolor=TEXT, fontsize=7, facecolor=CARD, edgecolor="#30363D")
    _fig2.tight_layout(pad=1.5)
    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig2); _buf2.seek(0)
    _b64_2 = base64.b64encode(_buf2.read()).decode()

    mo.Html(f"""
    <div class="card">
      <div class="section-title">📊 Current Premier League Table</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start">
        <div>
          <table class="ptable">
            <thead><tr><th style="text-align:center">#</th><th>Club</th>
              <th style="text-align:center">P</th><th style="text-align:center">W</th>
              <th style="text-align:center">D</th><th style="text-align:center">L</th>
              <th style="text-align:center">GD</th><th style="text-align:center">Pts</th>
              <th>Form</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
          <div style="font-size:0.7rem;color:#8B949E;margin-top:10px;font-family:monospace">
            <b style="color:#E6EDF3">Bold</b> = predicted &nbsp;·&nbsp; Blue=CL &nbsp;·&nbsp; Highlighted=top 6
          </div>
        </div>
        <div><img class="chart-img" src="data:image/png;base64,{_b64_2}" /></div>
      </div>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo, top_scorers):
    _top = top_scorers[0] if top_scorers else None
    _top_html = ""
    if _top:
        _top_html = f"""
        <div class="fact-grid" style="margin-bottom:16px">
          <div class="fact-card">
            <div class="fact-label">⚽ Golden Boot Leader</div>
            <div class="fact-value">{_top['name'].split()[-1]}</div>
            <div class="fact-sub">{_top['goals']} goals · {_top['team'].replace(' FC','')}</div>
          </div>
          <div class="fact-card">
            <div class="fact-label">🎯 Goals + Assists</div>
            <div class="fact-value">{_top['goals'] + _top['assists']}</div>
            <div class="fact-sub">{_top['goals']}G + {_top['assists']}A</div>
          </div>
          <div class="fact-card">
            <div class="fact-label">📋 Scorers tracked</div>
            <div class="fact-value">{len(top_scorers)}</div>
            <div class="fact-sub">top scorers this season</div>
          </div>
        </div>"""

    def _sr(i, s):
        _medal = ["🥇","🥈","🥉"][i] if i < 3 else f"{i+1}."
        _team  = s["team"].replace(" FC","").replace(" United","").replace(" Hotspur","")
        return (f'<tr><td style="text-align:center;font-family:monospace;color:#8B949E">{_medal}</td>'
                f'<td style="font-weight:600">{s["name"]}</td>'
                f'<td style="color:#8B949E;font-size:0.8rem">{_team}</td>'
                f'<td style="text-align:center;font-family:monospace;font-size:1.1rem;font-weight:700;color:#FFD700">{s["goals"]}</td>'
                f'<td style="text-align:center;font-family:monospace;color:#4FC3C3">{s["assists"]}</td></tr>')

    _srows = "".join(_sr(i, s) for i, s in enumerate(top_scorers))
    mo.Html(f"""
    <div class="card">
      <div class="section-title">🥅 Top Scorers — 2025/26</div>
      {_top_html}
      <table class="ptable">
        <thead><tr><th style="text-align:center">#</th><th>Player</th><th>Club</th>
          <th style="text-align:center">⚽ Goals</th><th style="text-align:center">🅰️ Assists</th>
        </tr></thead>
        <tbody>{_srows}</tbody>
      </table>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo, recent, upcoming):
    def _shorten(name):
        return name.replace(" FC","").replace(" United","").replace(" Hotspur","").replace(" City","")

    def _fmt_date(d):
        try:
            from datetime import datetime as _dt
            return _dt.fromisoformat(d.replace("Z","+00:00")).strftime("%d %b %H:%M")
        except Exception:
            return d[:10]

    _up = ""
    for _f in upcoming[:8]:
        _up += (f'<tr><td style="color:#8B949E;font-size:0.75rem;white-space:nowrap">{_fmt_date(_f["date"])}</td>'
                f'<td style="text-align:right;font-weight:600">{_shorten(_f["home"])}</td>'
                f'<td style="text-align:center;color:#8B949E;padding:0 8px">vs</td>'
                f'<td style="font-weight:600">{_shorten(_f["away"])}</td>'
                f'<td style="text-align:center;color:#8B949E;font-size:0.75rem">MD{_f["md"]}</td></tr>')

    _re = ""
    for _r in recent[:8]:
        _hg, _ag = _r["hg"], _r["ag"]
        if _hg > _ag:   _hc, _ac = "#4ade80", "#f87171"
        elif _ag > _hg: _hc, _ac = "#f87171", "#4ade80"
        else:           _hc = _ac = "#facc15"
        _re += (f'<tr><td style="color:#8B949E;font-size:0.75rem">{_r["date"]}</td>'
                f'<td style="text-align:right;font-weight:600;color:{_hc}">{_shorten(_r["home"])}</td>'
                f'<td style="text-align:center;font-family:monospace;font-weight:700;padding:0 10px">{_hg}–{_ag}</td>'
                f'<td style="font-weight:600;color:{_ac}">{_shorten(_r["away"])}</td></tr>')

    mo.Html(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
      <div class="card">
        <div class="section-title">📅 Upcoming Fixtures</div>
        <table class="ptable"><thead><tr>
          <th>Date (UTC)</th><th style="text-align:right">Home</th>
          <th></th><th>Away</th><th style="text-align:center">MD</th>
        </tr></thead><tbody>{_up}</tbody></table>
      </div>
      <div class="card">
        <div class="section-title">🎮 Recent Results</div>
        <table class="ptable"><thead><tr>
          <th>Date</th><th style="text-align:right">Home</th>
          <th style="text-align:center">Score</th><th>Away</th>
        </tr></thead><tbody>{_re}</tbody></table>
      </div>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, PREDICTIONS, TEXT, base64,
      best_md, current_table, gw_scores, io, mo, pe, plt, ranked, results):

    _fig3, _ax3 = plt.subplots(figsize=(12, 3.5), facecolor=BG)
    _ax3.set_facecolor(CARD)
    for _sp in _ax3.spines.values(): _sp.set_edgecolor("#30363D")

    if gw_scores and any(gw_scores.values()):
        _leader_by_gw = {}
        _all_mds = sorted({md for pts in gw_scores.values() for md, _ in pts})
        for _md in _all_mds:
            _at = {p: next((s for w, s in pts if w == _md), None) for p, pts in gw_scores.items()}
            _valid = {p: s for p, s in _at.items() if s is not None}
            if _valid: _leader_by_gw[_md] = min(_valid.values())

        for _p, _pts in gw_scores.items():
            _w   = [w for w, _ in _pts]
            _gap = [s - _leader_by_gw.get(w, s) for w, s in _pts]
            _c   = COLORS[_p]
            _ax3.fill_between(_w, _gap, 0, alpha=0.08, color=_c)
            _ax3.plot(_w, _gap, color=_c, lw=2, zorder=3, marker="o",
                      markersize=3, markerfacecolor=_c, markeredgewidth=0, solid_capstyle="round")
            _ax3.text(_w[-1]+0.2, _gap[-1], f" {_p}", color=_c, fontsize=8.5,
                      fontfamily="monospace", va="center",
                      path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

        _ax3.axhline(0, color="#4FC3C3", lw=1.5, linestyle="--", alpha=0.6, zorder=4)
        _ax3.text(0.01, 0.97, "← leading", transform=_ax3.transAxes,
                  color="#4FC3C3", fontsize=7.5, fontfamily="monospace", va="top")
        _gw3 = [w for w, _ in list(gw_scores.values())[0]]
        _ax3.set_xlim(min(_gw3)-0.5, max(_gw3)+3)
        _ax3.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax3.set_ylabel("Points behind leader", color=MUTED, fontsize=9, fontfamily="monospace")
    else:
        _ax3.text(0.5, 0.5, "No data yet", ha="center", va="center",
                  color=MUTED, fontsize=11, transform=_ax3.transAxes)

    _ax3.set_title("Gap to Leader by Matchday", color=TEXT, fontsize=11, fontfamily="monospace", pad=10)
    _ax3.tick_params(colors=MUTED)
    _ax3.grid(color="#30363D", lw=0.6, linestyle="--", alpha=0.5)
    _fig3.tight_layout(pad=1.5)
    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig3); _buf3.seek(0)
    _b64_3 = base64.b64encode(_buf3.read()).decode()

    _lp, _ls  = ranked[0]
    _gap12    = results[ranked[1][0]]["total"] - results[ranked[0][0]]["total"]
    _top6n    = {t["name"] for t in current_table if t["pos"] <= 6}

    def _t6c(person):
        return sum(1 for t in PREDICTIONS[person] if any(
            t.lower().replace(" fc","") in tn.lower() or tn.lower() in t.lower()
            for tn in _top6n))

    _t6counts = {p: _t6c(p) for p in PREDICTIONS}
    _best_t6  = max(_t6counts, key=_t6counts.get)

    _bg2 = None; _bg2_val = 0
    for _p3, _bmd in best_md.items():
        if _bmd[1] < _bg2_val:
            _bg2_val = _bmd[1]; _bg2 = (_p3, _bmd[0], _bmd[1])

    _exc  = {p: sum(1 for b in results[p]["breakdown"] if b["exact"]) for p in PREDICTIONS}
    _mex  = max(_exc, key=_exc.get)
    _dsts = {p: results[p]["dist"] for p in PREDICTIONS}
    _cls  = min(_dsts, key=_dsts.get)
    _bon  = {p: abs(results[p]["top6"]) + abs(results[p]["exact"]) for p in PREDICTIONS}
    _bk   = max(_bon, key=_bon.get)

    def _fc(label, val, sub, col=None):
        vc = f'style="color:{col}"' if col else ""
        return (f'<div class="fact-card"><div class="fact-label">{label}</div>'
                f'<div class="fact-value" {vc}>{val}</div>'
                f'<div class="fact-sub">{sub}</div></div>')

    _f3c = (_fc("📈 Biggest improvement", _bg2[0],
                f"-{abs(_bg2[2])} pts on MD{_bg2[1]}", COLORS[_bg2[0]])
            if _bg2 else _fc("📈 Biggest improvement", "—", "Not enough data yet"))

    mo.Html(f"""
    <div class="card">
      <div class="section-title">⚡ Prediction Battle Stats</div>
      <div class="fact-grid">
        {_fc("🥇 Current leader", _lp, f"{_ls['total']} pts · leads by {_gap12}", COLORS[_lp])}
        {_fc("✅ Most picks in top 6", _best_t6, f"{_t6counts[_best_t6]}/6 in actual top 6", COLORS[_best_t6])}
        {_f3c}
      </div>
      <div class="fact-grid">
        {_fc("🎯 Most exact picks", _mex, f"{_exc[_mex]} team(s) in exact position", COLORS[_mex])}
        {_fc("📏 Closest predictions", _cls, f"Total distance: {_dsts[_cls]}", COLORS[_cls])}
        {_fc("💰 Most bonus points", _bk, f"{_bon[_bk]} pts from bonuses", COLORS[_bk])}
      </div>
      <div class="section-title" style="margin-top:8px">📉 Points Gap to Leader over Time</div>
      <img class="chart-img" src="data:image/png;base64,{_b64_3}" />
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("""
    <details>
      <summary>📖 How the scoring works</summary>
      <div class="card" style="margin-top:10px">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;font-size:0.85rem">
          <div>
            <div style="color:#FF6B6B;font-family:monospace;font-weight:700;margin-bottom:6px">📏 Distance Penalty (+)</div>
            For each of your 6 picks, we measure how far they are from their actual position.
            Arsenal predicted at #3 but they're #5? That's +2. All 6 distances are summed.
            <b>Higher = worse.</b>
          </div>
          <div>
            <div style="color:#4FC3C3;font-family:monospace;font-weight:700;margin-bottom:6px">✅ Top-6 Bonus (−2 each)</div>
            For each predicted team that is actually in the real top 6 (at any position),
            you earn −2. Maximum −12 if all 6 picks land in the top 6.
          </div>
          <div>
            <div style="color:#FFD700;font-family:monospace;font-weight:700;margin-bottom:6px">🎯 Exact Pick Bonus (−5 each)</div>
            If a team is in the top 6 AND in the exact spot you predicted,
            you earn an additional −5. Maximum −30 for a perfect 6/6.
          </div>
        </div>
        <div style="margin-top:16px;padding-top:12px;border-top:1px solid #30363D;font-size:0.8rem;color:#8B949E;font-family:monospace">
          Example: Arsenal predicted #2, finish #4 → +2 (distance) −2 (top 6) = net 0<br>
          Example: Liverpool predicted #1, finish #1 → +0 (distance) −2 (top 6) −5 (exact) = −7
        </div>
      </div>
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, TEXT, base64, io, pe, plt):

    def make_evolution_chart(gw_scores_data, historical_data, season_label):
        fig, ax = plt.subplots(figsize=(12, 4), facecolor=BG)
        ax.set_facecolor(CARD)
        for sp in ax.spines.values():
            sp.set_edgecolor("#30363D")

        if historical_data:
            all_s = [s for pts in gw_scores_data.values() for _, s in pts]
            ymax  = max(all_s) + 1
            for p, pts in gw_scores_data.items():
                w = [ww for ww, _ in pts]
                s = [ss for _, ss in pts]
                c = COLORS[p]
                ax.fill_between(w, s, ymax + 2, alpha=0.07, color=c, zorder=1)
                ax.plot(w, s, color=c, lw=2.5, zorder=3, solid_capstyle="round",
                        marker="o", markersize=4, markerfacecolor=c, markeredgewidth=0)
                ax.plot(w[-1], s[-1], "o", ms=10, color=c, zorder=5,
                        markeredgecolor=BG, markeredgewidth=2)
                ax.text(w[-1]+0.25, s[-1], f" {p}  {s[-1]}", color=c,
                        fontsize=9, fontfamily="monospace", va="center", fontweight="bold",
                        path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)])
            gws = [ww for ww, _ in historical_data]
            ax.set_xlim(min(gws)-0.5, max(gws)+4)
            ax.invert_yaxis()
            ax.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
            ax.set_ylabel("Score  (↑ = better)", color=MUTED, fontsize=9, fontfamily="monospace")
            ax.text(0.01, 0.03, "↑ better", transform=ax.transAxes, color=MUTED, fontsize=8, fontfamily="monospace")
        else:
            ax.text(0.5, 0.5, "No data available",
                    ha="center", va="center", color=MUTED, fontsize=11, transform=ax.transAxes)

        ax.set_title(f"Prediction Score Evolution by Matchday — {season_label}",
                     color=TEXT, fontsize=11, fontfamily="monospace", pad=12)
        ax.tick_params(colors=MUTED)
        ax.grid(color="#30363D", lw=0.6, linestyle="--", alpha=0.6, zorder=0)
        fig.tight_layout(pad=1.5)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=BG)
        plt.close(fig); buf.seek(0)
        return base64.b64encode(buf.read()).decode()

    return (make_evolution_chart,)


@app.cell(hide_code=True)
def _(COLORS):

    def make_season_html(ranked_data, results_data, season_label, matchday_label, fetched, errors_list):
        medals = ["🥇", "🥈", "🥉"]

        def _rc(b): return "exact" if b["exact"] else ("top6" if b["in_top6"] else "")
        def _dc(b):
            if b["exact"]: return "d-good"
            return "d-bad" if b["dist"] > 3 else ("d-ok" if b["dist"] > 0 else "d-good")

        err_str = f" · ⚠️ {'; '.join(errors_list)}" if errors_list else ""

        lb_rows = ""
        for i, (p, _) in enumerate(ranked_data):
            s = results_data[p]; c = COLORS[p]
            lb_rows += f"""
            <div class="lb-row" style="border-color:{c}55">
              <span class="lb-medal">{medals[i]}</span>
              <span class="lb-name" style="color:{c}">{p}</span>
              <span class="lb-detail">
                <span>📏 dist: <b>+{s['dist']}</b></span>
                <span>✅ top-6: <b>{s['top6']}</b></span>
                <span>🎯 exact: <b>{s['exact']}</b></span>
              </span>
              <span class="lb-pts" style="color:{c}">{s['total']}</span>
            </div>"""

        pick_cards = ""
        for i, (p, _) in enumerate(ranked_data):
            c = COLORS[p]; s = results_data[p]
            rows = ""
            for b in s["breakdown"]:
                short = b["team"].replace(" FC","").replace(" United","").replace(" City"," C.").replace(" Hotspur","")
                rows += (f'<tr class="{_rc(b)}"><td style="color:#8B949E">{b["pred"]}</td>'
                         f'<td>{short}</td><td style="text-align:center">{b["actual"]}</td>'
                         f'<td style="text-align:center" class="{_dc(b)}">{b["dist"]}</td></tr>')
            legend = ('<tr><td colspan="4" style="padding-top:10px;font-size:0.7rem;color:#8B949E">'
                      '<span style="background:#1a2e1a;padding:2px 8px;border-radius:4px;color:#FFD700;margin-right:8px">🎯 exact (−5)</span>'
                      '<span style="background:#14232b;padding:2px 8px;border-radius:4px;color:#4FC3C3">✅ top-6 (−2)</span></td></tr>')
            pick_cards += (f'<div class="card" style="border-color:{c}44">'
                           f'<div class="section-title" style="color:{c}">{medals[i]} {p} &nbsp;·&nbsp;'
                           f'<span style="color:#E6EDF3;font-size:0.85rem">{s["total"]} pts</span></div>'
                           f'<table class="ptable"><thead><tr><th>#</th><th>Predicted</th>'
                           f'<th style="text-align:center">Actual</th><th style="text-align:center">Δ</th>'
                           f'</tr></thead><tbody>{rows}{legend}</tbody></table></div>')

        statusbar = f"""<div class="statusbar">
          <span>Final Season · {fetched}{err_str}</span>
          <span>{matchday_label}</span>
        </div>"""

        leaderboard = f"""<div class="card">
          <div class="section-title">🏆 Leaderboard — {season_label}</div>
          {lb_rows}
        </div>"""

        breakdown = f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px">
          {pick_cards}
        </div>"""

        return statusbar, leaderboard, breakdown

    return (make_season_html,)


@app.cell(hide_code=True)
def _(
    current_matchday_2024, current_table_2024, errors_2024, fetched_at_2024,
    gw_scores_2024, historical_2024, make_evolution_chart, make_season_html,
    mo, ranked_2024, results_2024,
):
    _md_label_2024 = f"Matchday {current_matchday_2024}" if current_matchday_2024 != "?" else "Final"
    _b64_ev_2024 = make_evolution_chart(gw_scores_2024, historical_2024, "2024/25")
    _statusbar_2024, _lb_2024, _bd_2024 = make_season_html(
        ranked_2024, results_2024,
        "2024/25 Season", _md_label_2024,
        fetched_at_2024, errors_2024,
    )

    mo.Html(f"""
    <details>
      <summary>📅 2024/25 Season — Final Results</summary>
      <div style="margin-top:16px">
        {_statusbar_2024}
        {_lb_2024}
        <div class="card">
          <div class="section-title">📈 Score Evolution</div>
          <img class="chart-img" src="data:image/png;base64,{_b64_ev_2024}" />
        </div>
        <div class="section-title">📋 Pick-by-pick Breakdown</div>
        {_bd_2024}
      </div>
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(
    current_matchday_2023, current_table_2023, errors_2023, fetched_at_2023,
    gw_scores_2023, historical_2023, make_evolution_chart, make_season_html,
    mo, ranked_2023, results_2023,
):
    _md_label_2023 = f"Matchday {current_matchday_2023}" if current_matchday_2023 != "?" else "Final"
    _b64_ev_2023 = make_evolution_chart(gw_scores_2023, historical_2023, "2023/24")
    _statusbar_2023, _lb_2023, _bd_2023 = make_season_html(
        ranked_2023, results_2023,
        "2023/24 Season", _md_label_2023,
        fetched_at_2023, errors_2023,
    )

    mo.Html(f"""
    <details>
      <summary>📅 2023/24 Season — Final Results</summary>
      <div style="margin-top:16px">
        {_statusbar_2023}
        {_lb_2023}
        <div class="card">
          <div class="section-title">📈 Score Evolution</div>
          <img class="chart-img" src="data:image/png;base64,{_b64_ev_2023}" />
        </div>
        <div class="section-title">📋 Pick-by-pick Breakdown</div>
        {_bd_2023}
      </div>
    </details>
    """)
    return


# ─── NEW: Bayesian SSM collapsible section ────────────────────────────────────
@app.cell(hide_code=True)
def _(
    BG, CARD, COLORS, MUTED, N_SIM_SEASON, PREDICTIONS, TEXT,
    base64, current_table, io, mo, mpatches, n_remaining,
    np, plt, pred_pos_dict, predicted_final_table,
    projected_ranked, projected_scores, ssm_ratings, ssm_teams,
):
    medals_ssm = ["🥇", "🥈", "🥉"]

    # ── Chart 1: Predicted final table (horizontal bar, pts) ────────────
    _fig_a, _ax_a = plt.subplots(figsize=(12, 6), facecolor=BG)
    _ax_a.set_facecolor(CARD)
    for _sp in _ax_a.spines.values(): _sp.set_edgecolor("#30363D")

    _names_a  = [r["name"].replace(" FC","").replace(" United","").replace(" Hotspur","")
                 for r in predicted_final_table]
    _pts_a    = [r["mean_pts"] for r in predicted_final_table]
    _curr_a   = [r["curr_pts"] for r in predicted_final_table]

    _colors_a = []
    for r in predicted_final_table:
        if r["pred_pos"] <= 4:    _colors_a.append("#60a5fa")
        elif r["pred_pos"] == 5:  _colors_a.append("#f59e0b")
        elif r["pred_pos"] == 6:  _colors_a.append("#8b5cf6")
        elif r["pred_pos"] >= 18: _colors_a.append("#f87171")
        else:                     _colors_a.append("#374151")

    _y_a = np.arange(len(_names_a))
    _bars_a  = _ax_a.barh(_y_a, _pts_a[::-1], color=_colors_a[::-1], alpha=0.75, height=0.6, label="Projected final pts")
    _ax_a.barh(_y_a, _curr_a[::-1], color=[c + "55" for c in _colors_a[::-1]], height=0.6, label="Current pts")

    for i, (bar, row) in enumerate(zip(_bars_a, reversed(predicted_final_table))):
        _ax_a.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   f"{row['mean_pts']:.0f} ± {row['std_pos']:.0f}  (top6: {row['top6_pct']:.0f}%)",
                   va="center", color=MUTED, fontsize=7.5, fontfamily="monospace")

    _ax_a.set_yticks(_y_a)
    _ax_a.set_yticklabels([n for n in reversed(_names_a)], fontsize=8.5, color=TEXT)
    _ax_a.set_xlabel("Points", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_a.set_title(f"Predicted Final Table — 2025/26  ({N_SIM_SEASON:,} simulations, {n_remaining} fixtures remaining)",
                    color=TEXT, fontsize=10, fontfamily="monospace", pad=12)
    _ax_a.tick_params(colors=MUTED)
    _ax_a.grid(axis="x", color="#30363D", lw=0.6, linestyle="--", alpha=0.6)
    _ax_a.set_xlim(0, max(_pts_a) + 18)
    _leg_a = [mpatches.Patch(color="#60a5fa", label="CL (1–4)"),
              mpatches.Patch(color="#f59e0b", label="EL (5)"),
              mpatches.Patch(color="#8b5cf6", label="Conf. (6)"),
              mpatches.Patch(color="#f87171", label="Relegation (18–20)"),
              mpatches.Patch(color="#4FC3C3", label="Projected pts"),
              mpatches.Patch(color="#4FC3C3aa", label="Current pts")]
    _ax_a.legend(handles=_leg_a, loc="lower right", framealpha=0.2, labelcolor=TEXT,
                 fontsize=7, facecolor=CARD, edgecolor="#30363D", ncol=2)
    _fig_a.tight_layout(pad=1.5)
    _buf_a = io.BytesIO()
    _fig_a.savefig(_buf_a, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig_a); _buf_a.seek(0)
    _b64_a = base64.b64encode(_buf_a.read()).decode()

    # ── Chart 2: Team strength ratings (attack vs defence scatter) ──────
    _fig_b, _ax_b = plt.subplots(figsize=(10, 6), facecolor=BG)
    _ax_b.set_facecolor(CARD)
    for _sp in _ax_b.spines.values(): _sp.set_edgecolor("#30363D")

    _all_pred_teams = {t.lower().replace(" fc","").strip() for picks in PREDICTIONS.values() for t in picks}
    def _is_pred_team(name):
        n = name.lower().replace(" fc","").strip()
        return any(n in p or p in n for p in _all_pred_teams)

    for team, rat in ssm_ratings.items():
        _is_p = _is_pred_team(team)
        _col  = "#6366f1" if _is_p else "#374151"
        _alpha = 0.9 if _is_p else 0.5
        _size  = 90 if _is_p else 50
        _ax_b.scatter(rat["atk"], rat["def"], color=_col, s=_size, alpha=_alpha, zorder=3,
                      edgecolors="#ffffff33", linewidth=0.5)
        _short = team.replace(" FC","").replace(" United","").replace(" Hotspur","").replace(" City","").replace("Brighton & Hove Albion","Brighton")
        _ax_b.annotate(_short, (rat["atk"], rat["def"]),
                       textcoords="offset points", xytext=(5, 3),
                       fontsize=7, color=TEXT if _is_p else MUTED, fontfamily="monospace",
                       fontweight="bold" if _is_p else "normal")

    # Quadrant lines at league average
    _atk_avg = np.mean([r["atk"] for r in ssm_ratings.values()])
    _def_avg = np.mean([r["def"] for r in ssm_ratings.values()])
    _ax_b.axvline(_atk_avg, color="#30363D", lw=1, linestyle="--", alpha=0.8)
    _ax_b.axhline(_def_avg, color="#30363D", lw=1, linestyle="--", alpha=0.8)

    _ax_b.set_xlabel("Attack strength α  (higher = more dangerous)", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_b.set_ylabel("Defence weakness δ  (lower = stronger defence)", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_b.set_title("Bayesian SSM Team Ratings — Posterior Means", color=TEXT, fontsize=10, fontfamily="monospace", pad=10)
    _ax_b.tick_params(colors=MUTED, labelsize=8)
    _ax_b.grid(color="#30363D", lw=0.4, linestyle="--", alpha=0.4)

    # Quadrant labels
    for txt, x, y, ha in [
        ("Strong attack\nStrong defence", 0.97, 0.03, "right"),
        ("Weak attack\nStrong defence",   0.03, 0.03, "left"),
        ("Strong attack\nWeak defence",   0.97, 0.97, "right"),
        ("Weak attack\nWeak defence",     0.03, 0.97, "left"),
    ]:
        _ax_b.text(x, y, txt, transform=_ax_b.transAxes, fontsize=7,
                   color="#ffffff22", ha=ha, va="top" if y > 0.5 else "bottom",
                   fontfamily="monospace")

    _leg_b = [mpatches.Patch(color="#6366f1", label="Predicted team"),
              mpatches.Patch(color="#374151", label="Other team")]
    _ax_b.legend(handles=_leg_b, loc="upper right", framealpha=0.2, labelcolor=TEXT,
                 fontsize=8, facecolor=CARD, edgecolor="#30363D")
    _fig_b.tight_layout(pad=1.5)
    _buf_b = io.BytesIO()
    _fig_b.savefig(_buf_b, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig_b); _buf_b.seek(0)
    _b64_b = base64.b64encode(_buf_b.read()).decode()

    # ── Predicted final table HTML ───────────────────────────────────────
    def _move_badge(curr, pred):
        diff = curr - pred
        if diff > 0:
            return f'<span class="ssm-badge ssm-up">▲ {diff}</span>'
        elif diff < 0:
            return f'<span class="ssm-badge ssm-down">▼ {abs(diff)}</span>'
        return '<span class="ssm-badge ssm-same">–</span>'

    _table_rows = ""
    for row in predicted_final_table:
        _short = row["name"].replace(" FC","").replace(" United","").replace(" Hotspur","")
        _pos_col = ("color:#60a5fa;" if row["pred_pos"] <= 4 else
                    "color:#f59e0b;" if row["pred_pos"] == 5 else
                    "color:#8b5cf6;" if row["pred_pos"] == 6 else
                    "color:#f87171;" if row["pred_pos"] >= 18 else "color:#8B949E;")
        _hl = "background:#1a1f2e;" if row["pred_pos"] <= 6 else ""
        _hl = "background:#2e1a1a;" if row["pred_pos"] >= 18 else _hl
        _is_p = _is_pred_team(row["name"])
        _bold = "font-weight:700;" if _is_p else ""
        _table_rows += (
            f'<tr style="{_hl}">'
            f'<td style="text-align:center;{_pos_col}font-family:monospace;font-weight:700">{row["pred_pos"]}</td>'
            f'<td style="{_bold}">{_short}</td>'
            f'<td style="text-align:center">{_move_badge(row["curr_pos"], row["pred_pos"])}</td>'
            f'<td style="text-align:center;color:#8B949E;font-family:monospace">{row["curr_pts"]}</td>'
            f'<td style="text-align:center;font-family:monospace;font-weight:700;color:#E6EDF3">{row["mean_pts"]:.0f}</td>'
            f'<td style="text-align:center;color:#8B949E;font-size:0.8rem">{row["std_pos"]:.1f}</td>'
            f'<td style="text-align:center;color:#60a5fa">{row["top4_pct"]:.0f}%</td>'
            f'<td style="text-align:center;color:#8b5cf6">{row["top6_pct"]:.0f}%</td>'
            f'<td style="text-align:center;color:#f87171">{row["rel_pct"]:.0f}%</td>'
            f'</tr>'
        )

    # ── Projected scores section ─────────────────────────────────────────
    def _rc_proj(_b): return "exact" if _b["exact"] else ("top6" if _b["in_top6"] else "")
    def _dc_proj(_b):
        if _b["exact"]: return "d-good"
        return "d-bad" if _b["dist"] > 3 else ("d-ok" if _b["dist"] > 0 else "d-good")

    _proj_lb = ""
    for _i, (_p, _) in enumerate(projected_ranked):
        _s = projected_scores[_p]; _c = COLORS[_p]
        _proj_lb += f"""
        <div class="lb-row" style="border-color:{_c}55">
          <span class="lb-medal">{medals_ssm[_i]}</span>
          <span class="lb-name" style="color:{_c}">{_p}</span>
          <span class="lb-detail">
            <span>📏 dist: <b>+{_s['dist']}</b></span>
            <span>✅ top-6: <b>{_s['top6']}</b></span>
            <span>🎯 exact: <b>{_s['exact']}</b></span>
          </span>
          <span class="lb-pts" style="color:{_c}">{_s['total']}</span>
        </div>"""

    _proj_cards = ""
    for _i, (_p, _) in enumerate(projected_ranked):
        _c = COLORS[_p]; _s = projected_scores[_p]
        _rows = ""
        for _b in _s["breakdown"]:
            _short = _b["team"].replace(" FC","").replace(" United","").replace(" City"," C.").replace(" Hotspur","")
            _rows += (f'<tr class="{_rc_proj(_b)}"><td style="color:#8B949E">{_b["pred"]}</td>'
                     f'<td>{_short}</td><td style="text-align:center">{_b["proj"]}</td>'
                     f'<td style="text-align:center" class="{_dc_proj(_b)}">{_b["dist"]}</td></tr>')
        _legend = ('<tr><td colspan="4" style="padding-top:10px;font-size:0.7rem;color:#8B949E">'
                  '<span style="background:#1a2e1a;padding:2px 8px;border-radius:4px;color:#FFD700;margin-right:8px">🎯 exact (−5)</span>'
                  '<span style="background:#14232b;padding:2px 8px;border-radius:4px;color:#4FC3C3">✅ top-6 (−2)</span></td></tr>')
        _proj_cards += (f'<div class="card" style="border-color:{_c}44">'
                        f'<div class="section-title" style="color:{_c}">{medals_ssm[_i]} {_p} &nbsp;·&nbsp;'
                        f'<span style="color:#E6EDF3;font-size:0.85rem">Projected: {_s["total"]} pts</span></div>'
                        f'<table class="ptable"><thead><tr><th>#</th><th>Predicted</th>'
                        f'<th style="text-align:center">Proj. Pos</th><th style="text-align:center">Δ</th>'
                        f'</tr></thead><tbody>{_rows}{_legend}</tbody></table></div>')

    # ── SSM ratings table ────────────────────────────────────────────────
    _sorted_ratings = sorted(ssm_ratings.items(), key=lambda _x: -_x[1]["net"])
    _ratings_rows = ""
    for _ri, (_team, _rat) in enumerate(_sorted_ratings):
        _short = _team.replace(" FC","").replace(" United","").replace(" Hotspur","")
        _is_p = _is_pred_team(_team)
        _bold = "font-weight:700;" if _is_p else ""
        _net_col = ("#22d3ee" if _ri < 4 else "#a78bfa" if _ri < 8 else "#f87171" if _ri >= 16 else "#94a3b8")
        _ratings_rows += (
            f'<tr><td style="text-align:center;color:#475569;font-family:monospace">{_ri+1}</td>'
            f'<td style="{_bold}">{_short}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_rat["atk"]:.3f}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_rat["def"]:.3f}</td>'
            f'<td style="text-align:center;color:{_net_col};font-family:monospace;font-weight:700">{_rat["net"]:.3f}</td>'
            f'</tr>'
        )

    mo.Html(f"""
    <details>
      <summary>🤖 Bayesian SSM — Season Forecast &amp; Projected Scores</summary>
      <div style="margin-top:16px">

        <div class="card" style="border-color:#6366f133">
          <div class="section-title" style="color:#a5b4fc">🧠 About the Model</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;font-size:0.82rem;color:#8B949E;line-height:1.7">
            <div>
              <span style="color:#22d3ee;font-family:monospace;font-weight:700">Gamma–Poisson Filter</span><br>
              Each team has latent attack α and defence δ drawn from Gamma posteriors.
              Goals are Poisson-distributed: λ_H = α_h/δ_a × e<sup>η</sup>.
              Bayesian conjugate updates after every match.
            </div>
            <div>
              <span style="color:#a78bfa;font-family:monospace;font-weight:700">Forgetting Factor φ=0.975</span><br>
              Applied after each match to inflate posterior variance,
              letting team strength drift over time. Recent form
              carries more weight than early-season results.
            </div>
            <div>
              <span style="color:#f59e0b;font-family:monospace;font-weight:700">Monte Carlo Completion</span><br>
              {N_SIM_SEASON:,} simulations of the remaining {n_remaining} fixtures.
              Each sim draws team strengths from posterior Gammas,
              samples Poisson goals, and records final standings.
            </div>
          </div>
        </div>

        <div class="card">
          <div class="section-title">📊 Predicted Final Table — 2025/26</div>
          <div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:24px;align-items:start">
            <table class="ptable">
              <thead><tr>
                <th style="text-align:center">Pos</th>
                <th>Club</th>
                <th style="text-align:center">Move</th>
                <th style="text-align:center">Cur Pts</th>
                <th style="text-align:center">Proj Pts</th>
                <th style="text-align:center">±Pos</th>
                <th style="text-align:center">Top 4</th>
                <th style="text-align:center">Top 6</th>
                <th style="text-align:center">Rel</th>
              </tr></thead>
              <tbody>{_table_rows}</tbody>
            </table>
            <div>
              <img class="chart-img" src="data:image/png;base64,{_b64_a}" />
              <div style="font-size:0.7rem;color:#8B949E;margin-top:8px;font-family:monospace">
                <b style="color:#E6EDF3">Bold</b> = predicted by someone &nbsp;·&nbsp;
                Proj Pts = mean across {N_SIM_SEASON:,} sims &nbsp;·&nbsp;
                ±Pos = std dev of final position
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="section-title">🏆 Projected Final Leaderboard (if season ends as predicted)</div>
          <div class="proj-highlight">
            <span style="font-size:0.8rem;color:#a5b4fc;font-family:monospace">
              📌 These scores apply the <em>same scoring rules</em> to the model's predicted final table.
              They show where each person is likely to finish if the SSM forecast is correct.
            </span>
          </div>
          {_proj_lb}
        </div>

        <div class="section-title">📋 Projected Pick-by-pick Breakdown</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:20px">
          {_proj_cards}
        </div>

        <div class="card">
          <div class="section-title">📡 Team Strength Ratings (Posterior Means)</div>
          <div style="display:grid;grid-template-columns:1fr 1.4fr;gap:24px;align-items:start">
            <table class="ptable">
              <thead><tr>
                <th style="text-align:center">#</th><th>Team</th>
                <th style="text-align:center">Attack α</th>
                <th style="text-align:center">Defence δ</th>
                <th style="text-align:center">Net (α/δ)</th>
              </tr></thead>
              <tbody>{_ratings_rows}</tbody>
            </table>
            <div>
              <img class="chart-img" src="data:image/png;base64,{_b64_b}" />
              <div style="font-size:0.7rem;color:#8B949E;margin-top:8px;font-family:monospace">
                Attack α: expected goals scored vs avg defence<br>
                Defence δ: expected goals conceded vs avg attack (lower = better)<br>
                Net = α/δ (higher = stronger team overall) &nbsp;·&nbsp; <b style="color:#E6EDF3">Bold</b> = predicted team
              </div>
            </div>
          </div>
        </div>

        <details style="margin-top:8px">
          <summary>📖 Model details &amp; caveats</summary>
          <div class="card" style="margin-top:10px;font-size:0.83rem;color:#8B949E;line-height:1.8">
            <p><b style="color:#E6EDF3">Bayesian State-Space Model</b> (Ridall, Titman &amp; Pettitt, 2024 — JRSS Series C).</p>
            <p>The model tracks each team's latent <em>attack strength α</em> and <em>defence weakness δ</em>
            as Gamma distributions updated sequentially after every match via the conjugate Gamma-Poisson relationship.
            Home advantage η ≈ 0.26 (≈ 1.30× goal multiplier) is held fixed.</p>
            <p>The <em>mean-field approximation</em> updates each team's parameters independently
            using posterior means of opponent strengths — avoiding MCMC while retaining accuracy.</p>
            <p><b style="color:#E6EDF3">Caveats:</b> The model treats all remaining fixtures as equally uncertain and
            does not account for injuries, suspensions, fixture congestion, or managerial changes.
            Simulations assume team strengths stay constant for remaining fixtures (no further forgetting).
            Projected scores are the expected outcome if the SSM point forecast is exactly right —
            treat them as directional, not precise.</p>
          </div>
        </details>
      </div>
    </details>
    """)
    return


# ── Render.com deployment ────────────────────────────────────────────────────
if __name__ == "__main__":
    # Render sets the port in the $PORT environment variable
    import os
    import sys
    
    print("=== DEPLOYMENT DEBUG ===")
    print(f"Python version: {sys.version}")
    print(f"Environment variables: {dict(os.environ)}")
    
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting marimo app on port {port}...")
        print(f"Host: 0.0.0.0, Port: {port}")
        print("About to call app.run...")
        app.run(host="0.0.0.0", port=port)
        print("app.run() completed")
    except Exception as e:
        print(f"Error starting app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)