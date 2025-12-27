//! Scheduler Subsystem
//!
//! Defines kernel-facing scheduler hooks.
//! Policy lives outside the kernel.

#![no_std]

pub mod interface;

/// Initialize scheduler subsystem
pub fn init() {
    interface::init();
}

/// Scheduler tick (called from kernel loop)
pub fn tick() {
    interface::tick();
}

/// Enqueue a process
pub fn enqueue(pid: crate::process::Pid) {
    interface::enqueue(pid);
}

/// Yield current process
pub fn yield_current() {
    interface::yield_current();
}
