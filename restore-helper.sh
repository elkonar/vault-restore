#!/bin/bash

set -e

# Configuration
NAMESPACE="${RESTORE_NAMESPACE:-default}"
#NAMESPACE2="${RESTORE_NAMESPACE:-vault}"
VAULT_HELM_RELEASE="${VAULT_HELM_RELEASE:-fk-vault}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
  exit 1
}

# Upload snapshot to Kubernetes
upload_snapshot() {
  local local_file="$1"
  local k8s_pod="$2"
  local remote_path="$3"

  log_info "Uploading snapshot: $local_file -> $k8s_pod:$remote_path"

  # Create remote directory
  kubectl exec -n "$NAMESPACE" "$k8s_pod" -- mkdir -p "$(dirname "$remote_path")" || true

  # Copy file
  kubectl cp "$local_file" "$NAMESPACE/$k8s_pod:$remote_path"

  log_success "Snapshot uploaded"
}

# Init and unseal new vault
init_unseal_new() {
  local vault_pod="${1:-fk-vault-0}"
  local creds_file="${VAULT_CREDS_FILE:-$SCRIPT_DIR/.vault-init.env}"

  if kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault status -format=json | jq -e '.initialized == true' > /dev/null; then
    echo "Vault is already initialized. Skipping init."

    if kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault status -format=json | jq -e '.sealed == true' > /dev/null; then
      echo "Vault is sealed. Unsealing.."
      if [ -z "$UNSEAL_KEY" ] && [ -f "$creds_file" ]; then
        # shellcheck disable=SC1090
        . "$creds_file"
      fi
      if [ -z "$UNSEAL_KEY" ]; then
        log_error "UNSEAL_KEY is not set. Export it or source $creds_file"
      fi
      kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault operator unseal "$UNSEAL_KEY"
    fi

    return 0
  fi

  local INIT_OUTPUT
  INIT_OUTPUT=$(kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault operator init -n 1 -t 1 -format=json)

  export UNSEAL_KEY
  UNSEAL_KEY=$(echo "$INIT_OUTPUT" | jq -r '.unseal_keys_b64[0]')
  export ROOT_TOKEN
  ROOT_TOKEN=$(echo "$INIT_OUTPUT" | jq -r '.root_token')

  # Persist credentials so they can be loaded in another shell session.
  local escaped_unseal_key
  local escaped_root_token
  printf -v escaped_unseal_key '%q' "$UNSEAL_KEY"
  printf -v escaped_root_token '%q' "$ROOT_TOKEN"
  umask 077
  cat > "$creds_file" <<EOF
export UNSEAL_KEY=${escaped_unseal_key}
export ROOT_TOKEN=${escaped_root_token}
EOF

  echo "Vault is inited"
  log_success "Credentials saved to: $creds_file"
  log_info "Load them in your shell with: source $creds_file"

# unseal vault
  kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault operator unseal "$UNSEAL_KEY"

# vault login with new root
  kubectl exec -n "$NAMESPACE" "$vault_pod" -- vault login "$ROOT_TOKEN"
}


# Force raft restore
raft_restore() {
  local container="${1:-fk-vault-0}"
  local job=$(kubectl exec -it -n "$NAMESPACE" "$container" -- sh -c 'set -- /tmp/*snap; [ -e "$1" ] || exit 1; vault operator raft snapshot restore -force "$1"')
}


# Main
if [ $# -lt 1 ]; then
  usage
  exit 0
fi

case "$1" in
  upload-snapshot)
    upload_snapshot "$2" "$3" "$4"
    ;;
  init_unseal_new)
    init_unseal_new "${2:-fk-vault-0}"
    ;;
  raft-restore)
    raft_restore "${2:-fk-vault-0}"
    ;;
  *)
    log_error "Unknown command: $1"
    usage
    exit 1
    ;;
esac

# commands
# bash -x ./restore-helper.sh upload-snapshot ./fk-vault-raft.snap fk-vault-0 /snapshots/fk-vault-raft.snap
# bash -x ./restore-helper.sh init_unseal_new fk-vault-0
# bash -x ./restore-helper.sh raft-restore fk-vault-0

