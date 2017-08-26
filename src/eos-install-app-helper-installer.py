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
import logging
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


def refine_source_app(source_app_id):
    '''Ensure that the souce app is refined in the software center.

    We need to perform this step if we want the souce app's icon to be
    replaced, since going directly to an app in the app center does not
    refine the other apps.
    '''
    logging.info("Refining source app {}".format(source_app_id))
    conn = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    conn.call_sync('org.gnome.Software',
                   '/org/gnome/Software',
                   'org.gtk.Actions',
                   'Activate',
                   GLib.Variant('(sava{sv})',
                                ('refine',
                                 [GLib.Variant('(ss)',
                                  ('eos-vlc.desktop', 'all'))],
                                 {})),
                   None,
                   Gio.DBusCallFlags.NONE,
                   -1,
                   None)


class InstallAppHelperInstaller:
    def __init__(self,
                 app_id,
                 remote,
                 source_app_id):
        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Couldn't not find current system installation: %r", e)

        if self._check_app_flatpak_launcher(app_id):
            logging.info("{app_id} is already installed".format(app_id))
            return

        logging.info("Could not find flatpak launcher for {}.".format(app_id))

        self._run_app_center_for_app(app_id, remote, source_app_id)


    def _check_app_flatpak_launcher(self, app_id):
        try:
            self._installation.get_current_installed_app(app_id, None)
        except GLib.Error as e:
            logging.info("{} application is not installed".format(app_id))
            return False
        return True

    def _wait_for_installation(self, app_id):
        def _installation_finished(monitor, file_, other_file, event_type):
            if event_type != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
                return

            if self._check_app_flatpak_launcher(app_id):
                logging.info("{} has been installed".format(app_id))
                loop.quit()

        loop = GLib.MainLoop()

        monitor = self._installation.create_monitor(None)
        monitor.connect('changed', _installation_finished)

        loop.run()

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

    def _run_app_center_for_app(self, app_id, remote, source_app_id):
        # FIXME: Ideally, we should be able to pass the app ID to GNOME Software
        # and it would do the right thing by opening the page for the app's branch matching
        # the default branch for the apps' source remote. Unfortunately, this is not the case
        # at the moment and fixing it is non-trivial, so we'll construct the full unique ID
        # that GNOME Software expects, right from here, based on the remote's metadata.
        unique_id = self._get_unique_id(app_id, remote)

        logging.info("Opening App Center for {}...".format(unique_id))
        app_center_argv = ['gnome-software', '--details={}'.format(unique_id)]

        try:
            subprocess.Popen(app_center_argv)
        except OSError as e:
            exit_with_error("Could not launch {}: {}".format(app_id, repr(e)))

        if source_app_id:
            refine_source_app(source_app_id)
        self._wait_for_installation(app_id)

        if not self._check_app_flatpak_launcher(app_id):
            exit_with_error("{} isn't installed - something went wrong in GNOME Software".format(app_id))

        logging.info("{} successfully installed".format(app_id))


def main():
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--app-id', dest='app_id', help='Flatpak App ID', type=str, required=True)
    parser.add_argument('--source-app-id', dest='source_app_id', help='App ID to be replaced', type=str)
    parser.add_argument('--remote', dest='remote', help='Flatpak Remote', type=str, required=True)
    parser.add_argument('--required-archs', dest='required_archs', default=[], nargs='*', type=str)

    parsed_args = parser.parse_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    if parsed_args.required_archs and Flatpak.get_default_arch() not in parsed_args.required_archs:
        exit_with_error("Found installation of unsupported architecture: {}".format(parsed_args.required_archs))

    InstallAppHelperInstaller(parsed_args.app_id,
                              parsed_args.remote,
                              parsed_args.source_app_id)
    sys.exit(0)


if __name__ == '__main__':
    main()
