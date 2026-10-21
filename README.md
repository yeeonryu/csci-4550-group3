# csci-4550-group3
Git repository for group 3's final project for CSCI 4550

Only dependency is Python3


Host1: virtual address = `hostOne`, UDP port = 1111  
Host2: virtual address = `hostTwo`, UDP port = 2222  
RouterA: virtual address = `routerA`, UDP port = 3333  
RouterB: virtual address = `routerB`, UDP port = 4444  
RouterC: virtual address = `routerC`, UDP port = 5555  
RouterD: virtual address = `routerD`, UDP port = 6666  

Config files are  
`configUp.json`: upper path, A -> B -> D  
`configLow.json`: lower path, A -> C -> D  
`configLoop.json`: forwarding loop between A and B for hop-limit test  

In config:  
`ip`, `local_port`: the actual UDP endpoint  
`address_name`: the virtual address  
`neighbor_ports`: the ports this device is allowed to send to  
`table` (for routers): virtual destination -> next hop port  


Running the network

Run each process in its own terminal, in order of the 4 routers, then the listening host, then the sending host.

Running a router

`python3 router.py [configType] [routerName]`

configType: `configUp`, `configLow`, or `configLoop`  
routerName: `routerA`, `routerB`, `routerC`, or `routerD`  

Say you want to run for routerA with upper path, then the command would be `python3 router.py configUp routerA`

Running a host

`python3 host.py [configType] [hostName] [action] [otherHostName](*only when action is send)`

configType: `configUp`, `configLow`, or `configLoop`  
hostName: `hostOne`, `hostTwo`  
action: `send` or `listen`  
otherHostName: `hostOne`, `hostTwo` (host other than the `hostName` chosen)  

Say you want to run for hostOne with upper path to send, then the command would be `python3 host.py configUp hostOne send hostTwo`

Hop limit rule

Hosts send every packet with a hop limit of 8  
Each router subtracts 1 from the hop limit. If the result is smaller than 1, the router drops the packet. If that's not the case, it forwards the packet with the new hop limit.  
Thus, on the upper path a probe leaves hostOne with 8 and reaches hostTwo with 5 since A, B, and D each subtract 1  
With configLoop a probe bounces between A and B until B drops it, and then the sender times out  

Forwarding

For every packet, the router looks up `dest` in its table to get the next hop port, then sends to that port. The router drops the packet and logs the reason. Reasons could be if the packet is not valid (`invalid packet`),the hop limit runs out (`hop limit passed`), the destination is not in the table (`destination not in forwarding table`), or the next hop is not a neighbor (`not a neighbor port`).

Loss and delay

Loss and delay are set on only for the link from routerA to the port in `next_hop` (routerB, 4444, in `configUp`). They apply to every packet type going over that link.

`seed`: random seed for the loss, so that a run can be reproduced  
`loss_rate`: chance of dropping each packet, e.g. `0.05` for 5% (`drop because of loss rate triggered`)  
`drop_id`: drop the packet with this id, to force one drop (`drop is forced`).  
`delay_ms`: added delay before sending.  
`next_hop`: the next hop port the loss and delay apply to  

Only the A to B direction is affected.  Leave `loss_rate` and `delay_ms` at 0 and `drop_id` at `null` for regular runs.

Logging

Every host and router write to `log.txt` in the folder you run from. The fields are, in order

`device, event, src, dest, type, hopLimit, id, nextHop, reason, timestamp, runId`

event: `send`, `receive`, `forward`, `delay`, `drop`, or `timeout`  
hopLimit: for routers, this is the value after subtracting 1  
timestamp: `time.time()` in seconds  
runId: taken from the `RUN_ID` environment variable, `manual` if it isn't set  

Baseline experiment

2 delay settings (0 ms, 100 ms) and 2 loss settings (0%, 5%) on the A -> B link, 3 runs each with seeds 720, 721, and 722, 25 probes per run, upper path. The raw lines are in `log.txt` under run ids like `d0ms-l0pct-s720`.

Progress report

https://docs.google.com/document/d/1LUcgTT27H8fMWzxBuGkkyLF-lJxDqNsxl7OFqX1S9ac/edit?usp=sharing
