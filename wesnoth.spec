# TODO
# - system lua?
# - unpackaged language files
#
# Conditional build
%bcond_without	server	# without server

Summary:	Strategy game with a fantasy theme
Summary(hu.UTF-8):	Fantasy környezetben játszódó stratégiai játék
Summary(pl.UTF-8):	Gra strategiczna z motywem fantasy
Name:		wesnoth
Version:	1.16.3
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications/Games/Strategy
Source0:	http://downloads.sourceforge.net/wesnoth/%{name}-%{version}.tar.bz2
# Source0-md5:	cd77174b393db96caa2b6fd61680af4f
Source1:	%{name}d.init
Source2:	%{name}.tmpfiles
Source3:	%{name}.sysconfig
Source4:	%{name}d.service
URL:		http://www.wesnoth.org/
BuildRequires:	SDL2-devel >= 2.0.8
BuildRequires:	SDL2_image-devel >= 2.0.2
BuildRequires:	SDL2_mixer-devel >= 2.0.0
BuildRequires:	boost-devel >= 1.50.0
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	cmake >= 2.8.5
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel >= 2.4.1
BuildRequires:	gettext-tools
BuildRequires:	libicu-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 1.0
BuildRequires:	pango-devel >= 1:1.22.0
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-data = %{epoch}:%{version}
Requires:	SDL2 >= 2.0.4
Requires:	fontconfig >= 2.4.1
Requires:	pango >= 1:1.22.8
Obsoletes:	wesnoth-tools < 1:1.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Battle for Wesnoth is a fantasy strategy game. Battle for control of
villages, using variety of units which have advantages and
disadvantages in different types of terrains and against different
types of attacks. Units gain experience and advance levels, and are
carried over from one scenario to the next campaign.

%description -l hu.UTF-8
Battle for Wesnoth (Harc Wesnothért) egy fantasy környezetben játszódó
stratégiai játék. Harc a falvak megszerzéséért, különböző egységek
felhasználásával, amelyeknek különböző előnyeik és hátrányaik vannak a
különféle terepeken és a különböző támadási stílusok ellen. Az
egységek tapasztalatot gyűjtenek, és fejlődnek, amelyek átvihetők a
következő pályára.

%description -l pl.UTF-8
Bitwa o Wesnoth jest strategiczną grą fantasy. Batalia o kontrolę nad
wsiami przy pomocy różnego rodzaju oddziałów, które mają przewagę lub
jej brak w odmiennym ukształtowaniu terenu i przeciwko różnym sposobom
ataku. Oddziały zdobywają doświadczenie i poziomy zaawansowania i są
przenoszone z jednej scenerii do następnej kampanii.

%package server
Summary:	Network server for Wesnoth
Summary(hu.UTF-8):	Hálózati szerver Wesnoth-hoz
Summary(pl.UTF-8):	Sieciowy serwer dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.0.17
Provides:	group(wesnothd)
Provides:	user(wesnothd)

%description server
Server for playing networked games of Wesnoth.

%description server -l hu.UTF-8
Szerver a Wesnoth hálózati játékához.

%description server -l pl.UTF-8
Serwer do prowadzenia sieciowych gier Wesnoth.

%package data
Summary:	Strategy game with a fantasy theme - data files
Summary(pl.UTF-8):	Gra strategiczna z motywem fantasy - pliki danych
Group:		Applications/Games
BuildArch:	noarch

%description data
This package contains the data files for Wesnoth.

%description data -l pl.UTF-8
Ten pakiet zawiera pliki danych dla gry Wesnoth.

%prep
%setup -q

# don't install locales in %{_datadir}/%{name}
%{__sed} -i 's,${DATADIR}/${LOCALEDIR},${LOCALEDIR},' CMakeLists.txt

%{__sed} -i '1s,/usr/bin/env python3$,%{__python3},' \
	data/tools/{GUI.pyw,about_cfg_to_wiki,addon_manager/__init__.py,addon_manager/html.py,extractbindings,hexometer.py,imgcheck,steam-changelog,terrain2wiki.py,unit_tree/TeamColorizer,unit_tree/__init__.py,unit_tree/animations.py,unit_tree/helpers.py,unit_tree/html_output.py,unit_tree/overview.py,unit_tree/wiki_output.py,wesnoth/campaignserver_client.py,wesnoth/libgithub.py,wesnoth/version.py,wesnoth/wescamp.py,wesnoth/wmliterator3.py,wesnoth/wmlparser3.py,wesnoth/wmltools3.py,trackviewer.pyw,wesnoth_addon_manager,wmlflip,wmlindent,wmllint,wmllint-1.4,wmlscope,wmlunits,wmlxgettext,tmx_trackplacer,wesnoth/wmldata.py,wesnoth/trackplacer3/datatypes.py,wesnoth/wmlparser.py,expand-terrain-macros.py}

