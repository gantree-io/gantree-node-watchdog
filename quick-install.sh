#!/usr/bin/env bash

# download latest linux release
echo "Downloading..."
curl -s https://api.github.com/repos/gantree-io/gantree-node-watchdog/releases/latest \
| grep "browser_download_url.*-linux.tar.gz" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -

# unpack
echo "Unpacking..."
tar -xf ./gantree-node-watchdog-v*.*.*-linux.tar.gz

# # execute
# echo "Executing..."
# cd gantree-node-watchdog-v*.*.*-linux && ./bin/gantree_node_watchdog
