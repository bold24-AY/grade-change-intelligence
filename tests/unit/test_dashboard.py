import pytest
from datetime import datetime
from fpdf import FPDF
from backend.app.recommendation.schema import AdjustmentRecommendation, ExplanationDetails, RecommendationOutput

def test_dashboard_imports():
    """Verify frontend dashboard assets and dependencies can resolve imports."""
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        import fpdf
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import dashboard dependencies: {str(e)}")

def test_pdf_report_compiler_logic():
    """Verify that FPDF compiles report document structures without raising errors."""
    pdf = FPDF()
    pdf.add_page()
    
    # Assert header block
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Test Grade Change Report", ln=True, align="C")
    
    # Assert body block
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Active Grade: GRADE_A", ln=True)
    pdf.cell(0, 8, "Pulp Stock Flow: 450.0 m3/h", ln=True)
    pdf.cell(0, 8, "Machine Speed: 850.0 mpm", ln=True)
    
    # Generate bytes
    pdf_bytes = pdf.output()
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
