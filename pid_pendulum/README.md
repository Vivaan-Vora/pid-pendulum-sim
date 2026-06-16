# PID Controller Simulation - Self-Balancing Inverted Pendulum

I built this project to show how I implement closed-loop control from scratch on a classic robotics problem: balancing an inverted pendulum on a cart in real time.

The goal was to avoid control-framework shortcuts and directly build the full loop myself:

- nonlinear physics simulation,
- manual PID controller implementation,
- live rendering and live state plotting,
- runtime gain tuning,
- disturbance testing and logged recovery metrics.

## What I built

Inside `pid_pendulum/`:

```text
main.py         # simulation loop / orchestration
physics.py      # nonlinear cart-pole dynamics + RK4/Euler integration
pid.py          # hand-built PID with anti-windup + derivative filtering
visualizer.py   # pygame cart + pendulum animation
plotter.py      # matplotlib real-time plots + gain sliders
logger.py       # CSV logging + step-response metrics
config.json     # default stable config
config_unstable.json
requirements.txt
```

## Why this project matters

The inverted pendulum is a standard benchmark in robotics and controls because it is unstable by default. If the controller design is weak, it fails quickly. I used it here to demonstrate practical controller behavior under disturbance, not just ideal textbook math.

## How to run

From repo root:

```bash
cd pid_pendulum
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py --config config.json
```

Headless run:

```bash
cd pid_pendulum
python3 main.py --config config.json --headless --no-realtime
```

## Runtime tuning (Kp, Ki, Kd)

When I run in GUI mode:

- `pygame` shows the cart and pendulum motion in real time,
- `matplotlib` shows angle, angular velocity, control output, and error,
- sliders let me tune `Kp`, `Ki`, and `Kd` while the simulation is running.

### How I think about each PID term physically

- **Kp**: reacts to current angle error.
  - too low: slow correction
  - too high: aggressive oscillation
- **Ki**: removes residual offset over time.
  - too high: windup and sluggish oscillation
- **Kd**: adds damping from motion trend.
  - too low: overshoot
  - too high: noisy or twitchy control

The PID implementation includes:

- explicit output limiting,
- integral clamping,
- back-calculation anti-windup,
- first-order derivative filtering.

## Disturbance testing and metrics

I inject a force impulse mid-run and then compute:

- recovery time,
- overshoot percentage,
- steady-state error.

Each run exports:

- `logs/run_<timestamp>.csv`
- `logs/run_<timestamp>_metrics.json`

Example stable-run metrics from this repo:

- recovery time: `0.14 s`
- overshoot: `16.64%`
- steady-state error: `0.0028 deg`

## Stable vs unstable examples

Generate comparison plots:

```bash
cd pid_pendulum

# Stable behavior (default config)
python3 main.py --config config.json --headless --no-realtime --duration 10 --save-plot examples/stable_run.png

# Deliberately poor tuning
python3 main.py --config config_unstable.json --headless --no-realtime --duration 10 --save-plot examples/unstable_run.png
```

This project is meant to be practical and transparent: every control and simulation piece is implemented directly so the behavior is easy to inspect, tune, and extend.

