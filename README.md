# eos-application-tools

# Description

This package currently contains two main components

  * eos-browser-tools: Endless-specific and browser-related tools
  * eos-install-app-helper: Wrapper application to run apps that
      we recommend but cannot distribute with Endless images

## eos-browser-tools

This currently provides a handler for webapp://<WM_CLASS>@<URI> URIs,
which allows us to easily run chromium in application mode by
specifying the desired WM_CLASS and final address to load in the URI.

As this handler gets installed in the OS, it can handle URLs loaded
from unsandboxed environments (e.g. Facebook, WhatsApp) as well as
those from sandboxed flatpak applications, that rely on the Flatpak's
OpenURI portal.

If Google Chrome has been installed via the App Center (which requires
having the eos-google-chrome-helper package installed), this script
will consider using it instead of Chromium if it's set as the default
browser, otherwise Chromium will be used.

## eos-install-app-helper

This package provides system level wrapper applications to allow easily
downloading, installing and running specific apps on Endless OS.

This wrapper application does mainly two things when you click on the desktop icon:

  * If the app is not yet installed, the wrapper script opens the app's detail
    page in the App Center (GNOME Software).

  * If the app has already been installed (using flatpak as a delivery mechanism),
    the wrapper script launches the app.
    In the specific case of Google Chrome, the wrapper script launches Chrome
    with its own sandbox (outside of flatpak), by calling a launcher script
    that is shipped along with the "headless" flatpak app.

For the browser integration, this package provides the following elements:
  * `eos-google-chrome`: wrapper to either launch Chrome or the App Center.
  * `eos-google-chrome.png`: icon to integrate with the desktop.
  * `google-chrome.desktop`: application information according to the Desktop Entry
  Specification, to integrate with the shell. Note that we can't name it like the
  icon (i.e. eos-google-chrome.desktop) since that way Google Chrome would not be
  able to recognize itself when running as the default browser, which would end up
  with Chromium asking to set itself as the default each time it was run.

All these files will be installed, exceptionally, as part of the OSTree, so that the
icon and the wrapper app are available on the desktop at any time, either to run
the app or to install it if not yet available.

## License

eos-application-tools is Copyright (C) 2016, 2017 Endless Mobile, Inc.
and is licensed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

See the COPYING file for the full version of the GNU GPLv2 license
