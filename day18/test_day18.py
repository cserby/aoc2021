import pytest

from .day18 import (add_carry_to_the_leftmost, add_carry_to_the_rightmost,
                    add_snailfish_num, explode, magnitude, parse_input,
                    parse_snailfish_num, split, sum_snailfish_num)


def test_parse():
    assert parse_snailfish_num("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]") == ((((1, 3), (5, 3)), ((1, 3), (8, 7))), (((4, 9), (6, 9)), ((8, 2), (7, 3))))

def test_add():
    assert add_snailfish_num(parse_snailfish_num("[1,2]"), parse_snailfish_num("[[3,4],5]")) == ((1, 2), ((3, 4), 5))

def test_split_10():
    assert split(parse_snailfish_num("10")) == (5, 5)

def test_split_11():
    assert split(parse_snailfish_num("11")) == (5, 6)

def test_split_12():
    assert split(parse_snailfish_num("12")) == (6, 6)

@pytest.mark.parametrize(
    argnames=["start", "result"],
    argvalues=[
        [ "[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]" ],
        [ "[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]" ],
        [ "[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]" ],
        [ "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]" ],
        [ "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]" ],
        [ "[[3,[2,[1,[7,3]]]],6]", "[[3,[2,[8,0]]],9]"]
    ],
)
def test_explode(start, result):
    assert explode(parse_snailfish_num(start)) == parse_snailfish_num(result)

def test_add_carry_to_the_leftmost():
    assert add_carry_to_the_leftmost((1, (2, 3)), 1) == (2, (2, 3))

def test_add_carry_to_the_rightmost():
    assert add_carry_to_the_rightmost((1, (2, 3)), 1) == (1, (2, 4))

def test_sum():
    assert sum_snailfish_num(parse_input("day18/sample")) == parse_snailfish_num("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

@pytest.mark.parametrize(
    argnames=["start", "result"],
    argvalues=[
        [ "[[1,2],[[3,4],5]]", 143 ],
        [ "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384 ],
        [ "[[[[1,1],[2,2]],[3,3]],[4,4]]", 445 ],
        [ "[[[[3,0],[5,3]],[4,4]],[5,5]]", 791 ],
        [ "[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137 ],
        [ "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488 ]
    ],
)
def test_magnitude(start, result):
    assert magnitude(parse_snailfish_num(start)) == result