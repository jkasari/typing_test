from cProfile import label
from click import style
import wx
import random
import time

class TestApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        self.InitFrame()

    def InitFrame(self):
        frame = MainFrame(parent=None, title="Main Frame", pos=(100, 100), size=(500, 350))
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
        self.time_limit = 1
        self.temp = ''
        self.result = 0
        self.start_prompt = 'Go'
        self.prompt = self.start_prompt
        self.run = False
        self.round = 2
        self.instruct_text = '' 

        self.init_prompt_text()
        self.init_restart_button()
        self.init_entry_field()
        self.init_result_text()
        #self.init_startup()
        self.init_vertical_sizer()

        self.refresh_list()
        self.restart()

    def init_sizers(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)


    #Creates a prompt character for the user to type in
    def init_prompt_text(self):
        self.prompt_text = wx.StaticText(self, label=self.prompt, style=wx.ALIGN_CENTER)
        prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.prompt_text.SetFont(prompt_font)
        #self.prompt_text.Hide()

    # Creates a vertical sizer and attaches most everything to it
    def init_vertical_sizer(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.result_text, 0, wx.ALIGN_CENTER)
        vbox.Add(0, 50, 0)
        vbox.Add(self.prompt_text, 0, wx.ALIGN_CENTER)
        vbox.Add(0, 70, 0)
        vbox.Add(self.entry, 0, wx.ALIGN_CENTER)
        vbox.Add(self.restart_button, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)



    # create a restart button that appears only when the game is over.
    # Also gives you a final score of how my times you where out of time.
    def init_restart_button(self):
        self.restart_button = wx.Button(self, label='', pos=(270, 370), size=(90, 30))
        self.Bind(wx.EVT_BUTTON, self.start_round)
        self.restart_button.Hide()


    #Creates an entry box for the user to type their answer into
    def init_entry_field(self):
        self.entry = wx.TextCtrl(parent=self, id=-1, value="", size=(60, 30), style=wx.TE_CENTER)
        self.Bind(wx.EVT_TEXT, self.read_entry)
        self.entry.Hide()

    def init_result_text(self):
        self.result_text = wx.StaticText(self, label='', style=wx.ALIGN_CENTER)
        result_font = wx.Font(pointSize= 30, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL, underline=True, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.result_text.SetFont(result_font)
        self.result_text.Hide()

    def create_instuction_text(self):
        self.instruct_text = ("Welcome to the typing test!   Please enter in the text box what ever is listed in the prompt field. 'Go' will always be the first prompt and is not tracked. Round one will measure your response time for each symbol. Round two will generate ten combos. The time you have to enter the combos is your average response time from round one.")

    def init_startup(self):
        self.create_instuction_text()
        self.instructions = wx.StaticText(self, label=self.instruct_text, pos=(240, 100), size=(200, 500))

    # check to see if the text in the entry matchs that in the prompt
    def read_entry(self, e):
        if self.run:
            if self.prompt == self.entry.GetValue():
                if self.entry.GetValue() == self.start_prompt:
                    self.update_prompt()
                else:
                    self.check_time()
                    self.update_prompt()
        else:
            pass   
        
    def color_chars(self):
        pass
            

    # Check to see if the time is below the limit. If it is, remove that current prompt from the list
    def check_time(self):
        time_diff = time.time() - self.start
        print(time_diff)
        if self.round == 1:
            self.check_time_round1(time_diff)
        elif self.round == 2:
            self.check_time_round2(time_diff)
        
    # Keeps track of if you beat the time limit
    def check_time_round2(self, time_diff: int):
        self.data_dict[str(self.prompt)] = time_diff
        if time_diff < self.time_limit * len(self.prompt):
            print(f"{self.prompt} gone!")
            self.data_list.remove(self.prompt)
            self.SetBackgroundColour("Green")
        else:
            self.SetBackgroundColour("Red")
        self.Refresh()

    # Records your response time in the first round
    def check_time_round1(self, time_diff: int):
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
        self.Layout()
        self.entry.SetValue('')


    #Reset the list back the original contents and put the "Go" prompt back up
    def refresh_list(self):
        self.data_list = ['~', '`', '!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', ':', '|', '/', '<', '>', ';', '.', ',', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        #self.data_list = ['a', 'f']
        self.data_dict = {}
        self.init_dict()
        self.result = 0
    
    def calibrate_list(self):
        big_list = []
        for i in self.data_dict:
            for _ in range(int(self.data_dict[i] * 4)):
                big_list.append(i)
        self.result = self.get_round_time()
        self.time_limit =  self.result / len(self.data_dict)
        print('Time!!!   :   ', self.time_limit)
        random.shuffle(big_list)
        for j in range(10):
            rand = random.randint(3, 6)
            temp_str = ''.join(big_list[0: rand])
            print(temp_str)
            self.data_list.append(temp_str)
            self.data_dict[temp_str] = 0
            random.shuffle(big_list)

    def get_round_time(self):
        count = 0
        for i in self.data_dict:
            count += self.data_dict[i]
            self.data_dict[i] = 0
        return count
    

    # Gives the user the restart button and displays there score if not the first round
    def restart(self):
        self.round += 1
        if self.round < 3:
            self.restart_button.SetLabel(f'Start Round {self.round}')
            if self.round == 2:
                self.calibrate_list()
        elif self.round == 3:
            self.result += self.get_round_time()
            self.result_text.SetLabel(self.get_result_string())
            print(self.result)
            self.prompt_text.Hide()
            self.result_text.Show()
            self.round = 1
            self.restart_button.SetLabel('Restart')
            self.result = 0
            self.refresh_list()
        self.restart_button.Show()
        self.entry.Hide()
        self.run = False

    def get_result_string(self):
        return f"Your result is: {int(self.result)}"

    # This resets the game back to its original starting position. 
    def start_round(self, e):
        # Hide all the restart stuff
        #self.instructions.Hide()
        self.restart_button.Hide()
        self.result_text.Hide()
        # Show all the run time stuff
        self.entry.Show()
        self.prompt_text.Show()
        self.prompt = self.start_prompt
        self.prompt_text.SetLabel(self.prompt)
        self.Layout()
        self.run = True

    def init_dict(self):
        for i in self.data_list:
            self.data_dict[i] = 0


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()

