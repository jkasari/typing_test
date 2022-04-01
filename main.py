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
        self.prompt = 'Go'
        self.run = False
        self.round = 0

        #Creates a prompt character for the user to type in
        self.prompt_text = wx.StaticText(self, label=(self.prompt), pos=(270, 100), size=(100, 100), style=wx.ALIGN_CENTER)
        self.prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.prompt_text.SetFont(self.prompt_font)
        self.refresh_list()

        # create a restart button that appears only when the game is over.
        # Also gives you a final score of how my times you where out of time.
        self.restart_button = wx.Button(self, label='', pos=(270, 370), size=(90, 30))
        self.result_text = wx.StaticText(self, label='', pos=(265, 420), size=(100, 50), style=wx.ALIGN_CENTER)
        self.result_text.Hide()
        self.restart_button.Hide()
        self.Bind(wx.EVT_BUTTON, self.start_round)

        #Creates an entry box for the user to type their answer into
        self.entry = wx.TextCtrl(parent=self, id=-1, value="", pos=(300, 250), size=(30, 30))
        self.Bind(wx.EVT_TEXT, self.change_prompt)
        
        self.restart()


    # check to see if the text in the entry matchs that in the prompt
    def change_prompt(self, e):
        if self.run:
            if self.prompt == self.entry.GetValue():
                if self.entry.GetValue() == 'Go':
                    self.update_prompt()
                else:
                    self.check_time()
                    self.update_prompt()
        else:
            pass   
            

    # Check to see if the time is below the limit. If it is, remove that current prompt from the list
    def check_time(self):
        time_diff = time.time() - self.start
        print(time_diff)
        if self.round == 1:
            self.check_time_round1(time_diff)
        elif self.round == 2:
            self.check_time_round2(time_diff)
        

    def check_time_round2(self, time_diff: int):
        if time_diff < self.time_limit * len(self.prompt):
            print(f"{self.prompt} gone!")
            self.data_list.remove(self.prompt)
            self.SetBackgroundColour("Green")
        else:
            self.SetBackgroundColour("Red")
            self.result += 1
        self.Refresh()


    def check_time_round1(self, time_diff):
        self.data_dict[str(self.prompt)] = time_diff
        self.data_list.remove(self.prompt)


    # If there is data in the list update the prompt with the next random value from the list
    def update_prompt(self):
        if self.data_list:
            self.prompt = random.choice(self.data_list)
            self.prompt_text.SetLabel(self.prompt)
            self.start = time.time()
        else:
            self.restart()
        self.entry.SetValue('')


    #Reset the list back the original contents and put the "Go" prompt back up
    def refresh_list(self):
        self.data_list = ['`', '!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', ':', '|', '/', '<', '>', ';', '.', ',', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        #self.data_list = ['a', 'b', 'c', 'd']
        self.data_dict = {}
        self.init_dict()
        self.result = 0
    
    def calibrate_list(self):
        big_list = []
        count = 0
        for i in self.data_dict:
            for _ in range(int(self.data_dict[i] * 4)):
                big_list.append(i)
        random.shuffle(big_list)
        for j in big_list:
            count += 1
            if count % 4 == 0:
                temp_str = ''.join(big_list[count-4: count])
                self.data_list.append(temp_str)
                print(''.join(big_list[count - 4: count]))
                #self.data_list.append("butts")
            

    def restart(self):
        self.round += 1
        if self.round == 2:
            self.result_text.SetLabel(self.get_result_string())
        if self.round < 3:
            self.restart_button.SetLabel(f'Start Round {self.round}')
        else: 
            self.restart_button.SetLabel('Restart')
            self.round = 1
        self.restart_button.Show()
        self.result_text.Show()
        self.run = False

    def get_result_string(self):
        return f"Your result is: {self.result}"

    # This resets the game back to its original starting position. 
    def start_round(self, e):
        self.prompt = 'Go'
        self.run = True
        self.prompt_text.SetLabel(self.prompt)
        self.restart_button.Hide()
        self.result_text.Hide()
        if self.round == 1:
            self.refresh_list()
        elif self.round == 2:
            self.calibrate_list()

    def init_dict(self):
        for i in self.data_list:
            self.data_dict[i] = 0


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()

