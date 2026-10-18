# csci-4550-group3
Git repository for group 3's final project for CSCI 4550

Running a router

`python3 router.py [configType] [routerName]`

- configType: `configUp` or `configLow`
- routerName: `routerA`, `routerB`, `routerC`, or `routerD`

Say you want to run for routerA with upper path, then the command would be `python3 router.py configUp routerA`

Running a host

`python3 host.py [configType] [hostName] [action] [otherHostName](*only when action is send)`

- configType: `configUp` or `configLow`
- hostName: `hostOne`, `hostTwo`
- action: `send` or `listen`
- otherHostName: `hostOne`, `hostTwo` (host other than the `hostName` chosen)


Say you want to run for hostOne with upper path to send, then the command would be `python3 host.py configUp hostOne send hsotTwo`


https://docs.google.com/document/d/1LUcgTT27H8fMWzxBuGkkyLF-lJxDqNsxl7OFqX1S9ac/edit?usp=sharing