%build
install -d build
cd build
# override *FLAGS to remove -DNDEBUG (wesnoth depends on asserts)
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
%cmake .. \
	-DENABLE_STRICT_COMPILATION=OFF \
	-DBINDIR="%{_bindir}" \
	-DMANDIR="%{_mandir}" \
	-DLOCALEDIR="%{_localedir}" \
	%{!?with_server:-DENABLE_SERVER=OFF} \
	%{?with_server:-DENABLE_CAMPAIGN_SERVER=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/var/run/wesnothd,/etc/rc.d/init.d,/etc/sysconfig} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{_docdir}/%{name}-%{version}} \
	$RPM_BUILD_ROOT%{systemdunitdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with server}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wesnothd
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/wesnoth
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/wesnothd.service
%endif

%{__mv} $RPM_BUILD_ROOT%{_docdir}/html $RPM_BUILD_ROOT%{_docdir}/%{name}

# unify
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ca_ES@valencia,ca@valencia}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nb_NO,nb}
%{__mv} $RPM_BUILD_ROOT%{_mandir}/{ca_ES@valencia,ca@valencia}

# unsupported(?)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ang@latin,grc,racv}
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/sr@ijekavian
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/sr@ijekavianlatin

# the same as manuals from %{_mandir}/man?
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/en_GB

# remove HighContrast icon
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/HighContrast/scalable/apps/wesnoth-icon.svg

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%pre server
%groupadd -P %{name}-server -g 178  wesnothd
%useradd -P %{name}-server -u 178 -d /var/run/wesnothd -c "Wesnothd User" -g wesnothd wesnothd

%post server
/sbin/chkconfig --add wesnothd
%service wesnothd restart
%systemd_post wesnothd.service

%preun server
if [ "$1" = "0" ]; then
	%service wesnothd stop
	/sbin/chkconfig --del wesnothd
fi
%systemd_preun wesnothd.service

%postun server
if [ "$1" = "0" ]; then
	%userremove wesnothd
	%groupremove wesnothd
fi
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md changelog.md
%doc %{_docdir}/%{name}
%attr(755,root,root) %{_bindir}/wesnoth
%{_mandir}/man6/wesnoth.6*
%lang(ca) %{_mandir}/ca/man6/wesnoth.6*
%lang(cs) %{_mandir}/cs/man6/wesnoth.6*
%lang(de) %{_mandir}/de/man6/wesnoth.6*
%lang(es) %{_mandir}/es/man6/wesnoth.6*
%lang(fr) %{_mandir}/fr/man6/wesnoth.6*
%lang(hu) %{_mandir}/hu/man6/wesnoth.6*
%lang(it) %{_mandir}/it/man6/wesnoth.6*
%lang(ja) %{_mandir}/ja/man6/wesnoth.6*
%lang(pt_BR) %{_mandir}/pt_BR/man6/wesnoth.6*
%lang(ru) %{_mandir}/ru/man6/wesnoth.6*
%lang(tr) %{_mandir}/tr/man6/wesnoth.6*
%lang(zh_CN) %{_mandir}/zh_CN/man6/wesnoth.6*
%lang(zh_TW) %{_mandir}/zh_TW/man6/wesnoth.6*
%{_desktopdir}/org.wesnoth.Wesnoth.desktop
%{_iconsdir}/hicolor/*x*/apps/wesnoth-icon.png
%{_datadir}/metainfo/org.wesnoth.Wesnoth.appdata.xml

%if %{with server}
%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/campaignd
%attr(755,root,root) %{_bindir}/wesnothd
%attr(754,root,root) /etc/rc.d/init.d/wesnothd
%attr(644,root,root) %{systemdunitdir}/wesnothd.service
%{_mandir}/man6/wesnothd.6*
%lang(ca) %{_mandir}/ca/man6/wesnothd.6*
%lang(cs) %{_mandir}/cs/man6/wesnothd.6*
%lang(de) %{_mandir}/de/man6/wesnothd.6*
%lang(es) %{_mandir}/es/man6/wesnothd.6*
%lang(fr) %{_mandir}/fr/man6/wesnothd.6*
%lang(gl) %{_mandir}/gl/man6/wesnothd.6*
%lang(hu) %{_mandir}/hu/man6/wesnothd.6*
%lang(it) %{_mandir}/it/man6/wesnothd.6*
%lang(ja) %{_mandir}/ja/man6/wesnothd.6*
%lang(pt_BR) %{_mandir}/pt_BR/man6/wesnothd.6*
%lang(ru) %{_mandir}/ru/man6/wesnothd.6*
%lang(tr) %{_mandir}/tr/man6/wesnothd.6*
%lang(zh_CN) %{_mandir}/zh_CN/man6/wesnothd.6*
%lang(zh_TW) %{_mandir}/zh_TW/man6/wesnothd.6*
%attr(770,wesnothd,wesnothd) %dir /var/run/wesnothd
%{systemdtmpfilesdir}/%{name}.conf
%endif

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}
