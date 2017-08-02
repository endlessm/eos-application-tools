polkit_policydir = $(datadir)/polkit-1/actions
polkit_policy_in_files = com.endlessm.AppInstallHelper.system-helper.policy.in
polkit_policy_DATA = $(polkit_policy_in_files:.policy.in=.policy)

do_edit = sed \
	-e "s|\@appinstallhelper\@|$(INSTALL_APP_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|"

%.policy: %.policy.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
	$(polkit_policy_in_files) \
	$(NULL)

CLEANFILES = \
	$(polkit_policy_DATA) \
	$(NULL)
