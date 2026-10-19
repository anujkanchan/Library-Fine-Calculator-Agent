from ta2.rag_policy import retrieve_policy

def test_rag_finds_reference_rule():
    hits = retrieve_policy("reference fine")
    assert hits
    assert "₹10" in "\n".join(h.text for h in hits)

def test_rag_reports_missing_rule():
    hits = retrieve_policy("laptop borrowing fee")
    assert hits == []
