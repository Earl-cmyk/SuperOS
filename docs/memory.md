# **Memory Model**

## **Scope**
This document defines the **memory model** for SuperOS.

It specifies:
- How memory is owned, mapped, and isolated
- What guarantees the kernel provides
- How shared memory is explicitly negotiated
- The authority boundaries around memory access

This document is an **architecture contract**.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Bare-metal paging or MMU programming
- NUMA optimization
- Garbage collection strategies
- Language-level memory models
- Performance tuning

Memory in SuperOS is about **correctness and isolation**, not speed.

---

## **Memory Invariants (Hard Rules)**

The following MUST always hold:

- Every process has a **private virtual address space**
- No implicit shared memory exists
- All memory mappings are kernel-owned
- User-space cannot remap memory arbitrarily
- Shared memory requires explicit capability
- Memory violations terminate the offending process

If any invariant is broken, the kernel is invalid.

---

## **Process Address Space**

Each process is created with:
- A fresh virtual address space
- Kernel-controlled mappings
- Read-only code segments
- Read-write data segments
- Non-executable data pages

The kernel is the sole authority over address space layout.

---

## **Memory Ownership**

Memory ownership is:
- Assigned at process creation
- Tracked by the kernel
- Never transferred implicitly

A process owns:
- Its heap
- Its stack(s)
- Its private mappings

Ownership is never shared by default.

---

## **Memory Allocation**

### Kernel Responsibilities
The kernel:
- Allocates memory on process spawn
- Tracks page ownership
- Enforces access permissions
- Handles page faults
- Revokes memory on process termination

### User-Space Responsibilities
User-space:
- Requests memory via syscalls
- Cannot allocate physical memory directly
- Cannot exceed assigned quotas
- Cannot remap kernel memory

---

## **Memory Quotas**

Each process is assigned:
- Maximum virtual memory size
- Maximum resident set size (RSS)
- Optional shared memory limits

Quota violations result in:
- Allocation failure
- Logged kernel event
- Optional process termination

Memory pressure is visible, not silent.

---

## **Shared Memory Model**

Shared memory is:
- Explicit
- Capability-gated
- Kernel-mediated
- Opt-in for all participants

### Shared Memory Setup Flow
1. Process A requests shared memory region
2. Kernel allocates region
3. Kernel issues `MEM_SHARE:<id>` capability
4. Process B is granted the capability
5. Kernel maps region into both address spaces

No step may be skipped.

---

## **Shared Memory Rules**

- Shared regions have defined ownership
- Read/write permissions are explicit
- Lifetime is kernel-managed
- Revocation is immediate and enforced
- No process can remap or resize the region

Shared memory is a contract, not a convenience.

---

## **Memory Revocation**

The kernel may revoke memory when:
- A process exits
- A capability is revoked
- A quota is exceeded
- A security violation occurs

Revocation:
- Unmaps pages immediately
- Invalidates references
- Triggers fault on access

There is no graceful degradation.

---

## **Copying vs Sharing**

Default communication:
- IPC messages
- Streamed data
- Explicit serialization

Shared memory is:
- Reserved for high-throughput needs
- Used sparingly
- Explicitly negotiated

If shared memory is used by default, the design is wrong.

---

## **Fault Handling**

Memory faults include:
- Invalid access
- Permission violations
- Use-after-revoke
- Access to unmapped pages

Fault handling:
- Kernel logs event
- Offending process is terminated
- No recovery path is guaranteed

Safety > availability.

---

## **Security Considerations**

- Memory is an authority surface
- Address spaces must be opaque
- No pointer sharing across processes
- No kernel memory mapping into user-space
- Side-channel resistance is best-effort, not guaranteed

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Implicit shared heaps
- Global memory pools
- Shell-controlled memory
- Runtime-managed address spaces
- Trusting user-space for memory safety

---

## **Summary**

Memory in SuperOS is:
- Isolated by default
- Kernel-owned
- Capability-gated
- Explicitly shared only when required

If two processes can touch the same memory without the kernel knowing, the system is broken.

