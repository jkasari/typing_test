from cProfile import label
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
        self.time_limit = 1.5
        self.temp = ''
        self.result = 0

        #Creates a prompt character for the user to type in
        self.prompt_text = wx.StaticText(self, label=(''), pos=(270, 100), size=(100, 100), style=wx.ALIGN_CENTER)
        self.prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.prompt_text.SetFont(self.prompt_font)
        self.refresh_list()

        # create a restart button that appears only when the game is over.
        # Also gives you a final score of how my times you where out of time.
        self.restart_button = wx.Button(self, label='Restart', pos=(285, 370), size=(60, 30), style=wx.ALIGN_CENTRE)
        self.result_text = wx.StaticText(self, label='', pos=(265, 420), size=(100, 50), style=wx.ALIGN_CENTER)
        self.result_text.Hide()
        self.restart_button.Hide()
        self.Bind(wx.EVT_BUTTON, self.restart_game)

        #Creates an entry box for the user to type their answer into
        self.entry = wx.TextCtrl(parent=self, id=-1, value="", pos=(300, 250), size=(30, 30))
        self.Bind(wx.EVT_TEXT, self.change_prompt)



    # check to see if the text in the entry matchs that in the prompt
    def change_prompt(self, e):
        if self.prompt_text.GetLabel() == self.entry.GetValue():
            self.check_time()
            self.update_prompt()

    # Check to see if the time is below the limit. If it is, remove that current prompt from the list
    def check_time(self):
        time_diff = time.time() - self.start
        print(time_diff)
        if time_diff < self.time_limit * len(self.temp):
            temp_char = self.prompt_text.GetLabel()
            print(f"{temp_char} gone!")
            self.data_list.remove(temp_char)
            self.SetBackgroundColour("Green")
        else:
            self.SetBackgroundColour("Red")
            self.result += 1
        self.Refresh()

    # If there is data in the list update the prompt with the next random value from the list
    def update_prompt(self):
        if self.data_list:
            self.temp = random.choice(self.data_list)
            self.prompt_text.SetLabel(self.temp)
            self.start = time.time()
        else:
            self.finish()
        self.entry.SetValue('')

    #Reset the list back the original contents and put the "Go" prompt back up
    def refresh_list(self):
        self.data_list = ['`', '!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', ':', '|', '/', '<', '>', '->', ';', '.', ',']
        #self.data_list = ['a', 'b', 'c', 'd']
        self.prompt_text.SetLabel('Go')
        self.result = 0

    def finish(self):
        self.result_text.SetLabel(self.get_result_string())
        self.restart_button.Show()
        self.result_text.Show()

    def get_result_string(self):
        return f"Your result is: {self.result - 1}"
    
    def restart_game(self, e):
        self.restart_button.Hide()
        self.result_text.Hide()
        self.refresh_list()


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()

