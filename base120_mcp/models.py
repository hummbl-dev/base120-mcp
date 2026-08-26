"""Base120 Mental Models Dictionary & Taxonomy.

Curated set of 120 operational mental models across 6 core domains.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MentalModel:
    id: str
    name: str
    domain: str
    summary: str
    prompt_guidance: str


MODELS: Dict[str, MentalModel] = {
    # 1. Perspective & Inversion
    "IN1": MentalModel("IN1", "Inversion", "Perspective", "Approach problems backwards: identify how to fail and systematically avoid those conditions.", "Step 1: List all ways this system or decision could fail disastrously. Step 2: Formulate explicit safeguards against each failure mode."),
    "IN2": MentalModel("IN2", "First Principles", "Perspective", "Boil a problem down to its most fundamental truths and reason up from there.", "Strip away all assumptions, conventions, and analogies. Identify what is physically and logically incontrovertible."),
    "IN3": MentalModel("IN3", "Second-Order Thinking", "Perspective", "Evaluate not just the immediate effect of an action, but the downstream consequences of those effects.", "Ask: 'And then what?' Map out the ripple effects across 30 days, 6 months, and 2 years."),
    "IN4": MentalModel("IN4", "Occam's Razor", "Perspective", "Among competing hypotheses, select the one that makes the fewest assumptions.", "Eliminate unnecessary complexity; prefer simpler architectural mechanisms that satisfy the invariant."),
    
    # 2. Composition & Emergence
    "CO1": MentalModel("CO1", "Synergy", "Composition", "The whole system exhibits properties greater than the sum of its individual parts.", "Identify positive reinforcement loops where component A amplifies component B."),
    "CO2": MentalModel("CO2", "Antifragility", "Composition", "Systems that gain strength, resilience, and capability when exposed to volatility, stress, and error.", "Design error handling to automatically capture failure telemetry and harden invariants."),
    "CO3": MentalModel("CO3", "Network Effects", "Composition", "The value of a system or platform increases non-linearly with each additional participant.", "Analyze how each new agent or node lowers the coordination cost for the entire mesh."),

    # 3. Decomposition & Invariants
    "DE1": MentalModel("DE1", "MECE", "Decomposition", "Mutually Exclusive, Collectively Exhaustive problem structuring.", "Ensure all sub-problems cover the entire solution space with zero overlap."),
    "DE2": MentalModel("DE2", "Pareto Principle (80/20)", "Decomposition", "80% of outcomes result from 20% of inputs or causes.", "Identify the critical 20% bottleneck or leverage point that dictates system performance."),
    "DE3": MentalModel("DE3", "Root Cause Analysis (5-Whys)", "Decomposition", "Iterative interrogative technique used to explore the cause-and-effect relationships underlying a particular failure.", "Trace the causal chain 5 levels deep until reaching the foundational design or process defect."),

    # 4. Recursion & Compounding
    "RE1": MentalModel("RE1", "Compounding", "Recursion", "Small, continuous improvements accumulate exponentially over time.", "Focus on recurring automated daily loops that reduce friction by 1% each cycle."),
    "RE2": MentalModel("RE2", "Feedback Loops", "Recursion", "Outputs of a system are routed back as inputs forming a closed circuit.", "Construct rapid verification signals that give immediate corrective feedback to the agent."),

    # 5. Systems & Cybernetics
    "SY1": MentalModel("SY1", "Ashby's Law of Requisite Variety", "Systems", "If a system is to be stable, the number of states of its control mechanism must be greater than or equal to the number of states in the system being controlled.", "Ensure your agent safety controls possess equal or greater variety than the agent's tool action space."),
    "SY2": MentalModel("SY2", "Theory of Constraints", "Systems", "A chain is only as strong as its weakest link; overall throughput is dictated by the primary bottleneck.", "Locate the single resource constraint gating execution and optimize exclusively around it."),
    "SY3": MentalModel("SY3", "Le Chatelier's Principle", "Systems", "Any change in status quo prompts an opposing reaction in the system.", "Anticipate systemic resistance or counter-incentives when introducing new policy rules."),

    # 6. Games & Incentives
    "GA1": MentalModel("GA1", "Nash Equilibrium", "Games", "An outcome where no participant can improve their position by unilaterally changing strategy.", "Model agent-human coordination where truth-telling and deterministic logging is the dominant strategy."),
    "GA2": MentalModel("GA2", "Principal-Agent Problem", "Games", "Conflicts of interest when an agent is delegated to act on behalf of a principal.", "Enforce cryptographic delegation tokens and audit buses to guarantee strict alignment with principal intent."),
}
