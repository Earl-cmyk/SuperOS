# **Machine Learning Integration**

## **Scope**
This document defines how **machine learning (ML)** is integrated into SuperOS.

It specifies:
- Where ML lives in the system
- How models are executed
- How data is accessed
- How authority and isolation are preserved

ML in SuperOS is a **service**, not a shortcut.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Training large foundation models
- GPU driver implementation
- Custom ML frameworks
- Model performance optimization
- Hosting proprietary models

SuperOS integrates ML as a controlled capability, not as a research platform.

---

## **Core Principles**

- ML runs in **user-space services**
- The kernel is unaware of “models”
- ML never bypasses IPC or capabilities
- Models are processes, not libraries
- UI never executes ML directly

If ML code can run without kernel mediation, the design is invalid.

---

## **ML Architecture**

```

┌──────────────────────────────┐
│            UI Shell          │
│   (Prompts / Views / Tools)  │
└──────────────┬───────────────┘
│ IPC
┌──────────────▼───────────────┐
│     ML Service (User Space)  │
│  Inference | Embeddings |    │
│  Indexing  | Ranking        │
└──────────────┬───────────────┘
│ IPC / FS / NET
┌──────────────▼───────────────┐
│       Orchestrator           │
│  Policy, Quotas, Routing    │
└──────────────┬───────────────┘
│ Syscalls
┌──────────────▼───────────────┐
│         Kernel               │
│  Process | IPC | Memory | Cap│
└──────────────────────────────┘

```

---

## **ML as a Service**

ML functionality is exposed via **dedicated services**, such as:
- `ml_inference_service`
- `ml_embedding_service`
- `ml_search_service`
- `ml_index_service`

Each ML service:
- Is a normal process
- Has a PID
- Has a capability table
- Is resource-limited
- Can be killed and restarted

There is no “embedded ML”.

---

## **Supported ML Capabilities**

ML services may be granted:
- `FS_READ:/projects`
- `FS_READ:/models`
- `NET_OUTBOUND:api.openai.com`
- `PROC_LIMIT`
- `MEM_LIMIT`
- `IPC_SERVE:ml_channel`

Capabilities are explicit and minimal.

---

## **Model Execution**

Models:
- Are loaded inside ML services
- Cannot access kernel memory
- Cannot spawn processes unless permitted
- Cannot read projects unless authorized

Execution flow:
1. UI sends request to ML service via IPC
2. Kernel validates IPC capability
3. ML service runs inference
4. Result streamed back via IPC

There is no synchronous blocking path through the kernel.

---

## **Local vs Remote Models**

### Local Models
- Stored under `/models`
- Loaded by ML services
- CPU-first by default
- GPU optional, capability-gated

### Remote Models
- Accessed via HTTP APIs
- Network access requires explicit capability
- Requests are logged
- Responses are treated as untrusted input

Remote ML is a network client, not a kernel feature.

---

## **Indexing & Search (Windsurf-like)**

SuperOS supports **ML-backed project intelligence**:
- File embeddings
- Semantic search
- Code navigation
- Project summaries

Indexing flow:
1. Project changes detected
2. Orchestrator schedules indexing job
3. ML indexing service reads project (capability-gated)
4. Embeddings stored in database
5. Search queries routed to ML search service

Indexing is asynchronous and killable.

---

## **Data Storage**

ML data may be stored in:
- Embedded databases (SQLite)
- External services (Supabase)
- In-memory caches (per-service)

The kernel does not care where data lives.

---

## **Supabase Integration**

Typical ML uses:
- Vector storage (embeddings)
- Metadata (projects, files)
- User-scoped access

Supabase access:
- Happens in ML services
- Uses service keys
- Is network capability-gated
- Is audited via logs

Supabase is a backend, not a trust anchor.

---

## **Resource Limits**

ML services are constrained by:
- Memory limits
- CPU quotas
- Timeouts
- Job cancellation

Runaway ML is terminated like any other process.

---

## **Failure Modes**

ML services may fail by:
- Crashing
- Timing out
- Returning invalid output

Failure handling:
- Kernel isolates failure
- Orchestrator restarts service
- UI receives structured error

ML failure never compromises system integrity.

---

## **Security Considerations**

- Models are untrusted code
- Prompt input is untrusted
- Output is untrusted
- No model can access kernel internals
- No model can bypass IPC

ML is a guest, not a resident.

---

## **Forbidden Designs**

The following are forbidden:
- ML code inside the kernel
- UI directly calling ML libraries
- Global embedding stores without access control
- Implicit project indexing
- Always-on background model execution

---

## **Summary**

Machine learning in SuperOS is:
- Explicit
- Isolated
- Service-based
- Capability-gated
- Killable

SuperOS does not “have AI”.
SuperOS **hosts ML processes** under the same laws as everything else.

If ML feels magical, the design is wrong.
