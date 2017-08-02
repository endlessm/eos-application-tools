icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = \
	com.google.Chrome/eos-google-chrome.png \
	com.spotify.Client/eos-spotify.png \
	org.videolan.VLC/eos-vlc.png \
	$(NULL)

desktopdir= $(datadir)/applications
desktop_DATA = \
	com.google.Chrome/eos-browser-appmode.desktop \
	com.google.Chrome/google-chrome.desktop \
	com.spotify.Client/eos-spotify.desktop \
	org.videolan.VLC/eos-vlc.desktop \
	$(NULL)

dist_bin_SCRIPTS = \
	com.google.Chrome/eos-browser-appmode \
	$(NULL)

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = \
	com.google.Chrome/com.endlessm.GoogleChromeInitialSetup.desktop.in \
	$(NULL)
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)

configdir = $(sysconfdir)/$(INSTALL_APP_HELPER_NAME)
config_DATA = \
	com.google.Chrome/com.google.Chrome.autoinstall.conf \
	$(NULL)

appdatadir = $(datadir)/appdata
appdata_DATA = \
	com.google.Chrome/eos-google-chrome-helper.appdata.xml \
	com.spotify.Client/eos-spotify.appdata.xml \
	org.videolan.VLC/eos-vlc.appdata.xml \
	$(NULL)

postinstalldir = $(datadir)/$(INSTALL_APP_HELPER_NAME)/postinstall
postinstall_DATA = \
	com.google.Chrome/com.google.Chrome.postinstall \
	$(NULL)

do_edit = sed \
	-e "s|\@appinstallhelper\@|$(INSTALL_APP_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|"

%.desktop: %.desktop.in Makefile
	$(MKDIR_P) $(dir $@) && \
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
	$(icon64_DATA) \
	$(desktop_DATA) \
	$(autostart_in_files) \
	$(config_DATA) \
	$(appdata_DATA) \
	$(postinstall_DATA) \
	$(NULL)

CLEANFILES = \
	$(autostart_DATA) \
	$(NULL)

install-data-hook:
	chmod +x $(DESTDIR)$(postinstalldir)/com.google.Chrome.postinstall
