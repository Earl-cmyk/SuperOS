```
# authd-swift

**SuperOS Authentication Daemon (Swift)**

`authd-swift` is a **user-space authentication and identity mediation service** for SuperOS.  
It handles authentication workflows and identity verification **without holding kernel authority**.

---

## Purpose

This service exists to:
- Authenticate users (local or external IdP)
- Issue identity assertions to the orchestrator
- Provide user/session metadata for UI and services

It does **not**:
- Grant capabilities
- Spawn processes
- Enforce permissions
- Interact with the kernel directly

Authentication ≠ Authorization in SuperOS.

---

## Architectural Position

```

UI ──► authd-swift ──► Orchestrator ──► Kernel
(identity)      (policy)        (law)

```

- `authd-swift` answers **who**
- The orchestrator decides **what**
- The kernel enforces **whether**

---

## Responsibilities

- User login / logout
- Token or credential verification
- Optional integration with external IdPs
- Session metadata issuance
- Auditable authentication logging

All outputs are **advisory**, never authoritative.

---

## What This Service Must Never Do

❌ Grant capabilities  
❌ Modify kernel state  
❌ Bypass orchestrator policy  
❌ Assume trust from authentication alone  

If authentication directly enables execution, it is a design violation.

---

## Build & Run

### Build
```bash
./gradlew build
````

### Run

```bash
./gradlew run
```

This produces a runnable JAR suitable for user-space deployment.

---

## Technology Choices

* **Java 21**
* Gradle
* Jackson (JSON)
* OkHttp (optional external auth)
* SLF4J (logging)

---

## Failure Model

If `authd-swift` crashes or is unavailable:

* Kernel continues running
* Existing processes remain unaffected
* New authenticated sessions may be blocked

System integrity is preserved.

---
