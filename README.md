# bittracker
A BitTorrent (v1) tracker implementation written in Python.

## Requirements
- *nix-based OS
- [Python 3.14](https://www.python.org/)
- [libev](https://github.com/enki/libev)

## BEPs
* Supported
    * [BEP 3 - The BitTorrent Protocol Specification](https://www.bittorrent.org/beps/bep_0003.html)
    * [BEP 23 - Tracker Returns Compact Peer Lists](https://www.bittorrent.org/beps/bep_0023.html)
    * [BEP 24 - Tracker Returns External IP](https://www.bittorrent.org/beps/bep_0024.html)

* To Be Supported
    * [BEP 21 - Extension for partial seeds](https://www.bittorrent.org/beps/bep_0021.html)
    * [BEP 31 - Failure Retry Extension](https://www.bittorrent.org/beps/bep_0031.html)

* Not Supported:
    * [BEP 7 - IPv6 Tracker Extension](https://www.bittorrent.org/beps/bep_0007.html)
    * [BEP 52 - The BitTorrent Protocol Specification v2](https://www.bittorrent.org/beps/bep_0052.html)

## Setup
1. `sudo apt install libev-dev`
2. `git clone https://github.com/snaacky/bittracker.git`
3. `cd bittracker`
4. `uv sync`
5. `cp config.example.toml config.toml`
6. `uv run -m bittracker.main`

Adjust the config values as needed but the defaults should be fine at scale.

## Benchmark
```
$ wrk -t4 -c5000 -d1s -s scripts/random_announce.lua http://127.0.0.1:8080/announce
Running 1s test @ http://127.0.0.1:8080/announce
  4 threads and 5000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    85.13ms   73.57ms 977.40ms   98.27%
    Req/Sec    11.56k     4.05k   18.51k    57.89%
  43736 requests in 1.10s, 9.00MB read
Requests/sec:  39872.95
Transfer/sec:      8.20MB
```
This benchmark was taken on an i7-13700KF @ 5.0 GHz with 32GB DDR4 @ 3200MHz. Your results will vary depending on your hardware.

## sysctl.conf
```
vm.overcommit_memory=0
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 10
net.core.netdev_max_backlog = 2000
net.ipv4.tcp_low_latency = 1
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_syncookies = 1
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 8192
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.netfilter.nf_conntrack_max = 524288
fs.file-max = 500000
net.ipv4.ip_local_port_range = 1024 65000
```