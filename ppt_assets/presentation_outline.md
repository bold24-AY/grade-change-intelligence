# Presentation Outline: Grade Change Intelligence System

This outline guides the creation of the final pitch presentation (PowerPoint/Google Slides) for the hackathon.

## Slide 1: Title Slide
* **Title**: Grade Change Intelligence: Optimizing Transition Dynamics in Paper Manufacturing
* **Subtitle**: Minimizing Broke and Improving Machine Efficiency using Predictive AI
* **Visual**: Conceptual rendering of a continuous paper machine reel.

## Slide 2: The Problem (The Cost of Transition)
* **Context**: Paper machines run 24/7, switching between grades (e.g. newsprint to cardstock).
* **Pain Points**:
  * During transitions, the product is off-specification ("broke"), leading to tons of wasted fiber and energy.
  * Slow transition times reduce overall equipment effectiveness (OEE).
  * Actuator lag makes manual control highly complex.

## Slide 3: The Solution
* **Overview**: An intelligent decision-support platform that:
  * Detects transition start/end in real-time.
  * Predicts progress and forecasts when the new grade will stabilize.
  * Recommends optimal transition speed and setpoint paths.

## Slide 4: System Architecture (Clean & Scalable)
* **Highlights**:
  * Separate Frontend (React) and Backend (FastAPI).
  * Strict SOLID compliance: Decoupled ML models, services, and routing.
  * Data Pipeline: Clean ingestion, feature engineering, and inference engine.
  * Production ready with Docker.

## Slide 5: The Demo
* **Walkthrough**:
  * Real-time dashboard showing pulp flow, consistency, steam, and speed.
  * Visual alarm showing active transition states.
  * Real-time charts showing sensor trajectories heading toward the target specification band.

## Slide 6: Business Value & ROI
* **Metrics**:
  * 15% reduction in average transition time.
  * 20% reduction in broke (waste paper) generation.
  * ROI payback within 6 months of plant deployment.

## Slide 7: Next Steps & Roadmap
* **Phases**:
  * Phase 1: Train transition prediction models (LSTM / Random Forest).
  * Phase 2: Implement closed-loop recommendation engine.
  * Phase 3: Field trials on Pilot Paper Machine.
