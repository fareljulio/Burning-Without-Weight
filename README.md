# Fire Behavior Across Gravity

An interactive app that shows how fire and smoke change on the ISS, the Moon and Mars.

Try it here: (https://burning-without-weight.streamlit.app/)
Built for NASA Space Apps 2026.

## What is this?

On Earth, hot air rises, so smoke goes up to the ceiling and a smoke detector can find it. In space there is little or no gravity, so smoke acts differently. This app lets you move a slider from 0 g (the ISS) to Mars gravity and see what changes.

## What you can do

- Drag the slider or click ISS, Moon or Mars
- See charts of how smoke changes with gravity
- Read a short note on what it means for smoke detectors
- Press Play to watch it change on its own

## Where the numbers come from

They come from a research paper on flames in reduced gravity.

| Place | Gravity | Smoke stays in the flame | Amount of soot |
|---|---|---|---|
| ISS | 0 g | 0.082 | 17.8 |
| Moon | 0.16 g | 0.029 | 13.8 |
| Mars | 0.38 g | 0.021 | 12.7 |

Paper: "Smoke-point transition under partial gravity" (https://www.sciencedirect.com/science/article/pii/S1540748926003421)

## Things to know

- There are only three data points, so the lines between them are estimates.
- We have no data above 0.38 g, so the app says so instead of guessing.
- The advice on smoke detectors is a simple rule we made up. It is not a tested model.
- The data comes from lab experiments, not real spacecraft fires.

## Run it on your computer

```
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501

## Made with

Python, Streamlit and Plotly.

Team: SAGUWW
