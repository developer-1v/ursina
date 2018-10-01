from ursina import *
import textwrap


class Button(Entity):

    color = color.black66

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'button'
        self.parent = scene.ui
        self.is_editor = False
        self.model = 'quad'
        self.color = Button.color
        # self.texture = 'panda_button'

        self.collision = True
        self.collider = 'box'
        # self.text = 'button'
        self.text_entity = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    @property
    def text(self):
        if self.text_entity:
            return self.text_entity.text

    @text.setter
    def text(self, value):
        if type(value) is str:
            if not self.text_entity:
                self.text_entity = Text(
                    parent = self,
                    size = Text.size * 20,
                    position = (0, 0, -.1),
                    origin = (0,0)
                    )

            self.text_entity.text = value
            self.text_entity.world_scale = (1,1,1)


    def __setattr__(self, name, value):
        if name == 'color':
            # ignore setting original color if the button is modifying its own color on enter, exit or click
            if ('self' in inspect.currentframe().f_back.f_locals
            and inspect.currentframe().f_back.f_locals['self'] != self
            or inspect.stack()[1][3] == '__init__'):
                self.original_color = value
                self.highlight_color = color.tint(self.original_color, .2)
                self.pressed_color = color.tint(self.original_color, -.2)


        if name == 'origin':
            super().__setattr__(name, value)
            try:    # update collider position by making a new one
                self.collider.remove()
                self.collider = 'box'
            except:
                pass

        if name == 'on_click' and isinstance(value, str):
            object.__setattr__(self, 'on_click_string', textwrap.dedent(value))
            return

        try:
            super().__setattr__(name, value)
        except Exception as e:
            return e


    def input(self, key):
        if key == 'left mouse down':
            if self.hovered:
                self.color = self.pressed_color

        if key == 'left mouse up':
            if self.hovered:
                self.color = self.highlight_color


    def on_mouse_enter(self):
        self.color = self.highlight_color

        if hasattr(self, 'tooltip'):
            self.tooltip_scale = self.tooltip.scale
            self.tooltip.scale = (0,0,0)
            self.tooltip.enabled = True
            self.scale_animator = self.tooltip.animate_scale(self.tooltip_scale)


    def on_mouse_exit(self):
        self.color = self.original_color

        if hasattr(self, 'tooltip'):
            if hasattr(self, 'tooltip_scaler'):
                self.scale_animator.finish()
            self.tooltip.enabled = False

    def on_click(self):
        if hasattr(self, 'on_click_string'):
            exec(self.on_click_string)

class Test():
    def __init__(self):
        self.b = Button(color = color.red, text='button_text')
        self.b.on_click = '''
            self.text = 'on_click_string'
            self.color = color.red
            print('on_click defined with string works!')
            '''
        # self.b.on_click = self.test_method
        self.b.scale *= .5
        self.b.color = color.azure
        # self.b.origin = (-.5, -.5)
        self.b.text = 'text'
        # self.b.text_entity.scale *= 2

    def test_method(self):
        print('test method')
        self.b.color = color.red

if __name__ == '__main__':
    app = Ursina()
    t = Test()
    # b = Button(text='test\ntest', scale=(4,1), model='quad', collision=False)
    # b.text_entity.scale *= .5
    # t.b.tooltip = Text(text='yolo', background=True)
    app.run()
