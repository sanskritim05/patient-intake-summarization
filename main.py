"""
main.py — Strands Agents patient intake summarization demo using GraphBuilder.

Graph topology
──────────────
                   ┌─────────────────────┐
                   │    intake_parser    │  (Node 1 - always runs first)
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │  completeness_check │  (Node 2 - always runs)
                   └──────┬──────┬───────┘
                          │      │
              complete ───┘      └──── incomplete
                          │                 │
             ┌────────────▼────────┐        │  (flagged path, skips symptom organizer)
             │  symptom_organizer  │        │
             └────────────┬────────┘        │
                          │                 │
                  ┌───────▼─────────────────▼──┐
                  │      summary_generator     │  (Node 4 - final summary)
                  └────────────────────────────┘
"""

import re
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

from config import get_model

from strands.multiagent.graph import GraphBuilder

from agents import (
    intake_parser_agent,
    completeness_check_agent,
    symptom_organizer_agent,
    summary_generator_agent,
)

# ---------------------------------------------------------------------------
# Conditional edge functions
# ---------------------------------------------------------------------------

def _extract_completeness_status(state) -> bool:
    """Parse the completeness status from the completeness_check node output."""
    result_node = state.results.get("completeness_check")
    if not result_node:
        return True

    text = str(result_node.result)
    match = re.search(
        r"COMPLETENESS_STATUS:\s*(COMPLETE|INCOMPLETE)",
        text,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).upper() == "COMPLETE"

    return True


def route_to_symptom_organizer(state) -> bool:
    """
    Traverse completeness_check to symptom_organizer
    ONLY when the intake record is complete.
    """
    is_complete = _extract_completeness_status(state)
    # print(
    #     f"[router] Completeness status: "
    #     f"{'COMPLETE — proceeding to symptom organizer' if is_complete else 'INCOMPLETE — routing to flagged summary'}"
    # )
    return is_complete


def route_to_flagged_summary(state) -> bool:
    """
    Traverse completeness_check directly to summary_generator
    ONLY when the intake record is incomplete.
    Skips symptom organization for a faster flagged summary.
    """
    return not _extract_completeness_status(state)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_intake_graph():
    """
    Construct and return the patient intake Graph.
    """
    model = get_model()

    for agent in (
        intake_parser_agent,
        completeness_check_agent,
        symptom_organizer_agent,
        summary_generator_agent,
    ):
        agent.model = model

    builder = GraphBuilder()

    # Nodes
    builder.add_node(intake_parser_agent,       "intake_parser")
    builder.add_node(completeness_check_agent,  "completeness_check")
    builder.add_node(symptom_organizer_agent,   "symptom_organizer")
    builder.add_node(summary_generator_agent,   "summary_generator")

    # Edges
    builder.add_edge("intake_parser", "completeness_check")

    builder.add_edge(
        "completeness_check",
        "symptom_organizer",
        condition=route_to_symptom_organizer,
    )

    builder.add_edge(
        "completeness_check",
        "summary_generator",
        condition=route_to_flagged_summary,
    )

    builder.add_edge("symptom_organizer", "summary_generator")

    builder.set_execution_timeout(300)
    builder.set_max_node_executions(20)

    return builder.build()


# ---------------------------------------------------------------------------
# Runner + sample scenarios
# ---------------------------------------------------------------------------

SAMPLE_INTAKES = [
    # Scenario A: complete intake — full summary path
    {
        "label": "Scenario A — Complete Intake",
        "request": (
            "New patient intake for Peter Parker, age 25. "
            "Chief complaint: persistent headache. "
            "Symptom duration: 5 days. "
            "Current medications: ibuprofen as needed. "
            "Allergies: penicillin. "
            "Relevant history: migraines since age 20."
        ),
    },
    # Scenario B: incomplete intake — flagged summary path
    {
        "label": "Scenario B — Incomplete Intake (flagged path)",
        "request": (
            "New patient intake for Steve Rogers, age 67. "
            "Chief complaint: shortness of breath on exertion. "
            "Current medications: not provided. "
            "Allergies: not provided. "
            "Relevant history: not provided."
        ),
    },
    # Scenario C: complete intake with urgent flags
    {
        "label": "Scenario C — Complete Intake with Urgent Flags",
        "request": (
            "New patient intake for Tony Stark, age 53. "
            "Chief complaint: sudden severe chest pain radiating to the left arm. "
            "Symptom duration: started 2 hours ago. "
            "Current medications: metformin, lisinopril. "
            "Allergies: aspirin. "
            "Relevant history: hypertension, type 2 diabetes diagnosed 2015."
        ),
    },
]


def run_intake(graph, scenario: dict) -> None:
    """Execute a single patient intake through the graph and print results."""
    label = scenario["label"]
    request = scenario["request"]

    print("\n" + "=" * 70)
    print(f"  {label}")
    print("=" * 70)
    print(f"Request: {request}\n")

    # Capture graph execution output
    output_buffer = StringIO()
    with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
        result = graph(request)

    captured_output = output_buffer.getvalue()

    # Print all captured output (includes all agent outputs and final summary)
    if captured_output.strip():
        print(captured_output)
    else:
        print("No output generated.")

    print("=" * 70)


def main():

    graph = build_intake_graph()

    scenarios = SAMPLE_INTAKES
    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
        scenarios = [SAMPLE_INTAKES[idx]]

    for scenario in scenarios:
        run_intake(graph, scenario)

    print("\n✅  Scenario complete.")


if __name__ == "__main__":
    main()
