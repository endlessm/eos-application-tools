# eos-application-tools

# Description

This package currently contains one component:

  * eos-install-app-helper: Wrapper application to run apps that
    we recommend but cannot distribute with Endless images.

## eos-install-app-helper

This package provides system level wrapper applications to allow easily
downloading, installing and running specific apps on Endless OS.

This wrapper application does mainly two things when you click on the desktop icon:

  * If the app is not yet installed, the wrapper script opens the app's detail
    page in the App Center (GNOME Software).

  * If the app has already been installed (using flatpak as a delivery mechanism),
    the wrapper script launches the app.

All these files will be installed, exceptionally, as part of the OSTree, so that the
icon and the wrapper app are available on the desktop at any time, either to run
the app or to install it if not yet available.

## License

eos-application-tools is Copyright (C) 2016, 2017 Endless Mobile, Inc.
and is licensed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

See the COPYING file for the full version of the GNU GPLv2 license
