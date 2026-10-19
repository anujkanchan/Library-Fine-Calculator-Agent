from ta2.profile_store import ProfileStore

if __name__ == "__main__":
    s = ProfileStore()
    s.save_profile("M001", {"member_id": "M001", "name": "Demo Member"})
    print(s.get_profile("M001"))
