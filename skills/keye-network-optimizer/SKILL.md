---
name: keye-network-optimizer
description: >
  Diagnose and improve macOS network speed and stability with before baselines,
  proxy/VPN/TUN separation, minimal reversible changes, and after retesting.
  Use for networkQuality, DNS latency, Wi-Fi quality, packet loss, MTU, system
  proxy, route takeover, CLI proxy, or background traffic investigations, and
  when the user asks to 优化网络、排查网络不稳定、检查代理或 runs
  /keye-network-optimizer.
license: MIT
compatibility: Requires macOS and Python 3. Network inspection uses built-in macOS tools; any privileged or connection-changing action requires explicit user approval.
metadata:
  author: keyelifeai
  version: "1.0.0"
---

# Keye Network Optimizer

Use this workflow on macOS. Preserve connectivity, proxy access, VPN access,
and remote sessions while collecting comparable evidence.

## Non-negotiable safety rules

- Follow this order: diagnose, make the smallest reversible change, retest.
- Never run destructive resets such as deleting network services, removing VPN
  profiles, resetting all network preferences, or unloading system daemons.
- Do not use `sudo`, disable a VPN/TUN/proxy, change MTU, or terminate a process
  without first explaining the effect and obtaining user approval.
- Treat a user requirement to keep a proxy for GFW access as a hard constraint.
- Record the current value and an exact rollback command before every change.
- Do not hardcode interface names, gateway addresses, proxy ports, DNS winners,
  or network service names from a previous run.
- Run throughput, ping, DNS, and traffic sampling sequentially. Concurrent tests
  create load and invalidate latency and packet-loss comparisons.
- Keep before and after conditions identical. A TUN-on versus TUN-off comparison
  is a separate A/B test and must be labeled as such.

## Phase 1: establish scope and safety

1. Confirm the host is macOS and note whether the user is local or connected
   through SSH, Screen Sharing, a VPN, or another remote-control path.
2. Ask whether proxy/VPN/TUN connectivity is mandatory if the user has not said.
3. Ask other users and applications to pause large transfers for the baseline.
4. Create a timestamped evidence directory and keep raw before/after outputs.
5. Do not make changes until all required before measurements are complete.

Use shell variables with task-specific names. If a multi-line snippet uses Bash
arrays, run it with `bash -lc` rather than relying on zsh behavior.

## Phase 2: collect the before baseline

Collect these snapshots first:

```sh
sw_vers
scutil --nwi
route -n get default
scutil --dns
scutil --proxy
networksetup -listallhardwareports
networksetup -listallnetworkservices
networksetup -listnetworkserviceorder
```

Derive the active physical interface and gateway from `route -n get default`.
Map that interface to its network service with
`networksetup -listnetworkserviceorder`. Do not assume Wi-Fi is `en0` or `en1`.

Inspect routes for representative destinations:

```sh
route -n get 1.1.1.1
route -n get 8.8.8.8
route -n get 100.100.100.100
netstat -rn -f inet
netstat -rn -f inet6
```

Interpret `utun*`, `198.18.0.0/15`, Tailscale DNS, and split routes as evidence
of VPN/TUN involvement. The system default route alone does not prove that a
public destination uses the physical interface.

Run the user-experience throughput test once while the machine is idle:

```sh
networkQuality
```

When the system proxy is enabled, normal `networkQuality` measures the
proxy-aware application path. Do not use `networkQuality -I <interface>` as the
raw-link baseline in that state. CFNetwork may still attempt the proxy and fail;
that is a measurement conflict, not proof that the network is down. Use route,
ping, and interface-bound DNS tests for the raw physical path.

After `networkQuality` has finished, run idle pings sequentially:

```sh
ping -c 30 -i 0.2 <gateway>
ping -c 30 -i 0.2 1.1.1.1
ping -c 30 -i 0.2 8.8.8.8
```

Record loss, min/average/max, and standard deviation. A public DNS ping may be a
TUN-path measurement or may be deprioritized by the destination, so correlate it
with `route -n get` and do not diagnose the WAN from one target alone.

Test DNS servers through the physical interface, bypassing route takeover:

```sh
python3 <skill-dir>/scripts/dns_latency.py \
  --interface <physical-interface> \
  --server <current-dns-1> \
  --server <candidate-dns-2> \
  --domain www.apple.com \
  --domain github.com \
  --domain baidu.com \
  --count 3
```

Include the active DHCP/ISP DNS servers and relevant local candidates. Public
resolvers such as `1.1.1.1` or `8.8.8.8` are examples, not automatic winners.
Require successful answers across local and international domains. Rank by
failures first, then median and p95 latency. Do not select a resolver only from a
cached `dig` result or a single fast response.

## Wi-Fi, MTU, cache, and background checks

