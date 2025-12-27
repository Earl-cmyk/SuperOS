//! Security Subsystem
//!
//! Defines kernel-enforced security primitives.
//! All authority is expressed via capabilities.

#![no_std]

pub mod capability;

/// Initialize security subsystem
pub fn init() {
    capability::init();
}
