//! IPC Shared Memory
//!
//! Provides explicitly negotiated, capability-gated shared memory regions.
//! Shared memory is owned, mapped, and revoked by the kernel.
//!
//! There is NO implicit shared memory in SuperOS.

#![no_std]

use crate::process::{Pid, current_pid};
use crate::security::capability;

/// Shared memory region identifier
pub type SharedMemId = usize;

/// Shared memory region descriptor
pub struct SharedMemRegion {
    id: SharedMemId,
    owner: Pid,
    size: usize,
    readers: [Pid; 8],
    writers: [Pid; 8],
}

impl SharedMemRegion {
    /// Create a new shared memory region
    pub fn new(owner: Pid, size: usize) -> Self {
        capability::require_current("MEM_SHARE");

        Self {
            id: 0, // Assigned by kernel allocator (stub)
            owner,
            size,
            readers: [0; 8],
            writers: [0; 8],
        }
    }

    /// Grant read access to a process
    pub fn grant_read(&mut self, pid: Pid) {
        capability::require_current("MEM_SHARE");
        // Add pid to readers list (stub)
    }

    /// Grant write access to a process
    pub fn grant_write(&mut self, pid: Pid) {
        capability::require_current("MEM_SHARE");
        // Add pid to writers list (stub)
    }

    /// Map shared memory into current process
    pub fn map(&self) -> *mut u8 {
        let pid = current_pid();

        if pid != self.owner
            && !self.readers.contains(&pid)
            && !self.writers.contains(&pid)
        {
            return core::ptr::null_mut();
        }

        // Kernel performs mapping (stub)
        core::ptr::null_mut()
    }

    /// Revoke shared memory region
    pub fn revoke(&self) {
        capability::require_current("MEM_SHARE");
        // Kernel unmaps region from all processes (stub)
    }
}
