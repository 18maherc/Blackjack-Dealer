from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

Builder.load_file('controller.kv')

# Declare both screens


class SplashScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class TestApp(App):

    def build(self):
        # Print an opening statement
        print("Play a game of Blackjack!!")
        # Create the screen manager
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(SettingsScreen(name='settings'))

        # for each player, add a playerscreen of name=f"player{playernum}"

        return sm


if __name__ == '__main__':
    TestApp().run()
