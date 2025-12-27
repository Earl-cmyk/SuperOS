# SuperOS Database Layer

This directory defines the **persistent metadata schema** for SuperOS.

## Purpose

The database exists to store:
- Project metadata
- UI-visible state
- Build artifacts
- Logs
- Declared (non-enforced) capability intent

It does **not** store:
- Kernel state
- Execution truth
- Security authority
- Scheduling decisions

If the database is deleted, **SuperOS must still boot and run**.

---

## Architectural Role

```
Kernel → Source of truth
Orchestrator → Policy & coordination
Database → Memory / persistence
UI → Presentation
```


The database is **memory**, not **law**.

---

## schema.sql

`schema.sql` is the **only required file**.

It:
- Declares all tables explicitly
- Acts as documentation
- Is applied manually via Supabase or SQL tools

It is **never** executed automatically by SuperOS.

---

## No Migrations (By Design)

SuperOS does **not** run migrations.

Reasons:
- No implicit authority
- No startup mutation
- No time-based schema logic
- No hidden state transitions

Schema changes are applied manually and explicitly.

---

## Rules (Locked)

- The kernel never reads from the database
- The database never grants permissions
- The orchestrator treats DB data as advisory
- The UI treats DB data as informational
- Supabase outages must not break execution

If a feature requires the database to be correct in order
for execution to be safe, that feature is invalid.

---

## Final Principle

The database remembers.  
The kernel decides.  
The system survives without memory.
