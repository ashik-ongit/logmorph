# Local Security Intelligence — Local Build

> **Pre-release / Work in Progress** · `v0.1.0-local`
>
> This repository is a working local prototype for a hackathon build. It is intentionally presented as an active engineering build, not a finished production security product.

A local-first security intelligence assistant designed to make endpoint security understandable to everyone — from a non-technical family member asking **“Is everything okay with my laptop?”** to an advanced user asking **“What happened while I was away?”** and drilling into evidence.

## Product direction

The prototype follows this pipeline:

```text
System telemetry
      ↓
Collect + normalize
      ↓
Detection
      ↓
Temporal / entity correlation
      ↓
Incident reconstruction
      ↓
Risk scoring
      ↓
Evidence model
      ↓
Natural-language investigation
```

The central experience is a **security flight recorder**: meaningful endpoint activity is turned into a timeline and related events can be reconstructed into a single incident rather than presented as disconnected alerts.

## Current local prototype

### User-facing experiences

- **Is Everything Okay?** — simple security status for everyday users.
- **When I Was Away** — reconstruct meaningful activity during a selected absence window.
- **Access Attempts** — summarize successful and failed authentication activity.
- **USB Activity** — explain what happened after a removable device was connected.
- **What Changed?** — surface persistence/file/system changes.
- **Ask My Computer** — evidence-backed natural-language investigation.
- **Incidents** — reconstructed activity chains and risk factors.
- **Attack Prediction (experimental)** — an explicitly experimental next-stage hypothesis based on the reconstructed behavior chain; it is not a claim that an attack will occur.
- **Evidence** — raw event references behind the explanation.

### Current demo chain

```text
USB inserted
    ↓
Executable started
    ↓
Child process created
    ↓
External network connection
    ↓
Persistence change
    ↓
Correlated incident
    ↓
Risk score + evidence
    ↓
AI-style investigation response
```

A second demo dataset includes failed remote-login attempts so the interface can demonstrate questions such as **“Who tried to access my computer?”** and **“What happened while I was away?”**.

## Repository structure

```text
endpoint-security-intelligence/
├── backend/                 # FastAPI API + reconstruction services
├── collector/               # Windows telemetry collector prototype
├── config/                  # Detection rule configuration
├── frontend/                # React + TypeScript local UI
├── docs/                    # Architecture and judging/demo notes
├── scripts/                 # Local demo/reset helpers
├── tests/                   # Backend tests
├── .github/workflows/       # CI smoke test
├── .env.example
├── pyproject.toml
└── README.md
```

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. The frontend expects the API at `http://localhost:8000/api`.

### One-command demo data

```bash
./scripts/demo.sh
```

## Important prototype boundary

This repository is **not** a production EDR, antivirus, SIEM, kernel monitor, malware sandbox, or autonomous remediation system. The current build uses deterministic demo telemetry and a Windows Event Log collector starting point so the hackathon team can demonstrate the architecture without pretending that every collector is complete.

The AI layer is deliberately constrained to retrieved evidence. The intended trust model is:

- **Observed** — what telemetry directly recorded.
- **Inferred** — what the correlation engine believes is likely related.
- **Unknown** — what the available evidence cannot establish.

## Roadmap

- [ ] Real Windows Event Log ingestion into the normalized event store
- [ ] Sysmon integration
- [ ] Real USB/device telemetry
- [ ] More process/network correlation
- [ ] Sigma-compatible rule loading
- [ ] ATT&CK technique mapping
- [ ] Local LLM integration through Ollama/llama.cpp
- [ ] Evidence citations in every AI answer
- [ ] Configurable user profiles and retention
- [ ] Linux/macOS collectors
- [ ] Experimental attack-prediction model evaluation

## Development status

**Status: active local prototype / hackathon build**

Interfaces and APIs may change while the project is being developed.
