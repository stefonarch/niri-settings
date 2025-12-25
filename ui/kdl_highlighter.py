from PyQt6.QtWidgets import (QApplication)
from PyQt6.QtCore import Qt, QFile, QRegularExpression
from PyQt6.QtGui import QPalette, QColor,QSyntaxHighlighter, QTextCharFormat

class KdlHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []
        self.init_formats()

        # Connect to palette changes
        app = QApplication.instance()
        app.paletteChanged.connect(self.handle_palette_change)

        # Store connection for potential cleanup
        self._connected = True

    def handle_palette_change(self, palette):
        """Reinitialize colors when the application palette changes."""
        self.init_formats()
        self.rehighlight()

    def cleanup(self):
        """Optional cleanup method for explicit disconnection."""
        if hasattr(self, '_connected') and self._connected:
            app = QApplication.instance()
            app.paletteChanged.disconnect(self.handle_palette_change)
            self._connected = False

    def __del__(self):
        """Fallback cleanup when object is garbage collected."""
        self.cleanup()

    def init_formats(self):
        """(Re)create all formatting rules based on the current palette."""
        self.rules.clear()

        base_color = QApplication.palette().color(QPalette.ColorRole.Base)
        is_dark = base_color.lightness() < 128

        if is_dark:
            string_color = QColor("lightgreen")
            keyword_color = QColor("lightblue")
            number_color = QColor("yellow")
            comment_color = QColor("lightgray")
            punctuation_color = QColor("goldenrod")
        else:
            string_color = QColor("blue")
            keyword_color = QColor("black")
            number_color = QColor("#965500")
            comment_color = QColor("red")
            punctuation_color = QColor("darkred")

        # ----- Node Names / Identifiers -----
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(keyword_color)

        self.rules.append((
            QRegularExpression(r"\b[a-zA-Z_][a-zA-Z0-9_-]*\b"),
            keyword_format
        ))

        # ----- Strings (in double quotes) -----
        string_format = QTextCharFormat()
        string_format.setForeground(string_color)
        self.rules.append((
            QRegularExpression(r'"([^"\\]|\\.)*"'),
            string_format
        ))

        number_format = QTextCharFormat()
        number_format.setForeground(number_color)
        self.rules.append((
            QRegularExpression(r"\b-?\d+(\.\d+)?\b"),
            number_format
        ))

        comment_format = QTextCharFormat()
        comment_format.setForeground(comment_color)
        self.rules.append((
            QRegularExpression(r"//[^\n]*"),
            comment_format
        ))

        punctuation_format = QTextCharFormat()
        punctuation_format.setForeground(punctuation_color)
        self.rules.append((
            QRegularExpression(r"[{}=]"),
            punctuation_format
        ))

        pass

    def highlightBlock(self, text):
        """Apply highlighting to a block (line) of text, called automatically by Qt."""
        for pattern, format in self.rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
