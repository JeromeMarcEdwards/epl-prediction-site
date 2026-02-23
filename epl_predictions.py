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
    import io, base64, time
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

    PREDICTIONS_2024 = {
        "Jerome": ["Manchester City FC", "Arsenal FC", "Tottenham Hotspur FC",
                   "Chelsea FC", "Liverpool FC", "Manchester United FC"],
        "Alex":   ["Arsenal FC", "Manchester City FC", "Liverpool FC",
                   "Tottenham Hotspur FC", "Aston Villa FC", "Manchester United FC"],
        "Erin":   ["Manchester City FC", "Arsenal FC", "Tottenham Hotspur FC",
                   "Liverpool FC", "Chelsea FC", "Newcastle United FC"],
    }

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
        mpatches, pe, plt, requests, time,
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


# ─── Single batched API fetch cell ───────────────────────────────────────────
# All API calls happen here in sequence with small delays to respect rate limits.
@app.cell(hide_code=True)
def _(BASE, COLORS, EX_BON, HEADERS, PREDICTIONS, PREDICTIONS_2023,
      PREDICTIONS_2024, SEASON, T6_BON, datetime, defaultdict, refresh,
      requests, time):
    _ = refresh

    errors = []

    def _api(path, params=None):
        """Fetch from API with retry on 429."""
        for _attempt in range(3):
            try:
                _r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=15)
                if _r.status_code == 200:
                    return _r.json()
                if _r.status_code == 429:
                    time.sleep(7)  # wait and retry
                    continue
                errors.append(f"{path} → HTTP {_r.status_code}")
                return {}
            except Exception as _e:
                errors.append(f"{path} → {_e}")
                return {}
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

    def _build_historical(all_matches_list):
        _stats = {}
        _hist = []
        _gw = defaultdict(list)
        for _m in all_matches_list:
            if _m.get("status") == "FINISHED" and _m.get("matchday"):
                _gw[_m["matchday"]].append(_m)
        def _init(n):
            if n not in _stats:
                _stats[n] = {"pts": 0, "gf": 0, "ga": 0}
        for _md in sorted(_gw.keys()):
            for _m in _gw[_md]:
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
            _hist.append((_md, {n: i+1 for i, (n, _) in enumerate(_sorted)}))
        return _hist

    # ── Fetch all data with pacing (6 calls total, well within 10/min) ───
    # Call 1
    _sd_2025 = _api("/competitions/PL/standings", {"season": SEASON})
    time.sleep(1)
    # Call 2
    _md_2025 = _api("/competitions/PL/matches", {"season": SEASON})
    time.sleep(1)
    # Call 3
    _sc_2025 = _api("/competitions/PL/scorers", {"season": SEASON, "limit": 10})
    time.sleep(1)
    # Call 4
    _sd_2024 = _api("/competitions/PL/standings", {"season": 2024})
    time.sleep(1)
    # Call 5
    _md_2024 = _api("/competitions/PL/matches", {"season": 2024})
    time.sleep(1)
    # Call 6
    _sd_2023 = _api("/competitions/PL/standings", {"season": 2023})
    time.sleep(1)
    # Call 7
    _md_2023 = _api("/competitions/PL/matches", {"season": 2023})

    # ── Parse 2025/26 ─────────────────────────────────────────────────
    current_table = []
    for _s in _sd_2025.get("standings", []):
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

    actual_pos      = {t["name"]: t["pos"] for t in current_table}
    current_matchday = _sd_2025.get("season", {}).get("currentMatchday", "?")
    all_matches     = _md_2025.get("matches", [])
    historical      = _build_historical(all_matches)

    top_scorers = []
    for _sc in _sc_2025.get("scorers", []):
        top_scorers.append({
            "name": _sc["player"]["name"], "team": _sc["team"]["name"],
            "goals": _sc["goals"], "assists": _sc.get("assists") or 0,
        })

    upcoming = sorted(
        [{"home": _m["homeTeam"]["name"], "away": _m["awayTeam"]["name"],
          "date": _m.get("utcDate", ""), "md": _m.get("matchday")}
         for _m in all_matches if _m.get("status") in ("SCHEDULED", "TIMED")],
        key=lambda x: x["date"])[:15]

    recent = []
    for _m in reversed(all_matches):
        if _m.get("status") == "FINISHED":
            recent.append({"home": _m["homeTeam"]["name"], "away": _m["awayTeam"]["name"],
                           "hg": _m["score"]["fullTime"].get("home"),
                           "ag": _m["score"]["fullTime"].get("away"),
                           "md": _m.get("matchday"), "date": _m.get("utcDate", "")[:10]})
            if len(recent) == 10:
                break

    results  = {p: _score(picks, actual_pos) for p, picks in PREDICTIONS.items()}
    ranked   = sorted(results.items(), key=lambda x: x[1]["total"])
    gw_scores = {p: [(md, _score(picks, pos)["total"]) for md, pos in historical]
                 for p, picks in PREDICTIONS.items()}

    best_md = {}
    for _p, _pts in gw_scores.items():
        if len(_pts) >= 2:
            _deltas = [(w, s - _pts[i-1][1]) for i, (w, s) in enumerate(_pts) if i > 0]
            best_md[_p] = min(_deltas, key=lambda x: x[1])

    # ── Parse 2024/25 ─────────────────────────────────────────────────
    current_table_2024 = []
    for _s in _sd_2024.get("standings", []):
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

    actual_pos_2024      = {t["name"]: t["pos"] for t in current_table_2024}
    current_matchday_2024 = _sd_2024.get("season", {}).get("currentMatchday", "?")
    all_matches_2024     = _md_2024.get("matches", [])
    historical_2024      = _build_historical(all_matches_2024)
    results_2024  = {p: _score(picks, actual_pos_2024) for p, picks in PREDICTIONS_2024.items()}
    ranked_2024   = sorted(results_2024.items(), key=lambda x: x[1]["total"])
    gw_scores_2024 = {p: [(md, _score(picks, pos)["total"]) for md, pos in historical_2024]
                      for p, picks in PREDICTIONS_2024.items()}

    # ── Parse 2023/24 ─────────────────────────────────────────────────
    current_table_2023 = []
    for _s in _sd_2023.get("standings", []):
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

    actual_pos_2023      = {t["name"]: t["pos"] for t in current_table_2023}
    current_matchday_2023 = _sd_2023.get("season", {}).get("currentMatchday", "?")
    all_matches_2023     = _md_2023.get("matches", [])
    historical_2023      = _build_historical(all_matches_2023)
    results_2023  = {p: _score(picks, actual_pos_2023) for p, picks in PREDICTIONS_2023.items()}
    ranked_2023   = sorted(results_2023.items(), key=lambda x: x[1]["total"])
    gw_scores_2023 = {p: [(md, _score(picks, pos)["total"]) for md, pos in historical_2023]
                      for p, picks in PREDICTIONS_2023.items()}

    errors_2024 = []
    errors_2023 = []
    fetched_at = datetime.now().strftime("%d %b %Y · %H:%M")

    return (
        actual_pos, actual_pos_2023, actual_pos_2024,
        all_matches, all_matches_2023, all_matches_2024,
        best_md, current_matchday, current_matchday_2023, current_matchday_2024,
        current_table, current_table_2023, current_table_2024,
        errors, errors_2023, errors_2024, fetched_at,
        gw_scores, gw_scores_2023, gw_scores_2024,
        historical, historical_2023, historical_2024,
        ranked, ranked_2023, ranked_2024,
        recent, results, results_2023, results_2024,
        top_scorers, upcoming,
    )


