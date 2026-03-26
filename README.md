# AI Social Media Generator for Gyms

A Streamlit MVP SaaS app for gyms to generate Instagram-ready content.  
Current build runs in offline content-bank mode (no API key needed) with target-wise post sequencing.

## Features

- Collects gym details:
  - Gym Name
  - City
  - Target Audience
  - Tone (Motivational, Friendly, Professional, Energetic)
- Includes 10 content targets (e.g. weightloss, fitness, weightgain, strength)
- Each target has 10 prebuilt posts (10-day sequence)
- On each click, app returns the next unused post for selected target
- Marks served posts as used and persists state locally
- Supports one-click reset for each target sequence
- Shows loading spinner while generating
- Displays formatted output in the app
- Lets users download the result as a `.txt` file

## Tech Stack

- Python
- Streamlit
- OpenAI Python SDK
- python-dotenv

## Project Structure

```text
.
├── app.py
├── prompts.py
├── requirements.txt
├── .env.example
└── README.md
```

## 1) Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Run Locally

```bash
streamlit run app.py
```

Open the local URL shown in your terminal (typically `http://localhost:8501`).

## 3) Deploy to Streamlit Cloud

1. Push this project to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and connect your GitHub repo.
4. Set the main file path to:
   - `app.py`
5. In **Advanced settings** or **Secrets**, add:
   - `OPENAI_API_KEY` = your OpenAI API key
6. Deploy the app.

## Notes

- Content library lives in `content_bank.py`.
- Usage tracking is persisted in `usage_state.json` (auto-created) via `content_store.py`.
- You can re-enable OpenAI generation later without changing the UI flow.
<<<<<<< HEAD
# promoting_gym
=======
>>>>>>> 41ebf03 (Initial MVP release for gym social content app.)
