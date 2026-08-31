# Architecture — Local Build

**Status:** WIP / local prototype

```text
                 ┌───────────────────────────┐
                 │       HUMAN USER          │
                 │ simple → advanced views  │
                 └────────────┬──────────────┘
                              │ natural language
                              ▼
                 ┌───────────────────────────┐
                 │   INVESTIGATION LAYER     │
                 │ query → retrieval →      │
                 │ evidence-backed answer   │
                 └────────────┬──────────────┘
                              ▼
                 ┌───────────────────────────┐
                 │ INCIDENT RECONSTRUCTION   │
                 │ temporal + entity links   │
                 │ process relationships     │
                 └────────────┬──────────────┘
                              ▼
                 ┌───────────────────────────┐
                 │ DETECTION + RISK          │
                 │ deterministic rules       │
                 │ interpretable score       │
                 └────────────┬──────────────┘
                              ▼
                 ┌───────────────────────────┐
                 │ UNIVERSAL EVENT MODEL     │
                 └────────────┬──────────────┘
                              ▼
                 ┌───────────────────────────┐
                 │ LOCAL EVENT STORE         │
                 └────────────┬──────────────┘
                              ▲
             ┌────────────────┼────────────────┐
             │                │                │
       Windows Events       Sysmon*         USB*
       collector            future          future

* planned/integration work
```

## Design principles

1. **Local-first:** core telemetry, storage, detection, correlation and timeline functions should work locally.
2. **Evidence-first:** explanations are generated from retrieved evidence rather than unrestricted access to the machine.
3. **Human-readable:** ordinary users see security meaning before technical details.
4. **Progressive disclosure:** advanced users can open the underlying event IDs, process relationships and risk factors.
5. **Modular:** collectors, rules, storage and AI providers can evolve independently.
6. **Conservative language:** suspicious activity is not automatically labelled a confirmed attack.

## Experimental prediction layer

The current repository treats attack prediction as a **future/experimental layer**. It consumes the reconstructed behavior chain and can surface a possible next stage, but the prototype must present that output as a hypothesis with confidence and evidence — never as certainty.
