# Library Fine Agent — TA2 (Unit 3 & 4)

A multi-agent library fine calculation system built with Python and LangGraph. It combines **RAG-based policy retrieval, tool-based fine calculation, persistent conversation memory, member profiles, supervisor routing, and human approval for fine-waiver requests**.

The system is designed to calculate fines using documented library rules while avoiding invented policy information and unauthorized fine waivers.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Unit 3: Memory and RAG](#unit-3-memory-and-rag)
- [Unit 4: Multi-Agent Workflow](#unit-4-multi-agent-workflow)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Demo and Test Cases](#demo-and-test-cases)
- [Evidence for Evaluation](#evidence-for-evaluation)
- [TA1 vs TA2 Comparison](#ta1-vs-ta2-comparison)
- [Jury Questions and Answers](#jury-questions-and-answers)
- [Limitations and Future Enhancements](#limitations-and-future-enhancements)

## Project Overview

The Library Fine Agent answers questions about overdue library books and calculates fines according to the library policy document.

Instead of allowing a language model to invent fine rates or calculate amounts from unsupported assumptions, the system separates policy retrieval, arithmetic, workflow coordination, and human approval.

### Objectives

- Retrieve relevant library rules using Retrieval-Augmented Generation (RAG).
- Calculate fines through the `calculate_library_fine` tool.
- Maintain conversation context across follow-up questions.
- Store thread memory and member profiles in SQLite.
- Validate inputs, including negative overdue-day values.
- Stop safely when no matching policy rule is found.
- Require human approval before granting a fine waiver.
- Demonstrate supervisor routing and agent interactions through execution traces.

## Architecture

```text
                         User
                           |
                           v
                      Supervisor
                           |
                           v
                    Policy Agent (RAG)
                           |
                           v
                 Retrieve Library Rules
                           |
                           v
                    Calculator Agent
                           |
                           v
                 calculate_library_fine
                           |
                           v
                      Supervisor
                           |
                           v
                 Optional Human Approval
                           |
                           v
                         Final
```

**Missing-policy path:**

```text
User -> Supervisor -> Policy Agent -> RAG
                                      |
                                      v
                              No matching chunk
                                      |
                                      v
                             Supervisor stops
                                      |
                                      v
                                Safe response
```

### Responsibilities

| Component | Responsibility |
| --- | --- |
| Supervisor | Coordinates workflow, routes requests, tracks execution hops, and stops when policy is missing or the hop limit is reached. |
| Policy Agent | Retrieves relevant policy information from the library rules document. |
| RAG Retriever | Searches the policy document for relevant information. |
| Calculator Agent | Uses the calculator tool with policy-derived rates and validated inputs. |
| Calculator Tool | Performs deterministic fine arithmetic and validates calculation inputs. |
| Thread Memory | Persists conversation history in SQLite so follow-up requests can reuse context. |
| Profile Store | Stores member profile information keyed by member ID. |
| Human Approval | Requests a human decision before a fine waiver can be granted. |

The arithmetic is handled by `calculate_library_fine`. The policy retriever supplies the relevant rules; it does not perform the calculation.

The supervisor enforces `MAX_HOPS = 6` as a workflow safety limit.

## Unit 3: Memory and RAG

### 1. Persistent Thread Memory

Conversation memory is stored in SQLite:

```text
ta2/library_ta2.db
```

This allows the application to retain conversation history associated with a thread and reuse relevant context for follow-up questions.

**Example**

First query:

```text
A novel was returned 5 days late.
```

Expected result:

```text
Fine: ₹10
```

Follow-up query in the same thread:

```text
and if it were a reference book?
```

The system can reuse the previous overdue-day value instead of requiring the user to repeat it.

### 2. Member Profile Storage

Member profiles are stored using SQLite through the profile store.

Conceptually, the profile is associated with a member ID:

```text
(member_id, profile)
```

The `profiles` table uses `member_id` as its key.

### 3. Retrieval-Augmented Generation (RAG)

The policy document is located at:

```text
ta2/docs/library_rules.txt
```

The RAG retriever searches this document for relevant library rules, such as applicable loan periods, fine rates, and waiver conditions when those rules are documented.

The retrieved policy information is used to determine the applicable rate before invoking the calculator.

**Important safety rule:** If the retriever cannot find a matching policy chunk, the system must not invent a rule or calculate a fine using an unsupported rate.

## Unit 4: Multi-Agent Workflow

### Policy Agent

- Retrieves relevant library policy information.
- Uses the RAG retriever to search the policy document.
- Does not perform fine arithmetic.
- Allows the workflow to stop safely when no relevant rule is found.

### Calculator Agent

- Uses the `calculate_library_fine` tool.
- Receives the overdue-day count, book type, and policy-derived daily rate.
- Validates calculation inputs.
- Returns a calculated fine or a clear error.
- Does not invent fine rates.

### Supervisor

- Coordinates the multi-agent workflow.
- Routes requests to the policy and calculator stages.
- Tracks execution using the workflow state and trace.
- Enforces the `MAX_HOPS = 6` safety limit.
- Prevents unsupported policy requests from proceeding to calculation.

### Human Approval

A waiver request requires a human decision. The system does not grant a waiver automatically.

For example:

```text
A novel is 5 days late. Please waive the fine.
```

The application requests a human decision. If the decision is negative, the waiver is denied and no waiver is granted.

## Key Features

- **RAG-based policy lookup:** Uses the documented library rules as the source of policy facts.
- **Deterministic calculation:** Calculates fines through `calculate_library_fine`.
- **Input validation:** Rejects negative overdue-day values.
- **Context-aware follow-ups:** Reuses relevant conversation history.
- **Persistent storage:** Uses SQLite for thread memory and member profiles.
- **Missing-policy handling:** Returns a safe response when no matching rule is available.
- **Human-in-the-loop approval:** Requires human approval for fine waivers.
- **Execution tracing:** Shows the stages followed by a request.
- **Supervisor hop limit:** Enforces `MAX_HOPS = 6`.

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Application implementation |
| LangGraph | Workflow and supervisor orchestration |
| LangChain tools/agent components | Tool integration and agent functionality |
| Ollama | Local model runtime |
| Qwen 2.5 3B | Local model configured for the agent components |
| RAG | Retrieval of policy information |
| SQLite | Persistent thread memory and profile storage |

## Project Structure

The main TA2 files are organized as follows:

```text
Library_Fine_Agent_by_Kgroup/
├── requirements.txt
└── ta2/
    ├── __init__.py
    ├── run_ta2.py
    ├── supervisor.py
    ├── policy_agent.py
    ├── rag_policy.py
    ├── calculator_agent.py
    ├── human_approval.py
    ├── memory_agent.py
    ├── profile_store.py
    ├── evaluate_ta1_vs_ta2.py
    ├── library_ta2.db
    ├── data/
    ├── docs/
    │   └── library_rules.txt
    └── traces/
```

### File Responsibilities

- `run_ta2.py` — Application entry point.
- `supervisor.py` — Coordinates the workflow and maintains execution state.
- `policy_agent.py` — Handles policy retrieval.
- `rag_policy.py` — Implements policy document retrieval.
- `calculator_agent.py` — Defines the fine calculation tool and calculator-related agent functionality.
- `human_approval.py` — Handles human approval for waiver requests.
- `memory_agent.py` — Manages persistent thread memory.
- `profile_store.py` — Manages member profile storage.
- `evaluate_ta1_vs_ta2.py` — Supports TA1 versus TA2 evaluation.
- `docs/library_rules.txt` — Source document for library policy retrieval.
- `library_ta2.db` — SQLite database for persistent application data.
- `traces/` — Directory for execution trace artifacts, if generated by the application.

The exact contents of `data/`, `traces/`, and other supporting directories may vary by project version.

## Installation and Setup

### Prerequisites

- Python installed on your system.
- Ollama installed and running.
- The local model `qwen2.5:3b` downloaded through Ollama.
- Project dependencies listed in `requirements.txt`.

### Step 1: Open the Project Directory

Open a terminal in the project root directory — the directory containing `requirements.txt` and the `ta2` package.

### Step 2: Create and Activate a Virtual Environment

Create the environment:

```bash
python -m venv .venv
```

On Windows Command Prompt:

```bat
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download the Local Model

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before launching the application.

### Step 5: Check Python Syntax

From the project root:

```bash
python -m py_compile ta2\supervisor.py ta2\calculator_agent.py
```

If the command finishes without an error, those files passed Python's syntax compilation check.

## Running the Application

From the project root, with the virtual environment activated and Ollama available, run:

```bash
python -m ta2.run_ta2
```

The application starts the Library Fine Agent demo. It uses a default thread ID and member ID when the user does not provide alternatives.

The interactive application supports commands such as:

```text
trace
profile
exit
```

Enter library questions at the application's `User:` prompt. Run installation commands and other shell commands in the terminal, not at the application's conversational prompt.

## Demo and Test Cases

Run these prompts in the application to demonstrate the main behaviors.

### Test 1: Normal Fine Calculation

**Input**

```text
A novel was returned 5 days late.
```

**Expected result**

```text
Fine: ₹10. The novel was 5 days overdue at ₹2 per day.
```

This demonstrates policy retrieval followed by tool-based arithmetic.

### Test 2: Follow-up Question Using Memory

**First input**

```text
A novel was returned 5 days late.
```

**Follow-up input**

```text
and if it were a reference book?
```

**Expected result**

```text
Fine: ₹50. The reference was 5 days overdue at ₹10 per day.
```

This demonstrates that the application can reuse the previous overdue-day value in the same conversation thread.

### Test 3: Negative Overdue Days

**Input**

```text
Calculate the fine for a novel returned -3 days late.
```

**Expected result**

```text
Error: The number of overdue days cannot be negative. Please provide a valid non-negative number of days.
```

This demonstrates input validation. A negative number of overdue days must not produce a valid fine.

### Test 4: Missing Policy Rule

**Input**

```text
What is the laptop borrowing fee?
```

**Expected result**

```text
I could not find a matching rule in the library policy document, so I will not invent one.
```

This demonstrates safe handling of a request that has no matching rule in the retrieved policy document.

### Test 5: Human Approval for a Waiver

**Input**

```text
A novel is 5 days late. Please waive the fine.
```

The application requests human approval.

If the human decision is negative, the expected result is:

```text
Waiver status: NOT APPROVED; no waiver was granted.
```

This demonstrates human-in-the-loop control for waiver requests.

> **Note:** The exact wording of prompts and traces may vary slightly depending on the implementation. Use the actual output from your running application as the final demonstration evidence.

## Evidence for Evaluation

### 1. Supervisor Routing Trace — Successful Calculation

A successful calculation should demonstrate the policy retrieval and calculator stages.

Example trace:

```text
SUPERVISOR -> POLICY_AGENT -> RAG -> CALCULATOR_AGENT -> TOOL -> SUPERVISOR -> FINAL
```

Expected calculation:

```text
Input:  A novel was returned 5 days late.
Output: Fine: ₹10
```

The fine is calculated using the policy-derived rate of ₹2 per overdue day.

### 2. Missing-Policy Trace

For an unsupported request such as:

```text
What is the laptop borrowing fee?
```

The retriever returns no matching policy chunk. The supervisor stops the workflow rather than passing an unsupported rate to the calculator.

Expected response:

```text
I could not find a matching rule in the library policy document, so I will not invent one.
```

### 3. Validation Trace

For a negative overdue-day value, show that the application returns a clear validation error rather than a calculated fine.

```text
Calculate the fine for a novel returned -3 days late.
```

Expected response:

```text
Error: The number of overdue days cannot be negative. Please provide a valid non-negative number of days.
```

### 4. Human Approval Trace

For a waiver request, show the approval prompt and the resulting approval or denial.

A denied request should show:

```text
Waiver status: NOT APPROVED; no waiver was granted.
```

### 5. Memory Demonstration

Show the initial novel fine calculation followed by the reference-book follow-up. The second query should reuse the prior overdue-day value.

## TA1 vs TA2 Comparison

| Case | TA1 behavior | TA2 evidence |
| --- | --- | --- |
| Novel returned 5 days late | Calculates the fine with a calculator/tool agent. | Retrieves the policy, invokes the calculator tool, and returns the fine. |
| Follow-up asks about a reference book | A fresh call may require the overdue days to be repeated. | Thread memory can retain relevant previous context. |
| Negative overdue days | Tool returns a validation error. | The error is handled within the supervised workflow. |
| Missing policy rule | No policy/RAG layer in the baseline design. | RAG detects the missing rule and the supervisor stops safely. |
| Fine-waiver request | No human approval gate in the baseline design. | Human approval is required before a waiver can be granted. |

This comparison describes the intended distinction between the TA1 baseline and the TA2 workflow. Demonstrate each behavior using the actual TA1 and TA2 implementations during evaluation.

## Jury Questions and Answers

### 1. Does the policy live in RAG and arithmetic in the tool?

**Yes.** The RAG retriever searches `ta2/docs/library_rules.txt` for relevant policy information. The `calculate_library_fine` tool performs the calculation and validates its inputs.

### 2. What happens if the Policy Agent finds no matching rule?

The supervisor stops the workflow and returns a missing-policy response. It does not invent a fine rate or pass an unsupported rate to the calculator.

### 3. What happens when the calculator returns an error?

The application reports the validation error clearly instead of treating it as a valid fine. For example, a negative overdue-day count must not produce a normal fine result.

### 4. Why use a supervisor?

The supervisor coordinates the workflow, routes requests between components, tracks execution, and enforces the maximum hop limit. This separates workflow control from policy retrieval and arithmetic.

### 5. Why use RAG instead of hardcoding every rule?

RAG allows the application to retrieve relevant information from the library policy document. This helps keep policy facts separate from the calculation logic and supports safe handling of unsupported questions.

### 6. What is the purpose of thread memory?

Thread memory stores conversation history so the application can use relevant information from earlier messages. For example, a follow-up can change the book type while reusing the previously stated overdue-day count.

### 7. Why use SQLite?

SQLite provides persistent local storage for conversation memory and member profiles without requiring a separate database server.

### 8. Why is human approval required for waivers?

Waiving a fine is an administrative decision. The system requests human approval rather than granting a waiver automatically.

### 9. What is `MAX_HOPS = 6`?

It is the configured maximum number of workflow hops. The supervisor uses this limit to prevent the workflow from continuing beyond the allowed bound.

### 10. What happens if a user asks for an unsupported borrowing fee?

The RAG retriever checks the policy document. If no matching rule is found, the supervisor returns a safe missing-policy response and does not calculate a fee using an invented rate.

## Limitations and Future Enhancements

Potential future enhancements include:

- Add a larger collection of policy documents and more advanced retrieval evaluation.
- Expand automated test coverage for the policy, calculator, memory, and approval components.
- Add structured logging and more detailed execution-trace exports.
- Add role-based authorization for librarian approval.
- Improve the interface for managing member profiles and viewing fine history.
- Add evaluation metrics for retrieval accuracy, calculation correctness, and end-to-end workflow reliability.

These are potential enhancements, not claims that the current implementation already includes them.

## Conclusion

The Library Fine Agent demonstrates a multi-agent workflow that combines policy retrieval, deterministic fine calculation, persistent memory, supervisor-based routing, and human approval.

Its central design principle is to **retrieve policy facts, calculate only from supported rules, validate inputs, and require human approval for fine waivers**