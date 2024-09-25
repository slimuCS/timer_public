import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QFontDatabase

# =========================
# Font and Color Variables
# =========================

# Font Family Name (Ensure it's the correct name as per your system)
DIGITAL_FONT_FAMILY = 'DSEG7 Classic'  # Update with the exact font family name

# Colors
BACKGROUND_COLOR = '#000000'       # Black background
TEXT_COLOR = '#D3D3D3'             # Gray-white text
BUTTON_COLOR = '#2DA042'           # Light green buttons
BUTTON_HOVER_COLOR = '#1F7A31'     # Darker green on hover
BUTTON_PRESSED_COLOR = '#14521F'   # Even darker green on press
COUNTDOWN_FINISH_COLOR = '#37373D' # Background color when countdown finishes

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.is_countdown = False
        self.is_running = False
        self.is_pinned = False
        self.init_ui()
        
        # Automatically execute actions when the program runs
        self.perform_initial_actions()

    def init_ui(self):
        self.setWindowTitle('Stopwatch')

        # Initialize time variables
        self.minutes = 0
        self.seconds = 0
        self.initial_minutes = 0
        self.initial_seconds = 0

        # Store digital font family name
        self.digital_font_family = DIGITAL_FONT_FAMILY

        # Create a timer object
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        # Create the time display label
        self.time_label = QLabel(self.format_time(), self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont(self.digital_font_family))
        self.time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.time_label.setContentsMargins(0, 0, 0, 0)

        # Create buttons
        self.start_pause_button = QPushButton('S', self)
        self.reset_button = QPushButton('Re', self)
        self.mode_button = QPushButton('SCD', self)
        self.pin_button = QPushButton('x', self)
        self.pin_button.setCheckable(True)
        self.pin_button.clicked.connect(self.toggle_pin)

        # Connect buttons to functions
        self.start_pause_button.clicked.connect(self.start_pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.mode_button.clicked.connect(self.switch_mode)

        # Arrange widgets using layouts
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(5)
        vbox.addWidget(self.time_label)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.setContentsMargins(0, 0, 0, 0)
        hbox_buttons.setSpacing(5)  # Some spacing between buttons

        # Set button size policies
        self.start_pause_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.mode_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.pin_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        hbox_buttons.addWidget(self.start_pause_button)
        hbox_buttons.addWidget(self.reset_button)
        hbox_buttons.addWidget(self.mode_button)
        hbox_buttons.addWidget(self.pin_button)

        vbox.addLayout(hbox_buttons)
        self.setLayout(vbox)

        # Apply initial styling
        self.apply_stylesheet(BACKGROUND_COLOR)

    def perform_initial_actions(self):
        # Schedule the button presses after the event loop starts
        QTimer.singleShot(0, self.press_scd)

    def press_scd(self):
        self.mode_button.click()  # Press "SCD" button
        QTimer.singleShot(100, self.press_sc)

    def press_sc(self):
        self.mode_button.click()  # Press "SC" button
        QTimer.singleShot(100, self.press_x)

    def press_x(self):
        self.pin_button.click()  # Press "x" button (pin button)
        QTimer.singleShot(100, self.press_o)

    def press_o(self):
        self.pin_button.click()  # Press "o" button (pin button again)

    def format_time(self):
        return f"{self.minutes:02d}:{self.seconds:02d}"

    def update_time(self):
        if not self.is_countdown:
            # Count up
            self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1
        else:
            # Countdown
            if self.seconds == 0 and self.minutes == 0:
                self.timer.stop()
                self.start_pause_button.setEnabled(False)
                self.is_running = False
                self.countdown_finished()
            else:
                if self.seconds == 0:
                    self.seconds = 59
                    self.minutes -= 1
                else:
                    self.seconds -= 1
        self.update_time_display()

    def countdown_finished(self):
        # Change background color when countdown finishes
        self.apply_stylesheet(COUNTDOWN_FINISH_COLOR)

    def start_pause_timer(self):
        if not self.is_running:
            # Start the timer
            if self.is_countdown and hasattr(self, 'time_input'):
                self.update_countdown_time()
                self.time_input.setReadOnly(True)
                self.time_input.setCursorPosition(0)
            self.timer.start(1000)
            self.start_pause_button.setText('P')
            self.is_running = True
            self.mode_button.setEnabled(False)
            self.pin_button.setEnabled(False)
        else:
            # Pause the timer
            self.timer.stop()
            self.start_pause_button.setText('S')
            self.is_running = False
            self.mode_button.setEnabled(True)
            self.pin_button.setEnabled(True)

    def reset_timer(self):
        self.timer.stop()
        if self.is_countdown:
            self.minutes = self.initial_minutes
            self.seconds = self.initial_seconds
            if hasattr(self, 'time_input'):
                self.time_input.setReadOnly(False)
            # Reset background color
            self.apply_stylesheet(BACKGROUND_COLOR)
        else:
            self.minutes = 0
            self.seconds = 0
        self.update_time_display()
        self.start_pause_button.setText('S')
        self.start_pause_button.setEnabled(True)
        self.is_running = False
        self.mode_button.setEnabled(True)
        self.pin_button.setEnabled(True)

    def switch_mode(self):
        if self.is_countdown:
            # Switch to Count mode
            self.is_countdown = False
            self.mode_button.setText('SCD')

            # Replace time_input with time_label
            self.layout().removeWidget(self.time_input)
            self.time_input.deleteLater()
            self.time_label = QLabel(self.format_time(), self)
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setFont(QFont(self.digital_font_family))
            self.time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout().insertWidget(0, self.time_label)
        else:
            # Switch to Countdown mode
            self.is_countdown = True
            self.mode_button.setText('SC')

            # Replace time_label with time_input
            self.layout().removeWidget(self.time_label)
            self.time_label.deleteLater()
            self.time_input = QLineEdit(self.format_time(), self)
            self.time_input.setAlignment(Qt.AlignCenter)
            self.time_input.setFont(QFont(self.digital_font_family))
            self.time_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.time_input.setContentsMargins(0, 0, 0, 0)
            self.time_input.setFrame(False)
            self.time_input.returnPressed.connect(self.update_countdown_time)
            self.layout().insertWidget(0, self.time_input)

            # Set initial countdown time
            self.minutes = 5
            self.seconds = 0
            self.initial_minutes = self.minutes
            self.initial_seconds = self.seconds
            self.time_input.setText(self.format_time())

        # Reset timer and buttons
        self.reset_timer()

        # Adjust font size after switching modes
        self.adjust_font_size()

    def update_countdown_time(self):
        text = self.time_input.text()
        try:
            minutes, seconds = map(int, text.split(':'))
            if 0 <= minutes and 0 <= seconds < 60:
                self.minutes = minutes
                self.seconds = seconds
                self.initial_minutes = minutes
                self.initial_seconds = seconds
            else:
                raise ValueError
        except ValueError:
            # Invalid input, reset to previous time
            self.time_input.setText(self.format_time())

    def update_time_display(self):
        time_text = self.format_time()
        if self.is_countdown and hasattr(self, 'time_input'):
            self.time_input.setText(time_text)
        else:
            self.time_label.setText(time_text)

    def adjust_font_size(self):
        width = self.size().width()
        height = self.size().height()
        font_size = int(min(width, height) * 0.6)  # Changed to 0.6
        if self.is_countdown and hasattr(self, 'time_input'):
            self.time_input.setStyleSheet(f"""
                font-size: {font_size}px;
                border: none;
                padding: 0px;
                margin: 0px;
                color: {TEXT_COLOR};
                background-color: transparent;
            """)
        else:
            self.time_label.setStyleSheet(f"""
                font-size: {font_size}px;
                border: none;
                padding: 0px;
                margin: 0px;
                color: {TEXT_COLOR};
                background-color: transparent;
            """)

    def resizeEvent(self, event):
        self.adjust_font_size()
        super().resizeEvent(event)

    def toggle_pin(self):
        current_size = self.size()
        if self.pin_button.isChecked():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.is_pinned = True
            self.pin_button.setText('o')
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.is_pinned = False
            self.pin_button.setText('x')
        self.resize(current_size)
        self.show()

    def showEvent(self, event):
        super().showEvent(event)
        screen = self.screen()
        screen_geometry = screen.availableGeometry()
        window_size = self.size()
        x = screen_geometry.width() - window_size.width()
        y = 0
        self.move(x, y)

    def apply_stylesheet(self, background_color):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {background_color};
            }}
            QLabel, QLineEdit {{
                color: {TEXT_COLOR};
                padding: 0px;
                margin: 0px;
                border: none;
            }}
            QPushButton {{
                background-color: {BUTTON_COLOR};
                color: #FFFFFF;
                font-size: 16px;
                border-radius: 5px;
                padding: 2px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {BUTTON_PRESSED_COLOR};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        """)

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())