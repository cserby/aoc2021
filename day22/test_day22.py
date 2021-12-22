import pytest

from .day22 import Brick, parse_input, reboot, reboot_2, sum_volume


@pytest.mark.parametrize(
    argnames=["b1", "b2", "result"],
    argvalues=[
        (Brick(0, 1, 0, 1, 0, 1), Brick(100, 101, 100, 101, 100, 101), None),
        (Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(0, 1, 0, 1, 0, 1), Brick(-1, 2, -1, 2, -1, 2), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(-1, 2, -1, 2, -1, 2), Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(0, 10, 0, 1, 0, 1), Brick(-10, 0, 0, 1, 0, 1), Brick(0, 0, 0, 1, 0, 1)),
        (Brick(10, 11, 10, 11, 0, 0), Brick(
            11, 12, 11, 12, 0, 0), Brick(11, 11, 11, 11, 0, 0)),
        (
            Brick(-5, 47, -31, 22, -19, 33),
            Brick(-44, 5, -27, 21, -14, 35),
            Brick(x_l=-5, x_h=5, y_l=-27, y_h=21, z_l=-14, z_h=33),
        ),
        (
            Brick(-5, 47, -31, 22, -19, 33),
            Brick(-49, -1, -11, 42, -10, 38),
            Brick(x_l=-5, x_h=-1, y_l=-11, y_h=22, z_l=-10, z_h=33),
        ),
        (
            Brick(-44, 5, -27, 21, -14, 35),
            Brick(-49, -1, -11, 42, -10, 38),
            Brick(x_l=-44, x_h=-1, y_l=-11, y_h=21, z_l=-10, z_h=35),
        ),
        (
            Brick(-49, -1, -11, 42, -10, 38),
            Brick(-44, 5, -27, 21, -14, 35),
            Brick(x_l=-44, x_h=-1, y_l=-11, y_h=21, z_l=-10, z_h=35),
        ),
        (
            Brick(0, 2, 0, 2, 0, 2),
            Brick(2, 4, 2, 4, 2, 4),
            Brick(2, 2, 2, 2, 2, 2),
        ),
        (
            Brick(0, 2, 0, 2, 0, 2),
            Brick(-2, 0, -2, 0, -2, 0),
            Brick(0, 0, 0, 0, 0, 0),
        ),
        (
            Brick(0, 2, 0, 2, 0, 2),
            Brick(-2, 0, 2, 4, 2, 4),
            Brick(0, 0, 2, 2, 2, 2),
        ),
    ],
    ids=[
        "no-intersect",
        "intersect-self",
        "superset",
        "subset",
        "x-face-touches",
        "asd",
        "1-2",
        "1-3",
        "2-3",
        "3-2",
        "2x 3x3x3 1",
        "2x 3x3x3 2",
        "2x 3x3x3 3",
    ]
)
def test_intersect(b1, b2, result):
    assert b1 & b2 == result


@pytest.mark.parametrize(
    argnames=["b1", "b2", "result"],
    argvalues=[
        (Brick(0, 1, 0, 1, 0, 1), Brick(100, 101, 100,
         101, 100, 101), set([Brick(0, 1, 0, 1, 0, 1)])),
        (Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1), set()),
        (Brick(0, 2, 0, 0, 0, 0), Brick(1, 1, 0, 0, 0, 0), set([
            Brick(0, 0, 0, 0, 0, 0),
            Brick(2, 2, 0, 0, 0, 0),
        ])),
        (Brick(0, 2, 0, 2, 0, 0), Brick(1, 1, 1, 1, 0, 0), set([
            Brick(0, 0, 0, 0, 0, 0),
            Brick(1, 1, 0, 0, 0, 0),
            Brick(2, 2, 0, 0, 0, 0),
            Brick(0, 0, 2, 2, 0, 0),
            Brick(1, 1, 2, 2, 0, 0),
            Brick(2, 2, 2, 2, 0, 0),
            Brick(0, 0, 1, 1, 0, 0),
            Brick(2, 2, 1, 1, 0, 0),
        ])),
        (Brick(0, 2, 0, 2, 0, 2), Brick(1, 1, 1, 1, 1, 1), set([
            Brick(0, 2, 0, 2, 0, 0),
            Brick(0, 2, 0, 2, 2, 2),
            Brick(0, 2, 0, 0, 1, 1),
            Brick(0, 2, 2, 2, 1, 1),
            Brick(0, 0, 0, 2, 1, 1),
            Brick(2, 2, 0, 2, 1, 1),
        ])),
        (Brick(1, 1, 1, 1, 1, 1), Brick(0, 2, 0, 2, 0, 2), set()),
        (Brick(0, 100, 0, 1, 0, 1), Brick(-100, 0, 0, 1, 0, 1), set([
            Brick(x_l=1, x_h=100, y_l=0, y_h=1, z_l=0, z_h=1)
        ]))
    ],
    ids=[
        "no-intersect",
        "intersect-self",
        "take-out-middle-1d",
        "take-out-middle-2d",
        "take-out-middle-3d",
        "superset",
        "x-face-touches",
    ]
)
def test_sub(b1, b2, result):
    assert cuboids(b1 - b2) == cuboids(result)


