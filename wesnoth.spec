# TODO
# - rename language files sr@latin to sr@Latn and include them
# - use desktop file included with project (consider which one are better)
# - dont know what should I do with sr@latin man pages
# Conditional build
%bcond_without	server	# without server
%bcond_without	tools	# without tools
%bcond_without	fribidi	# without Bidirectional language support
#
Summary:	Strategy game with a fantasy theme
Summary(hu.UTF-8):	Fantasy környezetben játszódó stratégiai játék
Summary(pl.UTF-8):	Strategiczna gra z motywem fantasy
Name:		wesnoth
Version:	1.4.6
Release:	2
Epoch:		1
License:	GPL v2+
Group:		X11/Applications/Games/Strategy
Source0:	http://www.wesnoth.org/files/%{name}-%{version}.tar.bz2
# Source0-md5:	9e92234b29f062b3779750ba3cd0a71b
Source1:	%{name}.desktop
Source2:	%{name}_editor.desktop
Source3:	%{name}d.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-locale_dir.patch
URL:		http://www.wesnoth.org/
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	SDL_image-devel >= 1.2
BuildRequires:	SDL_mixer-devel >= 1.2
BuildRequires:	SDL_net-devel >= 1.2
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	boost-devel >= 1.33
%{?with_fribidi:BuildRequires:	fribidi-devel}
BuildRequires:	gettext-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zipios++-devel
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
Summary(pl.UTF-8):	Sieciowy serwer dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.0.17

%description server
Server for playing networked games of Wesnoth.

%description server -l hu.UTF-8
Szerver a Wesnoth hálózati játékához.

%description server -l pl.UTF-8
Serwer do prowadzenia sieciowych gier Wesnoth.

%package tools
Summary:	Tools for Wesnoth
Summary(hu.UTF.8):	Eszközök a Wesnoth-hoz
Summary(pl.UTF-8):	Narzędzia dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description tools
Map editor and translations tools.

%description tools -l hu.UTF-8
Pályaszerkesztők és fordítási eszközök.

%description tools -l pl.UTF-8
Edytor map i narzędzia do tłumaczeń.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_server:--enable-server} \
	%{?with_tools:--enable-editor} \
	%{?with_tools:--enable-tools} \
	--with%{!?with_fribidi:out}-fribidi \
	--docdir=%{_docdir}/%{name}-%{version} \
	--with-icondir=%{_pixmapsdir} \
	--with-zipios
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/var/run/wesnothd,/etc/rc.d/init.d,%{_docdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# install additional docs
install changelog README  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{changelog,README}

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/wesnothd

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{nb_NO,nb}

# unsupported(?)
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ca_ES@valencia
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/la
rm -rf $RPM_BUILD_ROOT%{_mandir}/ca_ES@valencia

# the same as manuals from %{_mandir}/man?
rm -rf $RPM_BUILD_ROOT%{_mandir}/en_GB

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
%groupadd -P %{name}-server -g 178  wesnothd
%useradd -P %{name}-server -u 178 -d /var/run/wesnothd -c "Wesnothd User" -g wesnothd wesnothd

%post server
/sbin/chkconfig --add wesnothd
%service wesnothd restart

%preun server
if [ "$1" = "0" ]; then
	%service wesnothd stop
	/sbin/chkconfig --del wesnothd
	%userremove wesnothd
	%groupremove wesnothd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/wesnoth
%{_mandir}/man6/wesnoth.6*
%lang(cs) %{_mandir}/cs/man6/wesnoth.6*
%lang(da) %{_mandir}/da/man6/wesnoth.6*
%lang(de) %{_mandir}/de/man6/wesnoth.6*
%lang(es) %{_mandir}/es/man6/wesnoth.6*
%lang(fi) %{_mandir}/fi/man6/wesnoth.6*
%lang(fr) %{_mandir}/fr/man6/wesnoth.6*
%lang(gl) %{_mandir}/gl/man6/wesnoth.6*
%lang(hu) %{_mandir}/hu/man6/wesnoth.6*
%lang(it) %{_mandir}/it/man6/wesnoth.6*
%lang(ja) %{_mandir}/ja/man6/wesnoth.6*
%lang(lt) %{_mandir}/lt/man6/wesnoth.6*
%lang(nl) %{_mandir}/nl/man6/wesnoth.6*
%lang(pl) %{_mandir}/pl/man6/wesnoth.6*
%lang(sk) %{_mandir}/sk/man6/wesnoth.6*
%lang(sr) %{_mandir}/sr/man6/wesnoth.6*
%lang(sv) %{_mandir}/sv/man6/wesnoth.6*
%lang(tr) %{_mandir}/tr/man6/wesnoth.6*
%lang(zh_CN) %{_mandir}/zh_CN/man6/wesnoth.6*
%lang(zh_TW) %{_mandir}/zh_TW/man6/wesnoth.6*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}-icon.png

