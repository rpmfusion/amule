Name:           amule
Version:        2.3.3
Release:        10%{?dist}
Summary:        File sharing client compatible with eDonkey
License:        GPLv2+
Source0:        https://github.com/amule-project/amule/archive/%{version}/%{name}-%{version}.tar.gz
Source2:        %{name}.appdata.xml
URL:            http://amule.org
Patch0:         298.patch
Patch1:         https://git.alpinelinux.org/aports/plain/testing/amule/wxwidgets-3.2.patch
Patch2:         https://sources.debian.org/data/main/a/amule/1%3A2.3.3-3/debian/patches/wx3.2.patch

# See http://wiki.amule.org/wiki/Requirements
BuildRequires:  gcc-c++
%if 0%{?fedora} > 38
BuildRequires:  wxGTK-devel >= 3.0.5
%else
BuildRequires:  wxGTK3-devel >= 3.0.5
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  binutils-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(gdlib) >= 2.0
BuildRequires:  pkgconfig(libpng)
BuildRequires:  gettext-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(cryptopp)
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  pkgconfig(geoip)
BuildRequires:  libappstream-glib
BuildRequires:  libtool
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(ncurses)

Requires:       %{name}-nogui

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network. It is a fork of xMule, whis was based on eMule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package nogui
Summary:        Components of aMule which don't require a GUI (for servers)
Obsoletes:      xchat-amule < 2.3.2-7
Provides:       xchat-amule = 2.3.2-7

%description nogui
This package contains the aMule components which don't require a GUI.
It is useful for servers which don't have Xorg.


%prep
%autosetup -p1

%build
./autogen.sh
%configure \
    --disable-rpath \
    --disable-debug \
    --enable-wxcas \
    --enable-cas \
    --enable-alc \
    --enable-alcc \
    --enable-amule-daemon \
    --enable-amulecmd \
    --enable-webserver \
    --enable-amule-daemon \
    --enable-geoip \
    --enable-amule-gui \
    --enable-optimize \
    --enable-nls \
    --with-boost \
    --with-denoise-level=0

%make_build


%install
%make_install

%find_lang %{name}

# desktop files
desktop-file-install --vendor "" \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor "" \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop

desktop-file-install --vendor "" \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/wxcas.desktop

desktop-file-install --vendor "" \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}gui.desktop

# clean-up INSTALL file in doc
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/INSTALL
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/COPYING

install -m 0644 -D %{SOURCE2} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files -f %{name}.lang
%{_docdir}/%{name}
%license docs/COPYING
%{_bindir}/alc
%{_bindir}/amule
%{_bindir}/cas
%{_bindir}/wxcas
%{_bindir}/amulegui
%{_datadir}/%{name}
%{_datadir}/cas
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/alc.1.*
%{_mandir}/*/man1/alc.1.*
%{_mandir}/man1/amule.1.*
%{_mandir}/*/man1/amule.1.*
%{_mandir}/man1/cas.1.*
%{_mandir}/*/man1/cas.1.*
%{_mandir}/man1/wxcas.1.*
%{_mandir}/*/man1/wxcas.1.*
%{_mandir}/man1/amulegui.1.*
%{_mandir}/*/man1/amulegui.1.*
%exclude %{_datadir}/%{name}/webserver
%{_metainfodir}/%{name}.appdata.xml

%files nogui
%{_bindir}/alcc
%{_bindir}/amulecmd
%{_bindir}/amuled
%{_bindir}/amuleweb
%{_bindir}/ed2k
%{_datadir}/%{name}/webserver
%{_mandir}/man1/alcc.1.*
%{_mandir}/*/man1/alcc.1.*
%{_mandir}/man1/amulecmd.1.*
%{_mandir}/*/man1/amulecmd.1.*
%{_mandir}/man1/amuled.1.*
%{_mandir}/*/man1/amuled.1.*
%{_mandir}/man1/amuleweb.1.*
%{_mandir}/*/man1/amuleweb.1.*
%{_mandir}/man1/ed2k.1.*
%{_mandir}/*/man1/ed2k.1.*


%changelog
* Sat Mar 04 2023 Leigh Scott <leigh123linux@gmail.com> - 2.3.3-10
- Add patch for wx-3.2

* Sat Mar 04 2023 Leigh Scott <leigh123linux@gmail.com> - 2.3.3-9
- Rebuild due to wxGTK3-devel retirement (f39)

* Thu Aug 25 2022 Sérgio Basto <sergio@serjux.com> - 2.3.3-8
- Rollback to wx 3.0.5