@pytest.mark.parametrize(
    argnames=["b1", "result"],
    argvalues=[
        (Brick(1, 1, 1, 1, 1, 1), 1),
        (Brick(0, 1, 1, 1, 1, 1), 2),
        (Brick(0, 2, 0, 2, 0, 2), 27),
    ],
    ids=[
        "1x1x1",
        "2x1x1",
        "3x3x3",
    ]
)
def test_volume(b1, result):
    assert b1.volume == result


def cuboids(brick_set):
    return set(cuboid for brick in brick_set for cuboid in brick.cuboids())


@pytest.mark.parametrize(
    argnames=["instructions", "result"],
    argvalues=[
        (
            [
                ("on", Brick(0, 2, 0, 2, 0, 2)),
                ("off", Brick(1, 1, 1, 1, 1, 1)),
            ],
            [
                Brick(0, 2, 0, 2, 0, 0),
                Brick(0, 2, 0, 2, 2, 2),
                Brick(0, 2, 0, 0, 1, 1),
                Brick(0, 2, 2, 2, 1, 1),
                Brick(0, 0, 0, 2, 1, 1),
                Brick(2, 2, 0, 2, 1, 1),
            ]
        ),
        (
            [
                ("on", Brick(0, 2, 0, 2, 0, 2)),
                ("off", Brick(1, 1, 1, 1, 1, 1)),
                ("on", Brick(1, 1, 1, 1, 1, 1)),
            ],
            [
                Brick(0, 2, 0, 2, 0, 2),
            ]
        ),
        (
            [
                ("on", Brick(0, 1, 0, 2, 0, 2)),
                ("on", Brick(1, 2, 0, 2, 0, 2)),
                ("off", Brick(1, 1, 1, 1, 1, 1)),
            ],
            [
                Brick(0, 2, 0, 2, 0, 0),
                Brick(0, 2, 0, 2, 2, 2),
                Brick(0, 2, 0, 0, 1, 1),
                Brick(0, 2, 2, 2, 1, 1),
                Brick(0, 0, 0, 2, 1, 1),
                Brick(2, 2, 0, 2, 1, 1),
            ]
        ),
        (
            [
                ("on", Brick(10, 12, 10, 12, -1000, 1000)),
                ("on", Brick(11, 13, 11, 13, -1000, 1000)),
            ],
            [
                Brick(x_l=11, x_h=13, y_l=11, y_h=13, z_l=-1000, z_h=1000),
                Brick(x_l=10, x_h=12, y_l=10, y_h=12, z_l=-1000, z_h=1000),
            ]
        ),
        (
            [
                ("on", Brick(10, 12, 10, 12, 0, 0)),
                ("on", Brick(11, 13, 11, 13, 0, 0)),
                ("off", Brick(9, 11, 9, 11, 0, 0)),
            ],
            [
                Brick(12, 13, 11, 13, 0, 0),
                Brick(11, 13, 12, 13, 0, 0),
                Brick(10, 10, 12, 12, 0, 0),
                Brick(12, 12, 10, 10, 0, 0),
            ]
        ),
    ],
    ids=[
        "turn-middle-off",
        "turn-middle-off-on",
        "turn-on-on-off",
        "sample3-first-2-lines-2d",
        "sample3-first-3-lines-2d",
    ]
)
def test_instructions(instructions, result):
    assert cuboids(reboot_2(instructions)) == cuboids(result)


@pytest.mark.parametrize(
    argnames=["bs", "result"],
    argvalues=[
        (
            [
                Brick(1, 1, 1, 1, 1, 1),
            ],
            1
        ),
        (
            [
                Brick(0, 2, 0, 2, 0, 2),
            ],
            27
        ),
        (
            [
                Brick(0, 2, 0, 2, 0, 2),
                Brick(2, 4, 2, 4, 2, 4),
            ],
            27 * 2 - 1
        ),
        (
            [
                Brick(0, 2, 0, 2, 0, 2),
                Brick(2, 4, 0, 2, 0, 2),
            ],
            27 * 2 - 9
        ),
        (
            [
                Brick(0, 2, 0, 2, 0, 2),
                Brick(0, 2, 0, 2, 0, 2),
            ],
            27
        ),
        (
            [
                Brick(0, 2, 0, 2, 0, 2),
                Brick(2, 4, 2, 4, 2, 4),
                Brick(-2, 0, -2, 0, -2, 0),
            ],
            27 * 3 - 2
        ),
        (
            [
                Brick(-5, 47, -31, 22, -19, 33),
                Brick(-44, 5, -27, 21, -14, 35),
                Brick(-49, -1, -11, 42, -10, 38),
            ],
            310956
        ),
    ],
    ids=[
        "1x1x1",
        "3x3x3",
        "2x 3x3x3 1 interleaving",
        "2x 3x3x3 face touching",
        "2x 3x3x3 same",
        "3x 3x3x3 1 interleaving",
        "sample2 first 3 lines"
    ]
)
def test_sum_volume(bs, result):
    assert sum_volume(bs) == result


@pytest.mark.parametrize(
    "line_no",
    range(1, 14)
)
def test_sample2(line_no):
    instructions = parse_input("day22/sample2")[:line_no]
    assert sum_volume(
        reboot_2(instructions)
    ) == len(reboot(instructions, limit=None))
