from ta2.calculator_agent import calculate_library_fine

if __name__ == "__main__":
    print(calculate_library_fine.invoke({"days_overdue": 5, "book_type": "novel"}))
    print(calculate_library_fine.invoke({"days_overdue": -3, "book_type": "novel"}))
