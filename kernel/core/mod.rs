//! SuperOS Kernel Core Module
//!
//! This module defines the foundational wiring of the kernel:
//! - Global kernel interfaces
//! - Core initialization boundaries
//! - Subsystem exposure
//!
//! This module contains no policy and no unsafe shortcuts.

#![no_std]

pub mod kernel;
pub mod syscall;

// Re-export core kernel entry points
pub use kernel::kernel_main;
