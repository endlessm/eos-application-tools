icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = \
	com.google.Chrome/eos-google-chrome.png \
	org.videolan.VLC/eos-vlc.png

desktopdir= $(datadir)/applications
desktop_DATA = \
	com.google.Chrome/google-chrome.desktop \
	org.videolan.VLC/eos-vlc.desktop \
	$(NULL)

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = \
	com.google.Chrome/com.endlessm.GoogleChromeInitialSetup.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)

configdir = $(sysconfdir)/$(INSTALL_APP_HELPER_NAME)
config_DATA = \
	com.google.Chrome/com.google.Chrome.autoinstall.conf

appdatadir = $(datadir)/appdata
appdata_DATA = \
	com.google.Chrome/eos-google-chrome-helper.appdata.xml \
	org.videolan.VLC/eos-vlc-helper.appdata.xml

postinstalldir = $(datadir)/$(INSTALL_APP_HELPER_NAME)/postinstall
postinstall_DATA = \
	com.google.Chrome/com.google.Chrome.postinstall

do_edit = sed \
	-e "s|\@appinstallhelper\@|$(INSTALL_APP_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|"

%.desktop: %.desktop.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

showdata:
	echo $(autostart_DATA)

EXTRA_DIST = \
	$(appdata_DATA) \
	$(desktop_DATA) \
	$(icon64_DATA) \
	$(autostart_in_files) \
	$(config_DATA) \
	$(NULL)

CLEANFILES = \
	$(autostart_DATA) \
	$(NULL)

install-data-hook:
	chmod +x $(DESTDIR)$(postinstalldir)/com.google.Chrome.postinstall

