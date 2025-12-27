-- SuperOS Database Schema
--
-- This database stores NON-AUTHORITATIVE metadata only.
-- Kernel state, security decisions, and execution truth
-- NEVER depend on this database.
--
-- The database may be wiped without breaking SuperOS.

-- =========================
-- Projects
-- =========================
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- Process Observations
-- =========================
-- This table mirrors observed process state for UI/debugging.
-- It is NOT a source of truth.
CREATE TABLE processes (
    pid BIGINT PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    state TEXT NOT NULL,

    started_at TIMESTAMPTZ,
    exited_at TIMESTAMPTZ
);

-- =========================
-- Declared Capabilities (Policy Metadata)
-- =========================
-- Capabilities here describe intent and configuration.
-- Enforcement always happens in the kernel.
CREATE TABLE capabilities (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    scope TEXT NOT NULL,
    description TEXT
);

CREATE TABLE process_capabilities (
    pid BIGINT REFERENCES processes(pid) ON DELETE CASCADE,
    capability_id UUID REFERENCES capabilities(id) ON DELETE CASCADE,

    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (pid, capability_id)
);

-- =========================
-- Logs (User-Space Aggregation)
-- =========================
CREATE TABLE logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    meta JSONB
);

-- =========================
-- Build Artifacts
-- =========================
CREATE TABLE build_artifacts (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    artifact_type TEXT NOT NULL,
    location TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- Indexes
-- =========================
CREATE INDEX idx_projects_owner ON projects(owner);
CREATE INDEX idx_processes_project ON processes(project_id);
CREATE INDEX idx_logs_timestamp ON logs(timestamp);
