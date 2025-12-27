// userspace/authd-swift/Package.swift
//
// SuperOS Auth Daemon (Swift)
// User-space authentication & identity service.
// This package defines ZERO kernel authority.

import PackageDescription

let package = Package(
    name: "authd-swift",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "authd-swift",
            targets: ["AuthD"]
        )
    ],
    dependencies: [
        // JSON handling
        .package(
            url: "https://github.com/apple/swift-argument-parser.git",
            from: "1.3.0"
        )
    ],
    targets: [
        .executableTarget(
            name: "AuthD",
            dependencies: [
                .product(
                    name: "ArgumentParser",
                    package: "swift-argument-parser"
                )
            ],
            path: "Sources"
        ),
        .testTarget(
            name: "AuthDTests",
            dependencies: ["AuthD"],
            path: "Tests"
        )
    ]
)
