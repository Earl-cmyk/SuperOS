//! Process States
//!
//! Defines the lifecycle states of a kernel-managed process.
//! State transitions are enforced by the kernel.

#![no_std]

/// Process lifecycle states
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum ProcessState {
    /// Process has been created but not yet scheduled
    New,

    /// Process is ready to run
    Ready,

    /// Process is currently executing
    Running,

    /// Process is blocked (IPC, I/O, sleep)
    Blocked,

    /// Process has exited and awaits cleanup
    Terminated,
}
