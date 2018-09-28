TILES = [
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    "1z", "2z", "3z", "4z", "5z", "6z", "7z",
]


def count_to_tiles(cnt):
    if len(cnt) != len(TILES):
        print("cnt 长度必须为", len(TILES))
        return ""

    tiles = ""
    for i, type_ in enumerate(['m', 'p', 's', 'z']):
        wrote = False
        for j in range(9):
            idx = 9 * i + j
            if idx >= len(TILES):
                break
            for k in range(cnt[idx]):
                tiles += str(j + 1)
                wrote = True
        if wrote:
            tiles += type_ + " "
    return tiles.strip()


def tiles_to_count(tiles):
    tiles = tiles.strip()
    if tiles == "":
        print("参数错误: 处理的手牌不能为空")
        return []

    cnt = [0] * len(TILES)

    for split in tiles.split():
        split = split.strip()
        if len(split) <= 1:
            print("参数错误:", split)
            return []
        for c in split[:-1]:
            tile = c + split[-1]
            try:
                index = TILES.index(tile)
            except ValueError:
                print("参数错误:", tile)
                return []
            cnt[index] += 1
            if cnt[index] > 4:
                print("参数错误: 超过4张一样的牌")
                return []

    return cnt
