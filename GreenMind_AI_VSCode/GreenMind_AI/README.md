# GreenMind AI

GreenMind AI is a local Streamlit dashboard for plant leaf disease screening. It uses the public `mesabo/agri-plant-disease-resnet50` ResNet50 classifier (38 PlantVillage categories), then presents organic-first supportive guidance and a downloadable PDF summary.

## Run in VS Code

1. Extract this ZIP and open the `GreenMind_AI` folder in VS Code.
2. Install Python **3.11 or newer**. In the VS Code terminal, create and activate a virtual environment:

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python run.py
   ```
   Or run `streamlit run app/frontend/app.py`.
5. Open the local address shown in the terminal (usually `http://localhost:8501`).

The first diagnosis downloads and caches the public model (roughly 100 MB), so an internet connection is required once. Later launches reuse `model_cache/` and can work offline.

## Features

- JPG/PNG validation, RGB conversion, and size limits
- Cached ResNet50 inference with confidence, inference time, and top-three chart
- Disease facts and sustainable traditional/organic guidance
- Local JSON diagnosis history (no image uploads are stored)
- PDF report download
- Friendly model and image error messages

## Project layout

```text
app/
  frontend/app.py            Streamlit dashboard
  diagnosis/predictor.py     Model inference
  models/model_loader.py     Download and cache handling
  database/                  Remedy knowledge and local history
  utils/                     Image validation and PDF reports
configs/settings.py          Central configuration
data/                        Created automatically for local history
tests/                       Small unit tests
```

## Verify

Run the quick non-model test suite:

```bash
python -m pytest
```

## Responsible use

This is a visual screening aid, not a guarantee of diagnosis. Confirm fast-spreading symptoms and any treatment plan with a local agricultural extension professional. Follow local regulations and product labels.
