_**Fire Behavior Across Gravity**_

Live app: <add link> Demo video: <add link> Built for NASA Space Apps 2026, challenge: <add challenge name> Team: <add names>

**Why we made this**

Smoke detectors are built and tested on Earth, where hot air rises and carries smoke up to the ceiling. Take that away and flames behave very differently. On the ISS a flame can turn round and sooty because nothing pulls the hot gas away. The Moon and Mars have some gravity, but a lot less than Earth, so what happens to the smoke there is not obvious.

We wanted to look at one question: if you design a smoke detector for a lunar or Martian habitat, can you copy the ISS or Earth approach, or does it need something different?

**What the app does**

You pick a gravity level with the slider (or the ISS, Moon, Mars and Earth buttons) and the app shows:

how soot residence time changes with gravity
how peak soot volume fraction changes with gravity
both values as a percentage of the microgravity case
a short note on what that might mean for smoke detection
research notes that match the gravity you picked

There is also a Play button that sweeps from 0 to 0.38 g, which is handy for a demo.

**The data**

All numbers come from three measured points in a 2026 paper on the smoke-point transition in partial gravity (parabolic flight experiments):

Gravity	Residence time	Max soot volume fraction
1. 0 g (ISS)	0.082	17.8
2. 0.16 g (Moon)	0.029	13.8
3. 0.38 g (Mars)	0.021	12.7

Paper: https://www.sciencedirect.com/science/article/pii/S1540748926003421 DOI: <add> Table and units: <add>

The most interesting thing in the table is that residence time drops by roughly 74% between 0 g and the Moon, while peak soot only drops by about 29%.

**What this app can't tell you**

We would rather be upfront about this:

There are only three data points. The lines between them are straight-line guesses, and the real curve may bend.
There is no data above 0.38 g, so the app doesn't make recommendations there. The Earth button just shows that nothing was measured.
The detector advice is a simple rule we wrote ourselves (thresholds of 0.05 for residence time and 15 for soot). It is not a tested detector model and it does not predict alarm times.
The experiments were done in a lab, not on real spacecraft fires.
Oxygen level, cabin pressure, materials and cabin size all matter in real fires and none of them are in this app.
The Earth reference box uses a different type of flame (jet flames), so those figures show which way things go on Earth but can't be plotted on the same chart.

**Sources**
Smoke-point transition under partial gravity (2026): https://www.sciencedirect.com/science/article/pii/S1540748926003421
Non-buoyant smoke point: https://www.sciencedirect.com/science/article/abs/pii/S0010218018304395
Burning candles in microgravity: https://www.researchgate.net/publication/24329285_Burning_Candles_in_the_Microgravity_of_Space
SAFFIRE V: https://up2date.uni-bremen.de/en/article/brand-new-findings-on-fire-safety-in-space
Flame spread in exploration atmospheres: https://www.researchgate.net/publication/255013038_Microgravity_Flame_Spread_in_Exploration_Atmospheres_Pressure_Oxygen_and_Velocity_Effects_on_Opposed_and_Concurrent_Flame_Spread
NASA ACME: https://www.nasa.gov/centers-and-facilities/glenn/studying-flame-behavior-in-microgravity-with-a-solid-high-five/
Combustion Integrated Rack: https://www.americanscientist.org/article/fire-in-microgravity
Burning Rate Emulator: https://www.sciencedirect.com/science/article/abs/pii/S0010218021000493
Confined-space flame study: https://issnationallab.org/upward/upward-62-case-western-flame-study/
Soot in 1 g vs microgravity (NASA NTRS): https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf and https://ntrs.nasa.gov/api/citations/19970020584/downloads/19970020584.pdf

**Running it yourself**
You need Python 3.9 or newer.

git clone <repo url>
cd <repo folder>
pip install -r requirements.txt
streamlit run app.py

Then open http://localhost:8501 in your browser.

To put it online for free, push the repo to GitHub and deploy it at https://share.streamlit.io.

**Files**
app.py: the app
requirements.txt: streamlit, plotly, numpy

**Credits**
Built with Python, Streamlit and Plotly. The research belongs to the authors listed above. This project is not affiliated with or endorsed by NASA.
