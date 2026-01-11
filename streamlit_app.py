import os
import json
import pygame
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

if platform not in ('android', 'ios'):
    Window.size = (420, 800)

pygame.mixer.init()

# ลบ Comment ออกเพื่อให้ก๊อปวางง่ายและไม่ error
KV_CODE = '''
#:import hex kivy.utils.get_color_from_hex

<ThreeDButton>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: 0.8, 0.9, 1, 1
    font_size: '16sp'
    bold: True
    canvas.before:
        Color:
            rgba: (0.05, 0.05, 0.06, 1)
        RoundedRectangle:
            pos: (self.x + 3, self.y - 3)
            size: self.size
            radius: [10]
        Color:
            rgba: (0.2, 0.2, 0.23, 1) if self.state == 'normal' else (0.15, 0.15, 0.17, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]
        Color:
            rgba: (0.4, 0.4, 0.45, 0.5) if self.state == 'normal' else (0,0,0,0)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            width: 1

<EQSlider@Slider>:
    orientation: 'vertical'
    cursor_image: ''
    cursor_size: (0,0)
    background_width: 0
    canvas.before:
        Color:
            rgba: (0.05, 0.05, 0.05, 1)
        RoundedRectangle:
            pos: (self.center_x - dp(3), self.y)
            size: (dp(6), self.height)
            radius: [3]
        Color:
            rgba: (0, 1, 0.8, 0.3)
        Line:
            points: [self.center_x, self.y, self.center_x, self.top]
            width: 1
    canvas.after:
        Color:
            rgba: (0.25, 0.25, 0.28, 1)
        RoundedRectangle:
            pos: (self.center_x - dp(15), self.value_pos[1] - dp(10))
            size: (dp(30), dp(20))
            radius: [3]
        Color:
            rgba: (0, 1, 0.8, 0.8)
        Line:
            points: [self.center_x - dp(10), self.value_pos[1], self.center_x + dp(10), self.value_pos[1]]
            width: 1.5

<MixerLabel@Label>:
    font_size: '10sp'
    color: (0.6, 0.6, 0.6, 1)
    bold: True

<SongListItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: '55dp'
    padding: 10
    spacing: 10
    canvas.before:
        Color:
            rgba: (0.15, 0.15, 0.17, 1)
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: (0.05, 0.05, 0.05, 1)
        Line:
            points: [self.x, self.y, self.right, self.y]
            width: 1
    canvas.after:
        Color:
            rgba: (0, 1, 0.5, 1) if root.is_playing else (0,0,0,0)
        Rectangle:
            pos: (self.x, self.y)
            size: (dp(5), self.height)
    Label:
        text: root.text
        color: (0.9, 0.9, 0.9, 1) if not root.is_playing else (0, 1, 0.5, 1)
        text_size: self.width, None
        halign: 'left'
        valign: 'middle'

Screen:
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.11, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10

        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            size_hint_y: None
            height: '60dp'
            Image:
                source: 'log.jpg'
                size_hint: (None, None)
                size: (120, 60)
                allow_stretch: True
                keep_ratio: True

        BoxLayout:
            size_hint_y: 0.15
            padding: 5
            canvas.before:
                Color:
                    rgba: (0.05, 0.05, 0.08, 1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: (0, 0.8, 1, 0.4)
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
                    width: 2
            Label:
                text: app.current_song_name
                font_size: '16sp'
                color: (0, 1, 0.9, 1)
                text_size: self.size, None
                halign: 'center'
                valign: 'middle'

        BoxLayout:
            size_hint_y: 0.3
            orientation: 'vertical'
            padding: 10
            spacing: 5
            canvas.before:
                Color:
                    rgba: (0.13, 0.13, 0.15, 1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [15]
            
            Label:
                text: "EQ / PAN CONTROL"
                size_hint_y: None
                height: '20dp'
                font_size: '10sp'
                color: (0.5, 0.5, 0.5, 1)

            GridLayout:
                cols: 5
                spacing: 10
                BoxLayout:
                    orientation: 'vertical'
                    EQSlider:
                        min: 0
                        max: 100
                        value: 50
                    MixerLabel:
                        text: 'HI'
                        size_hint_y: None
                        height: '15dp'
                BoxLayout:
                    orientation: 'vertical'
                    EQSlider:
                        min: 0
                        max: 100
                        value: 50
                    MixerLabel:
                        text: 'MID'
                        size_hint_y: None
                        height: '15dp'
                BoxLayout:
                    orientation: 'vertical'
                    EQSlider:
                        min: 0
                        max: 100
                        value: 50
                    MixerLabel:
                        text: 'LOW'
                        size_hint_y: None
                        height: '15dp'
                Widget:
                    size_hint_x: None
                    width: '10dp'
                BoxLayout:
                    orientation: 'vertical'
                    BoxLayout:
                        size_hint_y: 0.3
                    Slider:
                        min: -1
                        max: 1
                        value: 0
                        cursor_size: (dp(20), dp(20))
                        background_width: dp(2)
                    MixerLabel:
                        text: 'PAN'
                        size_hint_y: None
                        height: '15dp'

        RecycleView:
            id: rv
            viewclass: 'SongListItem'
            scroll_type: ['bars', 'content']
            bar_width: '4dp'
            RecycleBoxLayout:
                default_size: None, dp(55)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.15
            orientation: 'vertical'
            BoxLayout:
                size_hint_y: None
                height: '30dp'
                Label:
                    text: 'VOL'
                    size_hint_x: 0.2
                    font_size: '10sp'
                Slider:
                    min: 0
                    max: 1
                    value: app.volume_level
                    on_value: app.set_volume(self.value)
                    cursor_size: (dp(20), dp(20))
            GridLayout:
                cols: 3
                spacing: 15
                padding: [0, 5, 0, 0]
                ThreeDButton:
                    text: 'STOP'
                    color: (1, 0.3, 0.3, 1)
                    on_release: app.stop_music()
                ThreeDButton:
                    text: 'PLAY/PAUSE'
                    color: (0.3, 1, 0.5, 1)
                    on_release: app.toggle_play()
                ThreeDButton:
                    text: '+ ADD'
                    color: (1, 0.8, 0.2, 1)
                    on_release: app.open_file_chooser()
'''