%if %{with server}
%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wesnothd
%attr(754,root,root) /etc/rc.d/init.d/wesnothd
%{_mandir}/man6/wesnothd.6*
%lang(cs) %{_mandir}/cs/man6/wesnothd.6*
%lang(da) %{_mandir}/da/man6/wesnothd.6*
%lang(de) %{_mandir}/de/man6/wesnothd.6*
%lang(es) %{_mandir}/es/man6/wesnothd.6*
%lang(fi) %{_mandir}/fi/man6/wesnothd.6*
%lang(fr) %{_mandir}/fr/man6/wesnothd.6*
%lang(gl) %{_mandir}/gl/man6/wesnothd.6*
%lang(hu) %{_mandir}/hu/man6/wesnothd.6*
%lang(it) %{_mandir}/it/man6/wesnothd.6*
%lang(ja) %{_mandir}/ja/man6/wesnothd.6*
%lang(nl) %{_mandir}/nl/man6/wesnothd.6*
%lang(pl) %{_mandir}/pl/man6/wesnothd.6*
%lang(sk) %{_mandir}/sk/man6/wesnothd.6*
%lang(sr) %{_mandir}/sr/man6/wesnothd.6*
%lang(sv) %{_mandir}/sv/man6/wesnothd.6*
%lang(tr) %{_mandir}/tr/man6/wesnothd.6*
%lang(zh_CN) %{_mandir}/zh_CN/man6/wesnothd.6*
%lang(zh_TW) %{_mandir}/zh_TW/man6/wesnothd.6*
%attr(770,wesnothd,wesnothd) %dir /var/run/wesnothd
%endif

%if %{with tools}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cutter
%attr(755,root,root) %{_bindir}/exploder
%attr(755,root,root) %{_bindir}/wesnoth_editor
%attr(755,root,root) %{_bindir}/wmlindent
%attr(755,root,root) %{_bindir}/wmllint
%attr(755,root,root) %{_bindir}/wmlscope
%{_mandir}/man6/wesnoth_editor.6*
%lang(cs) %{_mandir}/cs/man6/wesnoth_editor.6*
%lang(da) %{_mandir}/da/man6/wesnoth_editor.6*
%lang(de) %{_mandir}/de/man6/wesnoth_editor.6*
%lang(es) %{_mandir}/es/man6/wesnoth_editor.6*
%lang(fi) %{_mandir}/fi/man6/wesnoth_editor.6*
%lang(fr) %{_mandir}/fr/man6/wesnoth_editor.6*
%lang(gl) %{_mandir}/gl/man6/wesnoth_editor.6*
%lang(hu) %{_mandir}/hu/man6/wesnoth_editor.6*
%lang(it) %{_mandir}/it/man6/wesnoth_editor.6*
%lang(ja) %{_mandir}/ja/man6/wesnoth_editor.6*
%lang(lt) %{_mandir}/lt/man6/wesnoth_editor.6*
%lang(nl) %{_mandir}/nl/man6/wesnoth_editor.6*
%lang(pl) %{_mandir}/pl/man6/wesnoth_editor.6*
%lang(sk) %{_mandir}/sk/man6/wesnoth_editor.6*
%lang(sr) %{_mandir}/sr/man6/wesnoth_editor.6*
%lang(sv) %{_mandir}/sv/man6/wesnoth_editor.6*
%lang(tr) %{_mandir}/tr/man6/wesnoth_editor.6*
%lang(zh_CN) %{_mandir}/zh_CN/man6/wesnoth_editor.6*
%lang(zh_TW) %{_mandir}/zh_TW/man6/wesnoth_editor.6*
%{_desktopdir}/%{name}_editor.desktop
%{_pixmapsdir}/%{name}_editor-icon.png
%endif
