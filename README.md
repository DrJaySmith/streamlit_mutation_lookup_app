# SARS-CoV-2 Mutation Lookup App

A web application for analyzing specific mutations in SARS-CoV-2 proteins (Mpro, PLpro, and RBD) using data from GISAID and GenBank databases.

**Live App**: [https://mutationlookup.streamlit.app/](https://mutationlookup.streamlit.app/)

## Features

- Lookup population statistics for single or multiple mutations simultaneously
- Interactive timeline visualization with flexible data binning (Daily, Weekly, Monthly)
- Multiple visualization options (Linear/Log scale, Absolute/Relative counts)
- Support for three key SARS-CoV-2 proteins:
  - Mpro (Main Protease)
  - PLpro (Papain-Like Protease)
  - RBD (Receptor Binding Domain)
- Data sourced from GISAID and GenBank

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/DrJaySmith/streamlit_mutation_lookup_app.git
cd streamlit_mutation_lookup_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run src/functionless_app.py
```

The app will open in your default web browser. If it doesn't, navigate to the URL shown in the terminal (typically http://localhost:8501). 