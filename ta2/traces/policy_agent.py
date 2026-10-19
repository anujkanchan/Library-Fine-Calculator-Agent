from ta2.policy_agent import retrieve_library_policy

if __name__ == "__main__":
    print(retrieve_library_policy.invoke({"query": "reference fine"}))
    print(retrieve_library_policy.invoke({"query": "laptop fee"}))
