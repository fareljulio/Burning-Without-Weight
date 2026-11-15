import time
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Fire Behavior Across Gravity", layout="wide")

# ---------------- DATA (verify against the paper before submitting) ----------------
DATA = {
    0.0:  {"residence": 0.082, "soot": 17.8, "label": "Microgravity (ISS)"},
    0.16: {"residence": 0.029, "soot": 13.8, "label": "Moon"},
    0.38: {"residence": 0.021, "soot": 12.7, "label": "Mars"},
}

# If the paper has a measured 1 g row, fill it in here and it becomes a normal data point:
# EARTH_ROW = {"residence": 0.0, "soot": 0.0}
EARTH_ROW = none
if EARTH_ROW:
    DATA[1.0] = {**EARTH_ROW, "label": "Earth (1 g)"}

# Literature only (different experiments, jet flames): peak soot in microgravity is about
# 2-4x the 1 g value, so 1 g is roughly 25-50% of the 0 g value.
LIT_SOOT_RATIO = (2, 4)

GS = sorted(DATA.keys())
GMAX = GS[-1]
SOURCE_URL = "https://www.sciencedirect.com/science/article/pii/S1540748926003421"

RESEARCH = {
    "microgravity": [
        ("Non-buoyant smoke-point (Space Shuttle Columbia)",
         "Flames in true microgravity emit soot more easily and hold soot far longer than buoyant flames. This is why soot loading peaks at 0g.",
         "https://www.sciencedirect.com/science/article/abs/pii/S0010218018304395"),
        ("Burning Candles in Microgravity",
         "Without buoyancy, flames become spherical. Gas stays in the reaction zone longer, so soot has time to grow.",
         "https://www.researchgate.net/publication/24329285_Burning_Candles_in_the_Microgravity_of_Space"),
        ("SAFFIRE V (2025)",
         "In weightlessness, flame spreads only against the airflow. Blowing on a fire makes it worse. Ventilation design must account for this.",
         "https://up2date.uni-bremen.de/en/article/brand-new-findings-on-fire-safety-in-space"),
    ],
    "lunar": [
        ("Smoke-point transition under partial gravity (2026)",
         "At 0.16g, residence time drops ~3x versus 0g. Soot particles are fewer and smaller - optical detectors may miss them.",
         "https://www.sciencedirect.com/science/article/pii/S1540748926003421"),
        ("Saffire: large-scale spread",
         "Microgravity flames reach a limiting length instead of accelerating upward. Lunar flames sit between these two regimes.",
         "https://svs.gsfc.nasa.gov/31394/"),
    ],
    "martian": [
        ("Microgravity flame spread in exploration atmospheres",
         "Safe oxygen limits set on Earth are NOT conservative for reduced gravity. Some materials ignite more easily in 0.38g.",
         "https://www.researchgate.net/publication/255013038_Microgravity_Flame_Spread_in_Exploration_Atmospheres_Pressure_Oxygen_and_Velocity_Effects_on_Opposed_and_Concurrent_Flame_Spread"),
        ("SAFFIRE V (2025)",
         "Partial gravity changes flow direction and soot residence. Mars is neither a little Earth nor a little ISS.",
         "https://up2date.uni-bremen.de/en/article/brand-new-findings-on-fire-safety-in-space"),
    ],
    "general": [
        ("ACME - Advanced Combustion via Microgravity Experiments",
         "All data here comes from controlled, open-flame experiments on ISS, not from real fires.",
         "https://www.nasa.gov/centers-and-facilities/glenn/studying-flame-behavior-in-microgravity-with-a-solid-high-five/"),
        ("Combustion Integrated Rack (CIR)",
         "The ISS facility behind most microgravity flame data. Buoyancy-free flames are simpler to study and model.",
         "https://www.americanscientist.org/article/fire-in-microgravity"),
        ("BRE - Burning Rate Emulator",
         "Stable flames require roughly >26% O2 in microgravity test conditions. Below that, flames tend to quench.",
         "https://www.sciencedirect.com/science/article/abs/pii/S0010218021000493"),
        ("Confined-space flame study (Case Western)",
         "These results apply to flames in confined volumes (cabin-like). Confinement can increase smoke and burn duration.",
         "https://issnationallab.org/upward/upward-62-case-western-flame-study/"),
    ],
}

def pick_research(g):
    if g < 0.08:
        return "microgravity"
    if g < 0.27:
        return "lunar"
    return "martian"

def interp(key, g):
    return float(np.interp(g, GS, [DATA[x][key] for x in GS]))

