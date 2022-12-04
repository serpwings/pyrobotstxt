import pytest
from pyrobotstxt import RobotsTxt


def test_robot_name():
    mrt = RobotsTxt()
    resutl = mrt.robots_name("facebook")
    assert "facebot" in resutl, "test passed"
