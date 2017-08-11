AC_PREREQ([2.63])
AC_INIT([eos-application-tools], [1.0.2], [mario@endlessm.com])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([1.11 -Wno-portability foreign no-define tar-ustar no-dist-gzip dist-xz subdir-objects])
AM_MAINTAINER_MODE([enable])
AM_SILENT_RULES([yes])

AM_GNU_GETTEXT_VERSION([0.19.8])
AM_GNU_GETTEXT([external])

PKG_CHECK_MODULES([glib], [glib-2.0])
GLIB_GSETTINGS

AC_SUBST(INSTALL_APP_HELPER_NAME, "eos-install-app-helper")

AC_CONFIG_FILES([
Makefile
src/Makefile
apps/Makefile
po/Makefile.in
])
AC_OUTPUT

echo "
    eos-application-tools $VERSION
"