# ─── Bayesian SSM cell ────────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(EX_BON, PREDICTIONS, T6_BON, all_matches, current_table, np):
    _PRIOR_SHAPE = 4.0
    _PRIOR_RATE  = 4.0
    _PHI_WITHIN  = 0.975
    _ETA         = 0.26
    N_SIM_SEASON = 5000

    _ssm_teams = sorted({_t["name"] for _t in current_table})
    _n_teams   = len(_ssm_teams)
    _idx       = {_t: _ii for _ii, _t in enumerate(_ssm_teams)}

    _a = np.full(_n_teams, _PRIOR_SHAPE)
    _b = np.full(_n_teams, _PRIOR_RATE)
    _c = np.full(_n_teams, _PRIOR_SHAPE)
    _d = np.full(_n_teams, _PRIOR_RATE)

    def _inv_mean(_ci, _di):
        return _di / (_ci - 1) if _ci > 1 else _di / _ci

    def _ssm_update(_hi, _ai, _hg, _ag):
        _C_H = _inv_mean(_c[_ai], _d[_ai]) * np.exp(_ETA)
        _C_A = _inv_mean(_c[_hi], _d[_hi])
        _D_A = (_a[_hi] / _b[_hi]) * np.exp(_ETA)
        _D_H = (_a[_ai] / _b[_ai]) / np.exp(_ETA)
        _a[_hi] += _hg;  _b[_hi] += _C_H
        _a[_ai] += _ag;  _b[_ai] += _C_A
        _c[_hi] += _ag;  _d[_hi] += _D_A
        _c[_ai] += _hg;  _d[_ai] += _D_H
        for _fi in [_hi, _ai]:
            _a[_fi] *= _PHI_WITHIN;  _b[_fi] *= _PHI_WITHIN
            _c[_fi] *= _PHI_WITHIN;  _d[_fi] *= _PHI_WITHIN

    _finished = sorted(
        [_m for _m in all_matches if _m.get("status") == "FINISHED"],
        key=lambda _m: _m.get("utcDate", ""))
    for _m in _finished:
        _hn = _m["homeTeam"]["name"]
        _an = _m["awayTeam"]["name"]
        _hg = _m["score"]["fullTime"].get("home")
        _ag = _m["score"]["fullTime"].get("away")
        if _hn in _idx and _an in _idx and _hg is not None and _ag is not None:
            _ssm_update(_idx[_hn], _idx[_an], int(_hg), int(_ag))

    _remaining = [
        _m for _m in all_matches
        if _m.get("status") in ("SCHEDULED", "TIMED")
        and _m["homeTeam"]["name"] in _idx
        and _m["awayTeam"]["name"] in _idx
    ]
    n_remaining = len(_remaining)

    _current_pts = {_t["name"]: _t["pts"]                    for _t in current_table}
    _current_gf  = {_t["name"]: _t["gf"]                     for _t in current_table}
    _current_gd  = {_t["name"]: _t.get("goalDifference", 0)   for _t in current_table}

    ssm_ratings = {}
    for _tm in _ssm_teams:
        _ii  = _idx[_tm]
        _atk = _a[_ii] / _b[_ii]
        _dfc = _c[_ii] / _d[_ii]
        ssm_ratings[_tm] = {
            "atk": round(_atk, 3), "def": round(_dfc, 3),
            "net": round(_atk / _dfc, 3),
            "atk_sd": round(np.sqrt(_a[_ii] / _b[_ii]**2), 3),
            "def_sd": round(np.sqrt(_c[_ii] / _d[_ii]**2), 3),
        }

    _rng = np.random.default_rng(42)
    _atk_s = np.clip(_rng.gamma(_a, 1.0 / _b, size=(N_SIM_SEASON, _n_teams)), 0.05, 10)
    _def_s = np.clip(_rng.gamma(_c, 1.0 / _d, size=(N_SIM_SEASON, _n_teams)), 0.05, 10)

    _sim_pts = {_t: np.full(N_SIM_SEASON, _current_pts.get(_t, 0), dtype=float) for _t in _ssm_teams}
    _sim_gd  = {_t: np.full(N_SIM_SEASON, _current_gd.get(_t, 0),  dtype=float) for _t in _ssm_teams}
    _sim_gf  = {_t: np.full(N_SIM_SEASON, _current_gf.get(_t, 0),  dtype=float) for _t in _ssm_teams}

    for _m in _remaining:
        _hn2 = _m["homeTeam"]["name"]; _an2 = _m["awayTeam"]["name"]
        _hi2 = _idx[_hn2];            _ai2 = _idx[_an2]
        _lH  = np.clip(_atk_s[:, _hi2] / _def_s[:, _ai2] * np.exp(_ETA), 0.05, 10)
        _lA  = np.clip(_atk_s[:, _ai2] / _def_s[:, _hi2], 0.05, 10)
        _hgs = _rng.poisson(_lH);  _ags = _rng.poisson(_lA)
        _hw  = _hgs > _ags;  _dr = _hgs == _ags;  _aw = _ags > _hgs
        _sim_pts[_hn2] += np.where(_hw, 3, np.where(_dr, 1, 0))
        _sim_pts[_an2] += np.where(_aw, 3, np.where(_dr, 1, 0))
        _sim_gd[_hn2]  += (_hgs - _ags).astype(float)
        _sim_gd[_an2]  += (_ags - _hgs).astype(float)
        _sim_gf[_hn2]  += _hgs.astype(float)
        _sim_gf[_an2]  += _ags.astype(float)

    _pm = np.stack([_sim_pts[_t] for _t in _ssm_teams], axis=1)
    _gm = np.stack([_sim_gd[_t]  for _t in _ssm_teams], axis=1)
    _fm = np.stack([_sim_gf[_t]  for _t in _ssm_teams], axis=1)
    _sk = np.stack([-_pm, -_gm, -_fm], axis=2)

    _ranks = np.zeros((N_SIM_SEASON, _n_teams), dtype=int)
    for _si in range(N_SIM_SEASON):
        _order = np.lexsort((_sk[_si, :, 2], _sk[_si, :, 1], _sk[_si, :, 0]))
        _ranks[_si, _order] = np.arange(1, _n_teams + 1)

    _mean_pos  = _ranks.mean(axis=0)
    _std_pos   = _ranks.std(axis=0)
    _top4_prob = (_ranks <= 4).mean(axis=0)
    _top6_prob = (_ranks <= 6).mean(axis=0)
    _rel_prob  = (_ranks >= 18).mean(axis=0)
    _mean_pts  = np.array([_sim_pts[_t].mean() for _t in _ssm_teams])

    _pred_order = np.argsort(_mean_pos)
    predicted_final_table = []
    for _ri, _ti in enumerate(_pred_order):
        _tm = _ssm_teams[_ti]
        _cp = next((_t["pos"] for _t in current_table if _t["name"] == _tm), _ri + 1)
        predicted_final_table.append({
            "pred_pos": _ri + 1, "curr_pos": _cp, "name": _tm,
            "mean_pos": round(float(_mean_pos[_ti]), 1),
            "std_pos":  round(float(_std_pos[_ti]),  1),
            "mean_pts": round(float(_mean_pts[_ti]), 1),
            "curr_pts": _current_pts.get(_tm, 0),
            "top4_pct": round(float(_top4_prob[_ti]) * 100, 1),
            "top6_pct": round(float(_top6_prob[_ti]) * 100, 1),
            "rel_pct":  round(float(_rel_prob[_ti])  * 100, 1),
        })

    pred_pos_dict = {_row["name"]: _row["pred_pos"] for _row in predicted_final_table}

    def _fuzzy_ssm(_t, _pd):
        if _t in _pd: return _pd[_t]
        _tl = _t.lower().replace(" fc","").strip()
        for _k, _v in _pd.items():
            _kl = _k.lower().replace(" fc","").strip()
            if _tl in _kl or _kl in _tl: return _v
            if len(set(_tl.split()) & set(_kl.split())) >= 2: return _v
        return None

    def _score_ssm(_picks, _pd):
        _top6 = {_t for _t, _pp in _pd.items() if _pp <= 6}
        _dt = _tb = _eb = 0; _bk = []
        for _pr, _tm in enumerate(_picks, 1):
            _ar = _fuzzy_ssm(_tm, _pd)
            if _ar is None:
                _bk.append({"team": _tm, "pred": _pr, "proj": "?", "dist": 0, "in_top6": False, "exact": False})
                continue
            _dist = abs(_pr - _ar)
            _in_t6 = any(_tm.lower().replace(" fc","") in _t.lower() or _t.lower() in _tm.lower() for _t in _top6)
            _exact = (_pr == _ar)
            _dt += _dist
            if _in_t6: _tb += T6_BON
            if _exact: _eb += EX_BON
            _bk.append({"team": _tm, "pred": _pr, "proj": _ar, "dist": _dist, "in_top6": _in_t6, "exact": _exact})
        return {"dist": _dt, "top6": _tb, "exact": _eb, "total": _dt + _tb + _eb, "breakdown": _bk}

    projected_scores = {_p: _score_ssm(_picks, pred_pos_dict) for _p, _picks in PREDICTIONS.items()}
    projected_ranked = sorted(projected_scores.items(), key=lambda _x: _x[1]["total"])
    ssm_teams = _ssm_teams

    return (
        N_SIM_SEASON, n_remaining, pred_pos_dict, predicted_final_table,
        projected_ranked, projected_scores, ssm_ratings, ssm_teams,
    )


# ─── Leaderboard ─────────────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(COLORS, mo, ranked, results):
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


# ─── Score evolution chart ────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, TEXT, base64, gw_scores, historical, io, mo, pe, plt):
    _fig, _ax = plt.subplots(figsize=(12, 4), facecolor=BG)
    _ax.set_facecolor(CARD)
    for _sp in _ax.spines.values(): _sp.set_edgecolor("#30363D")

    if historical:
        _all_s = [s for pts in gw_scores.values() for _, s in pts]
        _ymax  = max(_all_s) + 1
        for _p, _pts in gw_scores.items():
            _w = [w for w, _ in _pts]; _s = [s for _, s in _pts]; _c = COLORS[_p]
            _ax.fill_between(_w, _s, _ymax + 2, alpha=0.07, color=_c, zorder=1)
            _ax.plot(_w, _s, color=_c, lw=2.5, zorder=3, solid_capstyle="round",
                     marker="o", markersize=4, markerfacecolor=_c, markeredgewidth=0)
            _ax.plot(_w[-1], _s[-1], "o", ms=10, color=_c, zorder=5, markeredgecolor=BG, markeredgewidth=2)
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

    _ax.set_title("Prediction Score Evolution by Matchday — 2025/26",
                  color=TEXT, fontsize=11, fontfamily="monospace", pad=12)
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


