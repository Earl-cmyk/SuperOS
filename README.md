
# **SuperOS**

**SuperOS** is a hosted, microkernel-inspired **process control plane** for developers.  
It provides real process isolation, explicit authority, and kernel-enforced execution, while remaining portable and developer-focused.

**SuperOS is not a terminal emulator.**  
**Shells are clients, never rulers.**

---

## **Table of Contents**
- [What SuperOS Is](#what-superos-is)
- [What SuperOS Is Not](#what-superos-is-not)
- [Core Principles](#core-principles)
- [System Architecture](#system-architecture)
- [Execution Model](#execution-model)
- [Security Model](#security-model)
- [Process Model](#process-model)
- [IPC Model](#ipc-model)
- [Memory Model](#memory-model)
- [Filesystem Model](#filesystem-model)
- [Scheduling Model](#scheduling-model)
- [Language Runtime Services](#language-runtime-services)
- [Database & Project Management](#database--project-management)
- [Machine Learning Integration](#machine-learning-integration)
- [UI Shell](#ui-shell)
- [Startup Sequence](#startup-sequence)
- [MVP Scope](#mvp-scope)
- [Non-Goals](#non-goals)
- [Repository Layout](#repository-layout)
- [Status](#status)
- [Final Principle (Locked)](#final-principle-locked)

---

## **What SuperOS Is**
SuperOS is a hosted operating system abstraction designed to:

- Manage real OS processes  
- Enforce capability-based security  
- Provide explicit IPC everywhere  
- Treat projects as first-class managed entities  
- Run language runtimes as user-space services  
- Separate **mechanism (Rust)** from **policy (Python)**  
- Integrate cloud services (DB, ML) without violating kernel authority  

SuperOS behaves like an OS **inside** a host OS, without pretending to be bare metal.

---

## **What SuperOS Is Not**
SuperOS is **not**:

- A terminal emulator  
- A REPL runner  
- A shell-centric system  
- A monolithic application  
- A “just run this command” environment  
- A self-modifying or autonomous agent platform  

If execution occurs without kernel mediation, it is a **design violation**.

---

## **Core Principles**

### **1. Microkernel-Inspired Architecture**
- Minimal trusted kernel  
- Everything else in user space  
- Explicit IPC between all components  

### **2. Explicit Authority**
- No ambient authority  
- No implicit permissions  
- All power flows from capabilities  

### **3. Real Processes**
- Every execution is a kernel-managed process  
- Lifecycle is observable, schedulable, terminable  
- Projects map to process trees  

### **4. Shells Are Clients**
- Shells are unprivileged user-space programs  
- UI, CLI, and API shells are equivalent  
- Killing a shell must not affect system integrity  

---

## **System Architecture**

```
┌──────────────────────────────┐
│            UI Shell          │
│  (Terminal, Web, SQL, ML)    │
└──────────────┬───────────────┘
               │ IPC
┌──────────────▼───────────────┐
│     User-Space Services      │
│  (Runtimes, Web, DB, ML)     │
└──────────────┬───────────────┘
               │ IPC
┌──────────────▼───────────────┐
│    Orchestrator (Python)     │
│  Scheduling & Policy Layer  │
└──────────────┬───────────────┘
               │ Syscalls / IPC
┌──────────────▼───────────────┐
│     SuperOS Kernel (Rust)    │
│ Process | IPC | Memory | Cap │
└──────────────────────────────┘
```

---


## **Execution Model**

1. User initiates an action (UI / Shell)
2. Request sent via IPC
3. Kernel validates capabilities
4. Kernel spawns or schedules a process
5. Runtime service executes code
6. `stdout` / `stderr` captured as streams
7. UI subscribes to output

There is **no direct execution path** from UI to host OS.

---

## **Security Model**

* Capability-based access control
* Per-process capability tables
* No global privileges
* No shell-granted authority
* Kernel enforces all boundaries

**Example capabilities:**

* `PROC_SPAWN`
* `FS_READ:/project`
* `FS_WRITE:/project`
* `NET_BIND:localhost`
* `IPC_SEND:channel_id`
* `ML_CONTEXT:logs`

---

## **Process Model**

A process is a kernel-managed execution context with:

* PID
* Address space
* Capability table
* IPC endpoints
* Thread set
* Lifecycle state

Projects map **1:1 to process trees**.

---

## **IPC Model**

All communication is explicit and kernel-mediated:

* Pipes (stream-oriented)
* Message queues (structured)
* Restricted shared memory (explicit mapping)
* Events / signals (state notifications)

There is **no implicit shared state**.

---

## **Memory Model**

* Per-process virtual address spaces
* Kernel-managed paging
* Fault isolation
* No unsafe shared memory
* Rust-only kernel implementation

Shared memory requires:

* Explicit capability
* Kernel-approved mapping
* Defined ownership rules

---

## **Filesystem Model**

* Kernel-visible logical filesystem
* Projects have isolated directory trees
* All filesystem access is capability-gated
* No ambient working directory
* Filesystem is an **authority surface**, not a convenience

Projects are **local-first** and authoritative on disk.

---

## **Scheduling Model**

* Context switching in Rust (mechanism)
* Scheduling policy in Python (policy)
* Cooperative + preemptive hybrid
* Foreground vs background priorities
* Starvation prevention via aging

The scheduler never lives in the UI or shell.

---

## **Language Runtime Services**

All languages execute via **user-space runtime services**:

* Python
* C / C++ / C#
* Java / Kotlin / Swift
* HTML / CSS / JS / TS (virtual web server)
* SQL (table visualization)
* R
* Rust
* Arduino
* Unreal Engine
* Bash
* Git
* PowerShell

Runtimes:

* Are normal processes
* Have limited capabilities
* Cannot escape their sandbox

---

## **Database & Project Management**

SuperOS uses a **cloud database (Supabase)** as a **metadata and sync layer**, not as an authority.

### **Supabase Stores**

* Project metadata
* Ownership and permissions
* Version / snapshot references
* UI state and sync status

### **Local Filesystem Stores**

* Actual project files
* Execution artifacts
* Runtime outputs

Projects are imported via an **Upload / Import Project** action:

* Folder selected in UI
* Orchestrator validates and registers project
* Metadata stored in Supabase
* Project mounted into `projects/`
* Kernel enforces access

Supabase never bypasses the kernel.

---

## **Machine Learning Integration**

Machine learning is implemented as a **user-space service**, never in the kernel.

ML services can:

* Request read-only context (logs, errors, metadata)
* Analyze execution output
* Suggest actions or fixes

ML services **cannot**:

* Execute code
* Spawn processes
* Write files
* Escalate privileges

All ML actions are capability-gated and enforced by the orchestrator.

---

## **UI Shell**

The UI is an **IPC client**, not an executor.

Components:

* Window manager
* Terminal
* Error sidebar
* Project explorer
* Web viewer
* SQL viewer
* ML panel

The UI reflects **kernel state**; it does not invent it.

---

## **Startup Sequence**

1. Host OS launches SuperOS
2. Kernel initializes core subsystems
3. Orchestrator starts (policy layer)
4. Runtime and system services register
5. UI shell launches
6. System enters steady state

---

## **MVP Scope**

### **Included**

* Rust kernel
* Python orchestrator
* Process spawning
* IPC
* Capability enforcement
* Logging
* One language runtime (Python)
* Project import & metadata
* Simple UI shell

Architecturally complete, minimal feature set.

---

## **Non-Goals**

Explicitly excluded from MVP:

* Bare-metal booting
* POSIX compatibility
* Full filesystem drivers
* Arbitrary native execution
* Autonomous agents
* Performance optimization
* Rich GUI frameworks

**Correctness > completeness.**

---

## **Repository Layout**

See [`/docs`](./docs) for detailed specifications.

* `kernel/` — Trusted microkernel (Rust)
* `orchestrator/` — User-space policy (Python)
* `services/` — Language runtimes & system services
* `ui/` — UI shell (IPC client)
* `projects/` — Sandboxed user projects
* `docs/` — Architecture contracts

---

## **Status**

SuperOS is under active architectural development.
Design correctness is prioritized over implementation speed.

Once an invariant is locked, it is **not broken**.

---

## **Final Principle (Locked)**

**SuperOS is a process control plane.**
**The kernel is law.**
**Shells are clients.**

If a feature violates this, **it does not ship**.

```

#   S u p e r O S  
 