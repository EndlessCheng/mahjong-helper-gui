import requests
import wx
import wx.lib.buttons as buts

from utils import TILES, count_to_tiles

is_interact_mode = False

# TODO: data binding
cnt = [0] * 34


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
            send_tiles(event)

    return on_click


def reset(event):
    global cnt, is_interact_mode
    is_interact_mode = False

    cnt = [0] * 34
    text_ctrl.Clear()
    for b in grid_buttons:
        b.Enabled = True
    panel.Refresh()


def send_tiles(event):
    global is_interact_mode, cnt
    is_interact_mode = True
    if sum(cnt) < 14:
        # 需要摸牌
        for i, b in enumerate(grid_buttons):
            if cnt[i] == 4:
                b.Enabled = False
    else:
        # 需要切牌
        for i, b in enumerate(grid_buttons):
            if cnt[i] > 0:
                b.Enabled = True
    panel.Refresh()

    # ~1s延迟
    resp = requests.post("http://localhost:12121/interact", json={
        "tiles": text_ctrl.GetValue(),
    })
    if resp.status_code != 200:
        print(resp.text)
        return False
    return True


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title='日麻辅助', size=(600, 480))
    panel = wx.Panel(frame)

    text_ctrl = wx.TextCtrl(panel)
    reset_button = wx.Button(panel, label='重置')
    reset_button.Bind(wx.EVT_BUTTON, reset)

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

    empty_label = wx.StaticText(panel, wx.ID_ANY, '')
    grid_sizer.Add(empty_label, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

    send_button = wx.Button(panel, label='发送')
    send_button.Bind(wx.EVT_BUTTON, send_tiles)
    grid_sizer.Add(send_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
    vbox.Add(grid_sizer, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
    panel.SetSizer(vbox)

    frame.Show()
    app.MainLoop()
