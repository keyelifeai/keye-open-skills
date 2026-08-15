#!/usr/bin/env python3
"""Measure IPv4 DNS latency through one macOS network interface."""

from __future__ import annotations

import argparse
import math
import random
import socket
import statistics
import struct
import time
from dataclasses import dataclass


IP_BOUND_IF = 25


@dataclass(frozen=True)
class QueryResult:
    elapsed_ms: float | None
    ok: bool
    detail: str


def encode_qname(domain: str) -> bytes:
    labels = domain.rstrip(".").split(".")
    encoded = bytearray()
    for label in labels:
        value = label.encode("idna")
        if not value or len(value) > 63:
            raise ValueError(f"invalid DNS label in {domain!r}")
        encoded.append(len(value))
        encoded.extend(value)
    encoded.append(0)
    return bytes(encoded)


def query_dns(
    server: str,
    domain: str,
    interface_index: int,
    timeout: float,
) -> QueryResult:
    transaction_id = random.randrange(0, 65536)
    header = struct.pack("!HHHHHH", transaction_id, 0x0100, 1, 0, 0, 0)
    question = encode_qname(domain) + struct.pack("!HH", 1, 1)
    packet = header + question

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.setsockopt(
        socket.IPPROTO_IP,
        IP_BOUND_IF,
        struct.pack("I", interface_index),
    )
    started = time.perf_counter()
    try:
        sock.sendto(packet, (server, 53))
        response, _ = sock.recvfrom(4096)
        elapsed_ms = (time.perf_counter() - started) * 1000
        if len(response) < 12:
            return QueryResult(elapsed_ms, False, "short_response")

        response_id, flags, _, answers, _, _ = struct.unpack(
            "!HHHHHH", response[:12]
        )
        rcode = flags & 0x000F
        ok = response_id == transaction_id and rcode == 0 and answers > 0
        detail = f"rcode={rcode},answers={answers}"
        return QueryResult(elapsed_ms, ok, detail)
    except (OSError, TimeoutError) as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000
        return QueryResult(elapsed_ms, False, f"{type(exc).__name__}:{exc}")
    finally:
        sock.close()


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = max(0, math.ceil(len(ordered) * fraction) - 1)
    return ordered[index]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Measure direct UDP DNS query latency while binding each "
            "IPv4 socket to a macOS network interface."
        )
    )
    parser.add_argument("--interface", required=True, help="Interface such as en0")
    parser.add_argument(
        "--server",
        action="append",
        required=True,
        help="IPv4 DNS server. Repeat for each candidate.",
    )
    parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Domain to query. Repeat for each domain.",
    )
    parser.add_argument("--count", type=int, default=3, help="Queries per domain")
    parser.add_argument("--timeout", type=float, default=2.0, help="Seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.count < 1:
        raise SystemExit("--count must be at least 1")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than 0")

    domains = args.domain or [
        "www.apple.com",
        "github.com",
        "baidu.com",
    ]
    try:
        interface_index = socket.if_nametoindex(args.interface)
    except OSError as exc:
        raise SystemExit(f"unknown interface {args.interface!r}: {exc}") from exc

    print(f"interface\t{args.interface}\tindex\t{interface_index}")
    print("server\tsuccess\ttotal\tmedian_ms\tp95_ms\tavg_ms\tfailures")

    for server in args.server:
        try:
            socket.inet_aton(server)
        except OSError as exc:
            raise SystemExit(f"invalid IPv4 DNS server {server!r}") from exc

        successful: list[float] = []
        failures: list[str] = []
        total = len(domains) * args.count
        for domain in domains:
            for _ in range(args.count):
                result = query_dns(
                    server,
                    domain,
                    interface_index,
                    args.timeout,
                )
                if result.ok and result.elapsed_ms is not None:
                    successful.append(result.elapsed_ms)
                else:
                    failures.append(f"{domain}:{result.detail}")
                time.sleep(0.05)

        if successful:
            median_ms = f"{statistics.median(successful):.1f}"
            p95_ms = f"{percentile(successful, 0.95):.1f}"
            avg_ms = f"{statistics.fmean(successful):.1f}"
        else:
            median_ms = p95_ms = avg_ms = "-"

        failure_text = ";".join(failures) if failures else "-"
        print(
            f"{server}\t{len(successful)}\t{total}\t{median_ms}\t"
            f"{p95_ms}\t{avg_ms}\t{failure_text}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
