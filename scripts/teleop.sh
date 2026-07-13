#!/usr/bin/env bash
# Plain teleoperation: move the leader arm by hand, the follower mirrors it. No cameras.
#
# Usage:  conda activate lerobot && bash scripts/teleop.sh
# Stop:   Ctrl+C
#
# Ports are machine-specific and can change when you replug (especially into a different
# physical USB port). If this errors with "port not found", re-run `lerobot-find-port`
# (once per arm) and update the values below. Calibration is NOT affected by port changes.
set -euo pipefail

FOLLOWER_PORT="${FOLLOWER_PORT:-/dev/tty.usbmodem5B610339821}"
LEADER_PORT="${LEADER_PORT:-/dev/tty.usbmodem5B3D0414741}"

lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port="${FOLLOWER_PORT}" \
  --robot.id=follower_arm \
  --teleop.type=so101_leader \
  --teleop.port="${LEADER_PORT}" \
  --teleop.id=leader_arm