* Tue Aug 23 2022 Sérgio Basto <sergio@serjux.com> - 2.3.3-7
- Rebuild with wxWidgets 3.2
- Conflict with std::byte is fixed in 2.3.3

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 06 2021 Sérgio Basto <sergio@serjux.com> - 2.3.3-4
- PR 298 from upstream to allow build with autoconf 2.71
- Force build and install cryptopp >= 8.6.0 to avoid crashs
- gcc-c++ installs gcc by default

* Tue Oct 05 2021 Sérgio Basto <sergio@serjux.com> - 2.3.3-3
- Rebuild for cryptopp update from 8.4.0 to 8.6.0

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 18 2021 Leigh Scott <leigh123linux@gmail.com> - 2.3.3-1
- New upstream release

* Thu Feb 11 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.3.3-0.9.20201122git0e9e3ef
- Rebuilt

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.3-0.8.20201122git0e9e3ef
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.3.3-0.7.20201122git0e9e3ef
- Update snapshot

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.3-0.5.20200131gitc0c2823
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Leigh Scott <leigh123linux@gmail.com> - 2.3.3-0.4.20200131gitc0c2823
- Rebuilt

* Sun Mar 01 2020 Sérgio Basto <sergio@serjux.com> - 2.3.3-0.3.20200131gitc0c2823
- Add appdata file, copied from
  https://github.com/sanjayankur31/rpmfusion-appdata

* Sat Feb 29 2020 Sérgio Basto <sergio@serjux.com> - 2.3.3-0.2.20200131gitc0c2823
- Some changes based on Mageia spec
- Let's try wxGTK with GTK3 instead GTK2

