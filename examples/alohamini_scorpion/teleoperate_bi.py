import argparse
import inspect
import os
import time

from lerobot.robots.alohamini_scorpion import LeKiwiClient, LeKiwiClientConfig
from lerobot.teleoperators.keyboard.teleop_keyboard import KeyboardTeleop, KeyboardTeleopConfig
from lerobot.utils.robot_utils import precise_sleep
from lerobot.utils.visualization_utils import init_rerun, log_rerun_data
from lerobot.teleoperators.dual_scorpion_leader import DualScorpionLeader, DualScorpionLeaderConfig

# ============ Parameter Section ============ #
parser = argparse.ArgumentParser()
parser.add_argument("--no_robot", action="store_true", help="Do not connect robot, only print actions")
parser.add_argument(
    "--no_leader",
    action="store_true",
    help="Do not connect leader arm, only perform keyboard-controlled actions.",
)
parser.add_argument("--fps", type=int, default=30, help="Main loop frequency (frames per second)")
parser.add_argument("--remote_ip", type=str, default="127.0.0.1", help="LeKiwi host IP address")
parser.add_argument("--leader_id", type=str, default="so101_leader_bi", help="Leader arm device ID")
parser.add_argument(
    "--invert_left_gripper",
    action="store_true",
    help="Invert left gripper action before sending (0-100 -> 100-0).",
)
parser.add_argument(
    "--invert_right_gripper",
    action="store_true",
    help="Invert right gripper action before sending (0-100 -> 100-0).",
)

args = parser.parse_args()

NO_ROBOT = args.no_robot
NO_LEADER = args.no_leader
FPS = args.fps
INVERT_LEFT_GRIPPER = args.invert_left_gripper
INVERT_RIGHT_GRIPPER = args.invert_right_gripper
# ========================================== #


def maybe_invert_gripper_actions(action: dict[str, float]) -> dict[str, float]:
    if INVERT_LEFT_GRIPPER and "arm_left_gripper.pos" in action:
        action["arm_left_gripper.pos"] = 100.0 - float(action["arm_left_gripper.pos"])
    if INVERT_RIGHT_GRIPPER and "arm_right_gripper.pos" in action:
        action["arm_right_gripper.pos"] = 100.0 - float(action["arm_right_gripper.pos"])
    return action

if NO_ROBOT:
    print("🧪 NO_ROBOT mode enabled: robot will not connect, only print actions.")

if NO_LEADER:
    print("🧪 NO_LEADER mode enabled: leader arm will not connect, only print actions.")
if INVERT_LEFT_GRIPPER:
    print("Left gripper inversion enabled.")
if INVERT_RIGHT_GRIPPER:
    print("Right gripper inversion enabled.")
# Create configs
robot_config = LeKiwiClientConfig(remote_ip=args.remote_ip, id="my_alohamini")

dual_scorpion_config = DualScorpionLeaderConfig(
    right_arm_port="/dev/right_arm",
    left_arm_port="/dev/left_arm",
)
leader = DualScorpionLeader(dual_scorpion_config)

keyboard_config = KeyboardTeleopConfig(id="my_laptop_keyboard")
keyboard = KeyboardTeleop(keyboard_config)
robot = LeKiwiClient(robot_config)

# Connection logic
if not NO_ROBOT:
    robot.connect()
else:
    print("🧪 robot.connect() skipped, only printing actions.")

if not NO_LEADER:
    leader.connect()
else:
    print("🧪 robot.connect() skipped, only printing actions.")

keyboard.connect()


init_rerun(session_name="lekiwi_teleop")

if not robot.is_connected or not leader.is_connected or not keyboard.is_connected:
    print("⚠️ Warning: Some devices are not connected! Still running for debug.")

# Main loop
while True:
    t0 = time.perf_counter()

    observation = robot.get_observation() if not NO_ROBOT else {}
    arm_actions = leader.get_action() if not NO_LEADER else {}
    arm_actions = {f"{k}": v for k, v in arm_actions.items()}
    arm_actions = maybe_invert_gripper_actions(arm_actions)
    keyboard_keys = keyboard.get_action()
    base_action = robot._from_keyboard_to_base_action(keyboard_keys)
    lift_action = robot._from_keyboard_to_lift_action(keyboard_keys)

    action = {**arm_actions, **base_action, **lift_action}
    log_rerun_data(observation, action)

    if NO_ROBOT:
        print(f"[NO_ROBOT] action → {action}")
    else:
        robot.send_action(action)
        print(f"Sent action → {action}")

    precise_sleep(max(1.0 / FPS - (time.perf_counter() - t0), 0.0))
