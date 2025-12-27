//! Process Descriptor & Lifecycle
//!
//! Defines kernel-managed processes.
//! All processes are created, scheduled, and destroyed by the kernel.
//!
//! There is no direct execution from user space.

#![no_std]

use crate::process::state::ProcessState;
use crate::security::capability;
use crate::memory;
use crate::scheduler;

pub type Pid = u32;

/// Kernel process descriptor
pub struct Process {
    pub pid: Pid,
    pub state: ProcessState,
    pub parent: Option<Pid>,
    pub capabilities: capability::CapabilityTable,
}

/// Initialize process subsystem
pub fn init() {
    // Initialize PID allocator and process table (stub)
}

/// Spawn a new process
pub fn spawn(_entry: *const u8, _flags: usize) -> usize {
    capability::require_current("PROC_SPAWN");

    // Allocate PID (stub)
    let pid: Pid = 1;

    let proc = Process {
        pid,
        state: ProcessState::New,
        parent: Some(current_pid()),
        capabilities: capability::CapabilityTable::new(),
    };

    // Register process (stub)
    scheduler::enqueue(pid);

    pid as usize
}

/// Kill a process
pub fn kill(pid: usize) -> usize {
    capability::require_current("PROC_KILL");

    // Transition to terminated state (stub)
    memory::revoke_process(pid as Pid);

    0
}

/// Yield CPU voluntarily
pub fn yield_now() {
    scheduler::yield_current();
}

/// Reap terminated processes
pub fn reap_zombies() {
    // Cleanup terminated processes (stub)
}

/// Get current PID
pub fn current_pid() -> Pid {
    // Return current PID (stub)
    0
}
