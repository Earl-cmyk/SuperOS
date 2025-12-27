//! Kernel Threads
//!
//! Defines thread descriptors and lifecycle.
//! Threads are scheduling units, not security principals.

#![no_std]

use crate::process::Pid;

/// Thread identifier
pub type Tid = u32;

/// Kernel thread descriptor
pub struct Thread {
    pub tid: Tid,
    pub pid: Pid,
    pub state: ThreadState,
}

/// Thread lifecycle states
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum ThreadState {
    New,
    Runnable,
    Running,
    Blocked,
    Terminated,
}

/// Initialize thread subsystem
pub fn init() {
    // Initialize TID allocator and thread table (stub)
}

/// Create a new thread within a process
pub fn create(_pid: Pid, _entry: *const u8) -> Tid {
    // Allocate TID and register thread (stub)
    0
}

/// Terminate a thread
pub fn terminate(_tid: Tid) {
    // Mark thread terminated (stub)
}
