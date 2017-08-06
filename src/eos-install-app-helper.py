#!/usr/bin/python3
#
# eos-install-app-helper: helper script to install/launch an App.
#
# Copyright (C) 2016, 2017 Endless Mobile, Inc.
# Authors:
#  Mario Sanchez Prada <mario@endlessm.com>
#  Sam Spilsbury <sam@endlessm.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import argparse
import logging
import os
import subprocess
import sys

import config
import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak
from gi.repository import Gio
from gi.repository import GLib
from systemd import journal


def exit_with_error(message):
    logging.error(message)
    sys.exit(1)


class InstallAppHelperLauncher:
    def __init__(self,
                 app_id,
                 remote,
                 params):
        self._params = params
        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Could not find current system installation: {}".format(repr(e)))

        self._start(app_id, remote)

    def _start(self, app_id, remote):
        is_installed = self._is_flatpak_installed(app_id)
        if is_installed:
            logging.info("Flatpak for {} found. Launching...".format(app_id))
            self._run_app(app_id, self._params)
        else:
            logging.info("Could not find flatpak for {}. Running installation script...".format(app_id))
            self._install_app_id(app_id,
                                 remote)

    def _run_app(self, app_id, params):
        logging.info("Launching {} flatpak app through desktop file".format(app_id))
        desktop_id = app_id + '.desktop'
        desktop_info = Gio.DesktopAppInfo.new(desktop_id)
        if desktop_info:
            try:
                desktop_info.launch()
            except GLib.Error as e:
                exit_with_error("Could not launch {}: {}".format(app_id, repr(e)))
        else:
           exit_with_error("Could not find desktop file for {}".format(app_id))

    def _install_app_id(self,
                        app_id,
                        remote):
        try:
            subprocess.Popen([os.path.join(config.PKG_DATADIR, 'eos-install-app-helper-installer.py'),
                              '--app-id', app_id,
                              '--remote', remote])
        except OSError as e:
            exit_with_error("Could not launch {}: {}".format(app_id, repr(e)))

    def _is_flatpak_installed(self, app_id):
        try:
            self._installation.get_current_installed_app(app_id, None)
            return True
        except GLib.Error:
            logging.info("{} application is not installed".format(app_id))
            return False

    def _get_app_flatpak_launcher(self, app_id, launcher_name):
        app = None
        try:
            app = self._installation.get_current_installed_app(app_id, None)
        except GLib.Error:
            logging.info("{} application is not installed".format(app_id))
            return None

        app_path = app.get_deploy_dir()
        if not app_path or not os.path.exists(app_path):
            exit_with_error("Could not find {}'s application directory".format(app_id))

        app_launcher_path = os.path.join(app_path, 'files', 'bin', launcher_name)
        if not os.path.exists(app_launcher_path):
            exit_with_error("Could not find flatpak launcher for {}".format(app_id))

        logging.info("Found flatpak launcher for {}: %{}".format(app_id, repr(app_launcher_path)))
        return app_launcher_path


if __name__ == '__main__':
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--app-id', dest='app_id', help='Flatpak App ID', type=str, required=True)
    parser.add_argument('--remote', dest='remote', help='Flatpak Remote', type=str, required=True)
    parser.add_argument('--required-archs', dest='required_archs', default=[], nargs='*', type=str)

    parsed_args, otherargs = parser.parse_known_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    # Some apps are only available for certain architectures
    if parsed_args.required_archs and Flatpak.get_default_arch() not in parsed_args.required_archs:
        exit_with_error("Found installation of unsupported architecture: {}".format(parsed_args.required_archs))

    InstallAppHelperLauncher(parsed_args.app_id,
                             parsed_args.remote,
                             otherargs)
    sys.exit(0)
