Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:	3.0.3
Release:	3%{?dist}
License:	LGPLv2 or MPLv2.0
URL:		https://libical.github.io/libical/
Source:		https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch01:	libical-3.0.3-covscan.patch

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	perl-interpreter
BuildRequires:	python3
BuildRequires:	python3-pip
BuildRequires:	python3-gobject
BuildRequires:	vala
Requires:	tzdata

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package devel
Summary:	Development files for libical
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(icu-i18n)
Requires:	pkgconfig(icu-uc)

%description devel
The libical-devel package contains libraries and header files for developing
applications that use libical.

%package glib
Summary:	GObject wrapper for libical library
Provides:	libical-glib%{?_isa} = %{version}-%{release}
Obsoletes:	libical-glib < 3.0.0
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description glib
This package provides a GObject wrapper for libical library with support
of GObject Introspection.

%package glib-doc
Summary:	Documentation files for %{name}-glib
Group:		Development/Libraries
Provides:	libical-glib-doc = %{version}-%{release}
Obsoletes:	libical-glib-doc < 3.0.0
BuildArch:	noarch

%description glib-doc
This package contains developer documentation for %{name}-glib.

%package glib-devel
Summary:	Development files for building against %{name}-glib
Group:		Development/Libraries
Provides:	libical-glib-devel%{?_isa} = %{version}-%{release}
Obsoletes:	libical-glib-devel < 3.0.0
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(gobject-2.0)

%description glib-devel
Development files needed for building things which link against %{name}-glib.

%prep
%setup -q

%patch01 -p1 -b .covscan

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DUSE_INTEROPERABLE_VTIMEZONES:BOOL=true \
  -DICAL_ALLOW_EMPTY_PROPERTIES:BOOL=true \
  -DGOBJECT_INTROSPECTION:BOOL=true \
  -DICAL_GLIB:BOOL=true \
  -DICAL_GLIB_VAPI:BOOL=true \
  -DSHARED_ONLY:BOOL=true
popd

make %{?_smp_mflags} -C %{_target_platform} -j1

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
make test ARGS="-V" -C %{_target_platform}

%ldconfig_scriptlets

%files
%doc LICENSE ReadMe.txt THANKS
%{_libdir}/libical.so.3*
%{_libdir}/libical_cxx.so.3*
%{_libdir}/libicalss.so.3*
%{_libdir}/libicalss_cxx.so.3*
%{_libdir}/libicalvcal.so.3*
%{_libdir}/girepository-1.0/libical-%{version}.typelib
%{_datadir}/gir-1.0/libical-%{version}.gir

%files devel
%doc doc/UsingLibical.txt
%{_libdir}/libical.so
%{_libdir}/libical_cxx.so
%{_libdir}/libicalss.so
%{_libdir}/libicalss_cxx.so
%{_libdir}/libicalvcal.so
%{_libdir}/pkgconfig/libical.pc
%{_libdir}/cmake/LibIcal/
%{_includedir}/libical/

%files glib
%{_libdir}/libical-glib.so.3*
%{_libdir}/girepository-1.0/ICalGLib-3.0.typelib
%{_datadir}/gir-1.0/ICalGLib-3.0.gir

%files glib-devel
%{_libdir}/libical-glib.so
%{_libdir}/pkgconfig/libical-glib.pc
%{_includedir}/libical-glib/
%{_datadir}/vala/vapi/libical-glib.vapi

%files glib-doc
%{_datadir}/gtk-doc/html/%{name}-glib

%changelog
* Thu Jul 19 2018 Milan Crha <mcrha@redhat.com> - 3.0.3-3
- Update Requires of libical-glib-devel
- Address a warning found by Coverity Scan

* Mon Mar 12 2018 Christian Stadelmann <fedora@genodeftest.de> - 3.0.3-2
- Update upstream URL

* Tue Feb 27 2018 Milan Crha <mcrha@redhat.com> - 3.0.3-1
- Update to 3.0.3
- Remove patch to allow DATE-only COMPLETED property (fixed upstream)

* Tue Feb 27 2018 Milan Crha <mcrha@redhat.com> - 3.0.2-2
- Add upstream patch to allow DATE-only COMPLETED property

* Mon Feb 19 2018 Milan Crha <mcrha@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.1-3
- Switch to %%ldconfig_scriptlets

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 3.0.1-2
- Rebuild for ICU 60.1

* Mon Nov 20 2017 Milan Crha <mcrha@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Nov 06 2017 Milan Crha <mcrha@redhat.com> - 3.0.0-2
- Add a patch to Correct possible deadlock caused in icaltimezone_load_builtin_timezone()

