# Distribution:
distribution dev

# Art assets:
model-path ../resources

# Server:
server-version infinite-dev
min-access-level 600
accountdb-type developer
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass:
dc-multiple-inheritance #f
dc-sort-virtual-inheritance #t
dc-sort-inheritance-by-file #f
dc-file astron/dclass/toon.dc

# Core features:
want-pets #f
want-parties #f
want-cogdominiums #f
want-achievements #f

# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Optional:
want-yin-yang #f

# Developer options:
show-population #t
force-skip-tutorial #t
want-instant-parties #t