# ─── Pick-by-pick breakdown ───────────────────────────────────────────────────
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


# ─── Current table + bar chart ────────────────────────────────────────────────
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
        _pcol  = ("color:#60a5fa;" if _pos <= 4 else "color:#f59e0b;" if _pos == 5 else
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


# ─── Top scorers ─────────────────────────────────────────────────────────────
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


# ─── Fixtures ─────────────────────────────────────────────────────────────────
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


# ─── Battle stats + gap chart ─────────────────────────────────────────────────
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
            t.lower().replace(" fc","") in tn.lower() or tn.lower() in t.lower() for tn in _top6n))
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

    _f3c = (_fc("📈 Biggest improvement", _bg2[0], f"-{abs(_bg2[2])} pts on MD{_bg2[1]}", COLORS[_bg2[0]])
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


# ─── Scoring explainer ────────────────────────────────────────────────────────
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


# ─── Helper functions for season archives ────────────────────────────────────
@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, TEXT, base64, io, pe, plt):
    def make_evolution_chart(gw_scores_data, historical_data, season_label):
        fig, ax = plt.subplots(figsize=(12, 4), facecolor=BG)
        ax.set_facecolor(CARD)
        for sp in ax.spines.values(): sp.set_edgecolor("#30363D")
        if historical_data:
            all_s = [s for pts in gw_scores_data.values() for _, s in pts]
            ymax  = max(all_s) + 1
            for p, pts in gw_scores_data.items():
                w = [ww for ww, _ in pts]; s = [ss for _, ss in pts]; c = COLORS[p]
                ax.fill_between(w, s, ymax + 2, alpha=0.07, color=c, zorder=1)
                ax.plot(w, s, color=c, lw=2.5, zorder=3, solid_capstyle="round",
                        marker="o", markersize=4, markerfacecolor=c, markeredgewidth=0)
                ax.plot(w[-1], s[-1], "o", ms=10, color=c, zorder=5, markeredgecolor=BG, markeredgewidth=2)
                ax.text(w[-1]+0.25, s[-1], f" {p}  {s[-1]}", color=c,
                        fontsize=9, fontfamily="monospace", va="center", fontweight="bold",
                        path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)])
            gws = [ww for ww, _ in historical_data]
            ax.set_xlim(min(gws)-0.5, max(gws)+4)
            ax.invert_yaxis()
            ax.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
            ax.set_ylabel("Score  (↑ = better)", color=MUTED, fontsize=9, fontfamily="monospace")
        else:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center",
                    color=MUTED, fontsize=11, transform=ax.transAxes)
        ax.set_title(f"Score Evolution — {season_label}", color=TEXT, fontsize=11, fontfamily="monospace", pad=12)
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
        statusbar = f'<div class="statusbar"><span>Final Season · {fetched}{err_str}</span><span>{matchday_label}</span></div>'
        leaderboard = f'<div class="card"><div class="section-title">🏆 Leaderboard — {season_label}</div>{lb_rows}</div>'
        breakdown = f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px">{pick_cards}</div>'
        return statusbar, leaderboard, breakdown
    return (make_season_html,)


# ─── 2024/25 archive ─────────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(
    current_matchday_2024, errors_2024, fetched_at,
    gw_scores_2024, historical_2024, make_evolution_chart, make_season_html,
    mo, ranked_2024, results_2024,
):
    _md_label_2024 = f"Matchday {current_matchday_2024}" if current_matchday_2024 != "?" else "Final"
    _b64_ev_2024 = make_evolution_chart(gw_scores_2024, historical_2024, "2024/25")
    _statusbar_2024, _lb_2024, _bd_2024 = make_season_html(
        ranked_2024, results_2024, "2024/25 Season", _md_label_2024, fetched_at, errors_2024)
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


# ─── 2023/24 archive ─────────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(
    current_matchday_2023, errors_2023, fetched_at,
    gw_scores_2023, historical_2023, make_evolution_chart, make_season_html,
    mo, ranked_2023, results_2023,
):
    _md_label_2023 = f"Matchday {current_matchday_2023}" if current_matchday_2023 != "?" else "Final"
    _b64_ev_2023 = make_evolution_chart(gw_scores_2023, historical_2023, "2023/24")
    _statusbar_2023, _lb_2023, _bd_2023 = make_season_html(
        ranked_2023, results_2023, "2023/24 Season", _md_label_2023, fetched_at, errors_2023)
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


