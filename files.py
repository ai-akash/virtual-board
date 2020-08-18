import os
import cv2
import imutils


class Files:
    def __init__(self, file_path):
        """

        :type file_path: byte
        """
        self.file_path = file_path
        self.selected = True
        if self.file_path.lower().endswith((b'.png', b'.jpg', b'.jpeg', b'.tiff', b'.bmp', b'.gif')):
            self.file_type = 0
            self.size = 1
            self.data = cv2.imread(self.file_path.decode("utf-8"))
            self.height, self.width, _ = self.data.shape
            if self.height > 720:
                self.data = imutils.resize(self.data,height=720)
                self.height, self.width, _ = self.data.shape
            if self.width > 1280:
                self.data = imutils.resize(self.data,1280)
                self.height, self.width, _ = self.data.shape
        elif self.file_path.lower().endswith(b'.txt'):
            self.file_type = 1
            self.font_size = 1
            self.thickness = 1
        else:
            self.file_type = None

        self.x = 0
        self.y = 0
    def get_file_path(self):
        return self.file_path.decode("utf-8")

    def get_file_data(self):
        data = None
        if self.file_type is not None:
            if self.file_type == 0:
                data = imutils.resize(self.data, int(self.width * self.size))
            elif self.file_type == 1:
                data = open(self.file_path, "r", encoding="utf-8").read()
            return data

    def get_size(self):
        size = None
        if self.file_type is not None:
            if self.file_type == 0:
                size = self.width
            elif self.file_type == 1:
                size = self.font_size
            return size

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def size_increase(self):
        if self.file_type is not None:
            if self.file_type == 0:
                self.size += 0.1
            elif self.file_type == 1:
                self.font_size += 0.1

    def size_decrease(self):
        if self.file_type is not None:
            if self.file_type == 0:
                self.size -= 0.1
            elif self.file_type == 1:
                self.font_size -= 0.1

    def get_name(self):
        return os.path.basename(self.file_path).decode("utf-8")

    def up(self):
        if self.file_type == 0:
            if not self.y - 5 <= 0:
                self.y -= 5
        else:
            self.y -= 5

    def down(self):
        if self.file_type == 0:
            if not self.y + self.height + 5 > 720:
                self.y += 5
        else:
            self.y += 5

    def right(self):
        if self.file_type == 0:
            if not self.x + self.width + 5 < 720:
                self.x += 5
        else:
            self.x += 5

    def left(self):
        if self.file_type == 0:
            if not self.x-5<0:
                self.x -= 5
        else:
            self.x -= 5
