from tkinter import Tk, Label, Button, Frame, Entry, Toplevel, Event, BOTH
from collections import defaultdict
from src.channel import Channel


class ConnectionDialog:
    """
    Class handling the user input for the connection with the controller
    """

    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.columnconfigure(0, weight=MainWindow.WEIGHT)
        self.top.columnconfigure(1, weight=MainWindow.WEIGHT)
        for i in range(4):
            self.top.rowconfigure(i, weight=MainWindow.WEIGHT)

        host_label = Label(self.top, text='Host: ', background=MainWindow.BACKGROUND_COLOR)
        host_label.grid(row=0, column=0, sticky=MainWindow.FILL)
        self.host_entry = Entry(self.top, background=MainWindow.BACKGROUND_COLOR)
        self.host_entry.grid(row=0, column=1, sticky=MainWindow.FILL)

        port_label = Label(self.top, text='Port: ', background=MainWindow.BACKGROUND_COLOR)
        port_label.grid(row=1, column=0, sticky=MainWindow.FILL)
        self.port_entry = Entry(self.top, background=MainWindow.BACKGROUND_COLOR)
        self.port_entry.grid(row=1, column=1, sticky=MainWindow.FILL)

        password_label = Label(self.top, text='Password: ', background=MainWindow.BACKGROUND_COLOR)
        password_label.grid(row=2, column=0, sticky=MainWindow.FILL)
        self.password_entry = Entry(self.top, show='*', background=MainWindow.BACKGROUND_COLOR)
        self.password_entry.grid(row=2, column=1, sticky=MainWindow.FILL)

        button_frame = Frame(self.top)
        button_frame.grid(row=3, column=0, sticky=MainWindow.FILL, columnspan=2)
        connect_button = Button(button_frame, text='Connect.', command=self.__connect, background=MainWindow.BACKGROUND_COLOR)
        connect_button.pack(fill=BOTH)

    def __connect(self) -> None:
        """
        Saves the inputs given by the user

        :Assumptions: None

        :return: None
        """
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.password = self.password_entry.get()
        self.top.destroy()


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

        # dial = ConnectionDialog(self.window)
        # self.window.wait_window(dial.top)

        # tmp!!!!! TODO:
        port = int(input('port: '))
        if port == '':
            port = 8000
        self.channel = Channel('192.168.1.11', port, '69420')
        # self.channel = Channel(dial.host, dial.port, dial.password)

        self.switcher = self.__create_switcher()
        self.key_event_modifier = defaultdict(bool)

        self.window.bind('<KeyPress>', self.__on_key_press_event)
        self.window.bind('<KeyRelease>', self.__on_key_release_event)
        self.channel.data_received.connect(self.__on_UI_update_received)

        self.window.mainloop()

    def __on_close_event(self) -> None:
        """
        Function that handles the user clicked exit event.
        The channel with the controller itself should be closed properly, before exiting the application.

        :Assumptions: None

        :return: None
        """
        self.channel.deactivate()
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

        self.left_indicator = Button(
            master=self.lights_layout,
            text=self.LEFT_INDICATOR_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.L_INDICATOR,
                not self.channel.get_value(self.channel.L_INDICATOR)
            )
        )
        self.left_indicator.grid(row=0, column=0, sticky=self.FILL)
        self.right_indicator = Button(
            master=self.lights_layout,
            text=self.RIGHT_INDICATOR_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.R_INDICATOR,
                not self.channel.get_value(self.channel.R_INDICATOR)
            )
        )
        self.right_indicator.grid(row=0, column=2, sticky=self.FILL)

        self.middle_light_frame = Frame(master=self.lights_layout)
        self.middle_light_frame.columnconfigure(0, weight=self.WEIGHT)
        self.middle_light_frame.rowconfigure(0, weight=self.WEIGHT)
        self.middle_light_frame.rowconfigure(1, weight=self.WEIGHT)
        self.middle_light_frame.grid(row=0, column=1, sticky=self.FILL)

        self.hazard_warning = Button(
            master=self.middle_light_frame,
            text=self.HAZARD_WARNING_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.HAZARD_WARNING,
                not self.channel.get_value(self.channel.HAZARD_WARNING)
            )
        )
        self.hazard_warning.grid(row=0, column=0, sticky=self.FILL)
        self.light_switch = Button(
            master=self.middle_light_frame,
            text=self.LIGHTS_SWITCH_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.LIGHTS,
                not self.channel.get_value(self.channel.LIGHTS)
            )
        )
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

        self.reverse_button = Button(
            master=self.button_layout,
            text=self.REVERSE_SWITCH_TEXT,
            foreground='red',
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.REVERSE,
                not self.channel.get_value(self.channel.REVERSE)
            )
        )
        self.reverse_button.grid(row=0, column=0, sticky=self.FILL)
        self.horn_button = Button(
            master=self.button_layout,
            text=self.HORN_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.HORN,
                not self.channel.get_value(self.channel.HORN)
            )
        )
        self.horn_button.grid(row=0, column=2, sticky=self.FILL)

        self.forward_button = Button(
            master=self.button_layout,
            text=self.FORWARD_ARROW_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.FORWARD,
                not self.channel.get_value(self.channel.FORWARD)
            )
        )
        self.forward_button.grid(row=0, column=1, sticky=self.FILL)
        self.backward_button = Button(
            master=self.button_layout,
            text=self.BACK_ARROW_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.BACKWARD,
                not self.channel.get_value(self.channel.BACKWARD)
            )
        )
        self.backward_button.grid(row=1, column=1, sticky=self.FILL)
        self.left_button = Button(
            master=self.button_layout,
            text=self.LEFT_ARROW_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.LEFT,
                not self.channel.get_value(self.channel.LEFT)
            )
        )
        self.left_button.grid(row=1, column=0, sticky=self.FILL)
        self.right_button = Button(
            master=self.button_layout,
            text=self.RIGHT_ARROW_TEXT,
            background=self.BACKGROUND_COLOR,
            command=lambda: self.channel.set_value(
                self.channel.RIGHT,
                not self.channel.get_value(self.channel.RIGHT)
            )
        )
        self.right_button.grid(row=1, column=2, sticky=self.FILL)

    def __create_switcher(self):
        """
        Create the switcher object, for the key events, so implementing a switch case is possible,
        without creating a new object every time a key is pressed

        :Assumptions:
          * The Channel object have been created, before this method is called

        :return: the switcher object
        """
        return defaultdict(
            lambda: 'None',
            {
                65362: self.channel.FORWARD,
                119: self.channel.FORWARD,
                65364: self.channel.BACKWARD,
                115: self.channel.BACKWARD,
                65361: self.channel.LEFT,
                97: self.channel.LEFT,
                65363: self.channel.RIGHT,
                100: self.channel.RIGHT,
                142: self.channel.HORN,
                108: self.channel.LIGHTS,
                104: self.channel.HAZARD_WARNING,
                114: self.channel.REVERSE,
                113: self.channel.L_INDICATOR,
                101: self.channel.R_INDICATOR
            }
        )

    def __on_key_press_event(self, event: Event) -> None:
        """
        Handles the event, when the user presses a key

        :Assumption:
          * This method should only be called from the Tkinter main loop

        :param event: Contains the events object

        :return: None
        """

        case = self.switcher[event.keysym_num]
        if event.keysym_num in [101, 104, 108, 113, 114]:
            self.channel.set_value(case, not self.channel.get_value(case))
        elif not self.key_event_modifier[case]:
            self.channel.set_value(case, True)
            self.key_event_modifier[case] = True

    def __on_key_release_event(self, event: Event) -> None:
        """
        Handles the event, when the user releases a key

        :Assumption:
          * This method should only be called from the Tkinter main loop

        :param event: Contains the events object

        :return: None
        """

        if event.keysym_num not in [101, 104, 108, 113, 114]:
            self.channel.set_value(self.switcher[event.keysym_num], False)
            self.key_event_modifier[self.switcher[event.keysym_num]] = False

    def __on_UI_update_received(self, _) -> None:
        """
        Handles the event, when data from the controller arrives, hence we should change the UI accordingly

        :Assumptions: none

        :return: None
        """
        # self.reverse_button.configure(
        #     background='red' if self.channel.get_value(self.channel.REVERSE) else self.BACKGROUND_COLOR,
        #     foreground=self.BACKGROUND_COLOR if self.channel.get_value(self.channel.REVERSE) else 'red'
        # )


if __name__ == '__main__':
    MainWindow()