# ─── Bayesian SSM display ─────────────────────────────────────────────────────
@app.cell(hide_code=True)
def _(
    BG, CARD, COLORS, MUTED, N_SIM_SEASON, PREDICTIONS, TEXT,
    base64, current_table, io, mo, mpatches, n_remaining,
    np, plt, predicted_final_table,
    projected_ranked, projected_scores, ssm_ratings, ssm_teams,
):
    _medals_ssm = ["🥇", "🥈", "🥉"]

    # ── Chart 1: projected points bar chart ──────────────────────────
    _fig_a, _ax_a = plt.subplots(figsize=(12, 6), facecolor=BG)
    _ax_a.set_facecolor(CARD)
    for _sp in _ax_a.spines.values(): _sp.set_edgecolor("#30363D")
    _names_a = [r["name"].replace(" FC","").replace(" United","").replace(" Hotspur","") for r in predicted_final_table]
    _pts_a   = [r["mean_pts"] for r in predicted_final_table]
    _curr_a  = [r["curr_pts"] for r in predicted_final_table]
    _colors_a = []
    for _r in predicted_final_table:
        if _r["pred_pos"] <= 4:    _colors_a.append("#60a5fa")
        elif _r["pred_pos"] == 5:  _colors_a.append("#f59e0b")
        elif _r["pred_pos"] == 6:  _colors_a.append("#8b5cf6")
        elif _r["pred_pos"] >= 18: _colors_a.append("#f87171")
        else:                      _colors_a.append("#374151")
    _y_a    = np.arange(len(_names_a))
    _bars_a = _ax_a.barh(_y_a, _pts_a[::-1], color=_colors_a[::-1], alpha=0.75, height=0.6)
    _ax_a.barh(_y_a, _curr_a[::-1], color=[_co + "55" for _co in _colors_a[::-1]], height=0.6)
    for _ib, (_bar, _row) in enumerate(zip(_bars_a, reversed(predicted_final_table))):
        _ax_a.text(_bar.get_width() + 0.5, _bar.get_y() + _bar.get_height()/2,
                   f"{_row['mean_pts']:.0f} ± {_row['std_pos']:.0f}  (top6: {_row['top6_pct']:.0f}%)",
                   va="center", color=MUTED, fontsize=7.5, fontfamily="monospace")
    _ax_a.set_yticks(_y_a)
    _ax_a.set_yticklabels(list(reversed(_names_a)), fontsize=8.5, color=TEXT)
    _ax_a.set_xlabel("Points", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_a.set_title(f"Predicted Final Table — 2025/26  ({N_SIM_SEASON:,} sims, {n_remaining} fixtures left)",
                    color=TEXT, fontsize=10, fontfamily="monospace", pad=12)
    _ax_a.tick_params(colors=MUTED)
    _ax_a.grid(axis="x", color="#30363D", lw=0.6, linestyle="--", alpha=0.6)
    _ax_a.set_xlim(0, max(_pts_a) + 18 if _pts_a else 100)
    _leg_a = [mpatches.Patch(color="#60a5fa", label="CL (1–4)"),
              mpatches.Patch(color="#f59e0b", label="EL (5)"),
              mpatches.Patch(color="#8b5cf6", label="Conf. (6)"),
              mpatches.Patch(color="#f87171", label="Relegation (18–20)")]
    _ax_a.legend(handles=_leg_a, loc="lower right", framealpha=0.2, labelcolor=TEXT,
                 fontsize=7, facecolor=CARD, edgecolor="#30363D", ncol=2)
    _fig_a.tight_layout(pad=1.5)
    _buf_a = io.BytesIO()
    _fig_a.savefig(_buf_a, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig_a); _buf_a.seek(0)
    _b64_a = base64.b64encode(_buf_a.read()).decode()

    # ── Chart 2: attack vs defence scatter ───────────────────────────
    _fig_b, _ax_b = plt.subplots(figsize=(10, 6), facecolor=BG)
    _ax_b.set_facecolor(CARD)
    for _sp in _ax_b.spines.values(): _sp.set_edgecolor("#30363D")
    _all_pred_teams = {_t.lower().replace(" fc","").strip() for _pk in PREDICTIONS.values() for _t in _pk}
    def _is_pred_team(_name):
        _n = _name.lower().replace(" fc","").strip()
        return any(_n in _pp or _pp in _n for _pp in _all_pred_teams)
    for _tm, _rat in ssm_ratings.items():
        _is_p = _is_pred_team(_tm)
        _ax_b.scatter(_rat["atk"], _rat["def"],
                      color="#6366f1" if _is_p else "#374151",
                      s=90 if _is_p else 50, alpha=0.9 if _is_p else 0.5,
                      zorder=3, edgecolors="#ffffff33", linewidth=0.5)
        _short = (_tm.replace(" FC","").replace(" United","").replace(" Hotspur","")
                     .replace(" City","").replace("Brighton & Hove Albion","Brighton"))
        _ax_b.annotate(_short, (_rat["atk"], _rat["def"]),
                       textcoords="offset points", xytext=(5, 3),
                       fontsize=7, color=TEXT if _is_p else MUTED, fontfamily="monospace",
                       fontweight="bold" if _is_p else "normal")
    _ax_b.axvline(np.mean([r["atk"] for r in ssm_ratings.values()]), color="#30363D", lw=1, linestyle="--")
    _ax_b.axhline(np.mean([r["def"] for r in ssm_ratings.values()]), color="#30363D", lw=1, linestyle="--")
    _ax_b.set_xlabel("Attack α  (higher = more dangerous)", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_b.set_ylabel("Defence δ  (lower = stronger)", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax_b.set_title("Bayesian SSM — Team Strength Ratings", color=TEXT, fontsize=10, fontfamily="monospace", pad=10)
    _ax_b.tick_params(colors=MUTED, labelsize=8)
    _ax_b.grid(color="#30363D", lw=0.4, linestyle="--", alpha=0.4)
    _ax_b.legend(handles=[mpatches.Patch(color="#6366f1", label="Predicted team"),
                           mpatches.Patch(color="#374151", label="Other team")],
                 loc="upper right", framealpha=0.2, labelcolor=TEXT, fontsize=8,
                 facecolor=CARD, edgecolor="#30363D")
    _fig_b.tight_layout(pad=1.5)
    _buf_b = io.BytesIO()
    _fig_b.savefig(_buf_b, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig_b); _buf_b.seek(0)
    _b64_b = base64.b64encode(_buf_b.read()).decode()

    # ── Predicted table HTML ─────────────────────────────────────────
    def _move_badge(_curr, _pred):
        _diff = _curr - _pred
        if _diff > 0:  return f'<span class="ssm-badge ssm-up">▲ {_diff}</span>'
        if _diff < 0:  return f'<span class="ssm-badge ssm-down">▼ {abs(_diff)}</span>'
        return '<span class="ssm-badge ssm-same">–</span>'

    _table_rows = ""
    for _row in predicted_final_table:
        _short = _row["name"].replace(" FC","").replace(" United","").replace(" Hotspur","")
        _pos_col = ("color:#60a5fa;" if _row["pred_pos"] <= 4 else
                    "color:#f59e0b;" if _row["pred_pos"] == 5 else
                    "color:#8b5cf6;" if _row["pred_pos"] == 6 else
                    "color:#f87171;" if _row["pred_pos"] >= 18 else "color:#8B949E;")
        _hl   = "background:#2e1a1a;" if _row["pred_pos"] >= 18 else ("background:#1a1f2e;" if _row["pred_pos"] <= 6 else "")
        _bold = "font-weight:700;" if _is_pred_team(_row["name"]) else ""
        _table_rows += (
            f'<tr style="{_hl}">'
            f'<td style="text-align:center;{_pos_col}font-family:monospace;font-weight:700">{_row["pred_pos"]}</td>'
            f'<td style="{_bold}">{_short}</td>'
            f'<td style="text-align:center">{_move_badge(_row["curr_pos"], _row["pred_pos"])}</td>'
            f'<td style="text-align:center;color:#8B949E;font-family:monospace">{_row["curr_pts"]}</td>'
            f'<td style="text-align:center;font-family:monospace;font-weight:700;color:#E6EDF3">{_row["mean_pts"]:.0f}</td>'
            f'<td style="text-align:center;color:#8B949E;font-size:0.8rem">{_row["std_pos"]:.1f}</td>'
            f'<td style="text-align:center;color:#60a5fa">{_row["top4_pct"]:.0f}%</td>'
            f'<td style="text-align:center;color:#8b5cf6">{_row["top6_pct"]:.0f}%</td>'
            f'<td style="text-align:center;color:#f87171">{_row["rel_pct"]:.0f}%</td>'
            f'</tr>'
        )

    # ── Projected leaderboard ─────────────────────────────────────────
    _proj_lb = ""
    for _pi, (_pp, _) in enumerate(projected_ranked):
        _ps = projected_scores[_pp]; _pc = COLORS[_pp]
        _proj_lb += f"""
        <div class="lb-row" style="border-color:{_pc}55">
          <span class="lb-medal">{_medals_ssm[_pi]}</span>
          <span class="lb-name" style="color:{_pc}">{_pp}</span>
          <span class="lb-detail">
            <span>📏 dist: <b>+{_ps['dist']}</b></span>
            <span>✅ top-6: <b>{_ps['top6']}</b></span>
            <span>🎯 exact: <b>{_ps['exact']}</b></span>
          </span>
          <span class="lb-pts" style="color:{_pc}">{_ps['total']}</span>
        </div>"""

    def _rc_proj(_bx): return "exact" if _bx["exact"] else ("top6" if _bx["in_top6"] else "")
    def _dc_proj(_bx):
        if _bx["exact"]: return "d-good"
        return "d-bad" if _bx["dist"] > 3 else ("d-ok" if _bx["dist"] > 0 else "d-good")

    _proj_cards = ""
    for _pi, (_pp, _) in enumerate(projected_ranked):
        _pc = COLORS[_pp]; _ps = projected_scores[_pp]
        _prows = ""
        for _bx in _ps["breakdown"]:
            _bshort = _bx["team"].replace(" FC","").replace(" United","").replace(" City"," C.").replace(" Hotspur","")
            _prows += (f'<tr class="{_rc_proj(_bx)}"><td style="color:#8B949E">{_bx["pred"]}</td>'
                       f'<td>{_bshort}</td><td style="text-align:center">{_bx["proj"]}</td>'
                       f'<td style="text-align:center" class="{_dc_proj(_bx)}">{_bx["dist"]}</td></tr>')
        _plegend = ('<tr><td colspan="4" style="padding-top:10px;font-size:0.7rem;color:#8B949E">'
                    '<span style="background:#1a2e1a;padding:2px 8px;border-radius:4px;color:#FFD700;margin-right:8px">🎯 exact (−5)</span>'
                    '<span style="background:#14232b;padding:2px 8px;border-radius:4px;color:#4FC3C3">✅ top-6 (−2)</span></td></tr>')
        _proj_cards += (f'<div class="card" style="border-color:{_pc}44">'
                        f'<div class="section-title" style="color:{_pc}">{_medals_ssm[_pi]} {_pp} &nbsp;·&nbsp;'
                        f'<span style="color:#E6EDF3;font-size:0.85rem">Projected: {_ps["total"]} pts</span></div>'
                        f'<table class="ptable"><thead><tr><th>#</th><th>Predicted</th>'
                        f'<th style="text-align:center">Proj. Pos</th><th style="text-align:center">Δ</th>'
                        f'</tr></thead><tbody>{_prows}{_plegend}</tbody></table></div>')

    # ── Ratings table ─────────────────────────────────────────────────
    _sorted_ratings = sorted(ssm_ratings.items(), key=lambda _x: -_x[1]["net"])
    _ratings_rows = ""
    for _ri, (_rteam, _rat) in enumerate(_sorted_ratings):
        _rshort = _rteam.replace(" FC","").replace(" United","").replace(" Hotspur","")
        _rbold  = "font-weight:700;" if _is_pred_team(_rteam) else ""
        _rnet_col = "#22d3ee" if _ri < 4 else "#a78bfa" if _ri < 8 else "#f87171" if _ri >= 16 else "#94a3b8"
        _ratings_rows += (
            f'<tr><td style="text-align:center;color:#475569;font-family:monospace">{_ri+1}</td>'
            f'<td style="{_rbold}">{_rshort}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_rat["atk"]:.3f}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_rat["def"]:.3f}</td>'
            f'<td style="text-align:center;color:{_rnet_col};font-family:monospace;font-weight:700">{_rat["net"]:.3f}</td>'
            f'</tr>'
        )

    mo.Html(f"""
    <details>
      <summary>🤖 Bayesian SSM — Season Forecast &amp; Projected Scores</summary>
      <div style="margin-top:16px">
        <div class="card" style="border-color:#6366f133">
          <div class="section-title" style="color:#a5b4fc">🧠 About the Model</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;font-size:0.82rem;color:#8B949E;line-height:1.7">
            <div><span style="color:#22d3ee;font-family:monospace;font-weight:700">Gamma–Poisson Filter</span><br>
              Each team has latent attack α and defence δ drawn from Gamma posteriors.
              Goals are Poisson-distributed: λ_H = α_h/δ_a × e<sup>η</sup>.
              Bayesian conjugate updates after every match.</div>
            <div><span style="color:#a78bfa;font-family:monospace;font-weight:700">Forgetting Factor φ=0.975</span><br>
              Applied after each match to inflate posterior variance,
              letting team strength drift. Recent form carries more weight.</div>
            <div><span style="color:#f59e0b;font-family:monospace;font-weight:700">Monte Carlo Completion</span><br>
              {N_SIM_SEASON:,} simulations of the remaining {n_remaining} fixtures.
              Each sim draws strengths from posterior Gammas and records final standings.</div>
          </div>
        </div>
        <div class="card">
          <div class="section-title">📊 Predicted Final Table — 2025/26</div>
          <div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:24px;align-items:start">
            <table class="ptable">
              <thead><tr>
                <th style="text-align:center">Pos</th><th>Club</th>
                <th style="text-align:center">Move</th><th style="text-align:center">Cur Pts</th>
                <th style="text-align:center">Proj Pts</th><th style="text-align:center">±Pos</th>
                <th style="text-align:center">Top 4</th><th style="text-align:center">Top 6</th>
                <th style="text-align:center">Rel</th>
              </tr></thead>
              <tbody>{_table_rows}</tbody>
            </table>
            <img class="chart-img" src="data:image/png;base64,{_b64_a}" />
          </div>
        </div>
        <div class="card">
          <div class="section-title">🏆 Projected Final Leaderboard</div>
          <div class="proj-highlight">
            <span style="font-size:0.8rem;color:#a5b4fc;font-family:monospace">
              📌 Applies the same scoring rules to the SSM's predicted final table.
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
            <img class="chart-img" src="data:image/png;base64,{_b64_b}" />
          </div>
        </div>
      </div>
    </details>
    """)
    return


# ─── Multi-season SSM: paper-faithful implementation ─────────────────────────
# Based on Ridall, Titman & Pettitt (2024) JRSS-C.
# Key improvements vs old approach:
#   1. Data from football-data.co.uk (free CSVs, no API rate limits, all seasons)
#   2. Cross-season state carry-over with a *between-season* forgetting factor φ_B
#      distinct from the within-season φ_W — faithful to the paper's SSM structure
#   3. Proper identifiability: defence anchored relative to a reference team
#   4. All 6 seasons (2019/20 → 2024/25) run as one continuous filter, so the
#      posterior at end of each season seeds the next — no isolated per-season resets
#   5. End-of-season snapshots used as the time-series for projection
@app.cell(hide_code=True)
def _(np, requests, time):
    # ── Parameters (Ridall, Titman & Pettitt 2024) ───────────────────
    # Within-season forgetting: applied after every match
    _PHI_W  = 0.975
    # Between-season forgetting: applied once at the season boundary.
    # Paper uses distinct φ_W and φ_B; φ_B < φ_W to allow more drift across summers.
    _PHI_B  = 0.85
    # Home goal advantage (log scale): λ_H = (α_h / δ_a) * exp(η)
    _ETA    = 0.26
    # Gamma prior hyper-parameters for new/unseen teams
    _A0     = 4.0
    _B0     = 4.0
    # Seasons to fetch from football-data.co.uk (free, no rate limits)
    # Format: season start year → CSV filename suffix used by that site
    _SEASONS = [
        (2019, "E0_1920"),
        (2020, "E0_2021"),
        (2021, "E0_2122"),
        (2022, "E0_2223"),
        (2023, "E0_2324"),
        (2024, "E0_2425"),
    ]
    _CSV_BASE = "https://www.football-data.co.uk/mmz4281"

    # ── Name normaliser: maps football-data.co.uk short names → canonical ──
    _NAME_MAP = {
        "Man City":        "Manchester City FC",
        "Man United":      "Manchester United FC",
        "Tottenham":       "Tottenham Hotspur FC",
        "Wolves":          "Wolverhampton Wanderers FC",
        "Sheffield United":"Sheffield United FC",
        "Sheff United":    "Sheffield United FC",
        "Sheffield Utd":   "Sheffield United FC",
        "Nott'm Forest":   "Nottingham Forest FC",
        "Nottm Forest":    "Nottingham Forest FC",
        "Luton":           "Luton Town FC",
        "Brighton":        "Brighton & Hove Albion FC",
        "Leicester":       "Leicester City FC",
        "West Brom":       "West Bromwich Albion FC",
        "West Ham":        "West Ham United FC",
        "Newcastle":       "Newcastle United FC",
        "Norwich":         "Norwich City FC",
        "Watford":         "Watford FC",
        "Burnley":         "Burnley FC",
        "Brentford":       "Brentford FC",
        "Fulham":          "Fulham FC",
        "Crystal Palace":  "Crystal Palace FC",
        "Everton":         "Everton FC",
        "Southampton":     "Southampton FC",
        "Arsenal":         "Arsenal FC",
        "Chelsea":         "Chelsea FC",
        "Liverpool":       "Liverpool FC",
        "Leeds":           "Leeds United FC",
        "Aston Villa":     "Aston Villa FC",
        "Bournemouth":     "AFC Bournemouth",
        "Ipswich":         "Ipswich Town FC",
    }

    def _norm(name):
        return _NAME_MAP.get(name, name)

    def _fetch_csv(suffix):
        """Fetch a season CSV from football-data.co.uk.
        Returns list of dicts {home, away, hg, ag, date} for finished matches."""
        _yr  = suffix[-4:-2]  # e.g. "19" from "E0_1920"
        _yr2 = suffix[-2:]    # e.g. "20"
        _url = f"{_CSV_BASE}/{_yr}{_yr2}/E0.csv"
        try:
            _r = requests.get(_url, timeout=15)
            if _r.status_code != 200:
                return []
            _rows = []
            _lines = _r.text.strip().splitlines()
            if not _lines:
                return []
            _headers = [h.strip() for h in _lines[0].split(",")]
            def _col(row_parts, *names):
                for _n in names:
                    if _n in _headers:
                        try: return row_parts[_headers.index(_n)].strip()
                        except Exception: pass
                return ""
            for _line in _lines[1:]:
                _p = _line.split(",")
                if len(_p) < 6: continue
                _ht = _col(_p, "HomeTeam")
                _at = _col(_p, "AwayTeam")
                _hg = _col(_p, "FTHG", "HG")
                _ag = _col(_p, "FTAG", "AG")
                _dt = _col(_p, "Date")
                if _ht and _at and _hg.isdigit() and _ag.isdigit():
                    _rows.append({"home": _norm(_ht), "away": _norm(_at),
                                  "hg": int(_hg), "ag": int(_ag), "date": _dt})
            return _rows
        except Exception:
            return []

    # ── Continuous cross-season SSM ───────────────────────────────────
    # State: for each team, Gamma posteriors (a, b) for attack and (c, d) for defence.
    # All state stored in dicts keyed by canonical team name so teams entering/leaving
    # the PL are handled gracefully. New entrants get the shared prior.

    _a_state: dict = {}   # attack shape
    _b_state: dict = {}   # attack rate
    _c_state: dict = {}   # defence shape
    _d_state: dict = {}   # defence rate

    def _ensure(tm):
        if tm not in _a_state:
            _a_state[tm] = _A0; _b_state[tm] = _B0
            _c_state[tm] = _A0; _d_state[tm] = _B0

    def _atk_mean(tm):
        return _a_state[tm] / _b_state[tm]

    def _def_mean(tm):
        _ci, _di = _c_state[tm], _d_state[tm]
        # Use E[1/X] ≈ d/(c-1) for c>1 (mean of inverse-Gamma), else d/c
        return _di / (_ci - 1) if _ci > 1 else _di / _ci

    def _update(home, away, hg, ag):
        """Single match update — MFA closed-form as per paper eq (2.7)."""
        _ensure(home); _ensure(away)
        # Expected defensive rate for each side (used as Poisson rate denominator)
        _dH = _def_mean(home)   # home's defence weakness (away team attacks into)
        _dA = _def_mean(away)   # away's defence weakness (home team attacks into)
        # Expected goal rates (Poisson means):
        #   λ_H = atk_home / def_away * exp(η)
        #   λ_A = atk_away / def_home / exp(η)
        _lH = _atk_mean(home) / max(_dA, 1e-9) * np.exp(_ETA)
        _lA = _atk_mean(away) / max(_dH, 1e-9) / np.exp(_ETA)
        # Attack update: conjugate Gamma — add goals to shape, expected def to rate
        _a_state[home] += hg;  _b_state[home] += _dA / np.exp(_ETA)
        _a_state[away] += ag;  _b_state[away] += _dH * np.exp(_ETA)
        # Defence update: add goals conceded to shape, expected attack rate to rate
        _c_state[home] += ag;  _d_state[home] += _lA
        _c_state[away] += hg;  _d_state[away] += _lH
        # Within-season forgetting (applied after every match, both teams)
        for _tm in (home, away):
            _a_state[_tm] *= _PHI_W;  _b_state[_tm] *= _PHI_W
            _c_state[_tm] *= _PHI_W;  _d_state[_tm] *= _PHI_W

    def _between_season_forget(teams_in_season):
        """Apply between-season forgetting to all teams that were in this season."""
        for _tm in teams_in_season:
            if _tm in _a_state:
                _a_state[_tm] *= _PHI_B;  _b_state[_tm] *= _PHI_B
                _c_state[_tm] *= _PHI_B;  _d_state[_tm] *= _PHI_B

    def _snapshot(teams):
        """Return a dict of current posterior means for the given teams."""
        _out = {}
        for _tm in teams:
            if _tm not in _a_state: continue
            _atk = _a_state[_tm] / _b_state[_tm]
            _dfc = _c_state[_tm] / _d_state[_tm]
            _out[_tm] = {
                "atk": round(float(_atk), 4),
                "def": round(float(_dfc), 4),
                "net": round(float(_atk / max(_dfc, 1e-9)), 4),
                # Posterior uncertainty (std of Gamma mean)
                "atk_sd": round(float(np.sqrt(_a_state[_tm]) / _b_state[_tm]), 4),
                "def_sd": round(float(np.sqrt(_c_state[_tm]) / _d_state[_tm]), 4),
            }
        return _out

    # ── Run the continuous filter across all seasons ──────────────────
    _season_ssm  = {}   # season_year -> snapshot dict
    _season_pos  = {}   # season_year -> {team: final_position}

    for _szn, _suffix in _SEASONS:
        _matches = _fetch_csv(_suffix)
        time.sleep(0.5)   # polite pause between CSV downloads
        # Sort by date string (DD/MM/YY format on football-data.co.uk)
        # Stable sort — ties (same date) go in file order (usually round order)
        try:
            from datetime import datetime as _dt
            _matches.sort(key=lambda _m: _dt.strptime(_m["date"], "%d/%m/%Y")
                          if "/" in _m["date"] and len(_m["date"]) > 7
                          else _dt.strptime(_m["date"], "%d/%m/%y")
                          if "/" in _m["date"] else _dt.min)
        except Exception:
            pass  # leave in file order if date parsing fails

        _season_teams = set()
        for _m in _matches:
            _ensure(_m["home"]); _ensure(_m["away"])
            _season_teams.update((_m["home"], _m["away"]))
            _update(_m["home"], _m["away"], _m["hg"], _m["ag"])

        # Snapshot posterior means at end of season
        _season_ssm[_szn] = _snapshot(_season_teams)

        # Build final table from match results (no API needed)
        _pts: dict = {}; _gd: dict = {}; _gf: dict = {}
        for _m in _matches:
            for _tm in (_m["home"], _m["away"]):
                if _tm not in _pts: _pts[_tm] = 0; _gd[_tm] = 0; _gf[_tm] = 0
            _hg2, _ag2 = _m["hg"], _m["ag"]
            _gf[_m["home"]] += _hg2; _gd[_m["home"]] += _hg2 - _ag2
            _gf[_m["away"]] += _ag2; _gd[_m["away"]] += _ag2 - _hg2
            if   _hg2 > _ag2: _pts[_m["home"]] += 3
            elif _ag2 > _hg2: _pts[_m["away"]] += 3
            else:              _pts[_m["home"]] += 1; _pts[_m["away"]] += 1
        _sorted_t = sorted(_pts, key=lambda t: (-_pts[t], -_gd[t], -_gf[t]))
        _season_pos[_szn] = {_tm: _ri + 1 for _ri, _tm in enumerate(_sorted_t)}

        # Apply between-season forgetting before next season starts
        _between_season_forget(_season_teams)

    # ── Build per-team longitudinal record ───────────────────────────
    # Include every team that appeared in ≥ 2 seasons (gives a trend)
    _all_teams_hist = sorted({_tm for _szn in _season_ssm for _tm in _season_ssm[_szn]})
    _ssm_history = {}
    for _tm in _all_teams_hist:
        _rows = []
        for _szn, _ in _SEASONS:
            _sm = _season_ssm.get(_szn, {}).get(_tm)
            _pos = _season_pos.get(_szn, {}).get(_tm)
            if _sm and _pos:
                _rows.append({"season": _szn, "pos": _pos, **_sm})
        if len(_rows) >= 2:
            _ssm_history[_tm] = _rows

    ssm_history = _ssm_history
    season_ssm  = _season_ssm
    season_pos  = _season_pos

    return ssm_history, season_ssm, season_pos


# ─── Multi-season projection display ─────────────────────────────────────────
@app.cell(hide_code=True)
def _(
    BG, CARD, COLORS, MUTED, PREDICTIONS, TEXT,
    base64, io, mo, mpatches, np, plt,
    ssm_history, ssm_ratings,
):
    _TARGET_SEASONS = [2026, 2027]
    _HIST_SEASON_LABELS = {2019:"19/20",2020:"20/21",2021:"21/22",2022:"22/23",2023:"23/24",2024:"24/25"}

    # ── Weighted linear regression helper ────────────────────────────
    # Recency-weight each season so the most recent data pulls hardest.
    # Weights: w_t = exp(λ · t) with λ = 0.5 (roughly halves weight each 2 seasons back).
    def _wls(xs, ys, lam=0.5):
        """Return (slope, intercept, residual_se) from WLS."""
        _w  = np.exp(lam * (xs - xs[-1]))   # higher for more recent
        _sw = _w.sum()
        _xw = (xs * _w).sum() / _sw
        _yw = (ys * _w).sum() / _sw
        _sxx = ((xs - _xw)**2 * _w).sum()
        _sxy = ((xs - _xw) * (ys - _yw) * _w).sum()
        if _sxx < 1e-12:
            return 0.0, _yw, float(np.std(ys))
        _slope = _sxy / _sxx
        _inter = _yw - _slope * _xw
        _resid = ys - (_slope * xs + _inter)
        _se    = float(np.sqrt((_w * _resid**2).sum() / _sw))
        return float(_slope), float(_inter), max(_se, 1e-4)

    # ── Build projections ─────────────────────────────────────────────
    _projections = {}   # team -> {2026: {...}, 2027: {...}}

    for _tm, _rows in ssm_history.items():
        _xs  = np.array([_r["season"] for _r in _rows], dtype=float)
        _atk = np.array([_r["atk"]    for _r in _rows], dtype=float)
        _dfc = np.array([_r["def"]    for _r in _rows], dtype=float)
        _pos = np.array([_r["pos"]    for _r in _rows], dtype=float)

        # Weighted least-squares trend (recency-weighted)
        _sa, _ia, _sea = _wls(_xs, _atk)
        _sd, _id, _sed = _wls(_xs, _dfc)
        _sp, _ip2, _sep = _wls(_xs, _pos)

        _proj = {}
        for _yr in _TARGET_SEASONS:
            _pa = float(_sa * _yr + _ia)
            _pd = float(_sd * _yr + _id)
            _pp = float(_sp * _yr + _ip2)
            _gap    = _yr - _xs[-1]
            _extrap = float(np.sqrt(1.0 + _gap + 0.5 * _gap**2))
            _proj[_yr] = {
                "atk":       max(0.15, round(_pa, 3)),
                "def":       max(0.15, round(_pd, 3)),
                "net":       max(0.05, round(_pa / max(_pd, 1e-9), 3)),
                "pos":       round(float(np.clip(_pp, 1, 20)), 1),
                "atk_se":    round(float(_sea * _extrap), 3),
                "def_se":    round(float(_sed * _extrap), 3),
                "pos_se":    round(float(_sep * _extrap), 1),
                "atk_trend": round(_sa, 4),
                "def_trend": round(_sd, 4),
                "pos_trend": round(_sp, 4),
            }
        _projections[_tm] = _proj

    # ── Rank by projected net score ───────────────────────────────────
    def _rank_by_net(_yr):
        _nets = {t: _projections[t][_yr]["net"] for t in _projections if _yr in _projections[t]}
        _srt  = sorted(_nets.items(), key=lambda x: -x[1])
        return {t: i + 1 for i, (t, _) in enumerate(_srt)}

    _rank_2026 = _rank_by_net(2026)
    _rank_2027 = _rank_by_net(2027)

    # ── Identify predicted teams ──────────────────────────────────────
    _pred_names = {t.lower().replace(" fc","").strip() for pk in PREDICTIONS.values() for t in pk}
    def _is_pred(nm):
        n = nm.lower().replace(" fc","").strip()
        return any(n in pp or pp in n for pp in _pred_names)

    def _shorten(nm):
        return (nm.replace(" FC","").replace(" United","").replace(" Hotspur","")
                  .replace(" City","").replace("Brighton & Hove Albion","Brighton")
                  .replace("Wolverhampton Wanderers","Wolves")
                  .replace("Nottingham","Nott'm"))

    # ── Chart 1: Side-by-side scatter 2026 vs 2027 ───────────────────
    _fig1, (_axL, _axR) = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
    for _ax1, _yr1, _rank_map in [(_axL, 2026, _rank_2026), (_axR, 2027, _rank_2027)]:
        _ax1.set_facecolor(CARD)
        for _sp in _ax1.spines.values(): _sp.set_edgecolor("#30363D")

        # 2024/25 actuals as dark backdrop
        for _tm2, _rat in ssm_ratings.items():
            _ax1.scatter(_rat["atk"], _rat["def"], color="#252c38", s=35, alpha=0.7, zorder=1)

        for _tm2, _proj in _projections.items():
            if _yr1 not in _proj: continue
            _p   = _proj[_yr1]
            _ip  = _is_pred(_tm2)
            _col = "#6366f1" if _ip else "#4b5563"
            _ax1.errorbar(
                _p["atk"], _p["def"],
                xerr=_p["atk_se"], yerr=_p["def_se"],
                fmt="o", color=_col, markersize=9 if _ip else 5,
                alpha=0.95 if _ip else 0.5,
                elinewidth=0.8, capsize=3, capthick=0.8, ecolor=_col + "77", zorder=3,
            )
            _ax1.annotate(
                _shorten(_tm2), (_p["atk"], _p["def"]),
                textcoords="offset points", xytext=(6, 3),
                fontsize=7.5 if _ip else 6.2, fontfamily="monospace",
                color=TEXT if _ip else MUTED,
                fontweight="bold" if _ip else "normal", zorder=4,
            )

        _proj_atks = [_projections[t][_yr1]["atk"] for t in _projections if _yr1 in _projections[t]]
        _proj_defs = [_projections[t][_yr1]["def"] for t in _projections if _yr1 in _projections[t]]
        if _proj_atks:
            _ax1.axvline(np.mean(_proj_atks), color="#30363D", lw=1, ls="--", alpha=0.8)
            _ax1.axhline(np.mean(_proj_defs), color="#30363D", lw=1, ls="--", alpha=0.8)
            _mx1, _my1 = np.mean(_proj_atks), np.mean(_proj_defs)
            _x0, _x1v = min(_proj_atks), max(_proj_atks)
            _y0, _y1v = min(_proj_defs), max(_proj_defs)
            for _xt, _yt, _lbl in [
                (_mx1 + (_x1v-_mx1)*0.5, _my1 - (_my1-_y0)*0.6, "Elite"),
                (_mx1 - (_mx1-_x0)*0.5, _my1 - (_my1-_y0)*0.6, "Defensive"),
                (_mx1 + (_x1v-_mx1)*0.5, _my1 + (_y1v-_my1)*0.6, "Attack-heavy"),
                (_mx1 - (_mx1-_x0)*0.5, _my1 + (_y1v-_my1)*0.6, "Struggling"),
            ]:
                _ax1.text(_xt, _yt, _lbl, color="#30363D", fontsize=7,
                          ha="center", fontfamily="monospace", fontstyle="italic")

        _ax1.set_xlabel("Projected Attack α  (higher = more dangerous)", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax1.set_ylabel("Projected Defence δ  (lower = stronger)", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax1.set_title(f"{'2026/27' if _yr1==2026 else '2027/28'} — Projected Strength",
                       color=TEXT, fontsize=11, fontfamily="monospace", pad=10)
        _ax1.tick_params(colors=MUTED, labelsize=8)
        _ax1.grid(color="#30363D", lw=0.4, ls="--", alpha=0.4)
        _ax1.legend(
            handles=[mpatches.Patch(color="#6366f1", label="Predicted team"),
                     mpatches.Patch(color="#4b5563", label="Other team"),
                     mpatches.Patch(color="#252c38", label="2024/25 actuals")],
            loc="upper right", framealpha=0.2, labelcolor=TEXT,
            fontsize=7, facecolor=CARD, edgecolor="#30363D",
        )

    _fig1.suptitle("Projected Team Strengths  (error bars = extrapolation SE; continuous cross-season SSM with φ_W=0.975, φ_B=0.85)",
                   color=TEXT, fontsize=9.5, fontfamily="monospace")
    _fig1.tight_layout(pad=1.5)
    _buf1 = io.BytesIO()
    _fig1.savefig(_buf1, format="png", dpi=130, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(_fig1); _buf1.seek(0)
    _b64_scatter = base64.b64encode(_buf1.read()).decode()

    # ── Chart 2: Longitudinal trend lines for top 10 teams ───────────
    _top_teams = sorted(
        [t for t in ssm_history if t in ssm_ratings],
        key=lambda t: -ssm_ratings[t]["net"]
    )[:10]
    _hist_xs_all = sorted({r["season"] for t in _top_teams for r in ssm_history[t]})
    _proj_xs = _hist_xs_all + _TARGET_SEASONS

    _fig2, (_ax_atk2, _ax_def2) = plt.subplots(2, 1, figsize=(14, 9), facecolor=BG)
    _fig2.suptitle(
        "Attack & Defence Trends: Top 10 Teams (2019/20 → 2027/28 projected)\n"
        "Solid = historical SSM posteriors  ·  Dashed = WLS recency-weighted projection",
        color=TEXT, fontsize=10, fontfamily="monospace",
    )
    _cmap2 = plt.cm.tab10(np.linspace(0, 0.95, len(_top_teams)))

    for _ci, _tm3 in enumerate(_top_teams):
        _rows3 = ssm_history[_tm3]
        _xs3   = np.array([r["season"] for r in _rows3], dtype=float)
        _atks3 = np.array([r["atk"]    for r in _rows3], dtype=float)
        _defs3 = np.array([r["def"]    for r in _rows3], dtype=float)
        _col3  = _cmap2[_ci]
        _lbl3  = _shorten(_tm3)

        for _ax3, _ys3 in [(_ax_atk2, _atks3), (_ax_def2, _defs3)]:
            _ax3.plot(_xs3, _ys3, "o-", color=_col3, lw=2.2, markersize=6,
                      alpha=0.9, label=_lbl3, solid_capstyle="round")

        if _tm3 in _projections:
            _proj_atk3 = [_atks3[-1]] + [_projections[_tm3][y]["atk"] for y in _TARGET_SEASONS]
            _proj_def3 = [_defs3[-1]] + [_projections[_tm3][y]["def"] for y in _TARGET_SEASONS]
            _proj_xs3  = [int(_xs3[-1])] + _TARGET_SEASONS
            _proj_atk_se3 = [0] + [_projections[_tm3][y]["atk_se"] for y in _TARGET_SEASONS]
            _proj_def_se3 = [0] + [_projections[_tm3][y]["def_se"] for y in _TARGET_SEASONS]

            _ax_atk2.plot(_proj_xs3, _proj_atk3, "--", color=_col3, lw=1.6, alpha=0.65)
            _ax_def2.plot(_proj_xs3, _proj_def3, "--", color=_col3, lw=1.6, alpha=0.65)
            for _yi3, _yr3 in enumerate(_TARGET_SEASONS):
                _ax_atk2.errorbar(_yr3, _proj_atk3[_yi3+1], yerr=_proj_atk_se3[_yi3+1],
                                  fmt="D", color=_col3, ms=7, alpha=0.8,
                                  elinewidth=1.2, capsize=4, ecolor=_col3)
                _ax_def2.errorbar(_yr3, _proj_def3[_yi3+1], yerr=_proj_def_se3[_yi3+1],
                                  fmt="D", color=_col3, ms=7, alpha=0.8,
                                  elinewidth=1.2, capsize=4, ecolor=_col3)

    _szn_labels = {2019:"19/20",2020:"20/21",2021:"21/22",2022:"22/23",2023:"23/24",2024:"24/25",
                   2026:"26/27 (proj)",2027:"27/28 (proj)"}
    for _ax3b, _yl3, _ttl3 in [
        (_ax_atk2, "Attack α  (higher = better)", "Attack Strength"),
        (_ax_def2, "Defence δ  (lower = better)", "Defence Weakness"),
    ]:
        _ax3b.set_facecolor(CARD)
        for _sp in _ax3b.spines.values(): _sp.set_edgecolor("#30363D")
        _ax3b.set_ylabel(_yl3, color=MUTED, fontsize=9, fontfamily="monospace")
        _ax3b.set_title(_ttl3, color=TEXT, fontsize=10, fontfamily="monospace")
        _ax3b.tick_params(colors=MUTED, labelsize=7.5)
        _ax3b.grid(color="#30363D", lw=0.5, ls="--", alpha=0.5)
        _ax3b.set_xticks(_proj_xs)
        _ax3b.set_xticklabels(
            [_szn_labels.get(s, str(s)) for s in _proj_xs],
            color=MUTED, fontsize=7.5, rotation=30,
        )
        _ax3b.axvspan(2025.5, 2027.5, alpha=0.07, color="#6366f1", zorder=0)
        _ax3b.axvline(2025.5, color="#6366f1", lw=0.8, ls=":", alpha=0.5)
        _ax3b.legend(loc="upper right", framealpha=0.2, labelcolor=TEXT,
                     fontsize=6.5, facecolor=CARD, edgecolor="#30363D", ncol=2)

    _ax_def2.invert_yaxis()
    _fig2.tight_layout(pad=1.5)
    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format="png", dpi=130, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(_fig2); _buf2.seek(0)
    _b64_trends = base64.b64encode(_buf2.read()).decode()

    # ── Projection table ──────────────────────────────────────────────
    _all_proj_teams = sorted(
        [t for t in _projections if 2026 in _projections[t]],
        key=lambda t: -_projections[t][2026]["net"],
    )

    def _trend_badge(slope, is_atk=True):
        _thr = 0.003
        if abs(slope) < _thr:
            return '<span class="ssm-badge ssm-same">→ flat</span>'
        _good = (slope > 0) if is_atk else (slope < 0)
        _dir  = "↑" if slope > 0 else "↓"
        _cls  = "ssm-up" if _good else "ssm-down"
        return f'<span class="ssm-badge {_cls}">{_dir} {abs(slope):.3f}/yr</span>'

    def _pos_style(rk):
        if not isinstance(rk, int): return "color:#8B949E"
        if rk <= 4:  return "color:#60a5fa;font-weight:700"
        if rk <= 6:  return "color:#8b5cf6;font-weight:700"
        if rk >= 18: return "color:#f87171;font-weight:700"
        return "color:#8B949E"

    _table_rows = ""
    for _ri, _tm4 in enumerate(_all_proj_teams):
        _p26  = _projections[_tm4][2026]
        _p27  = _projections[_tm4][2027]
        _curr = ssm_ratings.get(_tm4, {})
        _ip4  = _is_pred(_tm4)
        _sh4  = _shorten(_tm4)
        _rk26 = _rank_2026.get(_tm4, "—")
        _rk27 = _rank_2027.get(_tm4, "—")
        _hl4  = "background:rgba(99,102,241,0.08);" if _ip4 else ""
        _bd4  = "font-weight:700;" if _ip4 else ""
        _ca4  = f'{_curr["atk"]:.3f}' if _curr else "—"
        _cd4  = f'{_curr["def"]:.3f}' if _curr else "—"
        _ns4  = len(ssm_history.get(_tm4, []))

        _table_rows += (
            f'<tr style="{_hl4}">'
            f'<td style="text-align:center;color:#475569;font-family:monospace">{_ri+1}</td>'
            f'<td style="{_bd4}">{_sh4}</td>'
            f'<td style="text-align:center;color:#475569;font-size:0.75rem">{_ns4}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_ca4}</td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">{_cd4}</td>'
            f'<td style="text-align:center">{_trend_badge(_p26["atk_trend"], is_atk=True)}</td>'
            f'<td style="text-align:center">{_trend_badge(_p26["def_trend"], is_atk=False)}</td>'
            f'<td style="text-align:center;{_pos_style(_rk26)};font-family:monospace">'
            f'#{_rk26}&nbsp;<span style="font-size:0.72rem;color:#8B949E">(±{_p26["pos_se"]:.0f})</span></td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">'
            f'{_p26["atk"]:.3f}&nbsp;<span style="font-size:0.68rem">±{_p26["atk_se"]:.3f}</span></td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">'
            f'{_p26["def"]:.3f}&nbsp;<span style="font-size:0.68rem">±{_p26["def_se"]:.3f}</span></td>'
            f'<td style="text-align:center;{_pos_style(_rk27)};font-family:monospace">'
            f'#{_rk27}&nbsp;<span style="font-size:0.72rem;color:#8B949E">(±{_p27["pos_se"]:.0f})</span></td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">'
            f'{_p27["atk"]:.3f}&nbsp;<span style="font-size:0.68rem">±{_p27["atk_se"]:.3f}</span></td>'
            f'<td style="text-align:center;color:#94a3b8;font-family:monospace">'
            f'{_p27["def"]:.3f}&nbsp;<span style="font-size:0.68rem">±{_p27["def_se"]:.3f}</span></td>'
            f'</tr>'
        )

    mo.Html(f"""
    <details>
      <summary>🔭 Multi-Season Forecast — 2026/27 &amp; 2027/28 Projections</summary>
      <div style="margin-top:16px">

        <div class="card" style="border-color:#6366f133">
          <div class="section-title" style="color:#a5b4fc">🧠 Methodology — Ridall, Titman &amp; Pettitt (2024)</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;font-size:0.82rem;color:#8B949E;line-height:1.7">
            <div>
              <span style="color:#22d3ee;font-family:monospace;font-weight:700">Continuous cross-season SSM</span><br>
              A single Gamma-Poisson filter runs across all 6 seasons from 2019/20 onwards.
              Team states carry over between seasons rather than resetting — a key insight
              from the paper that captures longer-term structural strength.
            </div>
            <div>
              <span style="color:#a78bfa;font-family:monospace;font-weight:700">Dual forgetting factors</span><br>
              φ_W = 0.975 discounts within-season (after every match).
              φ_B = 0.85 is applied once per season boundary, allowing larger drift
              across the summer to capture transfers and managerial changes.
            </div>
            <div>
              <span style="color:#f59e0b;font-family:monospace;font-weight:700">Recency-weighted projection</span><br>
              End-of-season posterior snapshots form the time-series. WLS with
              exponential recency weights (λ = 0.5/season) projects α and δ forward.
              Uncertainty grows with extrapolation distance.
            </div>
          </div>
          <div style="margin-top:12px;font-size:0.76rem;color:#475569;font-family:monospace">
            Data: football-data.co.uk (free CSV downloads, no API rate limits, all seasons available) &nbsp;·&nbsp;
            ⚠️ Projections don't account for transfers or promotion/relegation.
          </div>
        </div>

        <div class="card">
          <div class="section-title">📊 Projected Standings — 2026/27 &amp; 2027/28</div>
          <div style="overflow-x:auto">
            <table class="ptable" style="font-size:0.78rem;min-width:960px">
              <thead>
                <tr>
                  <th style="text-align:center">#</th><th>Team</th>
                  <th style="text-align:center" title="seasons of PL data">Szns</th>
                  <th style="text-align:center">Cur α</th>
                  <th style="text-align:center">Cur δ</th>
                  <th style="text-align:center">Atk trend</th>
                  <th style="text-align:center">Def trend</th>
                  <th style="text-align:center;border-left:1px solid #30363D" colspan="3">— 2026/27 —</th>
                  <th style="text-align:center;border-left:1px solid #30363D" colspan="3">— 2027/28 —</th>
                </tr>
                <tr style="font-size:0.7rem;color:#475569">
                  <th></th><th></th><th></th><th></th><th></th><th></th><th></th>
                  <th style="text-align:center;border-left:1px solid #1c2130">Pos</th>
                  <th style="text-align:center">α</th><th style="text-align:center">δ</th>
                  <th style="text-align:center;border-left:1px solid #1c2130">Pos</th>
                  <th style="text-align:center">α</th><th style="text-align:center">δ</th>
                </tr>
              </thead>
              <tbody>{_table_rows}</tbody>
            </table>
          </div>
          <div style="font-size:0.7rem;color:#475569;margin-top:10px;font-family:monospace">
            <b style="color:#E6EDF3">Bold/shaded</b> = predicted by a player &nbsp;·&nbsp;
            <span style="color:#60a5fa">Blue</span> = projected CL (1–4) &nbsp;·&nbsp;
            <span style="color:#8b5cf6">Purple</span> = Europa/Conference (5–6) &nbsp;·&nbsp;
            <span style="color:#f87171">Red</span> = relegation zone (18–20) &nbsp;·&nbsp;
            Szns = seasons of PL data informing the trend
          </div>
        </div>

        <div class="card">
          <div class="section-title">🎯 Projected Strength Scatter — 2026/27 vs 2027/28</div>
          <img class="chart-img" src="data:image/png;base64,{_b64_scatter}" style="margin-bottom:8px">
          <div style="font-size:0.7rem;color:#475569;font-family:monospace">
            Dark grey = 2024/25 actuals &nbsp;·&nbsp; Coloured = projected &nbsp;·&nbsp;
            Error bars = extrapolation SE &nbsp;·&nbsp; Dashed lines = projected league average &nbsp;·&nbsp;
            Quadrant labels: Elite (high atk, low def) = top of table
          </div>
        </div>

        <div class="card">
          <div class="section-title">📈 Attack &amp; Defence Trends — Top 10 Teams</div>
          <img class="chart-img" src="data:image/png;base64,{_b64_trends}">
          <div style="font-size:0.7rem;color:#475569;margin-top:8px;font-family:monospace">
            Purple region = projection window &nbsp;·&nbsp; ◆ = projected values with error bars &nbsp;·&nbsp;
            Defence axis inverted (lower δ = stronger) &nbsp;·&nbsp; Solid = historical posterior, Dashed = WLS projection
          </div>
        </div>

      </div>
    </details>
    """)
    return

# ── Render.com deployment ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import os, sys
    try:
        port = int(os.environ.get("PORT", 8000))
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Error starting app: {e}", file=sys.stderr)
        import traceback; traceback.print_exc()
        sys.exit(1)