* Fri Feb 28 2020 leigh123linux <leigh123linux@googlemail.com> - 2.3.3-0.1.20200131gitc0c2823
- Update to the latest git snapshot

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 14 2019 Sérgio Basto <sergio@serjux.com> - 2.3.2-18
- Use wxGTK3-gtk2 since with gtk3 is crashing (#5197)

* Sat Mar 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-17
- Rebuilt for cryptopp
- Switch to wxGTK3

* Tue Aug 14 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-16
- Rebuilt for cryptopp

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Sérgio Basto <sergio@serjux.com> - 2.3.2-14
- Amule also have issues with compat-wxGTK3-gtk2, revert to wxGTK

* Sun Jun 03 2018 Sérgio Basto <sergio@serjux.com> - 2.3.2-13
- el7 compat

* Sun Jun 03 2018 Sérgio Basto <sergio@serjux.com> - 2.3.2-12
- Move to compat-wxGTK3-gtk2 and add Debian patch for libupnp1.8

* Tue Apr 17 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-11
- Rebuilt for libupnp

* Tue Feb 27 2018 Sérgio Basto <sergio@serjux.com> - 2.3.2-10
- Fix FTBFS with crypto++ 6.0.0

* Sun Feb 25 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-9
- Spec clean-up and rebuilt for cryptopp

* Tue Feb 06 2018 Sérgio Basto <sergio@serjux.com> - 2.3.2-8
- Clean up spec

* Wed Nov 15 2017 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-7
- Add obsoletes/provides
- Disable xchat-amule

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Sérgio Basto <sergio@serjux.com> - 2.3.2-3
- Back to wxGTK 2.8.12, wxGTK3.0 give me some problems.

* Thu Sep 22 2016 Sérgio Basto <sergio@serjux.com> - 2.3.2-2
- with-wx-config=/usr/bin/wx-config-3.0

* Wed Sep 21 2016 Sérgio Basto <sergio@serjux.com> - 2.3.2-1
- New upstream release

* Fri May 06 2016 Sérgio Basto <sergio@serjux.com> - 2.3.2-0.1.20160506git88aa023
- Update to amule to pre 0.3.2
- Use new location of sources.
- Move BR:wxGTK-devel to wxGTK3-devel
- Drop patch aMule-2.3.1-gcc47 is upstreamed.
- Man files and others are fixed, they are converted to UTF-8.

* Fri May 01 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-8
- Remove noarch from xchat fix build on Koji

* Sun Nov 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-7
- Clean spec file

* Sat Aug 30 2014 Sérgio Basto <sergio@serjux.com> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jan 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-5
- Drop docdir and desktop vendor

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for GD 2.1.0

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Mass rebuilt for Fedora 19 Features

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-2
- Add hardened build
- Fix build with gcc47

* Mon Jan 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-0
- Update to 2.3.1

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.2.6-3
- Fix FTBFS and gcc compiler bug
- Conditionalize noarch subpackage

* Fri Sep 24 2010 Felix Kaechele <heffer@fedoraproject.org> - 2.2.6-2
- rebuild for new wx

* Sun Sep 20 2009 Felix Kaechele <heffer@fedoraproject.org> - 2.2.6-1
- 2.2.6

* Tue May 19 2009 Felix Kaechele <heffer@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Wed Apr 15 2009 Felix Kaechele <felix at fetzig dot org> - 2.2.4-1
- upstream 2.2.4
- spec fixup

* Sun Mar 22 2009 Felix Kaechele <felix at fetzig dot org> - 2.2.3-1
- updated to 2.2.3
- replaced patch3 with new one for gcc4.4

* Thu Nov 20 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.2.2-2
- add remote GUI

* Sat Nov 08 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.2.2-1
- version 2.2.2
- patch 0 and 2 applied upstream
- drop patch1
- split off non-X-dependent tools

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.3-5
- rebuilt

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.3-4
- rebuild

* Sun Mar 04 2007 kwizart <kwizart at gmail.com > - 2.1.3-3
- Fix wxGTK 2.8.x
- Fix open with O_CREATE
- Prevent timestramps on install
- Add missing BR
- Fix gcc43
- Fix multiple parameter named ProgName

* Sat Oct 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.1.3-2
- rebuild

* Mon Jun 12 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.3-1
- version 2.1.3

* Tue May 30 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.2-1
- version 2.1.2

* Sat Apr 08 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.1-1
- version 2.1.1

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Jun 16 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.3-0.lvn.1
- version 2.0.3

* Sun Jun 05 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.2-0.lvn.1
- version 2.0.2

* Sat Jun 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.0.1-0.lvn.2
- BR /usr/bin/autopoint instead of gettext; This gives us gettext on pre
  FC4 and gettext-devel on FC4

* Mon May 23 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.1-0.lvn.1
- version 2.0.1

* Wed May 04 2005 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.1
- version 2.0 final(ly)
- drop epoch

* Fri Dec 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.7.rc8
- update to rc8

* Wed Oct 20 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.6.rc7
- update to rc7: no need for cryptopp anymore

* Mon Jul 19 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.5.rc5
- update to rc5

* Wed Jul 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.4.rc4a
- update to rc4a (hotfix)

* Wed Jul 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.3.rc4
- fix desktop files for alc and wxcas
- convert tabs into spaces (use diff -b)

* Tue Jul 13 2004 Dams <anvil[AT]livna.org> 0:2.0.0-0.lvn.0.2.rc4
- Removing temporary _docs directory before attempting to create it

* Mon Jul 12 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.1.rc4
- Version 2.0.0rc4
- new xchat-amule subpackage

* Sun Jun 13 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.1.rc3
- Version 2.0.0rc3

* Tue Feb 17 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.6-0.lvn.1
- Version 1.2.6

* Tue Feb 10 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.5-0.lvn.1
- Version 1.2.5
- Dropped alternatives support (we conflict and obsolete xmule)

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.2.4-0.lvn.4
- Added explicit BuildReq:openssl-devel (else it wont build on rh9/rh8
  because of curl-devel packaging bug)

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.2.4-0.lvn.3
- Re-add explicit conflits:xmule

* Tue Jan 13 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-0.lvn.2
- Obsoletes xmule (the project seems to have stopped)

* Mon Jan 12 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-0.lvn.1
- version 1.2.4 (small bugfix release)

* Sat Jan 03 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.3-0.lvn.1
- new version: 1.2.3
- added webserver support (still a little buggy according to aMule's website)

* Thu Dec 18 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.1-0.lvn.2
- remove enable-optimize
- update Conflicts
- add Epoch: 0

* Mon Dec 15 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.1-0.lvn.1
- version 1.2.1
- doesn't require wget anymore : libcurl is used instead
- add BuildRequires: curl-devel
- Move Prereq to Requires(pre)
- add enable-optimise to configure

* Thu Nov 27 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-0.lvn.1
- version 1.2.0

* Fri Nov 14 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.3
- Change conflicts
- s/Fedora/Livna/

* Wed Nov 12 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.2
- fix preun

* Wed Nov 12 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.1
- lots of fixes, thanks to Dams (anvil[AT]livna.org)

* Wed Nov 05 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-1
- new version

* Sat Nov 01 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.1-1
- RedHatification (from PLF/Mandrake)
