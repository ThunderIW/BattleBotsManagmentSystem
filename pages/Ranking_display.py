import streamlit as st
from streamlit import column_config

ranking_details = st.session_state['Ranking_data']

RANK_CONFIG = {
    "Recruit":          {"emoji": "🛡️", "color": "#A0A0A0"},
    "Rookie":           {"emoji": "🌱", "color": "#4CAF50"},
    "Designer":         {"emoji": "🔧", "color": "#2196F3"},
    "Competitor":       {"emoji": "⚔️", "color": "#FF9800"},
    "Match Winner":     {"emoji": "🏅", "color": "#FFD700"},
    "Podium Finisher":  {"emoji": "🥇", "color": "#E040FB"},
    "Ultimate Champion":{"emoji": "🏆", "color": "#FF1744"},
    "God":              {"emoji": "👑", "color": "#FFD700"},
}

RANK_ORDER = list(RANK_CONFIG.keys())
HIDDEN_RANKS = {"God"}
DISPLAY_RANKS = {k: v for k, v in RANK_CONFIG.items() if k not in HIDDEN_RANKS}

# --- Styled Header ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 20px;
    text-align: center;
">
    <h1 style="color: #FFD700; margin: 0;">⚔️ Battle Bots Rankings ⚔️</h1>
    <p style="color: #ccc; margin-top: 8px; font-size: 1.1em;">Current Member Rankings & Progression</p>
</div>
""", unsafe_allow_html=True)

# --- Metric Cards ---
rank_counts = ranking_details['Rank'].value_counts() if 'Rank' in ranking_details.columns else {}

cols = st.columns(len(DISPLAY_RANKS))
for i, (rank, cfg) in enumerate(DISPLAY_RANKS.items()):
    count = rank_counts.get(rank, 0) if len(rank_counts) > 0 else 0
    with cols[i]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, {cfg['color']}22, {cfg['color']}44);
            border-left: 4px solid {cfg['color']};
            border-radius: 8px;
            padding: 12px 10px;
            text-align: center;
            margin-bottom: 10px;
        ">
            <div style="font-size: 1.8em;">{cfg['emoji']}</div>
            <div style="font-weight: bold; color: {cfg['color']}; font-size: 0.85em;">{rank}</div>
            <div style="font-size: 1.5em; font-weight: bold;">{count}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Rank Progression Bar ---
st.markdown("#### Rank Progression")
col_widths = []
for i in range(len(DISPLAY_RANKS)):
    col_widths.append(3)
    if i < len(DISPLAY_RANKS) - 1:
        col_widths.append(1)
prog_cols = st.columns(col_widths)
col_idx = 0
for i, (rank, cfg) in enumerate(DISPLAY_RANKS.items()):
    with prog_cols[col_idx]:
        st.markdown(f"""<div style="text-align:center;">
            <span style="font-size:1.5em;">{cfg['emoji']}</span><br>
            <span style="font-size:0.65em; font-weight:bold; color:{cfg['color']}; white-space:nowrap;">{rank}</span>
        </div>""", unsafe_allow_html=True)
    col_idx += 1
    if i < len(DISPLAY_RANKS) - 1:
        with prog_cols[col_idx]:
            st.markdown('<div style="text-align:center; font-size:1.2em; padding-top:8px;">➡️</div>', unsafe_allow_html=True)
        col_idx += 1

# --- Member Cards ---
st.markdown("#### Member Details")

rank_priority = {rank: i for i, rank in enumerate(reversed(RANK_ORDER))}
sorted_members = ranking_details.copy()
sorted_members['_rank_order'] = sorted_members['Rank'].map(rank_priority).fillna(len(RANK_ORDER))
sorted_members = sorted_members.sort_values('_rank_order').drop(columns='_rank_order')

for _, row in sorted_members.iterrows():
    name = row.get("Name", "Unknown")
    rank = row.get("Rank", "Recruit")
    date = row.get("DateGiven", "")
    cfg = RANK_CONFIG.get(rank, {"emoji": "❓", "color": "#888"})

    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 5px solid {cfg['color']};
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 10px;
    ">
        <div style="font-size: 2.2em; margin-right: 18px;">{cfg['emoji']}</div>
        <div style="flex: 1;">
            <div style="font-size: 1.2em; font-weight: bold; color: #fff;">{name}</div>
            <div style="margin-top: 4px;">
                <span style="
                    background: {cfg['color']}33;
                    color: {cfg['color']};
                    padding: 3px 10px;
                    border-radius: 12px;
                    font-size: 0.85em;
                    font-weight: bold;
                ">{rank}</span>
            </div>
        </div>
        <div style="text-align: right; color: #aaa; font-size: 0.85em;">
            📅 {date}
        </div>
    </div>
    """, unsafe_allow_html=True)