@INTLTOOL_DESKTOP_RULE@

icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = \
	com.microsoft.Skype/eos-skype.png \
	com.spotify.Client/eos-spotify.png \
	org.videolan.VLC/eos-vlc.png \
	$(NULL)

desktopdir= $(datadir)/applications
desktop_in_files = \
	com.microsoft.Skype/eos-skype.desktop.in \
	com.spotify.Client/eos-spotify.desktop.in \
	org.videolan.VLC/eos-vlc.desktop.in \
	$(NULL)
desktop_DATA = \
	com.microsoft.Skype/eos-skype.desktop \
	com.spotify.Client/eos-spotify.desktop \
	org.videolan.VLC/eos-vlc.desktop \
	$(NULL)

appdatadir = $(datadir)/appdata
appdata_DATA = \
	com.microsoft.Skype/eos-skype.appdata.xml \
	com.spotify.Client/eos-spotify.appdata.xml \
	org.videolan.VLC/eos-vlc.appdata.xml \
	$(NULL)

EXTRA_DIST = \
	$(icon64_DATA) \
	$(desktop_in_files) \
	$(appdata_DATA) \
	$(NULL)

CLEANFILES = \
	$(desktop_DATA) \
	$(NULL)
