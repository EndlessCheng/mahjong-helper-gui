TILES = [
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    "1z", "2z", "3z", "4z", "5z", "6z", "7z",
]


def count_to_tiles(cnt):
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
