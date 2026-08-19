# 🏭 Agentic AI-Powered Digital Twin for Manufacturing Operations

An experimental **Agentic AI-powered Digital Twin** for manufacturing operations that combines discrete-event simulation, digital twins, machine learning, predictive maintenance, and autonomous decision-making.

The project explores how a traditional Digital Twin can evolve from simply **monitoring a manufacturing system** into an intelligent system capable of **predicting failures, making decisions, and autonomously triggering preventive actions**.

---

## 🔄 System Architecture

```text
MANUFACTURING SYSTEM
        ↓
   DIGITAL TWIN
        ↓
TIME-SERIES DATA
        ↓
 MACHINE LEARNING
        ↓
 PREDICT FAILURE
        ↓
 AI DECISION AGENT
        ↓
 AUTONOMOUS ACTION
        ↓
PREVENTIVE MAINTENANCE
        ↺
```

The closed-loop architecture follows:

**Observe → Predict → Decide → Act → Observe**

---

## 🏗️ Manufacturing Simulation

The simulated manufacturing environment contains a three-machine production line:

```text
Machine 1 → Buffer 1 → Machine 2 → Buffer 2 → Machine 3
```

The factory simulation includes:

- Variable processing times
- Finite production buffers
- Machine temperature changes
- Machine health degradation
- Cooling behaviour
- Overheating
- Machine failures
- Reactive maintenance
- Preventive maintenance
- Downtime tracking
- Product cycle-time tracking
- Throughput measurement

The simulation is implemented using **Python and SimPy**.

---

## 🪞 Digital Twin Layer

Each manufacturing machine has a corresponding digital twin that maintains its operational state.

The twin monitors information such as:

- Machine status
- Current product
- Products processed
- Temperature
- Temperature condition
- Machine health
- Health condition
- Utilisation
- Last update time

---

## 📊 Data Collection

Two logging mechanisms are used.

### Event Logging

Factory events include:

- Product arrivals
- Processing start/finish
- Buffer movements
- Product completion
- Machine failures
- Maintenance events

### Time-Series Monitoring

The complete factory state is recorded every simulated second.

This dataset provides the foundation for machine-learning-based monitoring and predictive maintenance.

---

## 🤖 ML Anomaly Detection

An **Isolation Forest** model is trained using normal factory operating conditions.

### Results

| Metric | Score |
|---|---:|
| Accuracy | 86.39% |
| Precision | 96.89% |
| Recall | 80.30% |
| F1-score | 87.82% |

The model is trained using normal observations from simulation runs 1–24 and evaluated using unseen runs 25–30.

---

## 🔧 Predictive Maintenance

A predictive-maintenance model estimates whether **Machine 2 is likely to fail within the next 15 simulated seconds**.

### Results

| Metric | Score |
|---|---:|
| Accuracy | 98.24% |
| Precision | 90.58% |
| Recall | 99.43% |
| F1-score | 94.79% |

The prediction is passed to the AI decision layer rather than being used only as an alert.

---

## 🧠 Agentic AI Decision Layer

The decision agent continuously evaluates the state of the manufacturing system.

```text
Observe factory state
        ↓
Estimate failure probability
        ↓
Assess operational risk
        ↓
Select an action
        ↓
Execute intervention
        ↓
Observe updated factory state
```

Possible decisions include:

- `CONTINUE`
- `MONITOR`
- `REDUCE_LOAD`
- `SCHEDULE_MAINTENANCE`
- `EMERGENCY_MAINTENANCE`

When failure probability becomes sufficiently high, the agent can autonomously initiate **preventive maintenance**.

---

## ⚡ Example Autonomous Intervention

During one simulation:

```text
AGENT ALERT | Failure probability = 82.7%

AGENT ACTION | Preventive maintenance started

AGENT ACTION | Preventive maintenance completed
```

Instead of waiting for Machine 2 to overheat and fail, the agent intervened before the reactive failure occurred.

---

# 📈 Baseline vs Agent Evaluation

The system was evaluated using **30 paired simulation experiments**.

Each baseline and agent-controlled experiment used the same random seed to provide a fair comparison.

| Metric | Baseline | Agent |
|---|---:|---:|
| Products completed | 21.667 | 22.467 |
| Throughput | 0.120 | 0.125 |
| Average cycle time | 31.882 s | 31.445 s |
| Reactive downtime | 15.0 s | 1.5 s |
| Preventive downtime | 0 s | 10.0 s |
| Total downtime | 15.0 s | 11.5 s |
| Reactive failure runs | 30/30 | 3/30 |

### Key Results

📉 **90% reduction in reactive downtime**

📈 **3.69% increase in throughput**

⏱️ **1.37% reduction in average cycle time**

🛠️ **Reactive failure runs reduced from 30/30 to 3/30**

The experiment demonstrates how predictive intervention can exchange unexpected failure downtime for controlled preventive-maintenance downtime.

---

## 📂 Project Structure

```text
Agentic_twin/
│
├── factory_sim.py
│   └── Manufacturing simulation and physical behaviour
│
├── twin.py
│   └── Machine Digital Twin implementation
│
├── logger.py
│   └── Factory event logging
│
├── timeseries_logger.py
│   └── Time-series factory monitoring
│
├── generate_dataset.py
│   └── Simulation dataset generation
│
├── anomaly_detection.py
│   └── Rule-based anomaly detection
│
├── ml_anomaly_detection.py
│   └── Isolation Forest anomaly detection
│
├── predictive_maintenance.py
│   └── Failure prediction model
│
├── risk_assessment.py
│   └── Machine risk assessment
│
├── decision_agent.py
│   └── Agent decision logic
│
├── agent_controller.py
│   └── Connection between ML prediction and agent actions
│
├── compare_agent_vs_baseline.py
│   └── Baseline vs agent-controlled experiments
│
├── run_demo.py
│   └── Main demonstration
│
└── requirements.txt
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/KKarunarathne1999/agentic-ai-manufacturing-digital-twin.git
```

Enter the project:

```bash
cd agentic-ai-manufacturing-digital-twin
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run the main Agentic Digital Twin simulation:

```bash
python run_demo.py
```

Run ML anomaly detection:

```bash
python ml_anomaly_detection.py
```

Run predictive-maintenance evaluation:

```bash
python predictive_maintenance.py
```

Run the baseline vs agent experiment:

```bash
python compare_agent_vs_baseline.py
```

---

## 🛠️ Technologies

- Python
- SimPy
- Pandas
- NumPy
- Scikit-learn
- Machine Learning
- Discrete-Event Simulation
- Digital Twins
- Predictive Maintenance
- Agentic AI

---

## 🔬 Future Work

Planned extensions include:

- Statistical significance testing across paired experiments
- Agent decision-threshold optimisation
- Maintenance-cost modelling
- Remaining Useful Life (RUL) prediction
- More realistic machine degradation
- Multi-machine failure prediction
- Production scheduling optimisation
- Reinforcement-learning-based decision policies
- Real-time monitoring dashboard
- Integration with IoT/MQTT data
- LLM-supported agent reasoning and explanation

---

## ⚠️ Disclaimer

This project is an **experimental simulation and research prototype**.

It is not intended for direct deployment in safety-critical or production manufacturing environments without additional validation, safety controls, and real-world testing.

---

## 👤 Author

**Kavindu Gayashan Karunarathne**

Research interests include Artificial Intelligence, Machine Learning, Data Science, Digital Twins, Agentic AI, and intelligent systems.