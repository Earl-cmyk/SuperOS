//! Thread Subsystem
//!
//! Defines kernel-managed threads.
//! Threads provide concurrency within a process and no authority.

#![no_std]

pub mod thread;

/// Initialize thread subsystem
pub fn init() {
    thread::init();
}
