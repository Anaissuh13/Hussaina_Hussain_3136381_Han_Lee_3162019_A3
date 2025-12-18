from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox,
                             QDialog, QFrame, QScrollArea, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont
import sys

from game_logic import Game21


class WelcomeOverlay(QWidget):
    """Welcome overlay that displays at the start of each game"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel("Welcome to Game of 21!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 32pt;
            font-weight: bold;
            color: white;
            padding: 20px;
        """)

        subtitle = QLabel("Get as close to 21 as possible without going over!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16pt;
            color: #ecf0f1;
            padding: 10px;
        """)

        layout.addWidget(welcome_label)
        layout.addWidget(subtitle)

        self.setLayout(layout)


class RulesDialog(QDialog):
    """Dialog displaying game rules with theme-appropriate styling"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Rules")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        #Apply object name for CSS styling
        self.setObjectName("rulesDialog")

        layout = QVBoxLayout()

        #Rules text with object name for styling
        rules_text = QLabel()
        rules_text.setObjectName("rulesText")
        rules_text.setWordWrap(True)
        rules_text.setTextFormat(Qt.TextFormat.RichText)
        rules_text.setText("""
            <h2>How to Play Game of 21</h2>

            <h3>Objective:</h3>
            <p>Get a hand value as close to 21 as possible without going over (busting).</p>

            <h3>Card Values:</h3>
            <ul>
                <li><b>Number cards (2-10):</b> Face value</li>
                <li><b>Face cards (J, Q, K):</b> Worth 10 points</li>
                <li><b>Ace:</b> Worth 11 or 1 (automatically adjusted to help you)</li>
            </ul>

            <h3>Gameplay:</h3>
            <ol>
                <li>You and the dealer each receive 2 cards</li>
                <li>Your cards are face up; dealer has one card face down</li>
                <li><b>Hit:</b> Take another card (you can hit multiple times)</li>
                <li><b>Stand:</b> End your turn with your current hand</li>
                <li>If you go over 21, you bust and lose immediately</li>
                <li>After you stand, dealer reveals their hidden card</li>
                <li>Dealer must hit on 16 or less, stand on 17 or more</li>
            </ol>

            <h3>Winning:</h3>
            <ul>
                <li>Highest hand ≤ 21 wins</li>
                <li>If dealer busts, you win</li>
                <li>Equal totals = Push (tie)</li>
            </ul>
        """)

        scroll = QScrollArea()
        scroll.setWidget(rules_text)
        scroll.setWidgetResizable(True)
        scroll.setObjectName("rulesScroll")

        close_button = QPushButton("Got It!")
        close_button.setObjectName("rulesButton")
        close_button.clicked.connect(self.accept)

        layout.addWidget(scroll)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ResultDialog(QDialog):
    """Dialog showing game results at the end of each round"""

    def __init__(self, result_message, player_total, dealer_total, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Round Complete!")
        self.setModal(True)
        self.setMinimumWidth(400)
        #Apply object name for theme-based styling
        self.setObjectName("resultDialog")

        layout = QVBoxLayout()

        #Result message label with object name for CSS styling
        result_label = QLabel(result_message)
        result_label.setObjectName("resultLabel")
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setWordWrap(True)

        #Score display label with object name for CSS styling
        scores = QLabel(f"Your Total: {player_total}\nDealer Total: {dealer_total}")
        scores.setObjectName("scoresLabel")
        scores.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()

        #Play again button with inline styling
        play_again_button = QPushButton("Play Another Round")
        play_again_button.clicked.connect(self.accept)
        play_again_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)

        #Quit button with inline styling
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.reject)
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        button_layout.addWidget(play_again_button)
        button_layout.addWidget(quit_button)

        layout.addWidget(result_label)
        layout.addWidget(scores)
        layout.addLayout(button_layout)

        self.setLayout(layout)


