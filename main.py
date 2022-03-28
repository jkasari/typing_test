import wx
import random


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
        self.data_list = ['`', '!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=']

        #Creates a prompt character for the user to type in
        self.prompt_text = wx.StaticText(self, label=('C'), pos=(300, 100), size=(100, 100))
        self.prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_ITALIC, weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.prompt_text.SetFont(self.prompt_font)

        #Creates an entry box for the user to type their answer into
        self.entry = wx.TextCtrl(parent=self, id=-1, value="", pos=(310, 250), size=(30, 30))
        self.Bind(wx.EVT_TEXT, self.change_prompt)

    # check to see if the text in the entry matchs that in the prompt
    def change_prompt(self, e):
        if self.prompt_text.GetLabel() == self.entry.GetValue():
            temp = random.choice(self.data_list)
            self.prompt_text.SetLabel(temp)
            self.entry.SetValue('')

if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()

