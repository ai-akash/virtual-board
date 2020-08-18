import time
import numpy as np
import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.slider import Slider
from kivy.config import Config
import pickle
import os


class ColorPicker(App):
    def __init__(self):
        App.__init__(self)
        self.range =None
        print("load pkl")
        try:
            if os.path.isfile("range.pkl"):
                with open('range.pkl', 'rb') as f:
                    self.range = pickle.load(f)
        except:
            pass
    def build(self):
        Config.set('graphics', 'window_state', 'maximized')
        sv = ScreenManager()


        self.main_img = Image(size_hint_y=None,height = 500)
        self.result_img = Image()
        self.confirm_btn = Button(text= "Confirm")
        self.previous_data_button = Button(text = "Load Previous Value")
        self.scrollbars = [Slider() for x in range(6)]
        if self.range ==None:
            self.previous_data_button.text = "No previous data"
        else:
            self.previous_data_button.bind(on_press =self.loadData)
        for i,x in enumerate(self.scrollbars):
            if i == 0 or i == 1:
                x.max = 179
            else:
                x.max = 255
            x.min = 0
            if i %2 == 0:
                x.value = x.min
            else:
                x.value = x.max
        self.confirm_btn.bind(on_press = self.getValue)
        self.layout = BoxLayout(orientation='vertical', spacing=250)
        self.bottom = BoxLayout()
        self.camerarow = GridLayout(rows=1, cols=2)
        self.bottomrow = BoxLayout()
        self.sliderrow = GridLayout(rows = 4 ,cols= 2)
        self.layout.add_widget(self.camerarow)
        self.layout.add_widget(self.bottomrow)
        self.bottomrow.add_widget(self.sliderrow)
        self.bottomrow.add_widget(self.previous_data_button)
        self.camerarow.add_widget(self.main_img)
        self.camerarow.add_widget(self.result_img)
        for x in self.scrollbars:
            self.sliderrow.add_widget(x)
        self.sliderrow.add_widget(self.confirm_btn)
        self.capture = cv2.VideoCapture(0)
        # self.capture = cv2.VideoCapture("http://100.88.169.251:8080/videofeed")

        Clock.schedule_interval(self.update, 1.0 / 33.0)
        return self.layout

    def getValue(self,e):
        vals = [int(x.value) for x in self.scrollbars]
        val = [[x  for i,x in enumerate(vals) if i % 2==0],[x for i,x in enumerate(vals)if i % 2 != 0]]
        with open('range.pkl', 'wb') as f:
            pickle.dump(val, f)
    def loadData(self,e):
        self.scrollbars[0].value = self.range[0][0]
        self.scrollbars[1].value = self.range[1][0]
        self.scrollbars[2].value = self.range[0][1]
        self.scrollbars[3].value = self.range[1][1]
        self.scrollbars[4].value = self.range[0][2]
        self.scrollbars[5].value = self.range[1][2]


    def update(self,dt):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame, 0)
        vals = [x.value for x in self.scrollbars]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_range = np.array([x  for i,x in enumerate(vals) if i % 2==0],dtype=np.int32)
        upper_range = np.array([x for i,x in enumerate(vals)if i % 2 != 0],dtype=np.int32)
        mask = cv2.inRange(hsv, lower_range, upper_range)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        buf1 = frame.tostring()
        buf2 = res.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        texture2 = Texture.create(size=(res.shape[1], res.shape[0]), colorfmt='bgr')
        texture2.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')
        self.main_img.texture = texture1
        self.result_img.texture = texture2




if __name__ == '__main__':
    ColorPicker().run()