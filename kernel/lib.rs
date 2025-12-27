//! SuperOS Kernel Crate
//!
//! This is the trusted kernel root.
//! All core subsystems are wired here.
//!
//! Policy does NOT live here.
//! User space does NOT bypass this crate.

#![no_std]

pub mod core;
pub mod process;
pub mod thread;
pub mod memory;
pub mod ipc;
pub mod scheduler;
pub mod security;
