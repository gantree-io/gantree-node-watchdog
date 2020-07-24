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

## Table of Contents

- [Gantree Node Watchdog](#gantree-node-watchdog)
  - [Table of Contents](#table-of-contents)
  - [Notes](#notes)
    - [Ipify Service](#ipify-service)
  - [Installation](#installation)
    - [Quick Start](#quick-start)
    - [Releases](#releases)
  - [Building](#building)
    - [Requirements](#requirements)
    - [Steps](#steps)

## Notes

### Ipify Service

Gantree Node Watchdog uses ipify to get your machine's public ip address automatically.

Although we have a legitimate use-case for the ipify service, some malicious actors use the same service for command-and-control botnets.

Any potential warnings related to gnw contacting `api.ipify.org` are false-positives and, if required, are safe to add to your firewall's allow list.

## Installation

### Quick Start

```bash
curl -o- https://raw.githubusercontent.com/gantree-io/gantree-node-watchdog/master/quick-install.sh | bash
cd gantree-node-watchdog-v*.*.*-linux
./bin/gantree_node_watchdog
```

### Releases

Stand-alone binaries can be found in [releases](https://github.com/gantree-io/gantree-node-watchdog/releases).

[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/gantree-io/gantree-node-watchdog?include_prereleases&logo=python)](https://github.com/gantree-io/gantree-node-watchdog/releases)

## Building

### Requirements

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/gantree-io/gantree-node-watchdog)

| Package | Version  | Notes                                         |
| ------- | -------- | --------------------------------------------- |
| pipenv  | *latest* | -                                             |
| pyenv   | *latest* | only if required python version not installed |
| make    | *latest* | -                                             |


### Steps

```bash
source configure.sh
pipenv install --dev # if prompted to install python version, accept
pipenv shell
make
```
