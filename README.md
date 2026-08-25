
# Q-CAT AI — Classical V1

A classical-computing prototype for sustainable fertiliser and nitrogen-fixation catalyst discovery.

## What this version does

1. Selects a catalyst candidate.
2. Runs a classical multi-factor screening score.
3. Displays predicted/estimated properties.
4. Ranks candidate catalysts.
5. Shows performance analytics.
6. Shows clearly labelled prototype estimates for energy and CO2 reduction.
7. Generates a simple research summary.
8. Provides a clean place to connect your trained ML model.

## Run

```bash
py -m pip install -r requirements.txt
py app.py
```

Open:

`http://127.0.0.1:5000`

## Connecting your Google Colab trained model

The integration point is in `app.py` inside `/api/analyze`.

Replace the demo scoring/prediction section with your actual model loading and preprocessing code.

Important:
- Do not claim quantum computation in V1.
- Do not present demo environmental numbers as experimentally validated.
- Use real model outputs wherever available.
- Quantum algorithms/simulation can be added as V2 later.
