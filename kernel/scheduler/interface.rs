//! Scheduler Interface
//!
//! Defines the minimal contract between the kernel and the scheduler.
//! The kernel provides mechanism; policy is external.

#![no_std]

use crate::process::Pid;

/// Initialize scheduler state
pub fn init() {
    // Initialize run queues (stub)
}

/// Scheduler tick handler
pub fn tick() {
    // Perform scheduling decision (stub)
}

/// Enqueue a process into scheduler
pub fn enqueue(_pid: Pid) {
    // Insert process into run queue (stub)
}

/// Yield currently running process
pub fn yield_current() {
    // Voluntary yield (stub)
}
