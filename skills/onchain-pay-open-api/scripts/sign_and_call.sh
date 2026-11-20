#!/usr/bin/env bash
set -euo pipefail

# Binance Onchain-Pay Open API - Sign & Call
# MODIFIED (Papao, 2026-11-19): the API key is NO LONGER accepted as a CLI
# argument (it used to be $4 and showed up in `ps`). It MUST come from the
# environment variable ONCHAIN_PAY_API_KEY.
# Usage: ONCHAIN_PAY_API_KEY="<key>" sign_and_call.sh <base_url> <api_path> <client_id> <pem_path> <json_body>
#
# Example:
#   ONCHAIN_PAY_API_KEY="your-api-key" sign_and_call.sh "https://api.commonservice.io" \
#     "papi/v1/ramp/connect/buy/payment-method-list" \
#     "your-client-id" \
#     "/path/to/private.pem" \
#     '{"fiatCurrency":"USD","cryptoCurrency":"BTC","totalAmount":100,"amountType":1}'

BASE_URL="$1"
API_PATH="$2"
CLIENT_ID="$3"
PEM_PATH="$4"
JSON_BODY="${5:-}"
API_KEY="${ONCHAIN_PAY_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "ERROR: ONCHAIN_PAY_API_KEY environment variable is not set. Refusing to run without it." >&2
  echo "Never pass the API key as a CLI argument (it would be visible in ps)." >&2
  exit 1
fi

# Generate timestamp (milliseconds) - cross-platform compatible
# Using arithmetic expansion works on macOS, Linux, and BSD
timestamp=$(($(date +%s) * 1000))

# Build signing payload: JSON body + timestamp
payload="${JSON_BODY}${timestamp}"

# RSA SHA256 sign with PEM private key, base64 encode
signature=$(echo -n "$payload" \
  | openssl dgst -sha256 -sign "$PEM_PATH" \
  | openssl enc -base64 -A)

# Build curl command
curl_args=(
  --silent
  --location
  --request POST "${BASE_URL}/${API_PATH}"
  --header "X-Tesla-ClientId: ${CLIENT_ID}"
  --header "X-Tesla-SignAccessToken: ${API_KEY}"
  --header "X-Tesla-Signature: ${signature}"
  --header "X-Tesla-Timestamp: ${timestamp}"
  --header "Content-Type: application/json"
  --header "x-trace-id: skill_${timestamp}"
  --header "User-Agent: onchain-pay-open-api/0.1.2 (Skill)"
)

if [ -n "$JSON_BODY" ]; then
  curl_args+=(--data-raw "$JSON_BODY")
fi

curl "${curl_args[@]}" | python3 -m json.tool 2>/dev/null || curl "${curl_args[@]}"