# ---------------- FIGURES ----------------
def line_fig(key, title, ylab, color, g):
    ys = [DATA[x][key] for x in GS]
    xs_f = np.linspace(0, GMAX, 60)
    fig = go.Figure()
    fig.add_vrect(x0=GMAX, x1=1, fillcolor="gray", opacity=0.15, line_width=0,
                  annotation_text="no measured data", annotation_position="top left")
    fig.add_trace(go.Scatter(x=xs_f, y=np.interp(xs_f, GS, ys), mode="lines",
                             line=dict(color=color, dash="dot", width=3), name="linear interpolation"))
    fig.add_trace(go.Scatter(x=GS, y=ys, mode="markers+text",
                             text=[DATA[x]["label"] for x in GS], textposition="top right",
                             marker=dict(size=12, color=color), name="measured"))
    if g <= GMAX:
        fig.add_trace(go.Scatter(x=[g], y=[interp(key, g)], mode="markers",
                                 marker=dict(size=18, color="red", symbol="star"), name="selected"))
    fig.add_vline(x=g, line_dash="dash", line_color="red")
    fig.update_layout(title=title, xaxis_title="Gravity (g)", yaxis_title=ylab,
                      xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, max(ys) * 1.25]),
                      height=340, margin=dict(l=10, r=10, t=50, b=10), showlegend=False)
    return fig

def relative_fig():
    labels = [DATA[x]["label"] for x in GS]
    res = [DATA[x]["residence"] / DATA[0.0]["residence"] * 100 for x in GS]
    soot = [DATA[x]["soot"] / DATA[0.0]["soot"] * 100 for x in GS]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=res, name="Residence time", marker_color="#ff7f0e",
                         text=[f"{v:.0f}%" for v in res], textposition="outside"))
    fig.add_trace(go.Bar(x=labels, y=soot, name="Peak soot volume fraction", marker_color="#444444",
                         text=[f"{v:.0f}%" for v in soot], textposition="outside"))
    if not EARTH_ROW:
        lo, hi = 100 / LIT_SOOT_RATIO[1], 100 / LIT_SOOT_RATIO[0]
        mid = (lo + hi) / 2
        fig.add_trace(go.Bar(x=["Earth (1 g)*"], y=[mid], name="Peak soot, literature range",
                             marker_color="rgba(68,68,68,0.35)", marker_line_color="#444444",
                             marker_line_width=2,
                             error_y=dict(type="data", array=[hi - mid], arrayminus=[mid - lo], visible=True),
                             text=[f"{lo:.0f}-{hi:.0f}%"], textposition="outside"))
    fig.update_layout(title="Compared with microgravity (0g = 100%)", barmode="group",
                      yaxis=dict(range=[0, 125], title="% of 0g value"), height=300,
                      margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.2))
    return fig

def gauge_fig(title, value, color):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=value, number={"suffix": "%"},
                                 title={"text": title},
                                 gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}))
    fig.update_layout(height=230, margin=dict(l=20, r=20, t=60, b=10))
    return fig

# ---------------- DECISION PANEL ----------------
def decision_panel(g):
    st.subheader("Smoke detector decision")
    if g > GMAX:
        st.warning(f"At {g:.2f} g there is no measured data (the experiments cover 0 to {GMAX} g). "
                   "No recommendation is made outside the measured range.")
        return
    res, soot = interp("residence", g), interp("soot", g)
    st.markdown(f"At **{g:.2f} g**: residence time **{res:.3f}**, peak soot volume fraction **{soot:.1f}** (paper units, interpolated).")
    if res >= 0.05:
        st.error("**Long residence time.** Soot has time to grow into large aggregates and the flame tail stays open, "
                 "releasing smoke. Detectors calibrated on Earth-type smoke may respond differently. "
                 "Recommendation: test and calibrate detectors with reduced-gravity soot.")
    else:
        st.warning("**Shorter residence time.** The flame tail closes and more soot is oxidized before it escapes. "
                   "Fewer, smaller particles: optical detectors may be slower or miss the fire. "
                   "Recommendation: consider higher-sensitivity or multi-sensor detection.")
    if soot >= 15:
        st.info("Peak soot loading is high (>= 15): heavy smoke is expected early in the fire.")
    st.caption("Rule-of-thumb logic for illustration. The thresholds (0.05 and 15) are our own choice, "
               "not a validated detector model, and no alarm times are claimed.")

