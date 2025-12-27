//! Syscall Interface
//!
//! Defines the kernel entry point for user-space syscalls.
//! All syscalls are validated, capability-checked, and dispatched here.
//!
//! There are NO direct kernel calls from user space.

#![no_std]

use crate::process;
use crate::security::capability;
use crate::ipc;
use crate::memory;

/// Syscall numbers
#[repr(u32)]
pub enum Syscall {
    ProcSpawn = 1,
    ProcKill = 2,
    IpcSend = 3,
    IpcRecv = 4,
    MemAlloc = 5,
    MemShare = 6,
    Yield = 7,
}

/// Syscall request frame (ABI-stable)
#[repr(C)]
pub struct SyscallFrame {
    pub syscall_id: u32,
    pub arg0: usize,
    pub arg1: usize,
    pub arg2: usize,
    pub arg3: usize,
}

/// Initialize syscall subsystem
pub fn init() {
    // Register syscall handler with interrupt/host bridge
}

/// Main syscall dispatcher
///
/// # Safety
/// Called from interrupt / host boundary.
#[no_mangle]
pub extern "C" fn syscall_entry(frame: &SyscallFrame) -> usize {
    match frame.syscall_id {
        x if x == Syscall::ProcSpawn as u32 => {
            capability::require_current("PROC_SPAWN");
            process::spawn(frame.arg0 as *const u8, frame.arg1)
        }

        x if x == Syscall::ProcKill as u32 => {
            capability::require_current("PROC_KILL");
            process::kill(frame.arg0)
        }

        x if x == Syscall::IpcSend as u32 => {
            capability::require_current("IPC_SEND");
            ipc::send(frame.arg0, frame.arg1 as *const u8, frame.arg2)
        }

        x if x == Syscall::IpcRecv as u32 => {
            capability::require_current("IPC_RECV");
            ipc::recv(frame.arg0, frame.arg1 as *mut u8, frame.arg2)
        }

        x if x == Syscall::MemAlloc as u32 => {
            capability::require_current("MEM_ALLOC");
            memory::alloc(frame.arg0)
        }

        x if x == Syscall::MemShare as u32 => {
            capability::require_current("MEM_SHARE");
            memory::share(frame.arg0, frame.arg1)
        }

        x if x == Syscall::Yield as u32 => {
            process::yield_now();
            0
        }

        _ => {
            // Invalid syscall
            usize::MAX
        }
    }
}
