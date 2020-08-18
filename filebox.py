from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from files import Files
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
import os


class FileBox(BoxLayout):
    def __init__(self):
        super(FileBox, self).__init__()
        self.orientation = "vertical"
        self.FileList = list()
        self.filelayouts = list()
        Window.bind(on_dropfile=self.on_file_drop)

    def on_file_drop(self, window, filepath):
        if os.path.isfile(filepath) and filepath.lower().endswith(
                (b'.png', b'.jpg', b'.jpeg', b'.tiff', b'.bmp', b'.gif', b'.txt')) and len(self.FileList) <= 5:
            self.FileList.append(Files(filepath))
            self.filelayouts.append(singleFile(self.FileList[-1]))
            self.add_widget(self.filelayouts[-1])
            self.filelayouts[-1].selectbutton.bind(on_press=self.select)
            self.filelayouts[-1].deletebutton.bind(on_press=self.delete)
            self.filelayouts[-1].removebutton.bind(on_press=self.remove)
            self.filelayouts[-1].plusbutton.bind(on_press=self.increase)
            self.filelayouts[-1].minusbutton.bind(on_press=self.decrease)
            self.filelayouts[-1].upbutton.bind(on_press=self.poschange)
            self.filelayouts[-1].downbutton.bind(on_press=self.poschange)
            self.filelayouts[-1].rightbutton.bind(on_press=self.poschange)
            self.filelayouts[-1].leftbutton.bind(on_press=self.poschange)

    def remove(self, e):
        self.FileList[self.filelayouts.index(e.parent)].unselect()

    def select(self, e):
        print("select")
        self.FileList[self.filelayouts.index(e.parent)].select()

    def delete(self, e):
        print("Delete")
        print(self.filelayouts.index(e.parent))
        self.remove_widget(e.parent)
        self.FileList.pop(self.filelayouts.index(e.parent))
        self.filelayouts.remove(e.parent)

    def increase(self, e):
        self.FileList[self.filelayouts.index(e.parent.parent)].size_increase()

    def decrease(self, e):
        self.FileList[self.filelayouts.index(e.parent.parent)].size_decrease()

    def poschange(self, e):
        obj = self.FileList[self.filelayouts.index(e.parent.parent)]
        if e.id == "up":
            obj.up()
        if e.id == "down":
            obj.down()
        if e.id == "right":
            obj.right()
        if e.id == "left":
            obj.left()


class singleFile(BoxLayout):
    def __init__(self, file):
        super(singleFile, self).__init__()
        self.scalelayout = BoxLayout(orientation="vertical", pos_hint={"top": 1}, size_hint_y=None)
        self.poslayout = RelativeLayout(pos_hint={"top": 1}, size_hint_y=None)
        self.orientation = "horizontal"
        self.name = file.get_name()
        self.deletebutton = Button(text="Delete", size_hint_y=None, pos_hint={"top": 1},
                                   background_color=(255, 0, 0, 1))
        self.selectbutton = Button(text="Select", size_hint_y=None, pos_hint={"top": 1},
                                   background_color=(0, 255, 0, 1))
        self.removebutton = Button(text="Remove", size_hint_y=None, pos_hint={"top": 1},
                                   background_color=(0, 0, 255, 1))
        self.plusbutton = Button(text="+", background_color=(0, 0, 255, 1))
        self.minusbutton = Button(text="-", background_color=(0, 0, 255, 1))
        self.upbutton = Button(text="/\\", background_color=(0, 0, 0, 1), pos_hint={'x': 0.3, 'y': 0.5},
                               size_hint=(None, None), size=(50, 50), id="up")
        self.downbutton = Button(text="\\/", background_color=(0, 0, 0, 1), pos_hint={'x': 0.3, 'y': 0.1},
                                 size_hint=(None, None), size=(50, 50), id="down")
        self.rightbutton = Button(text=">", background_color=(0, 0, 0, 1), pos_hint={'x': 0.6, 'y': 0.4},
                                  size_hint=(None, None), size=(50, 50), id="right")
        self.leftbutton = Button(text="<", background_color=(0, 0, 0, 1), pos_hint={'x': 0, 'y': 0.4},
                                 size_hint=(None, None), size=(50, 50), id="left")
        self.poslayout.add_widget(self.upbutton)
        self.poslayout.add_widget(self.downbutton)
        self.poslayout.add_widget(self.leftbutton)
        self.poslayout.add_widget(self.rightbutton)

        self.scalelayout.add_widget(self.plusbutton)
        self.scalelayout.add_widget(self.minusbutton)

        if file.file_type == 1:
            self.add_widget(Label(text=self.name, size_hint_y=None, pos_hint={"top": 1}))
        elif file.file_type == 0:
            self.add_widget(Image(source=file.get_file_path(), size_hint_y=None, pos_hint={"top": 1}))

        self.add_widget(self.selectbutton)
        self.add_widget(self.deletebutton)
        self.add_widget(self.removebutton)
        self.add_widget(self.scalelayout)
        self.add_widget(self.poslayout)
