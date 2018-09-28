import requests
import wx
import wx.lib.buttons as buts

from utils import TILES, count_to_tiles, tiles_to_count

is_interact_mode = False

# TODO: data binding
cnt = [0] * len(TILES)


def tile_on_click_func(tile_index):
    def on_click(event):
        global is_interact_mode, cnt

        if sum(cnt) > 14:
            return

        if not is_interact_mode:
            if cnt[tile_index] == 4:
                return
            cnt[tile_index] += 1
            text_ctrl.SetValue(count_to_tiles(cnt))
            if cnt[tile_index] == 4:
                grid_buttons[tile_index].Disable()
            if sum(cnt) == 14:
                for b in grid_buttons:
                    b.Enabled = False
                panel.Refresh()
        else:
            if sum(cnt) < 14:
                # 摸牌
                if cnt[tile_index] == 4:
                    return
                cnt[tile_index] += 1
                text_ctrl.SetValue(count_to_tiles(cnt))
            else:
                # 切牌
                if cnt[tile_index] == 0:
                    return
                cnt[tile_index] -= 1
                text_ctrl.SetValue(count_to_tiles(cnt))
            send_tiles_func(True, False)(event)

    return on_click


def reset_on_click(event):
    global cnt, is_interact_mode
    is_interact_mode = False

    cnt = [0] * len(TILES)
    text_ctrl.Clear()
    for b in grid_buttons:
        b.Enabled = True
    panel.Refresh()


def send_tiles_func(need_interact, reset):
    def send_tiles(event):
        global is_interact_mode, cnt

        tiles = text_ctrl.GetValue()
        _cnt = tiles_to_count(tiles)
        if not _cnt:
            return False
        cnt = _cnt

        try:
            # ~1s延迟
            # TODO: waiting circle
            resp = requests.post("http://localhost:12121/interact", json={
                "reset": reset,
                "tiles": tiles,
                "show_detail": sum(cnt) == 13,
            })
        except ConnectionRefusedError as e:
            print("未连接上服务器", e)
            return False
        except Exception as e:
            print(e)
            return False
        if resp.status_code != 200:
            print(resp.text)
            return False

        if need_interact:
            is_interact_mode = True
            if sum(cnt) < 14:
                # 需要摸牌
                for i, b in enumerate(grid_buttons):
                    b.Enabled = cnt[i] < 4
            else:
                # 需要切牌
                for i, b in enumerate(grid_buttons):
                    b.Enabled = cnt[i] > 0
            panel.Refresh()

        return True

    return send_tiles


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title='日麻辅助', size=(600, 480))
    panel = wx.Panel(frame)

    # TODO: 撤销按钮

    text_ctrl = wx.TextCtrl(panel)
    reset_button = wx.Button(panel, label='重置')
    reset_button.Bind(wx.EVT_BUTTON, reset_on_click)

    hbox = wx.BoxSizer()
    hbox.Add(text_ctrl, proportion=3, flag=wx.EXPAND)
    hbox.Add(reset_button, proportion=1, flag=wx.EXPAND, border=5)

    grid_sizer = wx.GridSizer(4, 9, 4, 4)

    grid_buttons = []
    for index, tile in enumerate(TILES):
        path = f'img/{tile}.png'
        button = buts.GenBitmapTextButton(panel, -1, bitmap=wx.Bitmap(path))
        button.Bind(wx.EVT_BUTTON, tile_on_click_func(index))
        grid_sizer.Add(button, proportion=1, flag=wx.EXPAND, border=5)
        grid_buttons.append(button)

    analysis_button = wx.Button(panel, label='分析')
    analysis_button.Bind(wx.EVT_BUTTON, send_tiles_func(False, True))
    grid_sizer.Add(analysis_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

    interact_button = wx.Button(panel, label='交互\n分析')
    interact_button.Bind(wx.EVT_BUTTON, send_tiles_func(True, True))
    grid_sizer.Add(interact_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
    vbox.Add(grid_sizer, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
    panel.SetSizer(vbox)

    frame.Show()
    app.MainLoop()
