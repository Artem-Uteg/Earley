from grammar import CFG


def read_test(number_of_test):
    first = CFG(f"test_{number_of_test}.txt").get_ans()
    second = open(f"ans_test_{number_of_test}.txt").readlines()
    return first == second


def test_easy_1():
    assert read_test(1)


def test_easy_2():
    assert read_test(2)


def test_easy_3():
    assert read_test(3)


def test_medium_4():
    assert read_test(4)


def test_medium_5():
    assert read_test(5)


def test_medium_6():
    assert read_test(6)


def test_medium_7():
    assert read_test(7)
