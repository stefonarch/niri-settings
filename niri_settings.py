#!/usr/bin/env python3

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo

from ui import SettingsWindow

APP_VERSION = "25.12"

def main():

    if "--version" in sys.argv or "-v" in sys.argv:
            print(f"niri-settings {APP_VERSION}")
            return

    app = QApplication(sys.argv)
    app.setDesktopFileName("niri-settings")

    # Setup translator with XDG_DATA_DIRS lookup
    locale = QLocale.system().name()  # e.g., "it_IT"
    language_only = locale.split('_')[0]  # e.g., "it"

    translator = QTranslator()
    translation_loaded = False

    # Get XDG_DATA_DIRS from environment with fallback
    xdg_data_dirs = os.environ.get('XDG_DATA_DIRS', '/usr/local/share/:/usr/share/')
    data_dirs = xdg_data_dirs.split(':')

    # Try both full locale and language-only versions
    locale_variants = [locale, language_only]

    qt_translator = QTranslator()
    qt_translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if qt_translator.load(f"qt_{language_only}", qt_translations_path):
        app.installTranslator(qt_translator)

    for locale_var in locale_variants:
        for data_dir in data_dirs:
            trans_path = os.path.join(data_dir, "niri-settings", "translations", f"niri_settings_{locale_var}.qm")
            if os.path.exists(trans_path) and translator.load(trans_path):
                app.installTranslator(translator)
                print(f"Loaded translation: {trans_path}")
                translation_loaded = True
                break

    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
