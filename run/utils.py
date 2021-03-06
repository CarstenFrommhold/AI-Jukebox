import time
import pytesseract
from PIL import Image
import os
from difflib import SequenceMatcher
from operator import itemgetter
from typing import Tuple


class Handler:

    def __init__(self):
        self.options = {
            "coldplay": "https://www.mboxdrive.com/Coldplay_X_BTS_-_My_Universe_Offic_(getmp3.pro).mp3",
            "guns n roses": "https://www.mboxdrive.com/Guns-N-Roses-Sweet-Child-O-Mine-Official-Music-Video_1w7OgIMMRc4.mp3",
            "queen": "https://www.mboxdrive.com/Queen%20-%20Another%20One%20Bites%20The%20Dust.mp3",
            "daftpunk": "https://www.mboxdrive.com/daft-punk-something-about-us-official-audio.mp3"
        }
        self.current_song = None
        self.threshold = 0.5

    @staticmethod
    def shot(camera=None):
        camera.capture("pic/pic.jpg")
        return Image.open("pic/pic.jpg")

    @staticmethod
    def del_():
        try:
            os.remove("pic/pic.jpg")
        except:
            pass

    @staticmethod
    def ocr(img) -> str:
        return pytesseract.image_to_string(img)

    @staticmethod
    def best_match(input: str, options: list) -> Tuple[str, float]:

        matches = []
        for option in options:
            matches.append((
                option,
                SequenceMatcher(None, input.lower(), option).ratio()
            ))

        matches.sort(reverse=True, key=itemgetter(1))
        return matches[0]

    def track_from_img(self, img):
        img_to_str = self.ocr(img)
        print(f"OCR says {img_to_str}")

        if img_to_str == "":
            return "", 0.01

        nearest_string, confidence = self.best_match(img_to_str, self.options.keys())

        return nearest_string, confidence

    def play_track_on_sonos_box(self, sonos_box, track):
        sonos_box.play_uri(self.options.get(track))
        self.current_song = track

    def run(self, sonos_box, camera):
        print("Write down what you want to hear...")
        while True:
            print("Next one?")
            try:
                os.makedirs("pic")
            except:
                pass
            img = self.shot(camera)
            track, confidence = self.track_from_img(img)
            if confidence > self.threshold:
                if track != self.current_song:
                    self.current_song = track
                    print(f"Playing {track}")
                    self.play_track_on_sonos_box(sonos_box, track)
                    time.sleep(10)
            # self.del_()
            time.sleep(0.1)
