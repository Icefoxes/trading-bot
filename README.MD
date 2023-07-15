## Introduction

OKX based, currently it can only support real time Tick/Bar/Order/Position live update, and monitor. In `bot/strategies/sample` , created a simple strategy, doing nothing but send notification 

## How to start

### 1. Setup Environment

```shell
python -m venv runtime
runtime\Scripts\activate
pip install -r requirement.txt
```

### 2. Change Configuration

copy `example.conf` and rename to `app.conf` , change parameter

```ini
[exchange]
apiKey           = apiKey
secretKey        = secretKey
passphrase       = passphrase
ws_private       = wss://wsaws.okx.com:8443/ws/v5/private
ws_public        = wss://wsaws.okx.com:8443/ws/v5/public
ws_business      = wss://wsaws.okx.com:8443/ws/v5/business
domain           = https://aws.okx.com
useServerTime    = False

[notification]
token            = token
prefix           = prefix
period           = 8-23
```

### 3. Strategy
implement your own Strategy (extends Strategy) and replace the strategy in `main.py`

```shell
python main.py
```

## Planned feature
- backtesting
- ui to show backtesting