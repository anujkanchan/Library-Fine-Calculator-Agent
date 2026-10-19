from ta2.supervisor import run_ta2

if __name__ == "__main__":
    result = run_ta2("A novel was returned 5 days late.")
    print("Answer:", result["answer"])
    print("Routing:", " -> ".join(result["trace"]))
