#
# Conditional build
%bcond_without	server	# without server
%bcond_without 	tools	# without tools
#
Summary:	Strategy game with a fantasy theme
Summary(pl):	Strategiczna gra z motywem fantasy
Name:		wesnoth
Version:	0.6.99.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Games/Strategy
Icon:		wesnoth-icon.xpm
Source0:	http://www.wesnoth.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	62c0184a1c044944f0e94911e918b93c
Source1:	%{name}.desktop
URL:		http://www.wesnoth.org
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	SDL_image-devel >= 1.2
BuildRequires:	SDL_mixer-devel >= 1.2
BuildRequires:	SDL_net-devel >= 1.2
BuildRequires:	SDL_ttf-devel >= 2.0
Requires:	SDL_image >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Battle for Wesnoth is a fantasy strategy game. Battle for control of
villages, using variety of units which have advantages and
disadvantages in different types of terrains and against different
types of attacks. Units gain experience and advance levels, and are
carried over from one scenario to the next campaign.

%description -l pl
Battle for Wesnoth jest strategiczn± gr± fantasy. Batalia o
kontrolê nad wsiami przy pomocy ró¿nego rodzaju oddzia³ów, które maj±
przewagê lub jej brak w odmiennym ukszta³towaniu terenu i przeciwko
ró¿nym sposobom ataku. Oddzia³y zdobywaj± do¶wiadczenie i poziomy
zaawansowania i s± przenoszene z jednej scenerii do nastêpnej kampani.

%package server
Summary:	Network server for Wesnoth
Summary(pl):	Sieciowy serwer dla Wesnoth
Group:		X11/Applications/Games/Strategy

%description server
Server for playing networked games of Wesnoth.

%description server -l pl
Serwer do prowadzenia sieciowych gier Wesnoth.

%package tools
Summary:	Tools for Wesnoth
Summary(pl):	Narzêdzia dla Wesnoth
Group:		X11/Applications/Games/Strategy
Requires:	%{name} = %{version}

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
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog README MANUAL*
%attr(755,root,root) %{_bindir}/wesnoth
%{_mandir}/man6/wesnoth.6*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop

%if %{with server}
%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wesnothd
%{_mandir}/man6/wesnothd.6*
%endif

%if %{with tools}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/make_translation
%attr(755,root,root) %{_bindir}/merge_translations
%attr(755,root,root) %{_bindir}/wesnoth_editor
%{_mandir}/man6/wesnoth_editor.6*
%endif
