#!/usr/bin/python3
#
# eos-install-app-helper-installer: helper script to install an App
#
# Copyright (C) 2016, 2017 Endless Mobile, Inc.
# Authors:
#  Michal Rostecki <michal@kinvolk.io>
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
import config
import configparser
import logging
import os
import subprocess
import sys

import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak
from gi.repository import Gio
from gi.repository import GLib
from systemd import journal


def exit_with_error(*args):
    logging.error(*args)
    sys.exit(1)


class InstallAppHelperInstaller:
    def __init__(self,
                 app_id,
                 remote,
                 app_name,
                 old_desktop_file_name,
                 initial_setup):
        self._initial_setup = initial_setup

        if self._initial_setup:
            if not self._automatic_install_enabled(config.CONFIG_FILE.format(app_id=app_id)):
                logging.info("{} installation is disabled".format(app_name))
                sys.exit(0)

            if self._initial_setup_already_done(app_id):
                logging.info("{} automatic installation already done".format(app_name))
                sys.exit(0)

        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Couldn't not find current system installation: %r", e)

        if self._check_app_flatpak_launcher(app_id, app_name):
            logging.info("{app_name} is already installed".format(app_name))
            self._touch_done_file()
            return

        logging.info("Could not find flatpak launcher for {}.".format(app_name))

        if self._initial_setup:
            self._wait_for_network_connectivity()

        self._run_app_center_for_app(app_id,
                                     remote,
                                     app_name,
                                     old_desktop_file_name)

    def _initial_setup_already_done(self, app_id):
        if os.path.exists(config.STAMP_FILE_INITIAL_SETUP_DONE.format(app_id=app_id)):
            return True

        return False

    def _automatic_install_enabled(self, config_file_path):
        if not os.path.exists(config_file_path):
            logging.warning("Could not find configuration file at {}"
                            .format(config.CONFIG_FILE))
            return False

        is_enabled = False
        with open(config_file_path, 'r') as config_file:
            helper_config = configparser.ConfigParser(allow_no_value=True)
            try:
                helper_config.read_file(config_file)
                logging.info("Read contents from configuration file at {}\n"
                             .format(config_file_path))
            except configparser.ParsingError as e:
                logging.error("Error parsing contents from configuration file at {}: {}"
                             .format(config_file_path, str(e)))
                return False

            try:
                is_enabled = helper_config.getboolean('Initial Setup', 'AutomaticInstallEnabled')
                logging.info("AutomaticInstallEnabled = {}".format(str(is_enabled)))
            except configparser.NoOptionError:
                logging.warning("AutomaticInstallEnabled key not found in {}".format(config.CONFIG_FILE))
                return False

        return is_enabled

    def _check_app_flatpak_launcher(self, app_id, app_name):
        try:
            self._installation.get_current_installed_app(app_id, None)
        except GLib.Error as e:
            logging.info("{} application is not installed".format(app_name))
            return False
        return True

    def _is_connected_state(self):
        monitor = Gio.NetworkMonitor.get_default()
        return monitor.get_connectivity() == Gio.NetworkConnectivity.FULL

    def _wait_for_network_connectivity(self):
        def _network_changed(monitor, available, loop):
            if not available:
                logging.info("No network available")
                return

            if monitor.get_connectivity() != Gio.NetworkConnectivity.FULL:
                logging.info("Network available, but not connected to the Internet")
                return

            logging.info("Connected to the network and the internet")
            loop.quit()

        logging.info("Checking network connectivity...")
        if self._is_connected_state():
            logging.info("Network connected")
            return

        logging.info("Not connected to any network, wait for connection")

        loop = GLib.MainLoop()

        monitor = Gio.NetworkMonitor.get_default()
        monitor.connect('network-changed', _network_changed, loop)
        loop.run()

    def _wait_for_installation(self, app_id, app_name):
        def _installation_finished(monitor, file_, other_file, event_type):
            if event_type != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
                return

            if self._check_app_flatpak_launcher(app_id, app_name):
                logging.info("{} has been installed".format(app_name))
                loop.quit()

        loop = GLib.MainLoop()

        monitor = self._installation.create_monitor(None)
        monitor.connect('changed', _installation_finished)

        loop.run()

    def _run_postinstall(self, app_id, app_name):
        postinstall_executable = config.POSTINSTALL_FILE.format(app_id=app_id)
        if not os.path.exists(postinstall_executable):
            logging.info("No post-installation script for {}".format(app_name))
            return False

        logging.info("Running post-installation script for {}".format(app_name))
        subprocess.check_call([postinstall_executable])
        return True

    def _remove_old_icon(self, old_desktop_file_name):
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        proxy = Gio.DBusProxy.new_sync(bus,
                                       Gio.DBusProxyFlags.NONE,
                                       None,
                                       'org.gnome.Shell',
                                       '/org/gnome/Shell',
                                       'org.gnome.Shell.AppStore',
                                       None)
        proxy.call_sync('RemoveApplication',
                        GLib.Variant('(s)', (old_desktop_file_name, )),
                        Gio.DBusCallFlags.NO_AUTO_START, 500, None)


    def _touch_done_file(self, app_id):
        # The system-wide stamp file touched by this helper makes sure that
        # the automatic installation won't ever be performed for other users.
        system_helper_cmd = os.path.join(config.PKG_DATADIR, 'eos-install-app-system-helper.py')
        try:
            subprocess.check_call('pkexec {} --app-id {}'.format(system_helper_cmd, app_id), shell=True)
        except subprocess.CalledProcessError as e:
            exit_with_error("Couldn't run {}: {}".format(system_helper_cmd, str(e)))

    def _post_install_app(self, app_id, app_name):
        self._run_postinstall(app_id, app_name)
        self._touch_done_file(app_id)

        logging.info("Post-installation configuration done")


    def _get_unique_id(self, app_id, remote_name):
        app_app_center_id = app_id

        default_branch = None
        try:
            remote = self._installation.get_remote_by_name(remote_name)
        except GLib.Error as e:
            logging.warning("Could not find flatpak remote {}: {}".format(remote, str(e)))

        # Get the default branch now to construct the full unique ID GNOME Software expects.
        default_branch = remote.get_default_branch()
        if default_branch:
            app_app_center_id = 'system/flatpak/{}/desktop/{}.desktop/{}'.format(remote_name,
                                                                                 app_id,
                                                                                 default_branch)
        return app_app_center_id

    def _run_app_center_for_app(self,
                                app_id,
                                remote,
                                app_name,
                                old_desktop_file_name):
        # FIXME: Ideally, we should be able to pass 'com.google.{}' to GNOME Software
        # and it would do the right thing by opening the page for the app's branch matching
        # the default branch for the apps' source remote. Unfortunately, this is not the case
        # at the moment and fixing it is non-trivial, so we'll construct the full unique ID
        # that GNOME Software expects, right from here, based on the remote's metadata.
        unique_id = self._get_unique_id(app_id, remote)

        logging.info("Opening App Center for {}...".format(unique_id))
        if self._initial_setup:
            app_center_argv = ['gnome-software', '--install', unique_id, '--interaction', 'none']
        else:
            app_center_argv = ['gnome-software', '--details={}'.format(unique_id)]

        try:
            subprocess.Popen(app_center_argv)
        except OSError as e:
            exit_with_error("Could not launch {}: {}".format(app_name, repr(e)))

        self._wait_for_installation(app_id, app_name)

        if not self._check_app_flatpak_launcher(app_id, app_name):
            exit_with_error("{} isn't installed - something went wrong in GNOME Software".format(app_name))

        logging.info("{} successfully installed".format(app_name))

        # Swap out .desktop files
        self._remove_old_icon(old_desktop_file_name)

        # There's a post-install procedure for automatic installations.
        if self._initial_setup:
            self._post_install_app(app_id, app_name)


def main():
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--initial-setup', dest='initial_setup', action='store_true')
    parser.add_argument('--app-name', dest='app_name', help='Human readable app name', type=str, required=True)
    parser.add_argument('--app-id', dest='app_id', help='Flatpak App ID', type=str, required=True)
    parser.add_argument('--remote', dest='remote', help='Flatpak Remote', type=str, required=True)
    parser.add_argument('--old-desktop-file-name', dest='old_desktop_file_name', help='File name for .desktop file to remove', type=str, required=True)
    parser.add_argument('--required-archs', dest='required_archs', default=[], nargs='*', type=str)

    parsed_args = parser.parse_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    if parsed_args.required_archs and Flatpak.get_default_arch() not in parsed_args.required_archs:
        exit_with_error("Found installation of unsupported architecture: %s", app_arch)

    InstallAppHelperInstaller(parsed_args.app_id,
                              parsed_args.remote,
                              parsed_args.app_name,
                              parsed_args.old_desktop_file_name,
                              parsed_args.initial_setup)
    sys.exit(0)


if __name__ == '__main__':
    main()
