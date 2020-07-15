# Gantree Node Watchdog

***This repo may be made public, please treat it was such***

- Ensure you **do not** commit sensitive information

## Table of Contents

- [Gantree Node Watchdog](#gantree-node-watchdog)
  - [Table of Contents](#table-of-contents)
  - [Building](#building)
    - [Requirements](#requirements)
    - [Steps](#steps)

## Building

### Requirements

| Package | Version | Notes                                         |
| ------- | ------- | --------------------------------------------- |
| pipenv  | latest  | -                                             |
| pyenv   | latest  | only if required python version not installed |
| make    | latest  | -                                             |

### Steps

```bash
source configure.sh
pipenv install --dev # if prompted to install python version, accept
pipenv shell
make
```
