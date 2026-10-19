from ta2.profile_store import ProfileStore

def test_profile_roundtrip(tmp_path):
    db = tmp_path / "profiles.db"
    store = ProfileStore(db)
    store.save_profile("M1", {"name": "Test", "department": "CSE"})
    assert store.get_profile("M1")["name"] == "Test"
