from src.app.contracts.revenue import StgRevenueRow


def test_revenue_contract_accepts_valid_row():
    row = {
        "RevenueMonth": "2024-01-01",
        "Revenue": 123.45
    }

    model = StgRevenueRow.model_validate(row)

    assert model.Revenue == 123.45
    assert str(model.RevenueMonth) == "2024-01-01"