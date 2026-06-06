#!/usr/bin/env bash
# Hermes Profile Wrapper: CMO
# Paperclip adapter compatibility layer.
# This script is sourced by hermes-profile-wrapper adapters to
# ensure the profile runs with the correct Hermes Agent configuration.
#
# Usage: source this script, then call run_hermes_profile "$@"

PROFILE_NAME="cmo"
PROFILE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

run_hermes_profile() {
    hermes --profile "${PROFILE_NAME}" "$@"
}

export PROFILE_NAME PROFILE_DIR
