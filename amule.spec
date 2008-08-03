Name:           amule
Version:        2.1.3
Release:        4%{?dist}
Summary:        File sharing client compatible with eDonkey
License:        GPLv2+
Group:          Applications/Internet
Source0:        http://dl.sourceforge.net/%{name}/aMule-%{version}.tar.bz2
Patch0:         aMule-wx-1.2.patch
Patch1:         aMule-2.1.3-ocreate.patch
Patch2:         aMule-2.1.3-multiple.patch
Patch3:         aMule-2.1.3-gcc43.patch
URL:            http://amule.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# See http://www.amule.org/wiki/index.php/Requirements
BuildRequires:  wxGTK-devel >= 0:2.6.2, desktop-file-utils, expat-devel
BuildRequires:  gd-devel >= 2.0.0, libpng-devel
BuildRequires:  gettext-devel, flex, bison
BuildRequires:  readline-devel
Requires(pre):  chkconfig

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network. It is a fork of xMule, whis was based on eMule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package -n xchat-%{name}
Summary:        Plugin to display aMule's statistics in XChat
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}
Requires:       xchat

%description -n xchat-%{name}
This plugins allows you to display aMule statistics in XChat


%prep
%setup -q -n aMule-%{version}
%patch0 -p1 -b .wx28
%patch1 -p1 -b .ocreate
%patch2 -p1 -b .multiple
%patch3 -p1 -b .gcc43


%build
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
    --enable-utf8-systray

#    --enable-amule-gui        compile aMule remote GUI (EXPERIMENTAL)


make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT _docs

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name}

# desktop files
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Application\
                     --add-category Network\
                     --add-category X-Livna\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

iconv -f ISO-8859-1 -t UTF-8 < src/utils/aLinkCreator/alc.desktop \
      > $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category X-Livna\
                     $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop
install -m 644 src/utils/aLinkCreator/alc.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/alc.xpm

desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category X-Livna\
                     $RPM_BUILD_ROOT%{_datadir}/applications/wxcas.desktop
install -m 644 src/utils/wxCas/wxcas.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root)
%doc %{_datadir}/doc/aMule-%{version}
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/cas
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/*.gz
%{_mandir}/*/man1/*.gz

%files -n xchat-%{name}
%defattr(-,root,root)
%{_libdir}/xchat/plugins/xas.pl


%changelog
* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.3-4
- rebuild

* Tue Mar 04 2007 kwizart <kwizart at gmail.com > - 2.1.3-3
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
