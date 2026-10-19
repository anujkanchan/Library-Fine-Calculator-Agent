# Library Fine Agent — TA1

## 1. Project Overview

The **Library Fine Agent — TA1** is a Python-based application designed to calculate library fines for overdue book returns. It accepts natural-language queries, identifies the book type and number of overdue days, and calculates the fine using the application's configured rules and calculation tool.

This project demonstrates the fundamentals of AI agents, tool-based calculations, and input validation. It also serves as the baseline for comparison with the more advanced TA2 multi-agent system.

## 2. Objectives

- Calculate library fines based on overdue days and book type.
- Accept user queries in natural language.
- Use a calculation tool to compute fines.
- Validate inputs, including negative overdue-day values.
- Test supported and unsupported book categories.
- Provide clear calculation results and error messages.

## 3. Project Structure

```text
ta1/
├── library_fine_agent.py
└── README.md
```

**File descriptions:**

- `library_fine_agent.py` — Main Python application containing the library fine agent and its calculation functionality.
- `README.md` — Project documentation, execution instructions, and test cases.

## 4. Technology Stack

- **Programming Language:** Python
- **AI Agent:** Natural-language request processing
- **Calculation Tool:** Fine calculation and input validation

The exact libraries and model configuration depend on the implementation in `library_fine_agent.py`.

## 5. Installation and Execution

### Prerequisites

- Python installed on your system.
- Required Python dependencies installed.
- Any model runtime or API configuration required by the application.

### Run the Application

Open a terminal in the project root directory and execute:

```bash
python ta1\library_fine_agent.py
```

Follow the instructions displayed by the application and enter a test query when prompted.

## 6. Test Cases

### Test Case 1: Novel Returned Late

**Input:**

```text
I returned a novel 5 days late. What is my library fine?
```

**Purpose:** Verify fine calculation for a novel returned five days late.

**Expected behavior:** The agent identifies the book type and overdue days and calculates the fine using the configured daily rate for novels.

### Test Case 2: Textbook Returned Late

**Input:**

```text
I returned a textbook 4 days late. How much fine do I need to pay?
```

**Purpose:** Verify fine calculation for a textbook.

**Expected behavior:** The agent identifies the textbook category and calculates the fine using its configured daily rate.

### Test Case 3: Negative Overdue Days

**Input:**

```text
My novel was returned -3 days late. Calculate my library fine.
```

**Purpose:** Test validation of invalid overdue-day values.

**Expected behavior:** The application should reject negative overdue days and return an appropriate error instead of calculating a normal fine.

### Test Case 4: Magazine Fine

**Input:**

```text
I returned a magazine 5 days late. What is my fine?
```

**Purpose:** Test how the application handles the magazine category.

**Expected behavior:** If magazines are supported and a fine rate is configured, the application should calculate the fine. Otherwise, it should return an appropriate unsupported-category response.

### Test Case 5: Comic Book Fine

**Input:**

```text
I returned a comic book 6 days late. Calculate the overdue charge.
```

**Purpose:** Test how the application handles the comic-book category.

**Expected behavior:** If comic books are supported and a fine rate is configured, the application should calculate the fine. Otherwise, it should return an appropriate unsupported-category response.

## 7. Test Case Summary

| Test Case | Scenario | Objective |
| --- | --- | --- |
| 1 | Novel returned 5 days late | Verify fine calculation |
| 2 | Textbook returned 4 days late | Verify textbook fine calculation |
| 3 | Novel returned -3 days late | Verify input validation |
| 4 | Magazine returned 5 days late | Verify category support |
| 5 | Comic book returned 6 days late | Verify category support |

**Note:** Actual results depend on the fine rates, supported categories, and validation logic implemented in `library_fine_agent.py`. Record the actual output after running each test case.

## 8. TA1 vs. TA2

| Feature | TA1 | TA2 |
| --- | --- | --- |
| Fine calculation | Calculator tool | Calculator tool within a supervised workflow |
| Policy retrieval | Baseline implementation | RAG-based policy retrieval |
| Workflow | Basic agent and tool interaction | Supervisor-based multi-agent orchestration |
| Conversation memory | Depends on the TA1 implementation | Persistent thread memory using SQLite |
| Missing-policy handling | Depends on the TA1 implementation | Explicit missing-policy handling |
| Fine waiver | No TA2-style human approval gate | Human approval required for waiver requests |

TA1 provides the baseline fine-calculation functionality. TA2 extends the system with policy retrieval, supervisor routing, persistent memory, and human-in-the-loop approval.

## 9. Limitations

Depending on the implementation, the TA1 system may have the following limitations:

- Fine rates may be configured directly rather than retrieved from a policy document.
- It may not include a dedicated supervisor for coordinating multiple agents.
- It may not preserve conversation context across requests.
- It may not include a dedicated missing-policy handling workflow.
- It may not require human approval for fine-waiver requests.

These areas provide opportunities for further development in TA2.

## 10. Conclusion

The **Library Fine Agent — TA1** demonstrates how an AI agent can process natural-language queries and use a calculation tool to determine library fines. Its test cases cover standard fine calculations, input validation, and handling of potentially unsupported book categories.

The project establishes a baseline for comparison with TA2, which introduces a more structured multi-agent architecture with RAG-based policy retrieval, persistent memory, supervisor orchestration, and human approval for fine-waiver requests.