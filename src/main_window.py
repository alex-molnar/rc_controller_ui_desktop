from time import sleep
from tkinter import Tk, Label, Button, Frame, Entry, Toplevel, Event, BOTH
from collections import defaultdict
from src.channel import Channel


class ConnectionDialog:
    """
    Class handling the user input for the connection with the controller

    .. attribute:: host
        The IP of the host, - given by the user input, - which we want to connect to.

    .. attribute:: port
        The port,  - given by the user input, - on which we reach the host.

    .. attribute:: password
        The users password

    .. warning:: Validation
        | None of the above entries are validated, hence if the user mistypes,
        | or misunderstands the entry field, it is possible that a non-legit IP address,
        | or port is returned. That can lead to exceptions, therefore checking these values,
        | before is advised.
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
        connect_button = Button(button_frame, text='Connect.', command=self.__connect,
                                background=MainWindow.BACKGROUND_COLOR)
        connect_button.pack(fill=BOTH)

    def __connect(self) -> None:
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.password = self.password_entry.get()
        self.top.destroy()


class MainWindow:
    """
    Class representing the main window, hence the user interface of the application.
    | Places all UI elements, in the right place, and connects necessary events to the corresponding handler.
    | Constantly updates the UI based on the given states received from the controller.

    .. note :: Tkinter
        | This class does not need any external dependency for the UI, instead it uses
        | the built-in Tkinter library

    .. attribute:: window
        The main window of the application

    .. attribute:: dial
        The dialog window responsible for the connection

    .. attribute:: channel
        A Channel object, which is responsible for the communication between this application, and the controller.



    :var: FILL
    :var: MIN_SIZE
    :var: WEIGHT
    :var: BACKGROUND_COLOR
    :var: ACTIVE_ARROW_COLOR

    :var: DISTANCE_TEXT
    :var: DISTANCE_MES
    :var: DISTANCE_LEN

    :var: SPEED_TEXT
    :var: SPEED_MES
    :var: SPEED_LEN

    :var: LEFT_INDICATOR_TEXT
    :var: RIGHT_INDICATOR_TEXT
    :var: HAZARD_WARNING_TEXT
    :var: LIGHTS_SWITCH_TEXT

    :var: FORWARD_ARROW_TEXT
    :var: BACK_ARROW_TEXT
    :var: LEFT_ARROW_TEXT
    :var: RIGHT_ARROW_TEXT
    :var: HORN_TEXT
    :var: REVERSE_SWITCH_TEXT

    """

    FILL = 'nesw'
    MIN_SIZE = 100
    WEIGHT = 1
    BACKGROUND_COLOR = '#87edfa'
    ACTIVE_ARROW_COLOR = '#ffb2f4'

    DISTANCE_TEXT = 'Distance: '
    DISTANCE_MES = 'cm'
    DISTANCE_LEN = len(DISTANCE_TEXT)

    SPEED_TEXT = 'Speed: '
    SPEED_MES = 'm/s'
    SPEED_LEN = len(SPEED_TEXT)

    LEFT_INDICATOR_TEXT = '⮈'
    RIGHT_INDICATOR_TEXT = '⮊'
    HAZARD_WARNING_TEXT = '⚠'
    LIGHTS_SWITCH_TEXT = '🔦'

    FORWARD_ARROW_TEXT = '⮝'
    BACK_ARROW_TEXT = '⮟'
    LEFT_ARROW_TEXT = '⮜'
    RIGHT_ARROW_TEXT = '⮞'
    HORN_TEXT = '📯'
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

        self.dial = ConnectionDialog(self.window)
        self.__connect_on_top = True
        self.window.after(100, self.__ensure_connect_on_top)
        self.window.wait_window(self.dial.top)
        self.__connect_on_top = False

        # tmp!!!!! TODO:
        self.channel = Channel('192.168.1.11', 8000 + int(self.dial.port), '69420')
        # self.channel = Channel(self.dial.host, self.dial.port, self.dial.password)

        self.switcher = self.__create_switcher()
        self.__key_event_modifier = defaultdict(bool)
        self.__ctrl_pressed = False

        self.window.bind('<KeyPress>', self.__on_key_press_event)
        self.window.bind('<KeyRelease>', self.__on_key_release_event)

        self.__continue_update = True
        self.window.after(10, self.__upadte_widgets)

        self.window.mainloop()

    def __on_close_event(self) -> None:
        """
        Function that handles the user clicked exit event.
          * The channel with the controller itself should be closed properly, before exiting the application.
          * The UI updating thread should be stopped

        :Assumptions: None

        :return: None
        """
        self.channel.set_value(self.channel.DISTANCE_KEEPING, False)
        self.channel.set_value(self.channel.LINE_FOLLOWING, False)
        self.__continue_update = False
        self.channel.deactivate()
        self.window.destroy()

    def __ensure_connect_on_top(self):
        if self.__connect_on_top:
            self.dial.top.lift()
            self.window.after(100, self.__ensure_connect_on_top)

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
                98: self.channel.HORN,
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
        mod_switcher = defaultdict(
            lambda: 'None',
            {
                100: self.channel.DISTANCE_KEEPING,
                108: self.channel.LINE_FOLLOWING
            }
        )

        case = self.switcher[event.keysym_num]
        if event.keysym_num in [65507, 65508] and not self.__key_event_modifier['Ctrl']:
            self.__key_event_modifier['Ctrl'] = True
            self.__ctrl_pressed = True
        elif self.__ctrl_pressed and event.keysym_num not in [65507, 65508]:
            self.channel.set_value(
                mod_switcher[event.keysym_num],
                not self.channel.get_value(mod_switcher[event.keysym_num])
            )
        elif not self.__ctrl_pressed and event.keysym_num in [101, 104, 108, 113, 114]:
            self.channel.set_value(case, not self.channel.get_value(case))
        elif not self.__ctrl_pressed and not self.__key_event_modifier[case] and event.keysym_num not in [65507, 65508]:
            self.channel.set_value(case, True)
            self.__key_event_modifier[case] = True

    def __on_key_release_event(self, event: Event) -> None:
        """
        Handles the event, when the user releases a key

        :Assumption:
          * This method should only be called from the Tkinter main loop

        :param event: Contains the events object

        :return: None
        """
        if event.keysym_num in [65507, 65508]:
            self.__key_event_modifier['Ctrl'] = False
            self.__ctrl_pressed = False
        if event.keysym_num not in [97, 100, 101, 104, 108, 113, 114, 65507, 65508]:
            self.channel.set_value(self.switcher[event.keysym_num], False)
            self.__key_event_modifier[self.switcher[event.keysym_num]] = False

    def __upadte_widgets(self) -> None:
        """
        Continuously updates the UI in the background.

        :Assumptions:
          * This method is called on a separate thread, via Tkinter's after function

        :return: None
        """
        self.forward_button['background'] = \
            self.ACTIVE_ARROW_COLOR if self.channel.get_value(self.channel.FORWARD) else self.BACKGROUND_COLOR
        self.backward_button['background'] = \
            self.ACTIVE_ARROW_COLOR if self.channel.get_value(self.channel.BACKWARD) else self.BACKGROUND_COLOR
        self.left_button['background'] = \
            self.ACTIVE_ARROW_COLOR if self.channel.get_value(self.channel.LEFT) else self.BACKGROUND_COLOR
        self.right_button['background'] = \
            self.ACTIVE_ARROW_COLOR if self.channel.get_value(self.channel.RIGHT) else self.BACKGROUND_COLOR

        self.reverse_button['background'] = \
            'red' if self.channel.get_value(self.channel.REVERSE) else self.BACKGROUND_COLOR
        self.reverse_button['foreground'] = \
            self.BACKGROUND_COLOR if self.channel.get_value(self.channel.REVERSE) else 'red'

        self.light_switch['background'] = \
            '#fdff82' if self.channel.get_value(self.channel.LIGHTS) else self.BACKGROUND_COLOR

        constants = [self.channel.HAZARD_WARNING, self.channel.R_INDICATOR, self.channel.L_INDICATOR]
        for index, indicator in enumerate([self.hazard_warning, self.right_indicator, self.left_indicator]):
            indicator['background'] = \
                'yellow' if self.channel.get_value(constants[index]) else self.BACKGROUND_COLOR

        distance = self.channel.get_value(self.channel.DISTANCE)
        speed = self.channel.get_value(self.channel.SPEED)

        self.distance_label['text'] = self.DISTANCE_TEXT + str(distance) + self.DISTANCE_MES
        if distance < 10:
            bg = 'red'
        elif distance < 25:
            bg = 'yellow'
        else:
            bg = self.BACKGROUND_COLOR
        self.distance_label['background'] = bg

        self.speed_label['text'] = self.SPEED_TEXT + str(speed) + self.SPEED_MES
        if speed > 30:
            bg = 'red'
        elif speed > 20:
            bg = 'yellow'
        else:
            bg = self.BACKGROUND_COLOR
        self.speed_label['background'] = bg

        self.line_label['background'] = 'black' if self.channel.get_value(self.channel.LINE) else 'white'

        if self.__continue_update:
            self.window.after(10, self.__upadte_widgets)


if __name__ == '__main__':
    MainWindow()
