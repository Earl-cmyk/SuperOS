//! IPC Pipes
//!
//! Provides stream-oriented, unidirectional IPC channels.
//! Pipes are kernel-managed, capability-gated, and copy-based.
//!
//! Pipes are for byte streams, not structured messages.

#![no_std]

use crate::process::{Pid, current_pid};
use crate::security::capability;

/// Maximum pipe buffer size (bytes)
const PIPE_BUFFER_SIZE: usize = 8192;

/// Pipe descriptor
pub struct Pipe {
    reader: Pid,
    writer: Pid,
    // internal ring buffer (opaque)
}

impl Pipe {
    /// Create a new pipe between two processes
    pub fn new(reader: Pid, writer: Pid) -> Self {
        Self { reader, writer }
    }

    /// Write bytes into the pipe
    pub fn write(&self, buffer: *const u8, len: usize) -> usize {
        capability::require_current("IPC_SEND");

        if current_pid() != self.writer {
            return usize::MAX;
        }

        // Copy bytes into kernel buffer (stub)
        len
    }

    /// Read bytes from the pipe
    pub fn read(&self, buffer: *mut u8, max_len: usize) -> usize {
        capability::require_current("IPC_RECV");

        if current_pid() != self.reader {
            return usize::MAX;
        }

        let to_read = core::cmp::min(max_len, PIPE_BUFFER_SIZE);

        // Copy bytes out of kernel buffer (stub)
        unsafe {
            core::ptr::write_bytes(buffer, 0, to_read);
        }

        to_read
    }
}
