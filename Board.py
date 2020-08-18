import numpy as np
import cv2
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.config import Config
import os
import pickle
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import imutils
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from datetime import datetime
from kivy.uix.popup import Popup
from filebox import FileBox
from audio import recorder
from sidebar import SideBar


class Board(App):
    def __init__(self):
        super(Board, self).__init__()
        Window.bind(on_key_down=self.on_keyboard_down)
        self.sidebar = SideBar()
        self.bindsidebarbutton()
        self.x1 = self.y1 = 0
        self.mode = 0  # 0 for camera and 1 for whiteboard
        self.draw = False
        self.erase = False
        self.canvas = None
        self.whiteboard = None
        self.overlaypen = None
        self.color = (255, 100, 145)
        self.record = False
        self.files = list()
        self.filebox = FileBox()
        self.popup = Popup(title='Files',
                           title_size=40,
                           title_color=(0, 0, 0, 1),
                           content=self.filebox,
                           background_color=(255, 3, 214, 0.1), background="water.png")

    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        print(keycode, ord(" "))
        print(text)
        if text == "m":
            if self.mode == 0:
                self.mode = 1
            else:
                self.mode = 0
        if text == "c":
            self.canvas = None

        if text == " ":

            if self.draw == True:
                self.draw = False
            else:
                self.erase = False
                self.draw = True
        if text == "e":
            if self.erase == True:
                self.erase = False
                self.draw = False
            else:
                self.erase = True
                self.draw = False

        if text == "r":
            if self.record == False:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.recorder = cv2.VideoWriter('{}.avi'.format(str(datetime.timestamp(datetime.today()))), fourcc, 6.0,
                                                (1280, 720))
                self.audiorecorder = recorder()
                self.record = True
            elif self.record == True:
                self.record = False
                self.recorder.release()
                self.audiorecorder.done()

        if text == "f":
            self.popup.open()

    def bindsidebarbutton(self):
        self.sidebar.pencil_button.bind(on_press=self.btn_click)
        self.sidebar.setting_button.bind(on_press=self.btn_click)
        self.sidebar.file_button.bind(on_press=self.btn_click)
        self.sidebar.clear_button.bind(on_press=self.btn_click)
        self.sidebar.mode_button.bind(on_press=self.btn_click)

    def btn_click(self, e):
        if e.id == "mode":
            if self.mode == 0:
                self.mode = 1
            else:
                self.mode = 0
        if e.id == "pencil":
            if self.draw == True:
                self.draw = False
            else:
                self.erase = False
                self.draw = True
        if e.id == "clear":
            self.canvas = None

        if e.id == "file":
            self.popup.open()

    def build(self):
        Config.set('graphics', 'window_state', 'maximized')
        try:
            if os.path.isfile("range.pkl"):
                with open('range.pkl', 'rb') as f:
                    self.range = pickle.load(f)
            else:
                quit()
        except:
            quit()
        self.img = Image()
        layout = BoxLayout()
        layout.add_widget(self.img)
        layout.add_widget(self.sidebar)
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # self.capture = cv2.VideoCapture("http://100.88.169.251:8080/videofeed")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        Clock.schedule_interval(self.update, 1.0 / 33.0)
        return layout

    def addfiles(self):
        for x in self.filebox.FileList:
            if x.file_type == 1 and x.selected:
                text = x.get_file_data()
                y0, dy = x.y, int(40 * x.font_size)
                for i, line in enumerate(text.split('\n')):
                    y = y0 + i * dy
                    cv2.putText(self.frame, line, (x.x, y), cv2.FONT_HERSHEY_SIMPLEX, x.font_size, (255, 0, 0), 2)
                    cv2.putText(self.whiteboard, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, x.font_size, (255, 0, 0), 2)
            if x.file_type == 0 and x.selected:
                f = x.get_file_data()
                height, width, _ = f.shape
                self.frame[x.y: height + x.y, x.x: width + x.x] = f
                self.whiteboard[x.y: height + x.y, x.x: width + x.x] = f

    def update(self, dt):
        ret, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)

        blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lower_range = np.array(self.range[0], dtype=np.int32)
        upper_range = np.array(self.range[1], dtype=np.int32)
        if self.canvas is None:
            self.canvas = np.zeros_like(self.frame)
        overlaypen = np.zeros_like(self.frame)
        # if self.whiteboard is None:
        self.whiteboard = np.zeros_like(self.frame)
        self.whiteboard.fill(255)
        self.addfiles()
        mask = cv2.inRange(hsv, lower_range, upper_range)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(c)
            # y2 = y2+h
            # cv2.rectangle(frame,(x2,y2),(x2+w,y2+h),(255,255,255),2)
            cv2.circle(overlaypen, (x2, y2), 10, (255, 255, 255), thickness=-1)
            self.frame = cv2.add(self.frame, overlaypen)
            self.whiteboard = cv2.subtract(self.whiteboard, overlaypen)
            if self.x1 == 0 and self.y1 == 0:
                self.x1, self.y1 = x2, y2
            if self.draw:
                self.canvas = cv2.line(self.canvas, (self.x1, self.y1), (x2, y2), self.color, 5)
            if self.erase:
                self.canvas = cv2.circle(self.canvas, (self.x1, self.y1), 30, (0, 0, 0), -1)

            self.x1, self.y1 = x2, y2
        _, mask = cv2.threshold(cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY), 20, 255, cv2.THRESH_BINARY)
        foreground = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        background = cv2.bitwise_and(self.frame, self.frame, mask=cv2.bitwise_not(mask))
        self.frame = cv2.add(foreground, background)

        white_background = cv2.bitwise_and(self.whiteboard, self.whiteboard, mask=cv2.bitwise_not(mask))
        self.whiteboard = cv2.add(foreground, white_background)
        if self.record == True:
            if self.mode == 0:
                self.recorder.write(self.frame)
            else:
                self.recorder.write(self.whiteboard)
            self.audiorecorder.record()
        frame = cv2.flip(self.frame, 0)
        self.whiteboard = cv2.flip(self.whiteboard, 0)
        if self.mode == 0:
            buf1 = frame.tostring()
        else:
            buf1 = self.whiteboard.tostring()

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture1


if __name__ == '__main__':
    Board().run()
    cv2.destroyAllWindows()
