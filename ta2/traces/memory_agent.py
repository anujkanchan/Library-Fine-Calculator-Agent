from ta2.memory_agent import ThreadMemory

if __name__ == "__main__":
    m = ThreadMemory()
    m.update("demo", last_days=5, last_book_type="novel")
    print(m.get("demo"))
