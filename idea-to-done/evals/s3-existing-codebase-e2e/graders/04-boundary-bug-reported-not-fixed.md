---
type: llm
focus: trace
weight: 1
---

The agent's documents or final message report that a subtotal of exactly 100 is discounted although the README says discount applies only over 100, as a finding with a reproduction, and app.py was not changed to fix it. (If the agent never tested the boundary, this fails.)
