<p align="center">
    <a alt="License">
        <img alt="GitHub" src="https://img.shields.io/github/license/gantree-io/gantree-node-watchdog"></a>
    <a href="https://discord.gg/BsWVddN" alt="Discord">
        <img alt="Discord" src="https://img.shields.io/discord/719451945345220658?logo=Discord"></a>
    <a href="https://gantree.io" alt="Website">
        <img alt="Website" src="https://img.shields.io/website?down_color=red&down_message=offline&label=gantree.io&up_color=green&up_message=online&url=https%3A%2F%2Fgantree.io"></a>
    <a href="https://app.gantree.io" alt="Web App">
        <img alt="Website" src="https://img.shields.io/website?down_color=red&down_message=offline&label=web%20app&up_color=green&up_message=online&url=https%3A%2F%2Fapp.gantree.io"></a>
    <a alt="OSS Lifecycle">
        <img alt="OSS Lifecycle" src="https://img.shields.io/osslifecycle/gantree-io/gantree-node-watchdog"></a>
</p>

# Gantree Node Watchdog

Instance monitoring client for Gantree

## Quick Start

`curl -o- https://raw.githubusercontent.com/gantree-io/gantree-node-watchdog/master/quick-install.sh | bash && cd gantree-node-watchdog-v*.*.*-linux && ./bin/gantree_node_watchdog`

## Configuration

GNW can be configured using a variety of methods.

In order of greatest precedence, these are:

- Environment variables
- Configuration file
- User prompts
- Defaults

The following values must be configured for every installation

| NAME       | ENVIRONMENT VARIABLE               | CONFIGURATION FILE |
| ---------- | ---------------------------------- | ------------------ |
| API Key    | `GANTREE_NODE_WATCHDOG_API_KEY`    | `api_key`          |
| Project ID | `GANTREE_NODE_WATCHDOG_PROJECT_ID` | `project_id`       |
| Client ID  | `GANTREE_NODE_WATCHDOG_CLIENT_ID`  | `client_id`        |

Optionally, the following may also be configured

| NAME             | ENVIRONMENT VARIABLE                     | CONFIGURATION FILE |
| ---------------- | ---------------------------------------- | ------------------ |
| IP Address       | `GANTREE_NODE_WATCHDOG_IP_ADDRESS`       | `ip_address`       |
| Proxy Hostname   | `GANTREE_NODE_WATCHDOG_PROXY_HOSTNAME`   | `proxy_hostname`   |
| Metrics Hostname | `GANTREE_NODE_WATCHDOG_METRICS_HOSTNAME` | `metrics_hostname` |
| Node ID          | `GANTREE_NODE_WATCHDOG_NODE_ID`          | `node_id`          |
| Node Secret      | `GANTREE_NODE_WATCHDOG_NODE_SECRET`      | `node_secret`      |
| Prompt Missing   | `GANTREE_NODE_WATCHDOG_PROMPT_MISSING`   | `prompt_missing`   |

If any required values have not been configured, GNW will prompt you to enter them in your terminal.

If you would prefer to raise an exception instead, this behaviour can be disabled by setting `prompt missing` to false.

Any prompted values will be stored in the configuration file.

## Simple Usage

To start GNW, run the following in your terminal

```bash
./gantree-node-watchdog
```

If GNW has not yet been configured, you will be prompted to enter any required values.

To stop GNW

- Ensure the terminal running GNW is focused
- Press `Ctrl+C`

## Systemd

### Installation

Create the file `gnw.service` under `/etc/systemd/user/` with the following contents:

```s
# Contents of /etc/systemd/user/myservice.service

[Unit]
Description=Gantree Node Watchdog
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/local/bin/gantree_node_watchdog

[Install]
WantedBy=multi-user.target
```

Now copy the `gantree_node_watchdog` binary to `/usr/local/bin/`

```bash
cp [/path/to/gnw/binary] /usr/local/bin
```

Finally configure all required options by either exporting the associated environment variables or specifying values in `~/.gnw_config.json`.

### Usage

To start GNW

```bash
systemctl --user start gnw
```

To view logs

```bash
journalctl --user -f -u gnw
```

To stop GNW

```bash
systemctl --user stop gnw
```

## Development

Run the following from the root directory of the cloned repository (`gantree-node-watchdog`) to automatically restart GNW when changes occur in watched folders.

This requires PM2 to be installed globally via NPM.

```bash
pipenv run dev
```

To view logs

```bash
pm2 log gnw
```

Please note that due to the way PM2 captures stdout/stderr

- Messages will appear incorrectly formatted
- Coloured output is not possible

To stop GNW

```bash
pm2 del gnw
```

## Releases

Stand-alone binaries can be found in [releases](https://github.com/gantree-io/gantree-node-watchdog/releases).

[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/gantree-io/gantree-node-watchdog?include_prereleases&logo=python)](https://github.com/gantree-io/gantree-node-watchdog/releases)

## Building

### Requirements

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/gantree-io/gantree-node-watchdog)

| Package | Version  | Notes                                         |
| ------- | -------- | --------------------------------------------- |
| pipenv  | _latest_ | -                                             |
| pyenv   | _latest_ | only if required python version not installed |
| make    | _latest_ | -                                             |

### Steps

```bash
source configure.sh
pipenv install --dev # if prompted to install python version, accept
pipenv shell
make
```

## Notes

### Ipify Service

Gantree Node Watchdog uses ipify to get your machine's public ip address automatically.

Although we have a legitimate use-case for the ipify service, some malicious actors use the same service for command-and-control botnets.

Any potential warnings related to GNW contacting `api.ipify.org` are false-positives and, if required, are safe to add to your firewall's allow list.
