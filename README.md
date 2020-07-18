<p align="center">
    <a alt="License">
        <img alt="GitHub" src="https://img.shields.io/github/license/gantree-io/gantree-node-watchdog"></a>
    <a alt="Vulnerabilities">
        <img alt="Snyk Vulnerabilities for GitHub Repo" src="https://img.shields.io/snyk/vulnerabilities/github/gantree-io/gantree-node-watchdog"></a>
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

***This repo may be made public, please treat it was such***

- Ensure you **do not** commit sensitive information

## Table of Contents

- [Gantree Node Watchdog](#gantree-node-watchdog)
  - [Table of Contents](#table-of-contents)
  - [Building](#building)
    - [Requirements](#requirements)
    - [Steps](#steps)

## Installation

Stand-alone binaries can be found in [releases](https://github.com/gantree-io/gantree-node-watchdog/releases).

[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/gantree-io/gantree-node-watchdog?include_prereleases&logo=python)](https://github.com/gantree-io/gantree-node-watchdog/releases)

## Building

### Requirements

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/gantree-io/gantree-node-watchdog)

| Package | Version | Notes                                         |
| ------- | ------- | --------------------------------------------- |
| pipenv  | *latest*  | -                                             |
| pyenv   | *latest*  | only if required python version not installed |
| make    | *latest*  | -                                             |


### Steps

```bash
source configure.sh
pipenv install --dev # if prompted to install python version, accept
pipenv shell
make
```
