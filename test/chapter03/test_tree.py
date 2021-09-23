from chapter03.tree import Branch, Leaf, size, maximum, depth, map, fold, sizeViaFold, maximumViaFold, depthViaFold, \
    mapViaFold

tree = Branch(Branch(Leaf(1), Leaf(2)), Leaf(3))


def test_size() -> None:
    assert size(tree) == 5


def test_maximum() -> None:
    assert maximum(tree) == 3


def test_depth() -> None:
    assert depth(tree) == 2


def test_map() -> None:
    assert map(tree, str) == Branch(Branch(Leaf('1'), Leaf('2')), Leaf('3'))

def test_fold() -> None:
    assert fold(tree, str, (lambda a, b: a + b)) == '123'

def test_size_via_fold() -> None:
    assert sizeViaFold(tree) == 5

def test_maximum_via_fold() -> None:
    assert maximumViaFold(tree) == 3

def test_depth_via_fold() -> None:
    assert depthViaFold(tree) == 2

def test_map_via_fold() -> None:
    assert mapViaFold(tree, str) == Branch(Branch(Leaf('1'), Leaf('2')), Leaf('3'))