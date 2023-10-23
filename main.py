from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window

from kivy.lang import Builder
from kivy.clock import Clock
import threading

# Translate Import
from models.voice_get import process_sound

navigation_helper = """        
Screen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items:
                        [['menu', lambda x: nav_drawer.set_state(app._get_state())]]
                        
                MDLabel:
                    id: translation_labelView
                    text: app._get_translation_label()
                    pos_hint: {"center_x": .8, "center_y": .8}
                    font_style: 'Subtitle1'

                MDIconButton:
                    id: toggle_button
                    icon: "power"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    adaptive_size: True
                    icon_size: "156sp"
                    on_release: app.toggle_state()
                    
                MDLabel:
                    id: translate_to_label
                    text: app._get_translation_to_label()
                    pos_hint: {"center_x": .85, "center_y": .3}
                    font_style: 'Subtitle2'
                    
                MDDropDownItem:
                    id: drop_item
                    pos_hint: {'center_x': .5, 'center_y': .2}
                    text: app._get_selection()
                    on_release: app.menu.open()

        MDNavigationDrawer:
            id: nav_drawer
            type: "standard"
            close_on_click: True
            size_hint: (0.5, 1)
            MDNavigationDrawerMenu:    
                MDNavigationDrawerHeader:
                                
                MDNavigationDrawerLabel:
                    text: "Volume"
            
                MDNavigationDrawerItem: 
                    _no_ripple_effect: True
                    focus_behavior: False
                    MDSlider:
                        id: volume_slider
                        hint: True
                        hint_bg_color: "red"
                        hint_text_color: "white"
                        min: 0
                        max: 100
                        value: app.volume
                        on_touch_up: app._adjust_volume(self.value)
                        pos_hint: {"top" : 1}
                        
                        
                MDNavigationDrawerDivider:
                
                MDNavigationDrawerLabel:
                    id: rate_label
                    text: app._get_rate_label()
            
                MDNavigationDrawerItem: 
                    _no_ripple_effect: True
                    focus_behavior: False
                    MDSlider:
                        id: rate_slider
                        hint: True
                        hint_bg_color: "red"
                        hint_text_color: "white"
                        min: 100
                        max: 300
                        value: app.rate
                        on_touch_up: app._adjust_rate(self.value)
                        pos_hint: {"top" : 1}
               
"""

class TranslatorApp(MDApp):
    # If AppState is False, Apps is not Running.
    Running = False
    language = "en"
    volume = 90
    rate = 150
    drawer = "close"
    
    def _get_state(self, instance=None):
        if self.drawer == "close":
            self.drawer = "open"
            return "open"
        else:
            self.drawer = "close"
            return "close"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(navigation_helper)
        menu_items = self._get_dropdown_items()
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()
        
    def _adjust_volume(self, value, instance = None):
        self.volume = value
        
    def _adjust_rate(self, value, instance = None):
        self.rate = value
    
    def build(self):
        screen = self.screen
        return screen
    
    def toggle_state(self, instance=None):
        if not self.Running:
            self.Running = True
        else:
            self.Running = False

        if self.Running:
            translation = threading.Thread(target=self.run_translation)
            translation.start()
            
    def run_translation(self):
        while self.Running:
            process_sound(self.language, self.volume/100, self.rate)
    
    def _run_translation_interval(self, dt=None):
        run = threading.Thread(target=process_sound, args=(self.language, self.volume/100, self.rate))
        run.start()
        
    def _get_selection(self):
        if self.language == "en":
            return "English"
        else:
            return "Indonesia"
        
    def _get_translation_label(self):
        if self.language == "en":
            return "Start Translation"
        else:
            return "Mulai Penerjemahan"
        
    def _get_translation_to_label(self):
        if self.language == "en":
            return "Translate To"
        else:
            return "Terjemahkan ke"
        
    def _get_rate_label(self, instance=None):
        if self.language == "en":
            return "Rate of Word"
        else:
            return "Kecepatan Kata"

    def _get_dropdown_items(self):
        return [
            {
                "viewclass": "OneLineListItem",
                "text": "English",
                "on_release": lambda x="en": self.set_language(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Indonesia",
                "on_release": lambda x="id": self.set_language(x),
            },
        ]
        
    def set_language(self, language):
        self.language = language
        text_item = self._get_selection()
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()
        
        # Set Translation Label
        self.screen.ids.translation_labelView.text = self._get_translation_label()
        
        # Set Translation Label
        self.screen.ids.translate_to_label.text = self._get_translation_to_label()
        
        # Set Rate of Word Label
        self.screen.ids.rate_label.text = self._get_rate_label()

if __name__ == '__main__':
    TranslatorApp().run()