class ThreeDButton(ButtonBehavior, Label):
    pass

class SongListItem(BoxLayout, RecycleDataViewBehavior):
    text = StringProperty("")
    index = None
    is_playing = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = os.path.basename(data['path'])
        self.is_playing = data.get('is_playing', False)
        return super(SongListItem, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.play_music(self.index)
            return True
        return super(SongListItem, self).on_touch_down(touch)

class MP3PlayerApp(App):
    current_song_name = StringProperty("READY")
    playlist = ListProperty([])
    current_index = -1
    is_paused = False
    is_active = False
    volume_level = NumericProperty(0.7)

    def build(self):
        self.load_playlist()
        pygame.mixer.music.set_volume(self.volume_level)
        Clock.schedule_interval(self.check_music_end, 1.0)
        return Builder.load_string(KV_CODE)

    def check_music_end(self, dt):
        if self.is_active and not self.is_paused:
            if not pygame.mixer.music.get_busy():
                self.play_next()

    def play_next(self):
        if self.playlist:
            next_index = self.current_index + 1
            if next_index >= len(self.playlist):
                next_index = 0
            self.play_music(next_index)

    def set_volume(self, value):
        self.volume_level = value
        try:
            pygame.mixer.music.set_volume(value)
        except:
            pass

    def load_playlist(self):
        if os.path.exists('playlist.json'):
            try:
                with open('playlist.json', 'r') as f:
                    self.playlist = json.load(f)
                self.update_list_ui()
            except:
                pass

    def save_playlist(self):
        try:
            with open('playlist.json', 'w') as f:
                json.dump(self.playlist, f)
        except:
            pass

    def update_list_ui(self):
        data = []
        for i, song in enumerate(self.playlist):
            is_playing = (i == self.current_index)
            data.append({'path': song, 'is_playing': is_playing})
        if self.root:
            self.root.ids.rv.data = data

    def open_file_chooser(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        start_path = '/storage/emulated/0/Music'
        if not os.path.exists(start_path):
            start_path = '/storage/emulated/0/'

        self.file_chooser = FileChooserIconView(path=start_path, filters=['*.mp3'])
        
        btn_box = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        select_btn = ThreeDButton(text='SELECT', color=(0, 1, 0.8, 1))
        select_btn.bind(on_release=self.add_selected_song)
        cancel_btn = ThreeDButton(text='CANCEL')
        
        btn_box.add_widget(cancel_btn)
        btn_box.add_widget(select_btn)
        
        content.add_widget(self.file_chooser)
        content.add_widget(btn_box)
        
        self.popup = Popup(title="ADD TRACKS", content=content, size_hint=(0.9, 0.85),
                           title_color=(0,1,0.8,1), separator_color=(0,1,0.8,0.5))
        self.popup.background_color = (0.1, 0.1, 0.12, 1)
        cancel_btn.bind(on_release=self.popup.dismiss)
        self.popup.open()

    def add_selected_song(self, instance):
        selection = self.file_chooser.selection
        if selection:
            for file_path in selection:
                if file_path not in self.playlist:
                    self.playlist.append(file_path)
            self.save_playlist()
            self.update_list_ui()
            self.popup.dismiss()

    def play_music(self, index):
        try:
            self.current_index = index
            song_path = self.playlist[index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            
            self.current_song_name = os.path.splitext(os.path.basename(song_path))[0]
            self.is_paused = False
            self.is_active = True
            self.update_list_ui()
            
        except Exception as e:
            self.current_song_name = "Error loading file!"
            print(f"Error: {e}")

    def toggle_play(self):
        if not self.playlist:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            if self.current_index == -1:
                self.play_music(0)
            else:
                self.play_music(self.current_index)

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            self.is_paused = False
            self.is_active = False
            self.current_song_name = "STOPPED"
            self.update_list_ui()
        except:
            pass

if __name__ == '__main__':
    try:
        MP3PlayerApp().run()
    except Exception as e:
        print(e)
