#!/usr/bin/env python3

import sys
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk, GLib, AppIndicator3
import shared
import service
import xinterface
import manager
import gtkui
from comun import ICON_ACTIVED_LIGHT, ICON_PAUSED_LIGHT
from comun import ICON_ACTIVED_DARK, ICON_PAUSED_DARK, _


class Indicator(object):

    def __init__(self):

        self.indicator = AppIndicator3.Indicator.new(
            'xpander',
            '',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.manager_ui = gtkui.ManagerUI()
        self.manager_ui.connect('saved_config', self.load_preferences)
        self.load_preferences()
        Gtk.main()

    def build_menu(self):

        menu = Gtk.Menu()
        shared.menu_toggle_service = Gtk.CheckMenuItem(_('Pause Expansion'))
        shared.menu_toggle_service.connect('toggled', self.toggle_service)
        shared.menu_show_manager = Gtk.MenuItem(_('Manager'))
        shared.menu_show_manager.connect('activate', self.show_manager)
        menu_quit = Gtk.MenuItem(_('Quit'))
        menu_quit.connect('activate', self.quit)
        menu.append(shared.menu_toggle_service)
        menu.append(shared.menu_show_manager)
        menu.append(menu_quit)
        menu.show_all()
        return menu

    def toggle_service(self, menu_item):

        shared.service.toggle_service()
        if shared.service_running:
            GLib.idle_add(self.indicator.set_icon, self.icon_actived)
        else:
            GLib.idle_add(self.indicator.set_icon, self.icon_paused)

    def show_manager(self, menu_item):

        if not shared.manager_shown:
            self.manager_ui.show_all()
            shared.manager_shown = True
        else:
            self.manager_ui.hide()
            shared.manager_shown = False

    def quit(self, menu_item):

        shared.interface.stop()
        shared.service.stop()
        Gtk.main_quit()
        # If Gtk throws an error or just a warning, main_quit() might not
        # actually close the app
        sys.exit(0)

    def load_preferences(self, *args):
        if shared.config['indicator_theme_light']:
            self.icon_actived = ICON_ACTIVED_LIGHT
            self.icon_paused = ICON_PAUSED_LIGHT
        else:
            self.icon_actived = ICON_ACTIVED_DARK
            self.icon_paused = ICON_PAUSED_DARK
        if shared.service_running:
            GLib.idle_add(self.indicator.set_icon, self.icon_actived)
        else:
            GLib.idle_add(self.indicator.set_icon, self.icon_paused)


def main():
    shared.service = service.Service()
    shared.interface = xinterface.Interface()
    shared.cmanager = manager.Config()
    shared.pmanager = manager.Phrases()

    shared.service.start()
    shared.interface.start()
    shared.service.grab_hotkeys()
    Indicator()


if __name__ == '__main__':
    main()
