# Loan Application Classification — HMDA 2023 Big Data ML Pipeline

A distributed machine learning pipeline for predicting mortgage loan approval/denial using the **HMDA 2023 Snapshot National Loan-Level Dataset** (10M+ records, 99 features, ~4 GB).

Built with **PySpark MLlib** for scalable processing and **Tableau** for interactive visualization.

---

## Dataset

| Property | Value |
|----------|-------|
| **Source** | [CFPB HMDA 2023 Snapshot](https://ffiec.cfpb.gov/data-publication/snapshot-national-loan-level-dataset/2023) |
| **Records** | 10,000,000+ loan applications |
| **Features** | 99 columns (loan, applicant, property, demographics, census) |
| **Size** | ~4 GB (CSV), ~800 MB (Parquet) |
| **Target** | `action_taken`: Originated (1) vs. Denied (3) |

### Download

Download directly from the [CFPB website](https://ffiec.cfpb.gov/data-publication/snapshot-national-loan-level-dataset/2023) and place in `data/raw/`.

---

## Project Structure

```
project/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   ├── spark_config.yaml          # SparkSession configuration
├── data/
│   ├── raw/                       # Original CSV (gitignored)
│   ├── processed/                 # Parquet + EDA outputs (gitignored)
│   └── schemas/
│       └── hmda_schema.json       # 99-column schema with validation rules
├── notebooks/
│   ├── 1_data_ingestion.ipynb     # CSV → Parquet, schema validation
│   ├── 2_eda_comprehensive.ipynb  # Full EDA on all 99 features
│   ├── 3_feature_engineering.ipynb # Pipeline: Imputer → Encoder → Scaler
│   └── 4_model_training.ipynb     
├── scripts/
│   ├── run_pipeline.py            # End-to-end execution script
├── tableau/
│   ├── dashboard_1.twbx            # Data Quality
│   ├── dashboard_2.twbx            # Model Performance
│   ├── dashboard_3.twbx            # Fair Lending
│   └── dashboard_4.twbx            # Scalability
└── tests/
    └── test_pipeline.py           # Schema & leakage checks
```

---