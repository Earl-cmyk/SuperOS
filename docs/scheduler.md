# **Scheduling Model**

## **Scope**
This document defines the **scheduling model** for SuperOS.

It specifies:
- How execution time is allocated
- How processes and threads are scheduled
- Where policy vs mechanism live
- What guarantees the system provides

Scheduling in SuperOS is explicit, observable, and enforceable.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Real-time scheduling guarantees
- NUMA-aware scheduling
- CPU affinity tuning
- Energy-aware scheduling
- Host OS scheduler internals

SuperOS scheduling is about **fairness and control**, not raw performance.

---

## **Core Principles**

- Scheduling mechanism lives in the **kernel**
- Scheduling policy lives in **user space**
- The kernel never makes policy decisions
- User-space cannot violate kernel invariants
- All scheduling decisions are observable

If scheduling policy leaks into the kernel, the design is invalid.

---

## **Policy vs Mechanism Split**

### Kernel (Mechanism)
The kernel is responsible for:
- Context switching
- Timer interrupts
- Preemption
- Run queue maintenance
- Enforcing time slices

The kernel does **not** decide who *should* run.

---

### Orchestrator (Policy)
The orchestrator defines:
- Process priorities
- Foreground vs background classification
- Time slice weights
- Aging rules
- Throttling decisions

Policy is replaceable without kernel changes.

---

## **Scheduling Entities**

### Processes
- Kernel-managed
- Own address space
- Own capability table
- Own thread set

Processes are the primary scheduling unit.

---

### Threads
- Belong to a process
- Share address space
- Individually schedulable
- Kernel-visible

Threads exist for concurrency, not authority.

---

## **Run Queues**

The kernel maintains:
- A global run queue
- Optional per-priority queues
- Per-core queues (host-dependent)

Run queues are opaque to user space.

---

## **Scheduling Classes**

SuperOS supports logical scheduling classes:
- **Foreground** — interactive, latency-sensitive
- **Background** — batch, long-running
- **System** — critical services

Classes influence policy, not privileges.

---

## **Time Slicing**

- Preemptive scheduling is mandatory
- Time slices are enforced by the kernel
- Slice duration is policy-configurable
- No process can disable preemption

Cooperative scheduling is optional, not trusted.

---

## **Priority Model**

- Priorities are numeric and ordered
- Lower number = higher priority
- Priorities are bounded
- Kernel enforces bounds

User-space may request priority changes, but the kernel validates them.

---

## **Aging & Starvation Prevention**

To prevent starvation:
- Waiting processes gain priority over time
- CPU hogs are deprioritized
- Long-running background jobs yield to foreground tasks

Starvation is treated as a bug.

---

## **Blocking & Wakeup**

Processes block when:
- Waiting on IPC
- Waiting on I/O
- Sleeping voluntarily

Blocked processes:
- Are removed from run queues
- Are reinserted on wakeup
- Do not consume CPU

Busy-waiting is discouraged and observable.

---

## **IPC Interaction**

IPC affects scheduling:
- Message arrival may trigger wakeup
- Priority inheritance is supported
- Deadlocks are detectable

IPC never bypasses scheduling rules.

---

## **Preemption Rules**

The kernel may preempt a running process when:
- Its time slice expires
- A higher-priority process becomes runnable
- A system event occurs

User-space cannot prevent preemption.

---

## **Observability**

Scheduling state is observable via:
- Kernel events
- Orchestrator metrics
- Debug IPC endpoints

Hidden scheduling behavior is forbidden.

---

## **Failure Handling**

Scheduling-related failures include:
- Runaway CPU usage
- Deadlocks
- Starvation
- Priority inversion

Handling includes:
- Logging
- Throttling
- Forced yield
- Process termination

Correctness > uptime.

---

## **Security Considerations**

- Scheduling is not a privilege escalation vector
- No process can starve others indefinitely
- Scheduling metadata is protected
- Kernel time accounting is authoritative

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Shell-controlled scheduling
- UI-based priority changes without policy validation
- Kernel hardcoded priorities
- Unpreemptible user processes
- Implicit background execution

---

## **Summary**

Scheduling in SuperOS is:
- Kernel-enforced
- Policy-driven
- Observable
- Fair by default
- Explicitly controlled

The kernel moves time.
User space decides who deserves it.

If a process can run forever without consent, the system is broken.

