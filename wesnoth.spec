#
# Conditional build
%bcond_without	server	# without server
%bcond_without 	tools	# without tools
#
Summary:	Strategy game with a fantasy theme
Summary(pl):	Strategiczna gra z motywem fantasy
Name:		wesnoth
Version:	0.8.7
Release:	1
License:	GPL v2
Group:		X11/Applications/Games/Strategy
Icon:		wesnoth-icon.xpm
Source0:	http://www.wesnoth.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	313a27d86c310c28ae049ea72b89c124
# Source0-size:	33383831
Source1:	%{name}.desktop
Source2:	%{name}d.init
URL:		http://www.wesnoth.org
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	SDL_image-devel >= 1.2
BuildRequires:	SDL_mixer-devel >= 1.2
BuildRequires:	SDL_net-devel >= 1.2
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	libstdc++-devel
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

%build
%configure \
	%{?with_server:--enable-server} \
	%{?with_tools:--enable-editor} \
	%{?with_tools:--enable-tools}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install images/wesnoth-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/wesnothd

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

%files
%defattr(644,root,root,755)
%doc changelog README MANUAL*
%attr(755,root,root) %{_bindir}/wesnoth
%{_mandir}/man6/wesnoth.6*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/*

%if %{with server}
%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wesnothd
%attr(754,root,root) /etc/rc.d/init.d/wesnothd
%{_mandir}/man6/wesnothd.6*
%endif

%if %{with tools}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cutter
%attr(755,root,root) %{_bindir}/exploder
%attr(755,root,root) %{_bindir}/make_translation
%attr(755,root,root) %{_bindir}/merge_translations
%attr(755,root,root) %{_bindir}/wesnoth_editor
%{_mandir}/man6/wesnoth_editor.6*
%endif