# ---------------- RENDER ----------------
def render(g, ph, tag):
    with ph.container():
        c1, c2 = st.columns(2)
        c1.plotly_chart(line_fig("residence", "Residence time vs gravity", "Residence time (paper units)", "#ff7f0e", g),
                        use_container_width=True, key=tag + "a")
        c2.plotly_chart(line_fig("soot", "Peak soot volume fraction vs gravity", "Soot volume fraction (paper units)", "#444444", g),
                        use_container_width=True, key=tag + "b")
        c3, c4, c5 = st.columns([2, 1, 1])
        c3.plotly_chart(relative_fig(), use_container_width=True, key=tag + "c")
        if not EARTH_ROW:
            c3.caption("*Earth (1 g) is a literature range for peak soot from different experiments (jet flames), "
                       "not a measurement from this dataset. No 1 g value for residence time is shown.")
        if g <= GMAX:
            c4.plotly_chart(gauge_fig("Residence time vs 0g", interp("residence", g) / DATA[0.0]["residence"] * 100, "#ff7f0e"),
                            use_container_width=True, key=tag + "d")
            c5.plotly_chart(gauge_fig("Peak soot vs 0g", interp("soot", g) / DATA[0.0]["soot"] * 100, "#444444"),
                            use_container_width=True, key=tag + "e")
        else:
            c4.info("Gauges only shown inside the measured range.")
        decision_panel(g)
        st.markdown("#### Why this matters")
        for title, insight, url in RESEARCH[pick_research(g)]:
            st.markdown(f"**{title}** - {insight}  \n[source]({url})")

# ---------------- PAGE ----------------
st.title("Fire Behavior Across Gravity")
st.caption("Does a spacecraft smoke detector behave the same on the ISS, the Moon and Mars? Drag the slider.")

if "g" not in st.session_state:
    st.session_state.g = 0.0
def set_g(v):
    st.session_state.g = v

b = st.columns(4)
b[0].button("ISS (0 g)", on_click=set_g, args=(0.0,))
b[1].button("Moon (0.16 g)", on_click=set_g, args=(0.16,))
b[2].button("Mars (0.38 g)", on_click=set_g, args=(0.38,))
b[3].button("Earth (1 g)", on_click=set_g, args=(1.0,))
g = st.slider("Gravity (g)", 0.0, 1.0, step=0.01, key="g")

play = st.button(f"Play sweep 0 to {GMAX} g")
ph = st.empty()
if play:
    for i, gi in enumerate(np.linspace(0, GMAX, 38)):
        render(float(gi), ph, f"p{i}")
        time.sleep(0.15)
else:
    render(g, ph, "main")

with st.expander("Data source and caveats"):
    st.markdown(f"Measured points: parabolic-flight flame spread experiments at 0g, 0.16g and 0.38g. "
                f"Paper: [Smoke-point transition under partial gravity]({SOURCE_URL}).")
    st.table({"Gravity": [DATA[x]["label"] for x in GS],
              "g": GS,
              "Residence time": [DATA[x]["residence"] for x in GS],
              "Max soot volume fraction": [DATA[x]["soot"] for x in GS]})
    st.markdown("- Dotted lines are straight-line interpolation between 3 measured points. The real curve may not be a straight line.\n"
                "- Values are in the units reported by the paper (relative units).\n"
                f"- Above {GMAX} g there is no measured data in this tool.\n"
                "- All data come from controlled experiments, not real spacecraft fires.")

with st.expander("Earth (1 g) reference - different experiments, not on the same scale"):
    st.markdown(
        "- Jet-diffusion flames: peak soot volume fraction is roughly 2-4x higher in microgravity than in 1 g "
        "([NASA NTRS](https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf)).\n"
        "- Another jet-flame study reports about 2x higher maximum soot volume fraction at 0 g "
        "([NASA NTRS](https://ntrs.nasa.gov/api/citations/19970020584/downloads/19970020584.pdf)).\n"
        "- The grey bar on the comparison chart turns this into 100/4 to 100/2, so about 25-50% of the 0 g value. "
        "It is a range from other experiments, not a measurement from this dataset.\n"
        "- These are different fuels and burners from the flame-spread data above. "
        "They show the direction of the trend on Earth, not values for this chart."
    )

with st.expander("What this tool does NOT do"):
    st.markdown("- It is not a validated smoke detector model and gives no alarm times.\n"
                "- It interpolates between only three measured points; it is not a physical simulation.\n"
                "- It does not cover oxygen level, pressure, materials or cabin geometry.\n"
                "- Its purpose is to show why Earth-based detector assumptions need testing in reduced gravity.")

with st.expander("Full research basis"):
    for cat in ["microgravity", "lunar", "martian", "general"]:
        for title, insight, url in RESEARCH[cat]:
            st.markdown(f"- **{title}** - {insight} ([link]({url}))")
