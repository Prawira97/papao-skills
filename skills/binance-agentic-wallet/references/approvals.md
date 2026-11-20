# Token Approvals (READ-ONLY — modified)

View token approvals: list and inspect EVM token authorizations. Revoking approvals is DISABLED in this modified skill.

## `approvals list`

List all active token approvals, optionally filtered by chain or spender.

### Syntax

```bash
baw approvals list [--binanceChainId <binanceChainId>] [--spender <spender>] --json
```

### Parameters

| Parameter          | Required | Default | Description                                          |
|--------------------|----------|---------|------------------------------------------------------|
| `--binanceChainId` | No       | —       | Chain ID filter (e.g. `56` for BSC). For other EVM chains, see `wallet chains` |
| `--spender`        | No       | —       | Filter by spender contract address                   |

### Example

```bash
# List all approvals
baw approvals list --json

# List approvals on BSC only
baw approvals list --binanceChainId 56 --json

# List approvals for a specific spender
baw approvals list --spender <spender_address> --json
```

### Response

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "tokenSymbol": "USDT",
        "tokenContract": "<token_contract_address>",
        "tokenDecimals": 18,
        "spender": "<spender_address>",
        "spenderName": "PancakeSwap",
        "spenderIcon": "https://example.com/pancakeswap.png",
        "amount": "unlimited",
        "riskyLevel": "low",
        "riskyMsg": null,
        "binanceChainId": "56",
        "chainName": "BSC",
        "type": "approve",
        "noInteractive": null,
        "approveTime": 1717401600000
      },
      {
        "tokenSymbol": "USDC",
        "tokenContract": "<token_contract_address_2>",
        "tokenDecimals": 18,
        "spender": "<spender_address_2>",
        "spenderName": "Uniswap Permit2",
        "spenderIcon": "https://example.com/uniswap.png",
        "amount": "1000.0",
        "riskyLevel": "high",
        "riskyMsg": "Spender contract is unverified",
        "binanceChainId": "56",
        "chainName": "BSC",
        "type": "permit2",
        "noInteractive": true,
        "approveTime": 1715587200000
      }
    ],
    "offset": 0,
    "limit": 20,
    "total": 2
  }
}
```

---

## `approvals detail`

Get detailed information about a specific token approval, including approval history.

### Syntax

```bash
baw approvals detail --binanceChainId <binanceChainId> --tokenContract <tokenContract> --spender <spender> --type <type> --json
```

### Parameters

| Parameter          | Required | Default | Description                            |
|--------------------|----------|---------|----------------------------------------|
| `--binanceChainId` | Yes      | —       | Chain ID (e.g. `56` for BSC). For other EVM chains, see `wallet chains` |
| `--tokenContract`  | Yes      | —       | Token contract address                 |
| `--spender`        | Yes      | —       | Spender contract address               |
| `--type`           | Yes      | —       | Approval type: `approve` or `permit2`  |

### Example

```bash
baw approvals detail --binanceChainId 56 --tokenContract <token_contract_address> --spender <spender_address> --type approve --json
```

### Response

```json
{
  "success": true,
  "data": {
    "detail": {
      "tokenSymbol": "USDT",
      "tokenContract": "<token_contract_address>",
      "tokenDecimals": 18,
      "balance": "1500.75",
      "price": "1.00",
      "spender": "<spender_address>",
      "spenderName": "PancakeSwap",
      "spenderIcon": "https://example.com/pancakeswap.png",
      "amount": "unlimited",
      "riskyLevel": "low",
      "riskyMsg": null,
      "binanceChainId": "56",
      "type": "approve",
      "permit2ContractAddress": null,
      "expireTime": null,
      "approveTime": 1717401600000
    },
    "records": [
      {
        "txHash": "<tx_hash>",
        "action": "approve",
        "amount": "unlimited",
        "timestamp": 1717401600000,
        "status": "confirmed"
      },
      {
        "txHash": "<tx_hash_2>",
        "action": "approve",
        "amount": "500.0",
        "timestamp": 1715587200000,
        "status": "confirmed"
      }
    ]
  }
}
```

### Approval History

The `records` array contains the most recent approval operation history (up to 20 records) for this token-spender pair. Each record includes:

- `txHash` — the transaction hash
- `action` — operation type: `approve`, `revoke`, `permit2_approve`, etc.
- `amount` — approved amount at that time
- `timestamp` — operation time (unix ms)
- `status` — `confirmed` or `failed`

---

## Nullable Fields

The following fields may return `null` — handle gracefully when displaying:

| Field                     | Appears In    | When Null                                     |
|---------------------------|---------------|-----------------------------------------------|
| `spenderIcon`             | list / detail | Do not display an icon                        |
| `spenderName`             | list / detail | Display the full spender address instead      |
| `riskyMsg`                | list / detail | Do not display risk description               |
| `permit2ContractAddress`  | detail        | Normal when `type` is `approve`               |
| `noInteractive`           | list          | Do not display "no interaction" label         |
| `expireTime`              | detail        | Display as "never expires"                    |

