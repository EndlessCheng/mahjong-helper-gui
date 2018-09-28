from utils import count_to_tiles, tiles_to_count


def test_count_to_tiles():
    assert count_to_tiles([]) == ""

    cnt = [0] * 34
    cnt[0] = 1
    cnt[3] = 2
    cnt[13] = 3
    cnt[33] = 2
    assert count_to_tiles(cnt) == "144m 555p 77z"


def test_tiles_to_count():
    assert tiles_to_count("") == []
    assert tiles_to_count("m") == []
    assert tiles_to_count("mm") == []
    assert tiles_to_count("1mm") == []
    assert tiles_to_count("mm1") == []
    assert tiles_to_count("1mm1") == []
    assert tiles_to_count("11111m") == []
    assert tiles_to_count("11m 15p 3") == []
    assert tiles_to_count("11m 15p 9z") == []
    assert tiles_to_count("11m 15p 3a") == []
    assert tiles_to_count("11m1 15p 3a") == []

    tiles = "1123456789m 15p 127z"
    assert tiles_to_count(tiles) == [2, 1, 1, 1, 1, 1, 1, 1, 1,
                                     1, 0, 0, 0, 1, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 1, 0, 0, 0, 0, 1]
