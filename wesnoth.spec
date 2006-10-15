#
# Conditional build
%bcond_without	server	# without server
%bcond_without	tools	# without tools
#
Summary:	Strategy game with a fantasy theme
Summary(pl):	Strategiczna gra z motywem fantasy
Name:		wesnoth
Version:	1.1.11
Release:	1
License:	GPL v2
Group:		X11/Applications/Games/Strategy
Source0:	http://www.wesnoth.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	ebd1e7407d8f888a7ea40afa407b8aca
Source1:	%{name}.desktop
Source2:	%{name}d.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.wesnoth.org/
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	SDL_image-devel >= 1.2
BuildRequires:	SDL_mixer-devel >= 1.2
BuildRequires:	SDL_net-devel >= 1.2
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	zipios++-devel
Requires:	SDL_image >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Battle for Wesnoth is a fantasy strategy game. Battle for control of
villages, using variety of units which have advantages and
disadvantages in different types of terrains and against different
types of attacks. Units gain experience and advance levels, and are
carried over from one scenario to the next campaign.

%description -l pl
Battle for Wesnoth jest strategiczn± gr± fantasy. Batalia o kontrolê
nad wsiami przy pomocy ró¿nego rodzaju oddzia³ów, które maj± przewagê
lub jej brak w odmiennym ukszta³towaniu terenu i przeciwko ró¿nym
sposobom ataku. Oddzia³y zdobywaj± do¶wiadczenie i poziomy
zaawansowania i s± przenoszone z jednej scenerii do nastêpnej
kampanii.

%package server
Summary:	Network server for Wesnoth
Summary(pl):	Sieciowy serwer dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires(post,preun):	/sbin/chkconfig

%description server
Server for playing networked games of Wesnoth.

%description server -l pl
Serwer do prowadzenia sieciowych gier Wesnoth.

%package tools
Summary:	Tools for Wesnoth
Summary(pl):	Narzêdzia dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires:	%{name} = %{version}-%{release}

%description tools
Map editor and translations tools.

%description tools -l pl
Edytor map i narzêdzia do t³umaczeñ.

%prep
%setup -q
%patch0 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_server:--enable-server} \
	%{?with_tools:--enable-editor} \
	%{?with_tools:--enable-tools}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/var/run/wesnothd,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install images/wesnoth-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/wesnothd

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add wesnothd
if [ -f /var/lock/subsys/wesnothd ]; then
	/etc/rc.d/init.d/wesnothd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/wesnothd start\" to start wesnothd." >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/wesnothd ]; then
		/etc/rc.d/init.d/wesnothd stop
	fi
	/sbin/chkconfig --del wesnothd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc changelog README MANUAL*
%attr(755,root,root) %{_bindir}/wesnoth
%attr(755,root,root) %{_bindir}/wmlxgettext
%{_mandir}/man6/wesnoth.6*
%lang(de) %{_mandir}/de/man6/wesnoth.6*
%lang(cs) %{_mandir}/cs/man6/wesnoth.6*
%lang(en_GB) %{_mandir}/en_GB/man6/wesnoth.6*
%lang(fr) %{_mandir}/fr/man6/wesnoth.6*
%lang(ja) %{_mandir}/ja/man6/wesnoth.6*
%lang(pt_BR) %{_mandir}/pt_BR/man6/wesnoth.6*
%lang(sk) %{_mandir}/sk/man6/wesnoth.6*
%lang(sv) %{_mandir}/sv/man6/wesnoth.6*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/*

%if %{with server}
%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wesnothd
%attr(754,root,root) /etc/rc.d/init.d/wesnothd
%{_mandir}/man6/wesnothd.6*
%lang(cs) %{_mandir}/cs/man6/wesnothd.6*
%lang(de) %{_mandir}/de/man6/wesnothd.6*
%lang(en_GB) %{_mandir}/en_GB/man6/wesnothd.6*
%lang(fr) %{_mandir}/fr/man6/wesnothd.6*
%lang(ja) %{_mandir}/ja/man6/wesnothd.6*
%lang(pt_BR) %{_mandir}/pt_BR/man6/wesnothd.6*
%lang(sk) %{_mandir}/sk/man6/wesnothd.6*
%lang(sv) %{_mandir}/sv/man6/wesnothd.6*
%dir /var/run/wesnothd
%endif

%if %{with tools}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cutter
%attr(755,root,root) %{_bindir}/exploder
%attr(755,root,root) %{_bindir}/wesnoth_editor
%{_mandir}/man6/wesnoth_editor.6*
%lang(cs) %{_mandir}/cs/man6/wesnoth_editor.6*
%lang(de) %{_mandir}/de/man6/wesnoth_editor.6*
%lang(en_GB) %{_mandir}/en_GB/man6/wesnoth_editor.6*
%lang(fr) %{_mandir}/fr/man6/wesnoth_editor.6*
%lang(it) %{_mandir}/it/man6/wesnoth_editor.6*
%lang(ja) %{_mandir}/ja/man6/wesnoth_editor.6*
%lang(pt_BR) %{_mandir}/pt_BR/man6/wesnoth_editor.6*
%lang(sk) %{_mandir}/sk/man6/wesnoth_editor.6*
%lang(sv) %{_mandir}/sv/man6/wesnoth_editor.6*
%endif
