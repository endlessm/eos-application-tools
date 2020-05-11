icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = \
	com.dropbox.Client/eos-dropbox.png \
	com.endlessnetwork.MidnightmareTeddy/eos-get-com.endlessnetwork.MidnightmareTeddy.png \
	com.endlessnetwork.aqueducts/eos-get-com.endlessnetwork.aqueducts.png \
	com.endlessnetwork.dragonsapprentice/eos-get-com.endlessnetwork.dragonsapprentice.png \
	com.endlessnetwork.frogsquash/eos-get-com.endlessnetwork.frogsquash.png \
	com.endlessnetwork.missilemath/eos-get-com.endlessnetwork.missilemath.png \
	com.endlessnetwork.passage/eos-get-com.endlessnetwork.passage.png \
	com.endlessnetwork.tankwarriors/eos-get-com.endlessnetwork.tankwarriors.png \
	com.google.AndroidStudio/eos-android-studio.png \
	com.skype.Client/eos-skype.png \
	com.spotify.Client/eos-spotify.png \
	com.unity.UnityHub/eos-unity.png \
	org.videolan.VLC/eos-vlc.png \
	$(NULL)

desktop_in_files = \
	com.dropbox.Client/eos-dropbox.desktop.in \
	com.endlessnetwork.MidnightmareTeddy/eos-get-com.endlessnetwork.MidnightmareTeddy.desktop.in \
	com.endlessnetwork.aqueducts/eos-get-com.endlessnetwork.aqueducts.desktop.in \
	com.endlessnetwork.dragonsapprentice/eos-get-com.endlessnetwork.dragonsapprentice.desktop.in \
	com.endlessnetwork.frogsquash/eos-get-com.endlessnetwork.frogsquash.desktop.in \
	com.endlessnetwork.missilemath/eos-get-com.endlessnetwork.missilemath.desktop.in \
	com.endlessnetwork.passage/eos-get-com.endlessnetwork.passage.desktop.in \
	com.endlessnetwork.tankwarriors/eos-get-com.endlessnetwork.tankwarriors.desktop.in \
	com.google.AndroidStudio/eos-android-studio.desktop.in \
	com.skype.Client/eos-skype.desktop.in \
	com.spotify.Client/eos-spotify.desktop.in \
	com.unity.UnityHub/eos-unity.desktop.in \
	org.videolan.VLC/eos-vlc.desktop.in \
	us.zoom.Zoom/eos-get-us.zoom.Zoom.desktop.in \
	$(NULL)

desktopdir = $(datadir)/applications
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
$(desktop_DATA): %.desktop: %.desktop.in
	$(AM_V_GEN) $(MKDIR_P) $(dir $@) && \
	$(MSGFMT) --desktop --template $< -d $(top_srcdir)/po -o $@

appdatadir = $(datadir)/appdata
appdata_DATA = \
	com.dropbox.Client/eos-dropbox.appdata.xml \
	com.endlessnetwork.MidnightmareTeddy/eos-get-com.endlessnetwork.MidnightmareTeddy.appdata.xml \
	com.endlessnetwork.aqueducts/eos-get-com.endlessnetwork.aqueducts.appdata.xml \
	com.endlessnetwork.dragonsapprentice/eos-get-com.endlessnetwork.dragonsapprentice.appdata.xml \
	com.endlessnetwork.frogsquash/eos-get-com.endlessnetwork.frogsquash.appdata.xml \
	com.endlessnetwork.missilemath/eos-get-com.endlessnetwork.missilemath.appdata.xml \
	com.endlessnetwork.passage/eos-get-com.endlessnetwork.passage.appdata.xml \
	com.endlessnetwork.tankwarriors/eos-get-com.endlessnetwork.tankwarriors.appdata.xml \
	com.google.AndroidStudio/eos-android-studio.appdata.xml \
	com.skype.Client/eos-skype.appdata.xml \
	com.spotify.Client/eos-spotify.appdata.xml \
	com.unity.UnityHub/eos-unity.appdata.xml \
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
