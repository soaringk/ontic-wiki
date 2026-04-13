# Streams of Experience

Streams of experience are long-lived sequences of actions and observations that persist across time, allowing an agent to learn and adapt beyond one-shot interactions.

## Why It Matters

- A stream lets the agent carry information forward instead of treating each task as isolated.
- Long-horizon goals can justify actions that are neutral or costly in the short term but beneficial over time.
- Persistent interaction enables adaptation to a user, environment, or task distribution as conditions change.

## Design Implications

- Agents need memory and learning loops that extend beyond a single prompt-response exchange.
- Evaluation should include long-term outcomes, not only immediate task completion.
- Training methods must handle incomplete trajectories and delayed consequences.

## Related Pages

- [Experiential AI](../topics/experiential-ai.md)
- [Grounded Rewards](grounded-rewards.md)

## Sources

- [Welcome to the Era of Experience](../sources/welcome-to-the-era-of-experience.md)
