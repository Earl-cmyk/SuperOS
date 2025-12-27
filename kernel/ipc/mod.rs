//! IPC Subsystem
//!
//! Defines all inter-process communication primitives.
//! All IPC is explicit, capability-gated, and kernel-mediated.

#![no_std]

pub mod pipe;
pub mod message;
pub mod shared_mem;

/// Initialize IPC subsystem
pub fn init() {
    // Initialize global IPC state
}
