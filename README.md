# SARS-CoV-2 Mutation Analysis App

A Streamlit application for analyzing mutations in SARS-CoV-2 proteins (Mpro, PLpro, and RBD) using data from GISAID and GenBank databases.

## Features

- 🔍 Analyze single or multiple mutations simultaneously
- 📊 Interactive timeline visualization
- 📈 Flexible data binning (Daily, Weekly, Monthly)
- 📉 Multiple visualization options (Linear/Log scale, Absolute/Relative counts)
- 🦠 Support for three key SARS-CoV-2 proteins:
  - Mpro (Main Protease)
  - PLpro (Papain-Like Protease)
  - RBD (Receptor Binding Domain)
- 📅 Important variant emergence date markers for RBD analysis
- 🔄 Automatic RBD position adjustment for mutations > position 330

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/streamlit_mutation_lookup_app.git
cd streamlit_mutation_lookup_app
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure your data files are in the correct location:
```
results/
├── gisaid/
│   ├── mpro/
│   │   └── tables/
│   │       └── gisaid_mpro_date_matrix.csv
│   ├── plpro/
│   │   └── tables/
│   │       └── gisaid_plpro_date_matrix.csv
│   └── rbd/
│       └── tables/
│           └── gisaid_rbd_date_matrix.csv
└── genbank/
    ├── mpro/
    │   └── tables/
    │       └── genbank_mpro_date_matrix.csv
    ├── plpro/
    │   └── tables/
    │       └── genbank_plpro_date_matrix.csv
    └── rbd/
        └── tables/
            └── genbank_rbd_date_matrix.csv
```

2. Run the Streamlit app:
```bash
streamlit run src/functionless_app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Data Format

The application expects CSV files containing mutation data matrices with the following format:
- Rows: Individual strains with mutation information
- Columns: Dates
- Values: Counts/presence of mutations

## Deployment

To deploy the app on Streamlit Cloud:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select the main file: `src/functionless_app.py`
5. Deploy!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 