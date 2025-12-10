#!/bin/bash
until [[ action == [123] ]]; do
    clear
    read -s -n1 -p "
    This will install niri-settings. Please select

    1. Install only for user
    2. Install system-wide
    3. Quit

    Select 1, 2, or 3
" action
    case $action in
        1)
        echo "Installing to user..."
            mkdir -p ~/bin
            mkdir -p ~/.local/share/applications

            # Install binary and .desktop file
            cp -v niri-settings ~/bin/niri-settings
            chmod a+x ~/bin/niri-settings
            cp -v niri-settings.desktop ~/.local/share/applications/

            # Install python files
            mkdir -p  ~/.local/lib/niri-settings/ui
            cp -v niri_settings.py  ~/.local/lib/niri-settings/
            cp -av ui/*.py  ~/.local/lib/niri-settings/ui

            # Install translations to standard XDG data directory
            mkdir -p ~/.local/share/niri-settings/translations
            cp -av translations/*.qm ~/.local/share/niri-settings/translations/

            # Icon
            mkdir -p ~/.local/share/icons/hicolor/scalable/apps
            cp -v niri-settings.svg ~/.local/share/icons/hicolor/scalable/apps/niri-settings.svg

            echo ""

            # Posted by tripleee on stackoverflow
            # Retrieved 2025-12-10, License - CC BY-SA 3.0
            case :$PATH:
            in *:$HOME/bin:*) ;;
                *) echo "Note: $HOME/bin is not in $PATH" >&2
                   echo ""
                   echo "You need to add it, e.g. add a line" >&2
                   echo "    'PATH=\"$HOME/bin:\$PATH\"' in ~/.profile, or ~/.zshrc" >&2
                   echo "Otherwise niri-settings cannot start." >&2 ;;
            esac
            echo "Installation finished."
        exit
        ;;
        2)
        echo "Installing to system..."

            # Install binary and .desktop file
            sudo cp -v niri-settings /usr/bin/niri-settings
            sudo chmod a+x /usr/bin/niri-settings
            sudo cp -v niri-settings.desktop /usr/share/applications/niri-settings.desktop

            # Install python files
            sudo mkdir -p /usr/lib/niri-settings/ui
            sudo cp -v niri_settings.py /usr/lib/niri-settings/
            sudo cp -av ui/*.py /usr/lib/niri-settings/ui

            # Install translations to standard XDG data directory
            sudo mkdir -p /usr/share/niri-settings/translations
            sudo cp -av translations/*.qm /usr/share/niri-settings/translations/

            # Icon
            sudo cp -v niri-settings.svg /usr/share/icons/hicolor/scalable/apps/niri-settings.svg

            echo ""
            echo "Installation finished."
        exit
    ;;
        3)
          echo "Goodbye!"
          exit
        ;;
      esac
done
