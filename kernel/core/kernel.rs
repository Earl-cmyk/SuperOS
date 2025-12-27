//! SuperOS Kernel Entry Point
//!
//! This file defines:
//! - Kernel initialization sequence
//! - Subsystem registration
//! - Kernel main loop
//!
//! This is the trusted root of execution.
//! If anything unsafe happens here, the system is compromised.

#![no_std]
#![no_main]

use core::panic::PanicInfo;

use crate::core::syscall;
use crate::ipc;
use crate::memory;
use crate::process;
use crate::scheduler;
use crate::security;

static mut KERNEL_INITIALIZED: bool = false;

/// Kernel entry point
///
/// Called exactly once by the host bootstrap layer.
#[no_mangle]
pub extern "C" fn kernel_main() -> ! {
    unsafe {
        if KERNEL_INITIALIZED {
            kernel_panic("kernel_main called twice");
        }
        KERNEL_INITIALIZED = true;
    }

    kernel_init();

    kernel_loop();
}

/// Initialize all kernel subsystems
fn kernel_init() {
    // Order matters. Do not reorder casually.

    security::init();
    memory::init();
    process::init();
    ipc::init();
    scheduler::init();
    syscall::init();

    log_kernel("kernel initialized");
}

/// Kernel main loop
///
/// The kernel does not execute user code.
/// It reacts to interrupts, syscalls, and scheduling events.
fn kernel_loop() -> ! {
    loop {
        scheduler::tick();
        ipc::dispatch();
        process::reap_zombies();
    }
}

/// Kernel logging (very limited, early-safe)
fn log_kernel(_msg: &str) {
    // Stub: routed to host logging / serial / ring buffer
}

/// Kernel panic handler
fn kernel_panic(_msg: &str) -> ! {
    // Stub: fatal halt
    loop {}
}

/// Rust panic handler
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    kernel_panic("rust panic in kernel")
}