For Wi-Fi, collect connected channel, band, width, RSSI, noise, Tx Rate, and
nearby-channel occupancy:

```sh
system_profiler SPAirPortDataType -json
```

Use the current macOS-supported data source. The old `airport` utility may be
missing, and privileged `wdutil` commands require approval. Strong RSSI does not
rule out narrow channel width, low Tx Rate, interference, or bufferbloat.

Inspect interface MTU and test path MTU without changing it:

```sh
ifconfig <physical-interface>
ping -D -s 1472 -c 3 <gateway>
ping -D -s 1400 -c 3 1.1.1.1
```

Treat ICMP filtering separately from fragmentation. Change MTU only after
repeatable evidence and explicit approval because VPN/TUN traffic may break.

Inspect caches and resolver state:

```sh
dscacheutil -statistics
scutil --dns
```

`dscacheutil -statistics` may not expose cache-node details. That message alone
is not a DNS failure.

Inspect route-owning and high-traffic processes with targeted output:

```sh
ps -axo pid,ppid,pcpu,pmem,comm,args | rg -i 'tailscale|shadowrocket|stash|surge|clash|mihomo|sing-box|wireguard|openvpn|vpn|cloudflare|warp|zerotier|bird|fileprovider|dropbox|onedrive|google drive|baidunetdisk|netdisk|aria2|transmission|qbittorrent|thunder|xunlei|syncthing|resilio'
nettop -P -L 3 -s 1 -t external -J bytes_in,bytes_out,rx_dupe,rx_ooo,re-tx
lsof -nP -iTCP -sTCP:ESTABLISHED
```

Use narrow process and connection checks instead of broad binary `strings`
searches. Do not stop sync, download, proxy, or VPN processes automatically.
Identify the process and ask the user to pause it when it materially affects the
baseline.

## Proxy and CLI inheritance checks

When GUI apps work but Terminal or Ghostty CLIs fail, compare all three layers:

```sh
scutil --proxy
launchctl getenv HTTP_PROXY
launchctl getenv HTTPS_PROXY
launchctl getenv ALL_PROXY
env | rg -i '^(http_proxy|https_proxy|all_proxy|no_proxy)='
```

Inspect shell startup files and actual process connections. macOS System
Settings proxy values do not automatically become shell environment variables.
Before recommending proxy exports, derive the current host and port and verify
the candidate proxy with a real HTTP CONNECT request. Existing terminal tabs and
running CLIs keep their old environment and must be restarted after an approved
shell change.

## Phase 3: choose minimal reversible changes

Make a change only when the before evidence supports it:

- Service order: move the active physical Wi-Fi or Ethernet service first while
  preserving every existing service in the command. Save the original complete
  order for rollback.
- Unused service: disable only a clearly inactive old or pseudo service with
  `networksetup -setnetworkserviceenabled <service> off`. Never remove it. Do not
  disable bridges used by virtual machines, docks, Internet Sharing, or remote
  access.
- DNS: set the active physical service to the fastest reliable measured pair
  with `networksetup -setdnsservers <service> <primary> <secondary>`. Save whether
  the original state was DHCP (`Empty`) or explicit addresses.
- Cache: run `dscacheutil -flushcache`. `killall -HUP mDNSResponder` normally
  needs administrator privileges, so explain the brief name-resolution impact
  and ask before using `sudo`.
- Background load: ask the user to pause the identified process. Send a signal
  only after approval and prefer a normal application quit.
- VPN/TUN: never change it silently. If the user approves an A/B test, preserve a
  required system proxy, capture TUN-on and TUN-off routes, and restore the chosen
  state after comparison.

After each change, immediately verify the setting and retain its rollback
command. If verification fails, stop and restore the prior value before trying
another approach.

## Phase 4: retest under matching conditions

Run the same tests in the same order:

1. Normal `networkQuality` under the same proxy/TUN state.
2. Idle gateway ping.
3. Idle pings to the same public targets.
4. Interface-bound DNS test with the same domains, count, and timeout.
5. Route, resolver, proxy, service-order, and process snapshots.

If a metric changes sharply, check for background traffic and repeat only that
measurement once. Do not hide regressions or compare unlike proxy/TUN states.

## Required final report

Report:

- before versus after downlink, uplink, idle latency, loaded responsiveness,
  gateway/public loss, and DNS failures/median/p95;
- whether each metric represents the proxy-aware application path, the TUN path,
  or the raw physical path;
- the three main issues, ordered by impact and backed by evidence;
- every applied change and exact rollback command;
- skipped privileged or connection-impacting actions;
- unresolved items that require manual work, including router/Wi-Fi changes;
- whether TUN-on/TUN-off was tested as a separate A/B comparison.

State that network measurements are variable and avoid claiming a lasting gain
from a single throughput sample.
