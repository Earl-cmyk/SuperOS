# **SuperOS**

**SuperOS** is a hosted, microkernel-inspired **process control plane** for developers.

It provides **real process isolation**, **capability-based authority**, and **kernel-enforced execution**, while remaining portable and developer-focused.

**SuperOS is not a terminal emulator.**  
**Shells are clients, never authorities.**

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

SuperOS is an operating-system *abstraction* that runs **on top of a host OS** and is designed to:

- Manage **real host OS processes** via a trusted kernel
- Enforce **capability-based security** with no ambient authority
- Require **explicit IPC** for all inter-component communication
- Treat **projects as first-class, kernel-managed entities**
- Run **language runtimes as user-space services**
- Strictly separate **mechanism (Rust kernel)** from **policy (Python orchestrator)**
- Integrate cloud services **without granting them authority**

SuperOS behaves like an OS *inside* another OS, without pretending to be bare metal.

---

## **What SuperOS Is Not**

SuperOS is **not**:

- A terminal emulator
- A shell-driven system
- A REPL runner
- A monolithic application
- A “just run this command” environment
- An autonomous or self-modifying agent platform

If execution bypasses kernel mediation, it is a **design violation**.

---

## **Core Principles**

### **1. Microkernel-Inspired Architecture**
- Minimal trusted kernel
- All services in user space
- Mandatory IPC between components

### **2. Explicit Authority**
- No ambient authority
- No implicit permissions
- All power derives from explicit capabilities

### **3. Real Processes**
- Every execution is a kernel-managed process
- Full lifecycle visibility and control
- Projects map to **process trees**, not folders

### **4. Shells Are Clients**
- Shells are unprivileged user-space processes
- UI, CLI, and API shells are equivalent
- Killing a shell must never affect system integrity

---

## **System Architecture**

```
┌─────────────────────────────┐
│ UI Shell                    │
│ (Terminal, Web, SQL, ML)    │
└──────────────┬──────────────┘
│ IPC
┌──────────────▼──────────────┐
│ User-Space Services         │
│ (Runtimes, Web, DB, ML)     │
└──────────────┬──────────────┘
│ IPC
┌──────────────▼──────────────┐
│ Orchestrator (Python)       │
│ Policy & Scheduling         │
└──────────────┬──────────────┘
│ Syscalls / IPC
┌──────────────▼──────────────┐
│ SuperOS Kernel (Rust)       │
│ Process | IPC | Memory |    │
│ Capabilities Enforcement    │
└─────────────────────────────┘
```

---

## **Execution Model**

1. User initiates an action via a shell
2. Shell sends a request over IPC
3. Kernel validates capabilities
4. Kernel spawns or schedules a process
5. Runtime service executes code
6. `stdout` / `stderr` are captured as streams
7. Shell subscribes to process output

There is **no direct execution path** from shell to host OS.

---

## **Security Model**

- Capability-based access control
- Per-process capability tables
- No global privileges
- No shell-granted authority
- Kernel-enforced boundaries

### **Example Capabilities**

- `PROC_SPAWN`
- `FS_READ:/project`
- `FS_WRITE:/project`
- `NET_BIND:localhost`
- `IPC_SEND:channel_id`
- `ML_CONTEXT:logs`

---

## **Process Model**

A process is a kernel-managed execution context with:

- PID
- Virtual address space
- Capability table
- IPC endpoints
- Thread set
- Lifecycle state

Projects map **1:1 to process trees**.

---

## **IPC Model**

All communication is explicit and kernel-mediated:

- Pipes (byte streams)
- Message queues (structured messages)
- Restricted shared memory (explicit mapping)
- Events and signals (state notifications)

There is **no implicit shared state**.

---

## **Memory Model**

- Per-process virtual address spaces
- Kernel-managed paging
- Fault isolation
- No unsafe shared memory
- Kernel implemented entirely in Rust

Shared memory requires:

- Explicit capability
- Kernel-approved mapping
- Defined ownership and lifetime rules

---

## **Filesystem Model**

- Kernel-visible logical filesystem
- Projects have isolated directory trees
- All filesystem access is capability-gated
- No ambient working directory
- Filesystem treated as an **authority surface**

Projects are **local-first** and authoritative on disk.

---

## **Scheduling Model**

- Context switching implemented in Rust (mechanism)
- Scheduling policy defined in Python (policy)
- Cooperative + preemptive hybrid
- Foreground and background priorities
- Starvation prevention via aging

The scheduler never lives in a shell.

---

## **Language Runtime Services**

All languages execute via **user-space runtime services**:

- Python
- C / C++ / C#
- Java / Kotlin / Swift
- HTML / CSS / JS / TS (virtual web server)
- SQL (query and table visualization)
- R
- Rust
- Arduino
- Unreal Engine
- Bash
- Git
- PowerShell

Runtimes:

- Are normal kernel-managed processes
- Have minimal, explicit capabilities
- Cannot escape their sandbox

---

## **Database & Project Management**

SuperOS uses a **cloud database (Supabase)** strictly as a **metadata and synchronization layer**.

### **Supabase Stores**

- Project metadata
- Ownership and permissions
- Version and snapshot references
- UI state and sync status

### **Local Filesystem Stores**

- Actual project files
- Execution artifacts
- Runtime outputs

Supabase **never** bypasses kernel enforcement.

---

## **Machine Learning Integration**

Machine learning is implemented as a **user-space analysis service**.

ML services may:

- Request read-only execution context
- Analyze logs, errors, and metadata
- Suggest actions or fixes

ML services may **not**:

- Execute code
- Spawn processes
- Write files
- Escalate privileges

All ML access is capability-gated and orchestrator-mediated.

---

## **UI Shell**

The UI is an **IPC client**, not an executor.

Components include:

- Window manager
- Terminal
- Error and diagnostics panel
- Project explorer
- Web viewer
- SQL viewer
- ML insights panel

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

- Rust kernel
- Python orchestrator
- Process spawning
- IPC
- Capability enforcement
- Logging
- One language runtime (Python)
- Project import and metadata
- Simple UI shell

Architecturally complete, minimally featured.

---

## **Non-Goals**

Explicitly excluded from MVP:

- Bare-metal booting
- POSIX compatibility
- Full filesystem drivers
- Arbitrary native execution
- Autonomous agents
- Performance optimization
- Rich GUI frameworks

**Correctness > completeness.**

---

## **Repository Layout**

- `kernel/` — Trusted microkernel (Rust)
- `orchestrator/` — User-space policy layer (Python)
- `services/` — Language runtimes and system services
- `ui/` — UI shell (IPC client)
- `projects/` — Sandboxed user projects
- `docs/` — Architecture and contracts

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

