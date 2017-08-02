bin_SCRIPTS = eos-install-app-helper

apphelperdir = $(datadir)/$(INSTALL_APP_HELPER_NAME)

dist_apphelper_SCRIPTS = \
	eos-install-app-helper.py \
	eos-install-app-helper-installer.py \
	eos-install-app-system-helper.py \
	$(NULL)

apphelper_DATA = \
        config.py \
        $(NULL)

do_edit = sed \
	-e "s|\@appinstallhelper\@|$(INSTALL_APP_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|" \
	-e "s|\@sysconfdir\@|$(sysconfdir)|"

eos-install-app-helper: eos-install-app-helper.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

config.py: config.py.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
        config.py.in \
        eos-install-app-helper.in \
        $(NULL)

CLEANFILES = \
        config.py \
        eos-install-app-helper \
        $(NULL)

