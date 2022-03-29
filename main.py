import wx
import random
import time

class TestApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        self.InitFrame()

    def InitFrame(self):
        frame = MainFrame(parent=None, title="Main Frame", pos=(100, 100), size=(640, 640))
        frame.Show()


class MainFrame(wx.Frame):
    def __init__ (self, parent, title, pos, size):
        super().__init__(parent=parent, title=title, pos=pos, size=size)
        self.init_panel()

    def init_panel(self):
        self.func_panel = FuncPanel(self)




class FuncPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.SetBackgroundColour("Grey")
        self.data_list = []
        self.start = time.time()
        self.time_limit = 2.0

        #Creates a prompt character for the user to type in
        self.prompt_text = wx.StaticText(self, label=(''), pos=(300, 100), size=(100, 100))
        self.prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_ITALIC, weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.prompt_text.SetFont(self.prompt_font)
        self.refresh_list()

        #Creates an entry box for the user to type their answer into
        self.entry = wx.TextCtrl(parent=self, id=-1, value="", pos=(310, 250), size=(30, 30))
        self.Bind(wx.EVT_TEXT, self.change_prompt)
        time.sleep(self.time_limit)


    # check to see if the text in the entry matchs that in the prompt
    def change_prompt(self, e):
        if self.prompt_text.GetLabel() == self.entry.GetValue():
            self.check_time()
            self.update_prompt()

    def check_time(self):
        time_diff = time.time() - self.start
        print(time_diff)
        if time_diff < self.time_limit:
            temp_char = self.prompt_text.GetLabel()
            print(f"{temp_char} gone!")
            self.data_list.remove(temp_char)

    def update_prompt(self):
        if self.data_list:
            temp = random.choice(self.data_list)
            self.prompt_text.SetLabel(temp)
            self.start = time.time()
        else:
            self.refresh_list()
        self.entry.SetValue('')

    def refresh_list(self):
        self.data_list = ['`', '!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=']
        #self.data_list = ['a', 'b', 'c', 'd']
        self.prompt_text.SetLabel('Go')


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()

