//! IPC Message Queues
//!
//! Provides structured, capability-gated message passing between processes.
//! All messages are copied, validated, and kernel-mediated.
//!
//! There is no shared state between processes.

#![no_std]

use crate::process::{Pid, current_pid};
use crate::security::capability;

/// Maximum message size (bytes)
const MAX_MESSAGE_SIZE: usize = 4096;

/// Message header
#[repr(C)]
pub struct Message {
    pub from: Pid,
    pub len: usize,
    pub data: [u8; MAX_MESSAGE_SIZE],
}

/// Message queue descriptor
pub struct MessageQueue {
    owner: Pid,
    capacity: usize,
    // internal queue storage (opaque)
}

impl MessageQueue {
    /// Create a new message queue
    pub fn new(owner: Pid, capacity: usize) -> Self {
        Self {
            owner,
            capacity,
        }
    }

    /// Send a message to this queue
    pub fn send(&self, buffer: *const u8, len: usize) -> usize {
        if len > MAX_MESSAGE_SIZE {
            return usize::MAX;
        }

        capability::require_current("IPC_SEND");

        // Kernel copies message from sender into queue
        let _msg = Message {
            from: current_pid(),
            len,
            data: unsafe { core::ptr::read(buffer as *const [u8; MAX_MESSAGE_SIZE]) },
        };

        // Enqueue message (stub)
        0
    }

    /// Receive a message from this queue
    pub fn recv(&self, buffer: *mut u8, max_len: usize) -> usize {
        capability::require_current("IPC_RECV");

        // Dequeue message (stub)
        let msg_len = core::cmp::min(max_len, MAX_MESSAGE_SIZE);

        // Copy to receiver buffer (stub)
        unsafe {
            core::ptr::write_bytes(buffer, 0, msg_len);
        }

        msg_len
    }
}
