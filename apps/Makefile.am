icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = \
	com.dropbox.Client/eos-dropbox.png \
	com.microsoft.Skype/eos-skype.png \
	com.spotify.Client/eos-spotify.png \
	org.videolan.VLC/eos-vlc.png \
	$(NULL)

desktop_in_files = \
	com.dropbox.Client/eos-dropbox.desktop.in \
	com.microsoft.Skype/eos-skype.desktop.in \
	com.spotify.Client/eos-spotify.desktop.in \
	org.videolan.VLC/eos-vlc.desktop.in \
	$(NULL)

desktopdir = $(datadir)/applications
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
$(desktop_DATA): %.desktop: %.desktop.in
	$(AM_V_GEN) $(MKDIR_P) $(dir $@) && \
	$(MSGFMT) --desktop --template $< -d $(top_srcdir)/po -o $@

appdatadir = $(datadir)/appdata
appdata_DATA = \
	com.dropbox.Client/eos-dropbox.appdata.xml \
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
