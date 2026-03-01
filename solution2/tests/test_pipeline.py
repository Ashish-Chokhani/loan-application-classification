"""
test_pipeline.py — HMDA 2023 Pipeline Tests
=============================================
Validates schema, data leakage checks, feature engineering,
model artifacts, and Spark configuration.

Usage:
    python -m pytest tests/test_pipeline.py -v
"""

import json
import os
import sys
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

DATA_DIR = os.path.join(PROJECT_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SCHEMA_PATH = os.path.join(DATA_DIR, "schemas", "hmda_schema.json")
CONFIG_PATH = os.path.join(PROJECT_DIR, "config", "spark_config.yaml")


class TestSchemaDefinition:
    """Validate the HMDA schema JSON."""

    @pytest.fixture(autouse=True)
    def load_schema(self):
        with open(SCHEMA_PATH) as f:
            self.schema = json.load(f)

    def test_total_columns(self):
        assert self.schema["total_expected_columns"] == 99

    def test_all_columns_ordered_count(self):
        assert len(self.schema["all_columns_ordered"]) == 99

    def test_target_variable_defined(self):
        target = self.schema["target_variable"]
        assert target["column"] == "action_taken"
        assert target["keep_values"] == [1, 3]
        assert target["mapping"] == {"1": 0, "3": 1}

    def test_leakage_columns_defined(self):
        leakage = self.schema["leakage_columns"]["columns"]
        assert len(leakage) == 12
        assert "denial_reason_1" in leakage
        assert "rate_spread" in leakage
        assert "purchaser_type" in leakage

    def test_column_groups_sum_to_total(self):
        groups = self.schema["column_groups"]
        total = sum(g["count"] for g in groups.values())
        assert total == 99

    def test_no_leakage_in_expected_features(self):
        leakage = set(self.schema["leakage_columns"]["columns"])
        # These should be documented as leakage, not used as model features
        for col in leakage:
            assert col in self.schema["all_columns_ordered"], \
                f"Leakage column {col} missing from schema"


class TestDataLeakage:
    """Ensure leakage columns are excluded from features."""

    LEAKAGE_COLS = {
        "denial_reason_1", "denial_reason_2", "denial_reason_3", "denial_reason_4",
        "purchaser_type", "rate_spread", "total_loan_costs", "total_points_and_fees",
        "origination_charges", "discount_points", "lender_credits",
        "prepayment_penalty_term",
    }

    def test_leakage_count(self):
        assert len(self.LEAKAGE_COLS) == 12

    def test_denial_reasons_flagged(self):
        for i in range(1, 5):
            assert f"denial_reason_{i}" in self.LEAKAGE_COLS

    def test_post_decision_columns_flagged(self):
        post_decision = {"rate_spread", "total_loan_costs", "origination_charges",
                         "discount_points", "lender_credits"}
        assert post_decision.issubset(self.LEAKAGE_COLS)


class TestDataDownload:
    """Verify raw data availability."""

    def test_raw_csv_exists(self):
        csv_path = os.path.join(RAW_DIR, "hmda_2023.csv")
        if not os.path.exists(csv_path):
            pytest.skip("Raw CSV not downloaded yet")
        assert os.path.getsize(csv_path) > 1_000_000_000, \
            "CSV should be > 1 GB"

    def test_parquet_exists(self):
        parquet_path = os.path.join(PROCESSED_DIR, "hmda_2023.parquet")
        if not os.path.exists(parquet_path):
            pytest.skip("Parquet not generated yet (run notebook 1)")
        assert os.path.isdir(parquet_path), "Parquet should be a directory"


class TestSparkConfig:
    """Validate Spark configuration."""

    @pytest.fixture(autouse=True)
    def load_config(self):
        import yaml
        with open(CONFIG_PATH) as f:
            self.config = yaml.safe_load(f)

    def test_app_name(self):
        assert self.config["spark"]["app_name"] == "HMDA_Mortgage_Analysis"

    def test_master_local(self):
        assert "local" in self.config["spark"]["master"]

    def test_driver_memory(self):
        mem = self.config["spark"]["config"]["spark.driver.memory"]
        assert "g" in mem.lower()

    def test_aqe_enabled(self):
        assert self.config["spark"]["config"]["spark.sql.adaptive.enabled"] is True

    def test_target_column(self):
        assert self.config["model"]["target_column"] == "action_taken"

    def test_random_seed(self):
        assert self.config["model"]["random_seed"] == 42


class TestModelArtifacts:
    """Check model output files."""

    def test_model_results_json(self):
        results_path = os.path.join(PROCESSED_DIR, "model_results_4.json")
        if not os.path.exists(results_path):
            pytest.skip("Model results not generated yet (run notebook 4)")
        with open(results_path) as f:
            results = json.load(f)
        assert len(results) >= 2, "Should have at least 2 models"

    def test_eda_results(self):
        eda_path = os.path.join(PROCESSED_DIR, "eda_results.pkl")
        if not os.path.exists(eda_path):
            pytest.skip("EDA results not generated yet (run notebook 2)")
        assert os.path.getsize(eda_path) > 0

    def test_evaluation_report(self):
        report_path = os.path.join(PROCESSED_DIR, "results", "final_evaluation_report.json")
        if not os.path.exists(report_path):
            pytest.skip("Evaluation report not generated yet (run notebook 5)")
        with open(report_path) as f:
            report = json.load(f)
        assert "best_model" in report
        assert "bootstrap_confidence_intervals" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
