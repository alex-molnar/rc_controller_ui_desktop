from tkinter import Tk, Label, Button, Frame, Event


class MainWindow:
    """class for creating the main window of the application"""

    FILL             = 'nesw'
    MIN_SIZE         = 100
    WEIGHT           = 1
    BACKGROUND_COLOR = '#87edfa'

    DISTANCE_TEXT = 'Distance: '
    DISTANCE_MES  = 'cm'
    DISTANCE_LEN  = len(DISTANCE_TEXT)

    SPEED_TEXT = 'Speed: '
    SPEED_MES  = 'm/s'
    SPEED_LEN  = len(SPEED_TEXT)

    LEFT_INDICATOR_TEXT  = '⮈'
    RIGHT_INDICATOR_TEXT = '⮊'
    HAZARD_WARNING_TEXT  = '⚠'
    LIGHTS_SWITCH_TEXT   = '🔦'

    FORWARD_ARROW_TEXT  = '⮝'
    BACK_ARROW_TEXT     = '⮟'
    LEFT_ARROW_TEXT     = '⮜'
    RIGHT_ARROW_TEXT    = '⮞'
    HORN_TEXT           = '📯'
    REVERSE_SWITCH_TEXT = 'R'


    def __init__(self):
        """Initializing the main window"""

        self.window = Tk()
        self.window.columnconfigure(0, weight=self.WEIGHT)
        self.window.rowconfigure(0, weight=self.WEIGHT)
        self.window.protocol('WM_DELETE_WINDOW', self.__on_close_event)

        self.__handle_labels_layout()
        self.__handle_light_button_layout()
        self.__handle_move_button_layout()

        self.window.mainloop()

    def __on_close_event(self) -> None:
        """
        Function that handles the user clicked exit event.
        The channel with the controller itself should be closed properly, before exiting the application

        :Assumptions: None

        :return: None
        """
        self.window.destroy()

    def __handle_labels_layout(self) -> None:
        """
        Creates, and manages the layout for the labels, such as the distance label, speed label, and the follow the line label
        
        :Assumptions: None
        
        :return: 
        """
        self.label_layout = Frame(master=self.window)
        self.label_layout.rowconfigure(0, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        for i in range(3):
            self.label_layout.columnconfigure(i, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        self.label_layout.grid(row=0, column=0, sticky=self.FILL)

        self.distance_label = Label(master=self.label_layout, text=self.DISTANCE_TEXT, background=self.BACKGROUND_COLOR)
        self.distance_label.grid(row=0, column=0, sticky=self.FILL)
        self.line_label = Label(master=self.label_layout, background='white')
        self.line_label.grid(row=0, column=1, sticky=self.FILL)
        self.speed_label = Label(master=self.label_layout, text=self.SPEED_TEXT, background=self.BACKGROUND_COLOR)
        self.speed_label.grid(row=0, column=2, sticky=self.FILL)

    def __handle_light_button_layout(self) -> None:
        """
        Creates, and manages the layout for the buttons, such as the light, and hazard warning switch, and the indicators

        :Assumptions: None
        
        :return: None
        """
        self.lights_layout = Frame(master=self.window)
        self.lights_layout.rowconfigure(0, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        for i in range(3):
            self.lights_layout.columnconfigure(i, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        self.lights_layout.grid(row=1, column=0, sticky=self.FILL)

        self.left_indicator = Button(master=self.lights_layout, text=self.LEFT_INDICATOR_TEXT, background=self.BACKGROUND_COLOR)
        self.left_indicator.grid(row=0, column=0, sticky=self.FILL)
        self.right_indicator = Button(master=self.lights_layout, text=self.RIGHT_INDICATOR_TEXT, background=self.BACKGROUND_COLOR)
        self.right_indicator.grid(row=0, column=2, sticky=self.FILL)

        self.middle_light_frame = Frame(master=self.lights_layout)
        self.middle_light_frame.columnconfigure(0, weight=self.WEIGHT)
        self.middle_light_frame.rowconfigure(0, weight=self.WEIGHT)
        self.middle_light_frame.rowconfigure(1, weight=self.WEIGHT)
        self.middle_light_frame.grid(row=0, column=1, sticky=self.FILL)

        self.hazard_warning = Button(master=self.middle_light_frame, text=self.HAZARD_WARNING_TEXT, background=self.BACKGROUND_COLOR)
        self.hazard_warning.grid(row=0, column=0, sticky=self.FILL)
        self.light_switch = Button(master=self.middle_light_frame, text=self.LIGHTS_SWITCH_TEXT, background=self.BACKGROUND_COLOR)
        self.light_switch.grid(row=1, column=0, sticky=self.FILL)

    def __handle_move_button_layout(self) -> None:
        """
        Creates, and manages the layout for the buttons, such as the arrows, the reverse switch, and the horn

        :Assumptions: None
        
        :return: None
        """

        self.button_layout = Frame(master=self.window)
        self.button_layout.rowconfigure(0, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        self.button_layout.rowconfigure(1, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        for i in range(3):
            self.button_layout.columnconfigure(i, weight=self.WEIGHT, minsize=self.MIN_SIZE)
        self.button_layout.grid(row=2, column=0, sticky=self.FILL)

        self.reverse_button = Button(master=self.button_layout, text=self.REVERSE_SWITCH_TEXT, foreground='red', background=self.BACKGROUND_COLOR)
        self.reverse_button.grid(row=0, column=0, sticky=self.FILL)
        self.horn_button = Button(master=self.button_layout, text=self.HORN_TEXT, background=self.BACKGROUND_COLOR)
        self.horn_button.grid(row=0, column=2, sticky=self.FILL)

        self.forward_button = Button(master=self.button_layout, text=self.FORWARD_ARROW_TEXT, background=self.BACKGROUND_COLOR)
        self.forward_button.grid(row=0, column=1, sticky=self.FILL)
        self.backward_button = Button(master=self.button_layout, text=self.BACK_ARROW_TEXT, background=self.BACKGROUND_COLOR)
        self.backward_button.grid(row=1, column=1, sticky=self.FILL)
        self.left_button = Button(master=self.button_layout, text=self.LEFT_ARROW_TEXT, background=self.BACKGROUND_COLOR)
        self.left_button.grid(row=1, column=0, sticky=self.FILL)
        self.right_button = Button(master=self.button_layout, text=self.RIGHT_ARROW_TEXT, background=self.BACKGROUND_COLOR)
        self.right_button.grid(row=1, column=2, sticky=self.FILL)


if __name__ == '__main__':
    MainWindow()
