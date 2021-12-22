import pytest

from .day22 import Brick, reboot_2, sum_volume


@pytest.mark.parametrize(
    argnames=["b1", "b2", "result"],
    argvalues=[
        (Brick(0, 1, 0, 1, 0, 1), Brick(100, 101, 100, 101, 100, 101), None),
        (Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(0, 1, 0, 1, 0, 1), Brick(-1, 2, -1, 2, -1, 2), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(-1, 2, -1, 2, -1, 2), Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1)),
        (Brick(0, 10, 0, 1, 0, 1), Brick(-10, 0, 0, 1, 0, 1), Brick(0, 0, 0, 1, 0, 1)),
        (Brick(10, 11, 10, 11, 0, 0), Brick(
            11, 12, 11, 12, 0, 0), Brick(11, 11, 11, 11, 0, 0))
    ],
    ids=[
        "no-intersect",
        "intersect-self",
        "superset",
        "subset",
        "x-face-touches",
        "asd",
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
            Brick(0, 2, 0, 0, 0, 0),
            Brick(0, 2, 2, 2, 0, 0),
            Brick(0, 0, 0, 2, 0, 0),
            Brick(2, 2, 0, 2, 0, 0),
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
    diff = set(b1 - b2)
    assert cuboids(diff) == cuboids(result)


@pytest.mark.parametrize(
    argnames=["b1", "b2", "result"],
    argvalues=[
        (Brick(0, 1, 0, 1, 0, 1), Brick(100, 101, 100, 101, 100, 101), set([
            Brick(0, 1, 0, 1, 0, 1),
            Brick(100, 101, 100, 101, 100, 101),
        ])),
        (Brick(0, 1, 0, 1, 0, 1), Brick(0, 1, 0, 1, 0, 1),
         set([Brick(0, 1, 0, 1, 0, 1)])),
        (Brick(0, 2, 0, 2, 0, 2), Brick(1, 1, 1, 1, 1, 1), set([
            Brick(0, 2, 0, 2, 0, 2),
        ])),
        (Brick(1, 1, 1, 1, 1, 1), Brick(0, 2, 0, 2, 0, 2), set([
            Brick(0, 2, 0, 2, 0, 2),
        ])),
        (Brick(0, 100, 0, 1, 0, 1), Brick(-100, 0, 0, 1, 0, 1), set([
            Brick(x_l=-100, x_h=-1, y_l=0, y_h=1, z_l=0, z_h=1),
            Brick(x_l=0, x_h=0, y_l=0, y_h=1, z_l=0, z_h=1),
            Brick(x_l=1, x_h=100, y_l=0, y_h=1, z_l=0, z_h=1),
        ])),
    ],
    ids=[
        "no-intersect",
        "intersect-self",
        "subset",
        "superset",
        "x-face-touches",
    ]
)
def test_add(b1, b2, result):
    assert set(b1 + b2) == result


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
            set([
                Brick(0, 2, 0, 2, 0, 0),
                Brick(0, 2, 0, 2, 2, 2),
                Brick(0, 2, 0, 0, 1, 1),
                Brick(0, 2, 2, 2, 1, 1),
                Brick(0, 0, 0, 2, 1, 1),
                Brick(2, 2, 0, 2, 1, 1),
            ])
        ),
        (
            [
                ("on", Brick(0, 2, 0, 2, 0, 2)),
                ("off", Brick(1, 1, 1, 1, 1, 1)),
                ("on", Brick(1, 1, 1, 1, 1, 1)),
            ],
            set([
                Brick(0, 2, 0, 2, 0, 2),
            ])
        ),
        (
            [
                ("on", Brick(0, 1, 0, 2, 0, 2)),
                ("on", Brick(1, 2, 0, 2, 0, 2)),
                ("off", Brick(1, 1, 1, 1, 1, 1)),
            ],
            set([
                Brick(0, 2, 0, 2, 0, 0),
                Brick(0, 2, 0, 2, 2, 2),
                Brick(0, 2, 0, 0, 1, 1),
                Brick(0, 2, 2, 2, 1, 1),
                Brick(0, 0, 0, 2, 1, 1),
                Brick(2, 2, 0, 2, 1, 1),
            ])
        ),
        (
            [
                ("on", Brick(10, 12, 10, 12, -1000, 1000)),
                ("on", Brick(11, 13, 11, 13, -1000, 1000)),
            ],
            set([
                Brick(x_l=11, x_h=13, y_l=11, y_h=13, z_l=-1000, z_h=1000),
                Brick(x_l=10, x_h=12, y_l=10, y_h=12, z_l=-1000, z_h=1000),
            ])
        ),
        (
            [
                ("on", Brick(10, 12, 10, 12, 0, 0)),
                ("on", Brick(11, 13, 11, 13, 0, 0)),
                ("off", Brick(9, 11, 9, 11, 0, 0)),
            ],
            set([
                Brick(12, 13, 11, 13, 0, 0),
                Brick(11, 13, 12, 13, 0, 0),
                Brick(10, 10, 12, 12, 0, 0),
                Brick(12, 12, 10, 10, 0, 0),
            ])
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
    ],
    ids=[
        "1x1x1",
        "3x3x3",
        "2x 3x3x3 1 interleaving",
        "2x 3x3x3 face touching",
        "2x 3x3x3 same",
    ]
)
def test_sum_volume(bs, result):
    assert sum_volume(bs) == result