# Grade Transition Optimization Notes

Grade transitions in paper making represent transient phases between steady states. Minimizing the transition duration and off-spec paper production (broke) is a classic control and scheduling problem.

## Dynamic Transition Mechanisms
During a transition:
1. **Basis Weight**: Adjusted by varying thick stock pulp flow valve openings. Follows a first-order lag with delay.
2. **Moisture**: Regulated by dryer cylinder steam pressure. Steam response time constants are slow (1-3 minutes).
3. **Machine Speed**: Scaled up or down depending on target grade limits.

## Potential Algorithms
- **Model Predictive Control (MPC)**: Formulates state-space control equations under constraints on valve slew rates.
- **Reinforcement Learning (RL)**: Policy gradients to adjust actuator targets step-by-step.
- **Dynamic Time Warping (DTW)**: To classify transition starts by comparing active sensor series with historical run templates.
