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
    COLORS = {"Jerome": "#E8A838", "Erin": "#4FC3C3", "Alex": "#E8608A"}
    T6_BON = -2
    EX_BON = -5
    BG     = "#0D1117"
    CARD   = "#161B22"
    TEXT   = "#E6EDF3"
    MUTED  = "#8B949E"

    return (
        API_KEY, BASE, BG, CARD, COLORS, EX_BON, HEADERS, MUTED,
        PREDICTIONS, SEASON, T6_BON, TEXT,
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
                    "pts": _t["points"], "gd": _t["goalDifference"],
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
        actual_pos, best_md, current_matchday, current_table, errors,
        fetched_at, gw_scores, historical, ranked, recent, results,
        top_scorers, upcoming,
    )


@app.cell(hide_code=True)
def _(COLORS, PREDICTIONS, current_matchday, current_table, errors,
      fetched_at, mo, refresh):
    _err = f" · ⚠️ {'; '.join(errors)}" if errors else ""
    _gws = f"Matchday {current_matchday}" if current_matchday != "?" else ""
    _all_predicted = {t.lower().replace(" fc","").strip()
                      for picks in PREDICTIONS.values() for t in picks}
    mo.vstack([
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
        """),
        refresh,
    ])
    return


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
    _leg = [mpatches.Patch(color="#60a5fa", label="Champions League (1–4)"),
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

    # Gap to leader chart
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

    # Fact cards
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
                f"−{abs(_bg2[2])} pts on MD{_bg2[1]}", COLORS[_bg2[0]])
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


if __name__ == "__main__":
    # Render sets the port in the $PORT environment variable
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)