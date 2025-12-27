# **Security Model**

## **Scope**
This document defines the **security model** of SuperOS.

It specifies:
- How authority is granted and enforced
- How isolation is maintained
- What the kernel guarantees
- What user space is allowed to decide

Security in SuperOS is structural, not optional.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Cryptographic algorithm design
- Network protocol security
- Host OS hardening
- Physical security
- Side-channel attack mitigation

SuperOS focuses on **authority and isolation**, not cryptography.

---

## **Core Security Principles**

- No ambient authority
- Explicit capabilities everywhere
- Kernel as the sole enforcer
- User space defines policy, not power
- Least privilege by default

If authority exists without a capability, the system is compromised.

---

## **Threat Model**

SuperOS assumes:
- User-space code is untrusted
- Runtime services are untrusted
- Shells are untrusted
- UI is untrusted
- The kernel is trusted

The kernel is the only trusted computing base.

---

## **Capability-Based Security**

### Capabilities
A capability is:
- An unforgeable token
- Issued by the kernel
- Bound to a process
- Scoped and revocable

Capabilities define *what* a process may do.

---

### Capability Examples

- `PROC_SPAWN`
- `PROC_KILL`
- `FS_READ:/projects/foo`
- `FS_WRITE:/projects/foo`
- `NET_OUTBOUND:api.example.com`
- `IPC_SEND:channel_id`
- `MEM_SHARE:region_id`

No wildcard capabilities exist.

---

## **Capability Tables**

Each process has:
- A private capability table
- Populated at spawn time
- Modifiable only by the kernel

User space may request capability changes, but cannot apply them.

---

## **Authority Flow**

Authority flows:
1. Kernel → Orchestrator
2. Orchestrator → Services
3. Services → Child processes

Authority never flows upward or sideways.

---

## **Process Isolation**

Isolation guarantees:
- Separate address spaces
- No shared memory by default
- Separate capability tables
- Isolated IPC endpoints

A compromised process cannot escape its sandbox.

---

## **IPC Security**

IPC is:
- Explicit
- Capability-gated
- Kernel-mediated
- Audited

A process cannot:
- Send to unauthorized endpoints
- Receive messages without permission
- Spoof identities

---

## **Filesystem Security**

Filesystem access:
- Requires explicit FS capabilities
- Is path-scoped
- Is enforced by the kernel
- Has no global working directory

Filesystem is an authority surface.

---

## **Network Security**

Network access:
- Disabled by default
- Capability-gated per destination
- Mediated by user-space services
- Audited and logged

There is no raw socket access.

---

## **Shell & UI Security**

Shells:
- Are unprivileged clients
- Cannot spawn processes directly
- Cannot grant capabilities
- Cannot bypass the orchestrator

UI:
- Reflects kernel state
- Has zero execution authority

Killing the UI must not affect system security.

---

## **Revocation**

Capabilities may be revoked:
- Explicitly by policy
- On process termination
- On security violation

Revocation is:
- Immediate
- Enforced by the kernel
- Non-negotiable

There is no “grace period”.

---

## **Audit & Logging**

Security-relevant events:
- Capability grants
- Capability revocations
- IPC violations
- Access denials
- Process terminations

All are logged centrally and immutably.

---

## **Failure Handling**

On security violation:
- The offending process is terminated
- Capabilities are revoked
- The event is logged
- The system continues

Security failures are isolated, not contagious.

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Global permissions
- Implicit trust in shells
- Capability checks in user space
- Hardcoded bypasses
- “Temporary” privileges

---

## **Summary**

Security in SuperOS is:
- Capability-based
- Kernel-enforced
- Explicit
- Revocable
- Observable

If a process can do something the kernel did not explicitly allow, the system is already broken.

