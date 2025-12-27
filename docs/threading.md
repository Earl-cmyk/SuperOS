# **Threading Model**

## **Scope**
This document defines the **threading model** for SuperOS.

It specifies:
- What threads are
- How they are created and scheduled
- How they interact with processes
- What guarantees the kernel provides

Threads in SuperOS exist for concurrency, not authority.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Language-level threading models
- Green threads or async runtimes
- Lock-free data structures
- Memory model guarantees at the language level
- Host OS thread implementation details

SuperOS threads are kernel constructs, not language abstractions.

---

## **Core Principles**

- Threads belong to processes
- Threads share a process address space
- Threads do not have independent authority
- Scheduling is thread-aware but process-bounded
- The kernel controls all thread lifecycles

If a thread can escape its process, the design is invalid.

---

## **Thread Definition**

A thread is a kernel-managed execution context with:
- Thread ID (TID)
- Parent process ID (PID)
- Register state
- Stack
- Scheduling state

Threads do not have:
- Capabilities
- Independent address spaces
- Direct IPC endpoints

---

## **Thread Creation**

Threads are created:
- Only by the kernel
- At process spawn time or via syscall
- Subject to process capability limits

User space requests threads; the kernel decides.

---

## **Thread Lifecycle**

Thread states include:
- **New**
- **Runnable**
- **Running**
- **Blocked**
- **Terminated**

Thread lifecycle is entirely kernel-managed.

---

## **Thread Scheduling**

- Threads are scheduled by the kernel scheduler
- Threads compete for CPU within process constraints
- Process-level policy bounds thread behavior
- No thread may monopolize CPU indefinitely

Threads are scheduling units, not policy units.

---

## **Preemption**

- Threads are preemptible
- Time slicing applies per thread
- Preemption cannot be disabled by user space

A runaway thread is treated as a runaway process.

---

## **Blocking & Synchronization**

Threads block when:
- Waiting on IPC
- Waiting on I/O
- Sleeping voluntarily

Synchronization primitives:
- Are provided by user-space runtimes
- Are not trusted for security
- Do not grant authority

The kernel does not enforce lock correctness.

---

## **Thread Limits**

Each process may have:
- A maximum thread count
- Stack size limits
- CPU usage quotas

Violations result in:
- Thread creation failure
- Logged kernel event
- Optional process termination

Threads are not free.

---

## **Failure Handling**

Thread-level failures:
- Illegal instruction
- Stack overflow
- Memory violation

Handling:
- Kernel terminates the process
- Fault is logged
- No partial recovery is guaranteed

A broken thread breaks its process.

---

## **Observability**

Thread state is observable via:
- Kernel debug interfaces
- Orchestrator metrics
- Logging

Invisible threads are forbidden.

---

## **Security Considerations**

- Threads cannot hold capabilities
- Threads cannot outlive their process
- Threads cannot communicate across processes directly
- Thread IDs are not authority tokens

Threads do not widen the attack surface.

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Thread-level capabilities
- User-space thread schedulers
- Unbounded thread creation
- Detached threads surviving process exit
- Implicit thread sharing

---

## **Summary**

Threading in SuperOS is:
- Kernel-controlled
- Process-scoped
- Preemptible
- Resource-bounded
- Authority-neutral

Threads exist to do work faster, not to gain power.

If a thread can do more than its process allows, the system is broken.

