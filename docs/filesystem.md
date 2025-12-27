# **Filesystem Model**

## **Scope**
This document defines the **filesystem model** for SuperOS.

It specifies:
- Filesystem authority boundaries
- Access control rules
- Project isolation semantics
- Kernel and user-space responsibilities

This document is an **architecture contract**.

---

## **Non-Scope**
This document explicitly does **not** cover:
- Host OS filesystem internals
- POSIX filesystem semantics
- Device files or drivers
- Networked filesystems
- Filesystem performance optimizations

SuperOS treats the host filesystem as an **implementation detail**, not an interface.

---

## **Filesystem Invariants (Hard Rules)**

The following MUST always hold:

- All filesystem access is **capability-gated**
- There is no ambient working directory
- No process may access files without explicit authority
- Projects are isolated from one another
- The kernel mediates all filesystem operations
- Filesystem paths are an authority surface

Violating any invariant is a **kernel error**.

---

## **Filesystem Authority Model**

Filesystem access is governed by **path-scoped capabilities**.

### Capability Types
- `FS_READ:<path>`
- `FS_WRITE:<path>`
- `FS_EXEC:<path>`
- `FS_ADMIN:<path>`

Capabilities apply recursively unless otherwise specified.

Example:
```

FS_READ:/projects/project_a

```

Grants read-only access to all files under `project_a`.

---

## **Kernel Responsibilities**

The kernel MUST:
- Enforce filesystem capabilities
- Validate all filesystem syscalls
- Resolve logical paths to host paths
- Prevent directory traversal
- Maintain isolation between projects

The kernel MUST NOT:
- Expose host filesystem structure
- Provide implicit access
- Trust user-space path resolution

---

## **Logical Filesystem Layout**

SuperOS exposes a **logical filesystem**, independent of the host layout.

```

/
├── projects/
│   ├── project_a/
│   │   ├── .superos/
│   │   │   ├── project.json
│   │   │   └── sync_state.json
│   │   └── src/
│   └── project_b/
│       └── src/
│
├── services/
│   └── <service_name>/
│
└── logs/
└── <pid>/

```

Logical paths are the only paths visible to processes.

---

## **Project Filesystems**

Each project:
- Has its own isolated directory tree
- Is mapped to a process tree
- Cannot see other projects by default

### Project Metadata Directory
```

.project_root/
└── .superos/
├── project.json
└── sync_state.json

```

This directory:
- Is kernel-managed
- Contains authoritative metadata
- Is not user-modifiable without capability

---

## **Path Resolution**

Path resolution follows strict rules:

1. Kernel receives logical path
2. Kernel validates capability against path
3. Kernel normalizes and canonicalizes path
4. Kernel maps to host filesystem
5. Operation is executed or denied

At no point does user-space resolve host paths.

---

## **Read / Write Semantics**

### Read
- Requires `FS_READ`
- Returns immutable buffers
- May be streamed

### Write
- Requires `FS_WRITE`
- Writes are atomic where possible
- Partial writes are visible only after commit

### Execute
- Requires `FS_EXEC`
- Execution is still process-mediated
- Files are never executed directly by the kernel

---

## **Filesystem and Processes**

Filesystem access is always associated with:
- A process
- A capability table
- An audit trail

There is no global filesystem context.

---

## **Services and Filesystem Access**

Services receive **minimal filesystem access**.

Examples:
- Language runtime: project directory only
- Build service: project + build cache
- ML service: read-only logs and metadata
- UI shell: read-only project view

Services MUST NOT request broad filesystem access.

---

## **No Implicit CWD**

SuperOS does NOT support:
- Implicit current working directory
- Relative paths without base authority
- Shell-based path assumptions

All paths are:
- Absolute (logical)
- Explicit
- Capability-validated

---

## **Filesystem Events**

The kernel may emit filesystem events:
- File created
- File modified
- File deleted

Events are:
- Read-only
- Delivered via IPC
- Never actionable directly

---

## **Failure Handling**

- Unauthorized access → denied, logged
- Invalid path → denied
- Capability mismatch → denied
- Kernel mapping failure → operation fails closed

No fallback behavior is allowed.

---

## **Security Considerations**

- Path traversal attacks are prevented at kernel level
- Symlinks are resolved and validated by the kernel
- Capabilities are non-transferrable unless delegated
- Filesystem operations are fully auditable

---

## **Forbidden Designs**

The following are explicitly forbidden:
- Implicit filesystem access
- Shell-controlled working directories
- User-space path resolution to host paths
- Shared writable directories across projects
- Direct host filesystem exposure

---

## **Summary**

The SuperOS filesystem is:
- Capability-gated
- Project-isolated
- Kernel-mediated
- Explicit by design

The filesystem is not a convenience layer.  
It is an **authority boundary**.

If a filesystem feature weakens isolation or authority, it does not ship.
