from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
import kivy
kivy.require('1.0.5')


class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''

    def button_pressed(self):
        self.button_wid.text = 'Hello, World!'


class ControllerApp(App):

    def build(self):
        return Controller()


if __name__ == '__main__':
    ControllerApp().run()
