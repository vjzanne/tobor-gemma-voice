"""
Robot Bridge
============
Maps relational states to physical Tobor body positions.
On a standard PC, all methods silently do nothing.
On a Raspberry Pi with PCA9685 connected, uncomment the hardware section
and wire your servos to the channel assignments below.

Servo channels (PCA9685):
  0 — torso lean     (neutral=320, forward=360, back=280)
  3 — port arm upper (resting=200, raised=150)
  6 — star arm upper (resting=400, raised=450)
"""

_ROBOT_STATES = {
    "attentive":  {"lean": 320, "arm_port": 200, "arm_star": 400},
    "leaning_in": {"lean": 355, "arm_port": 160, "arm_star": 440},
    "withdrawn":  {"lean": 285, "arm_port": 220, "arm_star": 380},
    "open":       {"lean": 330, "arm_port": 145, "arm_star": 455},
    "still":      {"lean": 320, "arm_port": 210, "arm_star": 390},
    "reaching":   {"lean": 370, "arm_port": 130, "arm_star": 470},
}

try:
    import Adafruit_PCA9685
    _pwm = Adafruit_PCA9685.PCA9685(busnum=1)
    _pwm.set_pwm_freq(60)
    _HARDWARE = True
except Exception:
    _pwm = None
    _HARDWARE = False


def apply_state(robot_state: str):
    """Move Tobor's body to express the current relational state."""
    if not _HARDWARE:
        return

    params = _ROBOT_STATES.get(robot_state, _ROBOT_STATES["attentive"])
    _set_pwm(0, params["lean"])
    _set_pwm(3, params["arm_port"])
    _set_pwm(6, params["arm_star"])


def _set_pwm(channel: int, pulse: int):
    if _pwm is not None:
        _pwm.set_pwm(channel, 0, pulse)
