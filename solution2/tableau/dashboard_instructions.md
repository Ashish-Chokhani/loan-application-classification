# Tableau Dashboard Instructions — HMDA Loan Denial Prediction

## Overview

Four Tableau dashboards are built from CSV files exported by `6_visualization_export.ipynb`.
---

## Dashboard 1: Data Quality & Loan Patterns

**Data source**: `tableau/data/dashboard_1_data_quality.csv`

Visualizes dataset quality and loan characteristics. Includes KPI summary cards (total records, denial rate, average loan amount), action taken distribution across all 8 categories, missing value analysis for top 30 columns, loan amount distribution by approval/denial status, and state-level denial rate geographic map.

---

## Dashboard 2: Model Performance Comparison

**Data source**: `tableau/data/dashboard_2_model_performance.csv`

Compares all trained models across evaluation metrics. Includes PR-AUC and ROC-AUC bar charts ranked by performance, bootstrap 95% confidence interval error bars, confusion matrix heatmaps, and denial precision/recall/F1 comparison across Logistic Regression, Random Forest, GBT, and SVM.

---

## Dashboard 3: Fair Lending & Business Insights

**Data source**: `tableau/data/dashboard_3_fair_lending.csv`

Provides fair lending analysis and operational insights. Covers denial rates by race, ethnicity, and sex demographics, denial patterns by loan purpose and loan type, occupancy type analysis, and average loan amount comparisons across demographic groups.

---

## Dashboard 4: Scalability & Cost Analysis

**Data source**: `tableau/data/dashboard_4_scalability.csv`

Demonstrates Spark's distributed processing characteristics. Includes strong scaling (fixed data, varying partitions), weak scaling (proportionally increasing data), training time comparison across all models, and estimated cloud compute cost per model.

---
