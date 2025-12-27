//! Memory Subsystem
//!
//! Defines kernel-owned memory management.
//! All memory allocation, mapping, and revocation is enforced here.

#![no_std]

pub mod vmm;
pub mod paging;

/// Initialize memory subsystem
pub fn init() {
    vmm::init();
    paging::init();
}
