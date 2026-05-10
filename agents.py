import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

TOTAL_9K = 9000
DEMOGRAPHIC_BRACKETS = {
    "Asia-Pacific": 0.60,
    "Sub-Saharan Africa": 0.15,
    "Europe": 0.09,
    "Latin America": 0.08,
    "Middle East & North Africa": 0.05,
    "North America": 0.02,
    "Other": 0.01,
}


def allocate_slots():
    slots = {}
    remaining = TOTAL_9K
    items = list(DEMOGRAPHIC_BRACKETS.items())
    for i, (region, pct) in enumerate(items):
        if i == len(items) - 1:
            slots[region] = remaining
        else:
            count = round(TOTAL_9K * pct)
            slots[region] = count
            remaining -= count
    return slots


def render_agents_module():
    st.subheader("Global Grid")
    slots = allocate_slots()
    df = pd.DataFrame([{"Region": r, "Share": p, "Seats": slots[r]} for r, p in DEMOGRAPHIC_BRACKETS.items()])
    fig = go.Figure(go.Bar(x=df["Region"], y=df["Seats"]))
    fig.update_layout(template="plotly_dark", title="Demographic Mirror Allocation")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Simulate global signal"):
            yes = random.randint(34, 78)
            st.metric("Global signal", f"YES {yes}%", "Escalated" if yes >= 51 else "Not escalated")
    with c2:
        if st.button("Simulate 9k vote"):
            yes_votes = random.randint(4200, 8200)
            yes_pct = round((yes_votes / TOTAL_9K) * 100, 1)
            st.metric("9k vote", f"YES {yes_votes:,}", "Emergency" if yes_pct >= 75 else "Standard review")
