# **Logging Model**

## **Scope**
This document defines the **logging model** for SuperOS.

It specifies:
- What is logged
- Where logs originate
- How logs flow through the system
- Authority boundaries for log access
- Audit and security guarantees

This document is an **architecture contract**.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Distributed tracing systems
- External log aggregation platforms
- Performance profiling
- Debugger integration
- Metrics collection

Logging in SuperOS is for **observability and audit**, not convenience debugging.

---

## **Logging Invariants (Hard Rules)**

The following MUST always hold:

- Logs are **append-only**
- Logs are **kernel-attributable**
- Logs are **non-authoritative**
- Logs are **read-only once written**
- No component can forge kernel logs
- Log access is capability-gated

If a log violates these rules, it is invalid.

---

## **Log Sources**

Logs originate from three layers:

### 1. Kernel Logs
- Process lifecycle events
- Capability checks
- IPC creation and teardown
- Scheduling decisions
- Filesystem access denials
- Boot and shutdown transitions

Kernel logs are the **ground truth** for system behavior.

---

### 2. Orchestrator Logs
- Policy decisions
- Scheduling policy actions
- Service lifecycle management
- Project registration and import
- Database interactions
- ML action approvals / denials

Orchestrator logs are **derivative**, not authoritative.

---

### 3. Service Logs
- Runtime stdout / stderr
- Internal service diagnostics
- Controlled error output

Service logs are:
- Process-scoped
- Non-privileged
- Never trusted as authority

---

## **Log Flow Architecture**

```

[ Kernel ]
|
v
[ Kernel Log Buffer ]
|
v
[ Orchestrator Log Aggregator ]
|
v
[ Persistent Log Store ]
|
v
[ UI / Tools (Read-Only) ]

```

No component may skip layers.

---

## **Log Storage Model**

### Logical Layout
```

/logs/
├── system.log
└── processes/
├── <pid>/
│   ├── stdout.log
│   ├── stderr.log
│   └── events.log

```

- `system.log` contains kernel and orchestrator logs
- Per-process logs are isolated by PID
- Logs are never shared across processes

---

## **Kernel Logging Responsibilities**

The kernel MUST:
- Timestamp all events
- Attribute events to PID and capability
- Emit immutable records
- Reject log mutation requests
- Log all security-relevant decisions

The kernel MUST NOT:
- Rely on user-space logging libraries
- Allow log deletion
- Trust user-provided log messages

---

## **Orchestrator Logging Responsibilities**

The orchestrator MUST:
- Collect kernel log streams
- Correlate logs across services
- Persist logs durably
- Enforce log access permissions

The orchestrator MUST NOT:
- Alter kernel logs
- Suppress security events
- Rewrite history

---

## **Service Logging Rules**

Services:
- May emit stdout / stderr
- May log internal diagnostics
- Cannot mark logs as authoritative
- Cannot write to other processes’ logs

Services MUST NOT:
- Forge kernel events
- Access logs without capability
- Delete or truncate logs

---

## **Log Access Control**

Log access is controlled via capabilities:

- `LOG_READ:system`
- `LOG_READ:process:<pid>`
- `LOG_SUBSCRIBE`
- `LOG_ADMIN`

Default access:
- UI: read-only, scoped
- Services: self-only
- Orchestrator: full read
- Kernel: write-only

---

## **Streaming vs Persistence**

Logs are:
- Streamed in real time via IPC
- Persisted asynchronously
- Never required for correctness

System behavior MUST NOT depend on logs.

---

## **Failure Handling**

- Log write failure → system continues
- Log persistence failure → warning emitted
- Log corruption → detected and flagged
- No retries may block execution

Logging failure MUST NOT cause execution failure.

---

## **Security Considerations**

- Logs may contain sensitive data
- Access must be explicit and auditable
- Logs must not leak capabilities
- Kernel logs must be tamper-evident

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Log-based control flow
- Mutable logs
- Shell-managed logging
- Services writing kernel logs
- Logs as a source of authority

---

## **Summary**

Logging in SuperOS is:
- Observational
- Append-only
- Capability-gated
- Kernel-attributed

Logs explain what happened.  
They do not decide what happens.

If logging becomes authoritative, the design is broken.
