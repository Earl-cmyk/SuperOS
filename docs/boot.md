# **Boot Sequence**

## **Scope**
This document defines the **boot and startup sequence** of SuperOS, from host invocation to steady-state operation.

This document specifies:
- Component initialization order
- Authority boundaries during boot
- Required invariants
- Failure handling rules

This document is an **architecture contract**.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Bare-metal boot loaders
- BIOS / UEFI / firmware
- Host OS startup
- Hardware initialization
- POSIX init systems

SuperOS is a **hosted system**.

---

## **Boot Invariants (Hard Rules)**

The following MUST always hold:

- The **kernel initializes first**
- The **kernel is authoritative before anything executes**
- No user-space code runs before kernel readiness
- The orchestrator cannot exist without the kernel
- Services cannot self-register without kernel mediation
- The UI cannot execute code or spawn processes
- Failure during boot MUST fail closed

If any invariant is violated, the system MUST halt startup.

---

## **High-Level Boot Phases**

```

Host OS
|
v
[ Kernel Init ]
|
v
[ Orchestrator Init ]
|
v
[ Service Registration ]
|
v
[ UI Launch ]
|
v
[ Steady State ]

```

---

## **Phase 0: Host Invocation**

SuperOS is launched by the host OS as a normal process.

Examples:
- CLI invocation
- Desktop launcher
- System service wrapper
- Container entrypoint

At this stage:
- No SuperOS components are initialized
- No authority exists
- No execution context is valid

---

## **Phase 1: Kernel Initialization**

The kernel is the **first SuperOS component** to initialize.

### Responsibilities
The kernel MUST:
- Initialize core subsystems
- Establish authority boundaries
- Prepare syscall and IPC interfaces
- Refuse execution until ready

### Kernel Subsystems Initialized
- Process manager
- Thread manager
- IPC primitives
- Virtual memory manager
- Capability system
- Scheduler hooks

### Kernel State Transitions
```

UNINITIALIZED
↓
INITIALIZING
↓
READY

```

No syscall other than `KERNEL_STATUS` is valid before `READY`.

---

## **Phase 2: Orchestrator Startup**

Once the kernel reports `READY`, the host launches the **orchestrator**.

The orchestrator is a **privileged user-space process**, but:
- It is NOT the kernel
- It holds only explicitly granted capabilities

### Orchestrator Responsibilities
- Load policy configuration
- Initialize scheduling policy
- Manage process lifecycle
- Enforce non-kernel security rules
- Act as the sole coordinator of services

### Required Capabilities
- `PROC_SPAWN`
- `PROC_KILL`
- `IPC_ADMIN`
- `SCHED_POLICY`
- `FS_ADMIN:/projects`
- `CAP_DELEGATE`

The kernel MUST validate these explicitly.

---

## **Phase 3: Service Registration**

System services are launched **by the orchestrator**, never by the UI.

### Services Include
- Language runtimes
- Web service
- Database service
- Build service
- Machine learning service
- Shell services

### Registration Flow
```

Service Spawn
↓
Capability Assignment
↓
IPC Endpoint Creation
↓
Kernel Registration

```

A service that fails registration MUST be terminated.

### Forbidden Behavior
- Services MUST NOT spawn other services
- Services MUST NOT grant capabilities
- Services MUST NOT bypass orchestrator policy

---

## **Phase 4: UI Shell Launch**

The UI shell is launched **last**.

### UI Properties
- Unprivileged
- No execution authority
- IPC client only
- Reflects kernel state

### UI Capabilities (Example)
- `IPC_SEND`
- `IPC_SUBSCRIBE`
- `FS_READ:/projects`
- `UI_RENDER`

The UI MUST NOT:
- Spawn processes
- Execute code
- Modify kernel or orchestrator state directly

---

## **Phase 5: Steady State**

SuperOS enters steady state when:
- Kernel is READY
- Orchestrator is running
- Core services are registered
- UI is connected

### Steady State Guarantees
- All execution is kernel-mediated
- All authority is explicit
- All state is observable
- Any component may be restarted independently

---

## **Failure Handling**

### Kernel Failure
- System MUST halt
- No recovery without restart

### Orchestrator Failure
- Kernel remains running
- All managed processes are paused or terminated
- Restart requires explicit host action

### Service Failure
- Orchestrator may restart service
- Capabilities MUST be revalidated
- No implicit recovery allowed

### UI Failure
- No system impact
- UI may reconnect at any time

---

## **Restart Semantics**

| Component     | Restart Allowed | State Preserved |
|---------------|-----------------|-----------------|
| Kernel        | No              | N/A             |
| Orchestrator  | Yes (controlled)| Kernel state    |
| Services      | Yes             | None            |
| UI            | Yes             | UI-local only   |

---

## **Security Considerations**

- No component may self-bootstrap authority
- Boot order enforces trust layering
- Capability assignment during boot is audited
- Logs MUST capture all boot transitions

---

## **Forbidden Designs**

The following are explicitly forbidden:
- UI-triggered boot logic
- Services initializing before orchestrator
- Orchestrator executing without kernel readiness
- Implicit service discovery
- Dynamic privilege escalation during boot

---

## **Summary**

SuperOS boot is:
- Deterministic
- Layered
- Authority-first
- Fail-closed

Boot is not convenience code.  
Boot is **law**.

If a startup shortcut violates these rules, it does not ship.