class SlidingSidebar(QFrame):
    """Sliding sidebar panel with game options"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("slidingSidebar")
        self.setFixedWidth(250)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        rules_btn = QPushButton("View Rules")
        rules_btn.setObjectName("sidebarButton")
        rules_btn.clicked.connect(self.show_rules)
        layout.addWidget(rules_btn)

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setObjectName("separator")
        layout.addWidget(separator1)

        font_label = QLabel("Font Size")
        font_label.setObjectName("sectionLabel")
        layout.addWidget(font_label)

        self.font_button_group = QButtonGroup(self)
        #Only 3 font sizes: Small, Medium, Large (no X-Large)
        font_sizes = [("Small (10pt)", 10), ("Medium (12pt)", 12), ("Large (14pt)", 14)]

        for text, size in font_sizes:
            rb = QRadioButton(text)
            rb.setObjectName("fontRadioButton")
            rb.size_value = size
            self.font_button_group.addButton(rb)
            layout.addWidget(rb)
            if size == 12:
                rb.setChecked(True)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setObjectName("separator")
        layout.addWidget(separator2)

        theme_label = QLabel("Theme")
        theme_label.setObjectName("sectionLabel")
        layout.addWidget(theme_label)

        self.theme_button_group = QButtonGroup(self)
        themes = [("Light", "light"), ("Dark", "dark"), ("High Contrast", "high_contrast")]

        for text, theme in themes:
            rb = QRadioButton(text)
            rb.setObjectName("themeRadioButton")
            rb.theme_value = theme
            self.theme_button_group.addButton(rb)
            layout.addWidget(rb)
            if theme == "light":
                rb.setChecked(True)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setObjectName("separator")
        layout.addWidget(separator3)

        new_game_btn = QPushButton("New Game")
        new_game_btn.setObjectName("newGameButton")
        new_game_btn.clicked.connect(self.request_new_game)
        layout.addWidget(new_game_btn)

        layout.addStretch()

        self.setLayout(layout)

    def show_rules(self):
        dialog = RulesDialog(self)
        dialog.exec()

    def request_new_game(self):
        #Shows confirmation dialog before starting new game
        reply = QMessageBox.question(
            self,
            "New Game",
            "Start a new game? Current round will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            #Get reference to main window and call new round
            main_window = self.window()
            if hasattr(main_window, 'on_new_round'):
                main_window.on_new_round()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of 21")
        self.setGeometry(200, 200, 1000, 700)
        self.setMinimumSize(900, 650)

        #Settings for font size and theme
        self.current_font_size = 12  #Default medium font
        self.current_theme = 'light'  #Start with light theme
        self.sidebar_visible = False  #Sidebar starts hidden

        #Create game instance - handles all game logic
        self.game = Game21()

        #Initialize UI components
        self.initUI()
        #Apply initial theme styling
        self.apply_theme()

        #Show welcome message after UI is ready (100ms delay)
        QTimer.singleShot(100, self.show_welcome)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        #Top ribbon with stats and menu button
        ribbon = QFrame()
        ribbon.setObjectName("statsRibbon")
        ribbon.setFixedHeight(50)
        ribbon_layout = QHBoxLayout()
        ribbon_layout.setContentsMargins(10, 5, 10, 5)

        self.menu_button = QPushButton("☰ Game Menu")
        self.menu_button.setObjectName("menuButton")
        self.menu_button.clicked.connect(self.toggle_sidebar)
        ribbon_layout.addWidget(self.menu_button)

        self.stats_label = QLabel("Games: 0 | Player Wins: 0 | Dealer Wins: 0 | Ties: 0")
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ribbon_layout.addWidget(self.stats_label, 1)

        ribbon.setLayout(ribbon_layout)
        main_layout.addWidget(ribbon)

        #Content area with sidebar
        content_container = QWidget()
        content_container_layout = QHBoxLayout()
        content_container_layout.setContentsMargins(0, 0, 0, 0)
        content_container_layout.setSpacing(0)
        content_container.setLayout(content_container_layout)

        #Sidebar
        self.sidebar = SlidingSidebar(content_container)
        self.sidebar.hide()

        for button in self.sidebar.font_button_group.buttons():
            button.clicked.connect(lambda: self.change_font_size())

        for button in self.sidebar.theme_button_group.buttons():
            button.clicked.connect(lambda: self.change_theme())

        content_container_layout.addWidget(self.sidebar)

        #Game area
        game_widget = QWidget()
        game_widget.setObjectName("gameArea")
        game_layout = QVBoxLayout()
        game_layout.setContentsMargins(20, 20, 20, 20)
        game_layout.setSpacing(15)
        game_widget.setLayout(game_layout)

        #Dealer Section
        dealer_section = QFrame()
        dealer_section.setObjectName("dealerSection")
        dealer_layout = QVBoxLayout()
        dealer_layout.setSpacing(8)

        dealer_header = QLabel("Dealer")
        dealer_header.setObjectName("sectionHeader")
        dealer_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dealer_layout.addWidget(dealer_header)

        self.dealer_total_label = QLabel("Total: ?")
        self.dealer_total_label.setObjectName("totalLabel")
        self.dealer_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dealer_layout.addWidget(self.dealer_total_label)

        self.dealerCardsLayout = QHBoxLayout()
        self.dealerCardsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dealerCardsLayout.setSpacing(8)
        dealer_layout.addLayout(self.dealerCardsLayout)

        dealer_section.setLayout(dealer_layout)
        game_layout.addWidget(dealer_section)

        #Player Section
        player_section = QFrame()
        player_section.setObjectName("playerSection")
        player_layout = QVBoxLayout()
        player_layout.setSpacing(8)

        player_header = QLabel("Player")
        player_header.setObjectName("sectionHeader")
        player_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_layout.addWidget(player_header)

        self.player_total_label = QLabel("Total: 0")
        self.player_total_label.setObjectName("totalLabel")
        self.player_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_layout.addWidget(self.player_total_label)

        self.playerCardsLayout = QHBoxLayout()
        self.playerCardsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.playerCardsLayout.setSpacing(8)
        player_layout.addLayout(self.playerCardsLayout)

        player_section.setLayout(player_layout)
        game_layout.addWidget(player_section)

        #Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.hit_button = QPushButton("Hit")
        self.hit_button.setObjectName("hitButton")
        self.hit_button.clicked.connect(self.on_hit)

        self.stand_button = QPushButton("Stand")
        self.stand_button.setObjectName("standButton")
        self.stand_button.clicked.connect(self.on_stand)

        button_layout.addStretch()
        button_layout.addWidget(self.hit_button)
        button_layout.addWidget(self.stand_button)
        button_layout.addStretch()

        game_layout.addLayout(button_layout)
        game_layout.addStretch()

        content_container_layout.addWidget(game_widget, 1)

        main_layout.addWidget(content_container, 1)

        #Welcome overlay
        self.welcome_overlay = WelcomeOverlay(central_widget)
        self.welcome_overlay.setGeometry(central_widget.rect())
        self.welcome_overlay.hide()

    def toggle_sidebar(self):
        """Toggle sidebar visibility with animation"""
        if self.sidebar_visible:
            self.sidebar.hide()
            self.sidebar_visible = False
        else:
            self.sidebar.show()
            self.sidebar_visible = True

    def show_welcome(self):
        self.welcome_overlay.setGeometry(self.centralWidget().rect())
        self.welcome_overlay.show()
        self.welcome_overlay.raise_()
        QTimer.singleShot(3000, self.start_game_after_welcome)

    def start_game_after_welcome(self):
        self.welcome_overlay.hide()
        self.welcome_overlay.setParent(None)
        self.welcome_overlay.deleteLater()
        #Mark overlay as deleted to prevent access after deletion
        self.welcome_overlay = None
        self.new_round_setup()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        #Only update overlay if it still exists and hasn't been deleted
        if hasattr(self, 'welcome_overlay') and self.welcome_overlay is not None:
            self.welcome_overlay.setGeometry(self.centralWidget().rect())

    def on_hit(self):
        #Player requests another card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)

        #Update displayed total
        player_total = self.game.player_total()
        self.player_total_label.setText(f"Total: {player_total}")

        #Check if player busted (went over 21)
        if player_total > 21:
            #Reveal dealer cards and end round
            self.reveal_all_and_end()
            #Get result message from game logic
            result = self.game.decide_winner()
            #Update win/loss statistics
            self.update_statistics()
            #Show result dialog to player
            self.show_result_dialog(result)

    def on_stand(self):
        #Player ends their turn - dealer now plays

        #Reveal dealer's hidden card
        self.game.reveal_dealer_card()
        self.update_dealer_cards(full=True)

        #Dealer automatically plays (hits until 17+)
        self.game.play_dealer_turn()
        #Update display with any new dealer cards
        self.update_dealer_cards(full=True)

        #Determine who won the round
        result = self.game.decide_winner()
        #Update win/loss/tie statistics
        self.update_statistics()
        #Disable action buttons (round is over)
        self.end_round()

        #Show result to player
        self.show_result_dialog(result)

    def on_new_round(self):
        #Start a fresh round of the game
        self.game.new_round()
        self.new_round_setup()

    def show_result_dialog(self, result_message):
        #Show result dialog at end of round with proper handling
        player_total = self.game.player_total()
        dealer_total = self.game.dealer_total()

        dialog = ResultDialog(result_message, player_total, dealer_total, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            #User clicked "Play Another Round" - start new round
            self.on_new_round()
        else:
            #User clicked "Quit" - close application
            QApplication.quit()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def add_card(self, layout, card_text):
        label = QLabel(card_text)
        label.setObjectName("cardLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

    def update_dealer_cards(self, full=False):
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, "🂠")
            else:
                self.add_card(self.dealerCardsLayout, card)

        if full:
            self.dealer_total_label.setText(f"Total: {self.game.dealer_total()}")
        else:
            self.dealer_total_label.setText("Total: ?")

    def new_round_setup(self):
        self.player_total_label.setText("Total: 0")
        self.dealer_total_label.setText("Total: ?")

        self.clear_layout(self.playerCardsLayout)
        self.clear_layout(self.dealerCardsLayout)

        self.game.deal_initial_cards()

        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)

        self.player_total_label.setText(f"Total: {self.game.player_total()}")
        self.update_dealer_cards(full=False)

        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)

    def end_round(self):
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    def reveal_all_and_end(self):
        self.game.reveal_dealer_card()
        self.update_dealer_cards(full=True)
        self.end_round()

    def update_statistics(self):
        stats = self.game.get_statistics()
        self.stats_label.setText(
            f"Games: {stats['total_games']} | "
            f"Player Wins: {stats['player_wins']} | "
            f"Dealer Wins: {stats['dealer_wins']} | "
            f"Ties: {stats['pushes']}"
        )

    def change_font_size(self):
        """Change font size based on selection - properly updates all text"""
        selected = self.sidebar.font_button_group.checkedButton()
        if selected and hasattr(selected, 'size_value'):
            self.current_font_size = selected.size_value
            #Create new font with selected size
            app_font = QFont()
            app_font.setPointSize(self.current_font_size)
            #Apply to entire application
            QApplication.instance().setFont(app_font)
            #Force update of all widgets
            self.update()

    def change_theme(self):
        """Change theme based on selection - properly updates styling"""
        selected = self.sidebar.theme_button_group.checkedButton()
        if selected and hasattr(selected, 'theme_value'):
            self.current_theme = selected.theme_value
            self.apply_theme()

    def apply_theme(self):
        try:
            if self.current_theme == 'light':
                stylesheet_path = 'light_theme.css'
            elif self.current_theme == 'dark':
                stylesheet_path = 'dark_theme.css'
            else:
                stylesheet_path = 'high_contrast_theme.css'

            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print(f"Warning: Could not find {stylesheet_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())