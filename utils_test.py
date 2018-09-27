from utils import count_to_tiles


def test_count_to_tiles():
    cnt = [0] * 34
    cnt[3] = 2
    cnt[13] = 3
    cnt[30] = 2
    print()
    print(count_to_tiles(cnt))
    print(sum(cnt))
