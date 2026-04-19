# Streams of Experience

Streams of experience are long-lived sequences of actions and observations that persist across time, allowing an agent to learn and adapt beyond one-shot interactions.

## Why It Matters

- A stream lets the agent carry information forward instead of treating each task as isolated.
- Long-horizon goals can justify actions that are neutral or costly in the short term but beneficial over time.
- Persistent interaction enables adaptation to a user, environment, or task distribution as conditions change.
- Sequential exposure can make evaluation more realistic by rewarding accumulated familiarity instead of forcing an agent to restart cold on every task.

## Design Implications

- Agents need memory and learning loops that extend beyond a single prompt-response exchange.
- Evaluation should include long-term outcomes, not only immediate task completion.
- Training methods must handle incomplete trajectories and delayed consequences.
- Benchmarks for software, customer service, and other real work should often preserve context across tasks rather than assume i.i.d. episodes.

## Related Pages

- [Experiential AI](../topics/experiential-ai.md)
- [Grounded Rewards](grounded-rewards.md)
- [Utility Problem](utility-problem.md)

## Sources

- [Welcome to the Era of Experience](../sources/welcome-to-the-era-of-experience.md)
- [We're at AI's Halftime](../sources/were-at-ais-halftime.md)
