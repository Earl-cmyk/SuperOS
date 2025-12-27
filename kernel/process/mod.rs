//! Process Subsystem
//!
//! Defines kernel-managed processes and their lifecycle.
//! Processes are the primary unit of execution and isolation.

#![no_std]

pub mod process;
pub mod state;

/// Initialize process subsystem
pub fn init() {
    process::init();
}
