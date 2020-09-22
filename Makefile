compile:
	pipenv run pyinstaller runner.py --onefile --name=gantree_node_watchdog

upload:
	make compile

	# ensure a binary in on the target instance
	scp -i ~/.ssh/id_rsa_digitalocean ./dist/gantree_node_watchdog root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS}:/root/gnw/

	# ensure binary is excutable
	ssh -i ~/.ssh/id_rsa_digitalocean root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS} -t 'bash -i -c "chmod +x /root/gnw/gantree_node_watchdog"'

rconfig:
	scp -i ~/.ssh/id_rsa_digitalocean ./remote/.gnw_config.json root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS}:/root/gnw/

rdnode:
	ssh -i ~/.ssh/id_rsa_digitalocean root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS} -t 'bash -i -c "mkdir -p /root/example_node/"'
	scp -i ~/.ssh/id_rsa_digitalocean ${GANTREE_NODE_WATCHDOG_PATH_TO_EXAMPLE_NODE}/${GANTREE_NODE_WATCHDOG_EXAMPLE_NODE_FILENAME} root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS}:/root/example_node/
	ssh -i ~/.ssh/id_rsa_digitalocean root@${GANTREE_NODE_WATCHDOG_DEV_INSTANCE_IP_ADDRESS} -t 'bash -i -c "chmod +x /root/example_node/${GANTREE_NODE_WATCHDOG_EXAMPLE_NODE_FILENAME}"'

rrnode:
	echo "not yet implemented"

rinstall:
	# upload the binary to the target
	make upload

	# copy config intended for target
	make rconfig

	# download mashnet node to target instace
	make rdnode

	# run mashnet node on target instance
	make rrnode