* Mon Nov 06 2017 Milan Crha <mcrha@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Milan Crha <mcrha@redhat.com> - 2.0.0-10
- Build with -DICAL_ALLOW_EMPTY_PROPERTIES=true (#1466906)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2.0.0-8
- rebuild for ICU 57.1

* Thu Feb 11 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-7
- Add patch for possible use-after-free of icalrecurrencetype::rscale

* Mon Feb 08 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-6
- Add libicu dependency to libical-devel subpackage

* Tue Feb 02 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-5
- Build with libicu, to enable RSCALE support

* Mon Feb 01 2016 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- %%build: -DSHARED_ONLY=TRUE (#1303598)

* Fri Jan 29 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-3
- Build with -DUSE_INTEROPERABLE_VTIMEZONES=true

* Mon Jan 18 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-2
- Add patch for missing function (icallangbind_quote_as_ical_r)

* Mon Jan 18 2016 Milan Crha <mcrha@redhat.com> - 2.0.0-1
- Update to 2.0.0
- Remove patch for RH bug #1176204 (fixed upstream)
- Add patch to fix ARM build break

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Jan 12 2015 Matthias Clasen <mclasen@redhat.com> - 1.0-9
- Fix a stupid typo in the definition of icaltime_days_in_year

* Mon Dec 22 2014 Milan Crha <mcrha@redhat.com> - 1.0-8
- Add patch for RH bug #1176204 (Avoid putenv() in libical)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Rex Dieter <rdieter@fedoraproject.org> 1.0-6
- minor .spec cleanup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 21 2013 Milan Crha <mcrha@redhat.com> - 1.0-4
- Add patch to fix icalvalue_kind enum generation (RH bug #1023020)

* Sun Oct 20 2013 Robert Scheck <robert@fedoraproject.org> 1.0-3
- Fixed timezone issue with evolution-data-server (#1021136)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.0-1
- Update to 1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Robert Scheck <robert@fedoraproject.org> 0.48-1
- Upgrade to 0.48 (#664412, #696891, #743236)

* Mon Oct 24 2011 Robert Scheck <robert@fedoraproject.org> 0.47-1
- Upgrade to 0.47 (#743236)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-2
- Added patch to work around upstream's broken AC_PROG_MKDIR_P

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-1
- Upgrade to 0.46 (#525933, #628893)
- Fixed race in populating builtin timezone components (#637150)
- Fixed wrong ICAL_ERRORS_ARE_FATAL preprocessor check (#575715)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-4
- Updated patch to fix #includes in the headers to work with
  'pkg-config --cflags libical'. (Red Hat Bugzilla #484091)

* Wed Feb 25 2009 Release Engineering <rel-eng@.fedoraproject.org> - 0.43-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-2
- Added patch to fix CFLAGS in libical.pc. (Red Hat Bugzilla #484091)

* Tue Jan 13 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-1
- Version bump to 0.43.
- Added patch to fix implicit pointer conversion from Debian. (Debian BTS
  #511598)
- Upstream has switched off ICAL_ERRORS_ARE_FATAL by default. This behaviour
  is being retained across all distributions, including Fedora 11.
- Added 'Requires: tzdata'.
- Enabled backtrace dumps in the syslog.

* Thu Jan 08 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.41-2
- Switched off ICAL_ERRORS_ARE_FATAL for all distributions, except Fedora 11.
  (Red Hat Bugzilla #478331)

* Sun Nov 23 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.41-1
- Version bump to 0.41. (Red Hat Bugzilla #469252)
- Disabled C++ bindings.

* Tue Oct 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.40-1
- Version bump to 0.40. (Red Hat Bugzilla #466359)
- Add patch from upstream to fix crash in icalvalue.c.
- Update makefile patch, remove the test part (already applied).
- Package libical.pc, add Requires: pkgconfig to -devel.

* Wed Sep 03 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.32-1
- Version bump to 0.32.
- Parallel build problems fixed.

* Sun Jul 27 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-3
- Added 'BuildRequires: bison byacc flex'.

* Sun Jul 27 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.31-2
- Fixed linkage problems and disabled parallel build till upstream accepts fix.

* Thu Jul 17 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-1
- Version bump to 0.31.

* Thu Jul 17 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.30-4
- Changed value of License according to Fedora licensing guidelines.
- Enabled reentrant system calls and C++ bindings.
- Omitted unused direct shared library dependencies.
- Added ChangeLog, COPYING, LICENSE, NEWS and README to doc and dropped
  examples.

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-3
- Source URL... Fixed

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-2
- Removed untrue note about libical's homepage (to get rid of eventuall mess)

* Sat Feb 23 2008 David Nielsen <gnomeuser@gmail.com> - 0.30-1
- Switch to freeassociation libical
- bump to 0.30

* Sat Feb 09 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-5
- Mass rebuild for new GCC... Done

* Sat Jan 19 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-4
- Licence... Fixed

* Fri Jan 18 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-3
- Files section... Fixed

* Thu Jan 17 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-2
- Source... Changed
- Debug information in libical main package... Excluded
- Non-numbered .so files in libical main package... Moved
- libical-devel documentation... Added

* Mon Dec 24 2007 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-1
- Initial release
