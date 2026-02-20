import marimo

__generated_with = "0.20.1"
app = marimo.App(width="full")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1 — imports & constants (hidden in present mode)
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _():
    import marimo as mo
    import requests
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
    import matplotlib.patches as mpatches
    import io, base64, json
    from datetime import datetime
    from collections import defaultdict

    # ── CONFIG ─────────────────────────────────────────────────────────────────
    API_KEY = "7a874a538506441bbdc6b4aca3dbb648"
    HEADERS = {"X-Auth-Token": API_KEY}
    BASE    = "https://api.football-data.org/v4"
    SEASON  = 2025   # 2025 = 2025/26 season on football-data.org

    PREDICTIONS = {
        "Jerome": ["Manchester City FC", "Liverpool FC", "Chelsea FC",
                   "Arsenal FC", "Newcastle United FC", "Tottenham Hotspur FC"],
        "Erin":   ["Liverpool FC", "Arsenal FC", "Chelsea FC",
                   "Manchester City FC", "Aston Villa FC", "Tottenham Hotspur FC"],
        "Alex":   ["Liverpool FC", "Arsenal FC", "Manchester City FC",
                   "Chelsea FC", "Aston Villa FC", "Tottenham Hotspur FC"],
    }
    COLORS  = {"Jerome": "#E8A838", "Erin": "#4FC3C3", "Alex": "#E8608A"}
    T6_BON  = -2
    EX_BON  = -5

    # Palette
    BG      = "#0D1117"
    CARD    = "#161B22"
    BORDER  = "#30363D"
    TEXT    = "#E6EDF3"
    MUTED   = "#8B949E"
    GOLD    = "#FFD700"
    GREEN   = "#4FC3C3"
    RED     = "#FF6B6B"

    return (
        API_KEY, BASE, BG, BORDER, CARD, COLORS, EX_BON, GOLD, GREEN,
        HEADERS, MUTED, PREDICTIONS, RED, SEASON, T6_BON, TEXT,
        base64, datetime, defaultdict, io, json, matplotlib, mo,
        mpatches, pe, plt, requests,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 2 — CSS (hidden)
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

    body, .marimo-app, [class*="marimo"] {
        background: #0D1117 !important;
        color: #E6EDF3 !important;
        font-family: 'Inter', sans-serif !important;
    }
    /* hide all code cells in present mode */
    .marimo-output-wrapper { padding: 0 !important; }

    .hero {
        text-align: center; padding: 36px 0 16px;
        border-bottom: 1px solid #30363D; margin-bottom: 24px;
    }
    .hero h1 {
        font-family: 'Space Mono', monospace;
        font-size: 2.1rem; font-weight: 700;
        color: #E6EDF3; margin: 0 0 8px;
        letter-spacing: 0.02em;
    }
    .hero p { color: #8B949E; font-size: 0.88rem; margin: 0; }

    .card {
        background: #161B22; border-radius: 14px;
        padding: 22px 26px; border: 1px solid #30363D; margin-bottom: 20px;
    }
    .section-title {
        font-family: 'Space Mono', monospace; font-size: 0.7rem;
        letter-spacing: 0.14em; text-transform: uppercase;
        color: #8B949E; margin-bottom: 16px;
        padding-bottom: 8px; border-bottom: 1px solid #30363D;
    }

    /* leaderboard */
    .lb-row {
        display: flex; align-items: center; gap: 14px;
        padding: 14px 18px; border-radius: 10px; margin-bottom: 10px;
        border: 1px solid #30363D; background: #0D1117;
        transition: transform 0.15s, border-color 0.15s;
        cursor: default;
    }
    .lb-row:hover { transform: translateX(5px); }
    .lb-medal  { font-size: 1.7rem; min-width: 36px; }
    .lb-name   { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; min-width: 80px; }
    .lb-detail { font-size: 0.76rem; color: #8B949E; display: flex; gap: 14px; flex-wrap: wrap; }
    .lb-pts    {
        margin-left: auto; font-family: 'Space Mono', monospace;
        font-size: 1.6rem; font-weight: 700;
        padding: 2px 18px; border-radius: 999px;
        background: rgba(255,255,255,0.05);
    }

    /* pick table */
    .ptable { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
    .ptable th { color: #8B949E; font-weight: 500; padding: 6px 10px; border-bottom: 1px solid #30363D; text-align: left; }
    .ptable td { padding: 7px 10px; border-bottom: 1px solid #1c2130; }
    .ptable tr.exact td { background: #1a2e1a; color: #FFD700; }
    .ptable tr.top6  td { background: #14232b; }
    .d-good { color: #4FC3C3; font-weight: 700; }
    .d-ok   { color: #FFD700; font-weight: 700; }
    .d-bad  { color: #FF6B6B; font-weight: 700; }

    /* form dots */
    .form-dot {
        display: inline-block; width: 22px; height: 22px;
        border-radius: 50%; line-height: 22px; text-align: center;
        font-size: 0.65rem; font-weight: 700; margin: 0 2px;
    }
    .form-W { background: #1a3a1a; color: #4ade80; border: 1px solid #4ade8055; }
    .form-D { background: #2a2a1a; color: #facc15; border: 1px solid #facc1555; }
    .form-L { background: #3a1a1a; color: #f87171; border: 1px solid #f8717155; }

    /* status */
    .statusbar {
        display: flex; justify-content: space-between; align-items: center;
        font-family: 'Space Mono', monospace; font-size: 0.72rem;
        color: #8B949E; padding: 6px 4px 16px;
    }
    .live-dot {
        display: inline-block; width: 7px; height: 7px;
        border-radius: 50%; background: #4FC3C3;
        animation: blink 2s ease-in-out infinite; margin-right: 6px;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }

    /* tab buttons */
    .tab-row { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
    .tab-btn {
        font-family: 'Space Mono', monospace; font-size: 0.72rem;
        letter-spacing: 0.08em; text-transform: uppercase;
        padding: 7px 16px; border-radius: 8px; border: 1px solid #30363D;
        background: #161B22; color: #8B949E; cursor: pointer;
        transition: all 0.15s;
    }
    .tab-btn.active { background: #21262d; color: #E6EDF3; border-color: #8B949E; }
    .tab-btn:hover  { border-color: #6e7681; color: #E6EDF3; }

    /* full-width chart img */
    .chart-img { width: 100%; border-radius: 10px; display: block; }

    /* top scorer / fact cards */
    .fact-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-bottom: 20px; }
    .fact-card {
        background: #0D1117; border: 1px solid #30363D; border-radius: 10px;
        padding: 16px 18px;
    }
    .fact-label { font-size: 0.7rem; color: #8B949E; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
    .fact-value { font-family: 'Space Mono', monospace; font-size: 1.3rem; font-weight: 700; color: #E6EDF3; }
    .fact-sub   { font-size: 0.76rem; color: #8B949E; margin-top: 3px; }

    details summary {
        cursor: pointer; font-family: 'Space Mono', monospace;
        font-size: 0.7rem; color: #8B949E; letter-spacing: 0.1em;
        text-transform: uppercase; padding: 10px 4px;
        user-select: none;
    }
    details summary:hover { color: #E6EDF3; }
    </style>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 3 — refresh control (hidden)
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(mo):
    refresh = mo.ui.refresh(default_interval="10m")
    return (refresh,)


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 4 — DATA FETCH (hidden) — all API calls in one place
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(BASE, COLORS, EX_BON, HEADERS, PREDICTIONS, SEASON, T6_BON,
       datetime, defaultdict, refresh, requests):
    _ = refresh  # reactive dependency

    errors = []

    # ── helpers ────────────────────────────────────────────────────────────────
    def _api(path, params=None):
        try:
            r = requests.get(f"{BASE}{path}", headers=HEADERS,
                             params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            errors.append(f"{path} → HTTP {r.status_code}")
        except Exception as e:
            errors.append(f"{path} → {e}")
        return {}

    def _fuzzy(team, pos_dict):
        """Match a prediction name to an API team name."""
        if team in pos_dict:
            return pos_dict[team]
        tl = team.lower().replace(" fc", "").strip()
        for k, v in pos_dict.items():
            kl = k.lower().replace(" fc", "").strip()
            if tl in kl or kl in tl:
                return v
            tw, kw = set(tl.split()), set(kl.split())
            if len(tw & kw) >= 2:
                return v
        return None

    def _score(picks, pos_dict):
        top6 = {t for t, p in pos_dict.items() if p <= 6}
        dt = tb = eb = 0
        bk = []
        for pr, team in enumerate(picks, 1):
            ar = _fuzzy(team, pos_dict)
            if ar is None:
                bk.append({"team": team, "pred": pr, "actual": "?",
                            "dist": 0, "in_top6": False, "exact": False})
                continue
            dist  = abs(pr - ar)
            in_t6 = any(team.lower().replace(" fc","") in t.lower()
                        or t.lower() in team.lower() for t in top6)
            exact = (pr == ar)
            dt += dist
            if in_t6: tb += T6_BON
            if exact: eb += EX_BON
            bk.append({"team": team, "pred": pr, "actual": ar,
                       "dist": dist, "in_top6": in_t6, "exact": exact})
        return {"dist": dt, "top6": tb, "exact": eb,
                "total": dt + tb + eb, "breakdown": bk}

    # ── 1. Current standings ──────────────────────────────────────────────────
    standings_data = _api("/competitions/PL/standings", {"season": SEASON})
    current_table  = []  # [{pos, name, pts, gd, gf, played, won, draw, lost, form}]
    for _s in standings_data.get("standings", []):
        if _s.get("type") == "TOTAL":
            for _t in _s["table"]:
                current_table.append({
                    "pos":    _t["position"],
                    "name":   _t["team"]["name"],
                    "pts":    _t["points"],
                    "gd":     _t["goalDifference"],
                    "gf":     _t["goalsFor"],
                    "ga":     _t["goalsAgainst"],
                    "played": _t["playedGames"],
                    "won":    _t["won"],
                    "draw":   _t["draw"],
                    "lost":   _t["lost"],
                    "form":   _t.get("form") or "",
                })
            break

    actual_pos = {t["name"]: t["pos"] for t in current_table}
    current_matchday = standings_data.get("season", {}).get("currentMatchday", "?")

    # ── 2. All matches this season (for historical reconstruction) ────────────
    matches_data = _api("/competitions/PL/matches", {"season": SEASON})
    all_matches  = matches_data.get("matches", [])

    gw_matches = defaultdict(list)
    for _m in all_matches:
        if _m.get("status") == "FINISHED" and _m.get("matchday"):
            gw_matches[_m["matchday"]].append(_m)

    # Simulate cumulative table after each matchday
    _stats = {}
    historical = []  # [(matchday, {team: position})]

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

        _sorted = sorted(_stats.items(),
                         key=lambda x: (-x[1]["pts"],
                                        -(x[1]["gf"]-x[1]["ga"]),
                                        -x[1]["gf"]))
        historical.append((_md, {n: i+1 for i, (n, _) in enumerate(_sorted)}))

    # ── 3. Top scorers ────────────────────────────────────────────────────────
    scorers_data = _api("/competitions/PL/scorers",
                        {"season": SEASON, "limit": 10})
    top_scorers = []
    for _sc in scorers_data.get("scorers", []):
        top_scorers.append({
            "name":   _sc["player"]["name"],
            "team":   _sc["team"]["name"],
            "goals":  _sc["goals"],
            "assists": _sc.get("assists") or 0,
        })

    # ── 4. Upcoming fixtures ──────────────────────────────────────────────────
    upcoming = []
    for _m in all_matches:
        if _m.get("status") in ("SCHEDULED", "TIMED"):
            upcoming.append({
                "home": _m["homeTeam"]["name"],
                "away": _m["awayTeam"]["name"],
                "date": _m.get("utcDate", ""),
                "md":   _m.get("matchday"),
            })
    upcoming = sorted(upcoming, key=lambda x: x["date"])[:15]

    # ── 5. Recent results (last 10 finished) ─────────────────────────────────
    recent = []
    for _m in reversed(all_matches):
        if _m.get("status") == "FINISHED":
            recent.append({
                "home": _m["homeTeam"]["name"],
                "away": _m["awayTeam"]["name"],
                "hg":   _m["score"]["fullTime"].get("home"),
                "ag":   _m["score"]["fullTime"].get("away"),
                "md":   _m.get("matchday"),
                "date": _m.get("utcDate", "")[:10],
            })
            if len(recent) == 10:
                break

    # ── 6. Compute prediction scores ─────────────────────────────────────────
    results = {p: _score(picks, actual_pos) for p, picks in PREDICTIONS.items()}
    ranked  = sorted(results.items(), key=lambda x: x[1]["total"])

    gw_scores = {
        p: [(md, _score(picks, pos)["total"]) for md, pos in historical]
        for p, picks in PREDICTIONS.items()
    }

    # Best/worst matchday per person (biggest score swing)
    best_md = {}
    for _p, _pts in gw_scores.items():
        if len(_pts) >= 2:
            _deltas = [(w, s - _pts[i-1][1]) for i, (w, s) in enumerate(_pts) if i > 0]
            _best = min(_deltas, key=lambda x: x[1])
            best_md[_p] = _best  # (matchday, delta) — negative = improved

    fetched_at = datetime.now().strftime("%d %b %Y · %H:%M")

# prevent marimo from rendering raw data
_ = (
    results, ranked, gw_scores, current_table, actual_pos, historical,
    top_scorers, upcoming, recent, current_matchday, fetched_at,
    best_md, errors, PREDICTIONS, COLORS
)

return (
    PREDICTIONS, COLORS, actual_pos, best_md, current_matchday,
    current_table, errors, fetched_at, gw_scores, historical,
    ranked, recent, results, top_scorers, upcoming,
)


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5 — HERO + STATUS BAR
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(current_matchday, current_table, errors, fetched_at, mo, refresh):
    _err = f" · ⚠️ {'; '.join(errors)}" if errors else ""
    _gws = f"Matchday {current_matchday}" if current_matchday != "?" else ""
    mo.Html(f"""
    <div class="hero">
      <h1>⚽  Premier League Prediction Challenge  ⚽</h1>
      <p>Lower score = better &nbsp;·&nbsp; Distance penalty (+) &nbsp;·&nbsp;
         Top-6 bonus (−2) &nbsp;·&nbsp; Exact pick bonus (−5)</p>
    </div>
    <div class="statusbar">
      <span><span class="live-dot"></span>Live · {fetched_at}{_err}</span>
      <span>{len(current_table)} clubs &nbsp;·&nbsp; {_gws} &nbsp;·&nbsp; auto-refresh every 10 min</span>
    </div>
    {mo.as_html(refresh)}
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 6 — LEADERBOARD
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(COLORS, mo, ranked, results):
    _medals = ["🥇", "🥈", "🥉"]

    def _lb(i, p):
        s = results[p]; c = COLORS[p]
        return f"""
        <div class="lb-row" style="border-color:{c}55">
          <span class="lb-medal">{_medals[i]}</span>
          <span class="lb-name" style="color:{c}">{p}</span>
          <span class="lb-detail">
            <span title="sum of position distances">📏 dist: <b>+{s['dist']}</b></span>
            <span title="bonus for correct top-6 picks">✅ top-6: <b>{s['top6']}</b></span>
            <span title="bonus for exact position picks">🎯 exact: <b>{s['exact']}</b></span>
          </span>
          <span class="lb-pts" style="color:{c}">{s['total']}</span>
        </div>"""

    mo.Html(
        '<div class="card">'
        '<div class="section-title">🏆 Leaderboard — 2025/26 Season</div>'
        + "".join(_lb(i, p) for i, (p, _) in enumerate(ranked))
        + '</div>'
    )
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7 — SCORE EVOLUTION CHART
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, TEXT, base64, gw_scores, historical, io, mo, pe, plt):
    _fig, _ax = plt.subplots(figsize=(12, 4), facecolor=BG)
    _ax.set_facecolor(CARD)
    for _sp in _ax.spines.values():
        _sp.set_edgecolor("#30363D")

    if historical:
        _all_scores = [s for pts in gw_scores.values() for _, s in pts]
        _ymin, _ymax = min(_all_scores) - 1, max(_all_scores) + 1

        for _p, _pts in gw_scores.items():
            _w = [w for w, _ in _pts]
            _s = [s for _, s in _pts]
            _c = COLORS[_p]
            _ax.fill_between(_w, _s, _ymax + 2, alpha=0.07, color=_c, zorder=1)
            _ax.plot(_w, _s, color=_c, lw=2.5, zorder=3,
                     solid_capstyle="round", marker="o",
                     markersize=4, markerfacecolor=_c, markeredgewidth=0)
            # Endpoint marker + label
            _ax.plot(_w[-1], _s[-1], "o", ms=10, color=_c, zorder=5,
                     markeredgecolor=BG, markeredgewidth=2)
            _ax.text(_w[-1] + 0.25, _s[-1], f" {_p}  {_s[-1]}",
                     color=_c, fontsize=9, fontfamily="monospace",
                     va="center", fontweight="bold",
                     path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)])

        _gws = [w for w, _ in historical]
        _ax.set_xlim(min(_gws) - 0.5, max(_gws) + 4)
        _ax.invert_yaxis()
        _ax.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax.set_ylabel("Score  (↑ = better)", color=MUTED, fontsize=9, fontfamily="monospace")
        # Shade top-of-chart as "better zone"
        _ax.text(0.01, 0.03, "↑  better", transform=_ax.transAxes,
                 color=MUTED, fontsize=8, fontfamily="monospace", va="bottom")
    else:
        _ax.text(0.5, 0.5, "No finished matches yet this season",
                 ha="center", va="center", color=MUTED,
                 fontsize=11, fontfamily="monospace", transform=_ax.transAxes)

    _ax.set_title("Prediction Score Evolution by Matchday — 2025/26",
                  color=TEXT, fontsize=11, fontfamily="monospace", pad=12)
    _ax.tick_params(colors=MUTED)
    _ax.grid(color="#30363D", lw=0.6, linestyle="--", alpha=0.6, zorder=0)
    _fig.tight_layout(pad=1.5)

    _buf = io.BytesIO()
    _fig.savefig(_buf, format="png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(_fig); _buf.seek(0)
    _b64 = base64.b64encode(_buf.read()).decode()

    mo.Html(f"""
    <div class="card">
      <div class="section-title">📈 Score Evolution</div>
      <img class="chart-img" src="data:image/png;base64,{_b64}" />
    </div>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8 — PICK BREAKDOWN CARDS
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(COLORS, mo, ranked, results):
    _medals2 = ["🥇", "🥈", "🥉"]

    def _row_cls(b):
        return "exact" if b["exact"] else ("top6" if b["in_top6"] else "")

    def _dist_cls(b):
        if b["exact"]:    return "d-good"
        if b["dist"] > 3: return "d-bad"
        if b["dist"] > 0: return "d-ok"
        return "d-good"

    def _card(i, p):
        c = COLORS[p]; s = results[p]
        rows = ""
        for b in s["breakdown"]:
            short = (b["team"].replace(" FC","").replace(" United","")
                              .replace(" City"," C.").replace(" Hotspur",""))
            actual = str(b["actual"]) if b["actual"] != "?" else "?"
            rows += (f'<tr class="{_row_cls(b)}">'
                     f'<td style="color:#8B949E">{b["pred"]}</td>'
                     f'<td>{short}</td>'
                     f'<td style="text-align:center">{actual}</td>'
                     f'<td style="text-align:center" class="{_dist_cls(b)}">{b["dist"]}</td>'
                     f'</tr>')
        legend = ('<tr><td colspan="4" style="padding-top:10px;font-size:0.7rem;color:#8B949E">'
                  '<span style="background:#1a2e1a;padding:2px 8px;border-radius:4px;color:#FFD700;margin-right:8px">🎯 exact (−5)</span>'
                  '<span style="background:#14232b;padding:2px 8px;border-radius:4px;color:#4FC3C3">✅ top-6 (−2)</span>'
                  '</td></tr>')
        return f"""
        <div class="card" style="border-color:{c}44">
          <div class="section-title" style="color:{c}">
            {_medals2[i]} {p} &nbsp;·&nbsp;
            <span style="color:#E6EDF3;font-size:0.85rem">{s['total']} pts total</span>
          </div>
          <table class="ptable">
            <thead><tr>
              <th>#</th><th>Predicted Team</th>
              <th style="text-align:center">Actual Pos</th>
              <th style="text-align:center">Δ</th>
            </tr></thead>
            <tbody>{rows}{legend}</tbody>
          </table>
        </div>"""

    mo.Html(
        '<div class="section-title">📋 Pick-by-pick Breakdown</div>'
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px">'
        + "".join(_card(i, p) for i, (p, _) in enumerate(ranked))
        + '</div>'
    )
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9 — LEAGUE TABLE + FORM
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, PREDICTIONS, TEXT, base64, current_table, io, mo, plt):
    # Build form dots HTML
    def _form_html(form_str):
        dots = ""
        for ch in (form_str or "").replace(",", "")[-5:]:
            cls = {"W": "form-W", "D": "form-D", "L": "form-L"}.get(ch, "form-D")
            dots += f'<span class="form-dot {cls}">{ch}</span>'
        return dots

    # Which teams are predicted by anyone?
    _all_predicted = {t.lower().replace(" fc","").strip()
                      for picks in PREDICTIONS.values() for t in picks}

    def _is_predicted(name):
        n = name.lower().replace(" fc","").strip()
        return any(n in p or p in n for p in _all_predicted)

    rows_html = ""
    for _t in current_table:
        _pos   = _t["pos"]
        _name  = _t["name"]
        _short = _name.replace(" FC","").replace(" United","").replace(" Hotspur","")
        _form  = _form_html(_t["form"])
        _hl    = "background:#1a1f2e;" if _pos <= 6 else ""
        _bold  = "font-weight:700;" if _is_predicted(_name) else ""
        _cl4   = "color:#60a5fa;" if _pos <= 4 else ""    # CL spots blue
        _cl5   = "color:#f59e0b;" if _pos == 5 else ""    # EL
        _cl6   = "color:#8b5cf6;" if _pos == 6 else ""    # Conference
        _pos_col = _cl4 or _cl5 or _cl6 or "color:#8B949E"
        rows_html += (
            f'<tr style="{_hl}">'
            f'<td style="text-align:center;{_pos_col};font-family:monospace;font-weight:700">{_pos}</td>'
            f'<td style="{_bold}">{_short}</td>'
            f'<td style="text-align:center;color:#8B949E">{_t["played"]}</td>'
            f'<td style="text-align:center;color:#4ade80">{_t["won"]}</td>'
            f'<td style="text-align:center;color:#facc15">{_t["draw"]}</td>'
            f'<td style="text-align:center;color:#f87171">{_t["lost"]}</td>'
            f'<td style="text-align:center">{_t["gd"]:+d}</td>'
            f'<td style="text-align:center;font-family:monospace;font-weight:700;color:#E6EDF3">{_t["pts"]}</td>'
            f'<td>{_form}</td>'
            f'</tr>'
        )

    # Mini bar chart: pts for top 10
    _fig2, _ax2 = plt.subplots(figsize=(10, 3.2), facecolor=BG)
    _ax2.set_facecolor(CARD)
    for _sp in _ax2.spines.values(): _sp.set_edgecolor("#30363D")
    _top10  = current_table[:10]
    _names  = [t["name"].replace(" FC","").replace(" United","").replace(" Hotspur","")
               for t in _top10]
    _pts    = [t["pts"] for t in _top10]
    _bar_c  = ["#60a5fa"]*4 + ["#f59e0b"] + ["#8b5cf6"] + ["#374151"]*4
    _bars   = _ax2.barh(_names[::-1], _pts[::-1], color=_bar_c[::-1],
                        alpha=0.85, height=0.65)
    for _bar, _p in zip(_bars, _pts[::-1]):
        _ax2.text(_bar.get_width() + 0.3, _bar.get_y() + _bar.get_height()/2,
                  str(_p), va="center", color=TEXT,
                  fontsize=9, fontfamily="monospace")
    _ax2.set_xlabel("Points", color=MUTED, fontsize=9, fontfamily="monospace")
    _ax2.set_title("Top 10 by Points", color=TEXT, fontsize=10,
                   fontfamily="monospace", pad=10)
    _ax2.tick_params(colors=MUTED, labelsize=8)
    _ax2.grid(axis="x", color="#30363D", lw=0.6, linestyle="--", alpha=0.6)
    _ax2.set_xlim(0, max(_pts) + 5)

    # Legend for colours
    import matplotlib.patches as _mpatches
    _leg = [_mpatches.Patch(color="#60a5fa", label="Champions League (1–4)"),
            _mpatches.Patch(color="#f59e0b", label="Europa League (5)"),
            _mpatches.Patch(color="#8b5cf6", label="Conference (6)")]
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
            <thead><tr>
              <th style="text-align:center">#</th>
              <th>Club</th>
              <th style="text-align:center">P</th>
              <th style="text-align:center" title="Won">W</th>
              <th style="text-align:center" title="Drawn">D</th>
              <th style="text-align:center" title="Lost">L</th>
              <th style="text-align:center">GD</th>
              <th style="text-align:center">Pts</th>
              <th>Form</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
          <div style="font-size:0.7rem;color:#8B949E;margin-top:10px;font-family:monospace">
            <b style="color:#E6EDF3">Bold</b> = predicted by someone &nbsp;·&nbsp;
            Blue top-4 = CL &nbsp;·&nbsp; Highlighted rows = top 6
          </div>
        </div>
        <div>
          <img class="chart-img" src="data:image/png;base64,{_b64_2}" />
        </div>
      </div>
    </div>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 10 — TOP SCORERS
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(mo, top_scorers):
    def _scorer_row(i, s):
        _medal = ["🥇","🥈","🥉"][i] if i < 3 else f"{i+1}."
        _team  = s["team"].replace(" FC","").replace(" United","").replace(" Hotspur","")
        return (f'<tr>'
                f'<td style="text-align:center;font-family:monospace;color:#8B949E">{_medal}</td>'
                f'<td style="font-weight:600">{s["name"]}</td>'
                f'<td style="color:#8B949E;font-size:0.8rem">{_team}</td>'
                f'<td style="text-align:center;font-family:monospace;font-size:1.1rem;'
                f'font-weight:700;color:#FFD700">{s["goals"]}</td>'
                f'<td style="text-align:center;font-family:monospace;color:#4FC3C3">{s["assists"]}</td>'
                f'</tr>')

    _rows = "".join(_scorer_row(i, s) for i, s in enumerate(top_scorers))

    # Fun fact block
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
            <div class="fact-label">🎯 Goals + Assists (leader)</div>
            <div class="fact-value">{_top['goals'] + _top['assists']}</div>
            <div class="fact-sub">{_top['goals']}G + {_top['assists']}A</div>
          </div>
          <div class="fact-card">
            <div class="fact-label">📋 Scorers tracked</div>
            <div class="fact-value">{len(top_scorers)}</div>
            <div class="fact-sub">top scorers this season</div>
          </div>
        </div>"""

    mo.Html(f"""
    <div class="card">
      <div class="section-title">🥅 Top Scorers — 2025/26</div>
      {_top_html}
      <table class="ptable">
        <thead><tr>
          <th style="text-align:center">#</th>
          <th>Player</th><th>Club</th>
          <th style="text-align:center">⚽ Goals</th>
          <th style="text-align:center">🅰️ Assists</th>
        </tr></thead>
        <tbody>{_rows}</tbody>
      </table>
    </div>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 11 — UPCOMING FIXTURES + RECENT RESULTS side by side
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(mo, recent, upcoming):
    def _shorten(name):
        return (name.replace(" FC","").replace(" United","")
                    .replace(" Hotspur","").replace(" City",""))

    def _fmt_date(d):
        try:
            from datetime import datetime
            return datetime.fromisoformat(d.replace("Z","+00:00")).strftime("%d %b %H:%M")
        except Exception:
            return d[:10]

    # Upcoming
    _up_rows = ""
    for _f in upcoming[:8]:
        _up_rows += (f'<tr>'
                     f'<td style="color:#8B949E;font-size:0.75rem;white-space:nowrap">{_fmt_date(_f["date"])}</td>'
                     f'<td style="text-align:right;font-weight:600">{_shorten(_f["home"])}</td>'
                     f'<td style="text-align:center;color:#8B949E;padding:0 8px">vs</td>'
                     f'<td style="font-weight:600">{_shorten(_f["away"])}</td>'
                     f'<td style="text-align:center;color:#8B949E;font-size:0.75rem">MD{_f["md"]}</td>'
                     f'</tr>')

    # Recent results
    _re_rows = ""
    for _r in recent[:8]:
        _hg, _ag = _r["hg"], _r["ag"]
        if _hg > _ag:   _hcol, _acol = "#4ade80", "#f87171"
        elif _ag > _hg: _hcol, _acol = "#f87171", "#4ade80"
        else:           _hcol = _acol = "#facc15"
        _re_rows += (f'<tr>'
                     f'<td style="color:#8B949E;font-size:0.75rem">{_r["date"]}</td>'
                     f'<td style="text-align:right;font-weight:600;color:{_hcol}">{_shorten(_r["home"])}</td>'
                     f'<td style="text-align:center;font-family:monospace;font-weight:700;padding:0 10px">'
                     f'{_hg}–{_ag}</td>'
                     f'<td style="font-weight:600;color:{_acol}">{_shorten(_r["away"])}</td>'
                     f'</tr>')

    mo.Html(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
      <div class="card">
        <div class="section-title">📅 Upcoming Fixtures</div>
        <table class="ptable">
          <thead><tr>
            <th>Date (UTC)</th><th style="text-align:right">Home</th>
            <th></th><th>Away</th><th style="text-align:center">MD</th>
          </tr></thead>
          <tbody>{_up_rows}</tbody>
        </table>
      </div>
      <div class="card">
        <div class="section-title">🎮 Recent Results</div>
        <table class="ptable">
          <thead><tr>
            <th>Date</th><th style="text-align:right">Home</th>
            <th style="text-align:center">Score</th><th>Away</th>
          </tr></thead>
          <tbody>{_re_rows}</tbody>
        </table>
      </div>
    </div>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 12 — FUN STATS: prediction battle details
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(BG, CARD, COLORS, MUTED, PREDICTIONS, TEXT, base64,
       best_md, current_table, gw_scores, io, mo, mpatches, pe, plt, ranked, results):

    # ── Gap chart: distance to leader over time ────────────────────────────────
    _fig3, _ax3 = plt.subplots(figsize=(12, 3.5), facecolor=BG)
    _ax3.set_facecolor(CARD)
    for _sp in _ax3.spines.values(): _sp.set_edgecolor("#30363D")

    if gw_scores and any(gw_scores.values()):
        _leader_by_gw = {}
        _all_mds = sorted({md for pts in gw_scores.values() for md, _ in pts})
        for _md in _all_mds:
            _scores_at = {p: next((s for w, s in pts if w == _md), None)
                          for p, pts in gw_scores.items()}
            _valid = {p: s for p, s in _scores_at.items() if s is not None}
            if _valid:
                _leader_by_gw[_md] = min(_valid.values())

        for _p, _pts in gw_scores.items():
            _w  = [w for w, _ in _pts]
            _gap = [s - _leader_by_gw.get(w, s) for w, s in _pts]
            _c  = COLORS[_p]
            _ax3.fill_between(_w, _gap, 0, alpha=0.08, color=_c)
            _ax3.plot(_w, _gap, color=_c, lw=2, zorder=3, marker="o",
                      markersize=3, markerfacecolor=_c, markeredgewidth=0,
                      solid_capstyle="round")
            _ax3.text(_w[-1]+0.2, _gap[-1], f" {_p}",
                      color=_c, fontsize=8.5, fontfamily="monospace", va="center",
                      path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

        _ax3.axhline(0, color="#4FC3C3", lw=1.5, linestyle="--", alpha=0.6, zorder=4)
        _ax3.text(0.01, 0.97, "← leading", transform=_ax3.transAxes,
                  color="#4FC3C3", fontsize=7.5, fontfamily="monospace", va="top")
        _gws = [w for w, _ in list(gw_scores.values())[0]]
        _ax3.set_xlim(min(_gws)-0.5, max(_gws)+3)
        _ax3.set_xlabel("Matchday", color=MUTED, fontsize=9, fontfamily="monospace")
        _ax3.set_ylabel("Points behind leader", color=MUTED, fontsize=9, fontfamily="monospace")
    else:
        _ax3.text(0.5, 0.5, "No data yet", ha="center", va="center",
                  color=MUTED, fontsize=11, transform=_ax3.transAxes)

    _ax3.set_title("Gap to Leader by Matchday", color=TEXT,
                   fontsize=11, fontfamily="monospace", pad=10)
    _ax3.tick_params(colors=MUTED)
    _ax3.grid(color="#30363D", lw=0.6, linestyle="--", alpha=0.5)
    _fig3.tight_layout(pad=1.5)
    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(_fig3); _buf3.seek(0)
    _b64_3 = base64.b64encode(_buf3.read()).decode()

    # ── Fun fact cards ─────────────────────────────────────────────────────────
    _leader_p, _leader_s = ranked[0]
    _gap_1_2 = results[ranked[1][0]]["total"] - results[ranked[0][0]]["total"]

    # Count how many of each person's picks are currently in the actual top 6
    _top6_names = {t["name"] for t in current_table if t["pos"] <= 6}
    def _in_top6_count(person):
        picks = PREDICTIONS[person]
        return sum(1 for t in picks if any(
            t.lower().replace(" fc","") in tn.lower() or tn.lower() in t.lower()
            for tn in _top6_names))

    _t6_counts = {p: _in_top6_count(p) for p in PREDICTIONS}
    _best_t6   = max(_t6_counts, key=_t6_counts.get)

    # Best matchday improvement
    _best_gainer = None
    _best_gain   = 0
    for _p, _bmd in best_md.items():
        if _bmd[1] < _best_gain:
            _best_gain   = _bmd[1]
            _best_gainer = (_p, _bmd[0], _bmd[1])

    _fact1 = f"""
    <div class="fact-card">
      <div class="fact-label">🥇 Current leader</div>
      <div class="fact-value" style="color:{COLORS[_leader_p]}">{_leader_p}</div>
      <div class="fact-sub">{_leader_s['total']} pts · leads by {_gap_1_2} pts</div>
    </div>"""

    _fact2 = f"""
    <div class="fact-card">
      <div class="fact-label">✅ Most picks in actual top 6</div>
      <div class="fact-value" style="color:{COLORS[_best_t6]}">{_best_t6}</div>
      <div class="fact-sub">{_t6_counts[_best_t6]}/6 teams correctly in top 6</div>
    </div>"""

    _fact3_content = (
        f'<div class="fact-value" style="color:{COLORS[_best_gainer[0]]}">{_best_gainer[0]}</div>'
        f'<div class="fact-sub">Best gain: {abs(_best_gainer[2])} pts on MD{_best_gainer[1]}</div>'
    ) if _best_gainer else (
        '<div class="fact-value">—</div><div class="fact-sub">Not enough data yet</div>'
    )
    _fact3 = f"""
    <div class="fact-card">
      <div class="fact-label">📈 Biggest single-week improvement</div>
      {_fact3_content}
    </div>"""

    # Exact picks so far
    _exact_counts = {p: sum(1 for b in results[p]["breakdown"] if b["exact"])
                     for p in PREDICTIONS}
    _most_exact = max(_exact_counts, key=_exact_counts.get)
    _fact4 = f"""
    <div class="fact-card">
      <div class="fact-label">🎯 Most exact predictions</div>
      <div class="fact-value" style="color:{COLORS[_most_exact]}">{_most_exact}</div>
      <div class="fact-sub">{_exact_counts[_most_exact]} team(s) in exact position</div>
    </div>"""

    # Total distance
    _dists = {p: results[p]["dist"] for p in PREDICTIONS}
    _closest = min(_dists, key=_dists.get)
    _fact5 = f"""
    <div class="fact-card">
      <div class="fact-label">📏 Closest predictions overall</div>
      <div class="fact-value" style="color:{COLORS[_closest]}">{_closest}</div>
      <div class="fact-sub">Total position distance: {_dists[_closest]}</div>
    </div>"""

    # Who has the most points from bonuses
    _bonus_counts = {p: abs(results[p]["top6"]) + abs(results[p]["exact"])
                     for p in PREDICTIONS}
    _bonus_king = max(_bonus_counts, key=_bonus_counts.get)
    _fact6 = f"""
    <div class="fact-card">
      <div class="fact-label">💰 Most bonus points earned</div>
      <div class="fact-value" style="color:{COLORS[_bonus_king]}">{_bonus_king}</div>
      <div class="fact-sub">{_bonus_counts[_bonus_king]} pts from top-6 & exact bonuses</div>
    </div>"""

    mo.Html(f"""
    <div class="card">
      <div class="section-title">⚡ Prediction Battle Stats</div>
      <div class="fact-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:20px">
        {_fact1}{_fact2}{_fact3}
      </div>
      <div class="fact-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:20px">
        {_fact4}{_fact5}{_fact6}
      </div>
      <div class="section-title" style="margin-top:8px">📉 Points Gap to Leader over Time</div>
      <img class="chart-img" src="data:image/png;base64,{_b64_3}" />
    </div>
    """)
    return


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 13 — SCORING RULES (collapsible)
# ═══════════════════════════════════════════════════════════════════════════════
@app.cell(hide_code=True)
def _(mo):
    mo.Html("""
    <details>
      <summary>📖 How the scoring works</summary>
      <div class="card" style="margin-top:10px">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;font-size:0.85rem">
          <div>
            <div style="color:#FF6B6B;font-family:monospace;font-weight:700;margin-bottom:6px">📏 Distance Penalty (+)</div>
            For each of your 6 predicted teams, we measure how far they are from
            their actual position. Predicted Arsenal at #3 but they're #5? That's +2.
            All 6 distances are summed. <b>Higher = worse.</b>
          </div>
          <div>
            <div style="color:#4FC3C3;font-family:monospace;font-weight:700;margin-bottom:6px">✅ Top-6 Bonus (−2 each)</div>
            For each of your 6 predicted teams that is <em>actually</em> in the
            real top 6 at any position, you earn −2 points.
            You can earn up to −12 if all 6 of your picks are in the top 6.
          </div>
          <div>
            <div style="color:#FFD700;font-family:monospace;font-weight:700;margin-bottom:6px">🎯 Exact Pick Bonus (−5 each)</div>
            If a team is not only in the top 6 but in the <em>exact spot</em>
            you predicted (e.g. you said Liverpool #1 and they're #1), you earn
            an additional −5 points. Max −30 for a perfect 6/6.
          </div>
        </div>
        <div style="margin-top:16px;padding-top:12px;border-top:1px solid #30363D;
                    font-size:0.8rem;color:#8B949E;font-family:monospace">
          Example: Pick Arsenal at #2, they finish #4 → +2 (distance) −2 (in top 6) = net 0<br>
          Example: Pick Liverpool at #1, they finish #1 → +0 (distance) −2 (top 6) −5 (exact) = −7
        </div>
      </div>
    </details>
    """)
    return


if __name__ == "__main__":
    app.run()
