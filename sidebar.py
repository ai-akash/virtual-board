from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class SideBar(BoxLayout):
    def __init__(self):
        super(SideBar, self).__init__()

        self.orientation = "vertical"
        self.size_hint_max_x = 60
        self.setting_button = Button(background_normal = "icons/settings.png",id ="setting",size_hint_max_y=60 )
        self.file_button = Button(background_normal = "icons/file.png",id ="file",size_hint_max_y=60 )
        self.clear_button = Button(background_normal = "icons/trash.png",id ="clear",size_hint_max_y=60 )
        self.pencil_button = Button(background_normal = "icons/pencil.png",id ="pencil",size_hint_max_y=60 )
        self.mode_button = Button(background_normal = "icons/editcopy.png",id ="mode",size_hint_max_y=60 )
        self.add_widget(self.setting_button)
        self.add_widget(self.file_button)
        self.add_widget(self.clear_button)
        self.add_widget(self.pencil_button)
        # self.add_widget(Button(background_normal="icons/files.png", id="file_add", size_hint_max_y=70))
