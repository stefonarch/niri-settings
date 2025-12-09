#!/bin/sh
echo "Updating .qm files ..."
/usr/lib/qt6/bin/lrelease translations/niri_settings_*.ts
ls -l translations
