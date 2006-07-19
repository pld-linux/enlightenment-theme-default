#
# TODO:
#	- some smart way to create symlink when one theme is uninstalled
#	  but other still exists

%define		_src_name	enlightenment

Summary:	Default Enlightenment themes
Summary(pl):	Domy¶lne motywy Enlightenmenta
Name:		enlightenment-theme-default
Version:	0.16.999.030
Release:	1
License:	BSD
Group:		Themes
Source0:	http://enlightenment.freedesktop.org/files/%{_src_name}-%{version}.tar.gz
# Source0-md5:	16724991638d19d5a67b9d9273b584c9
Source1:	e17_icon_background.png
# Source1-md5:	5087c23fc21bc27dc8561d2735a1be64
URL:		http://enlightenment.org/
BuildRequires:	edje
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Enlightenment default theme.

%description -l pl
Domy¶lne motywy Enlightenmenta.

%package slow_pc
Summary:	Default Enlightenment theme with small textures
Summary(pl):	Domy¶lny motyw Enlightenmenta z ma³ymi teksturami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-theme-default = %{version}

%description slow_pc
Default Enlightenment theme with small textures.

%description slow_pc -l pl
Domy¶lny motyw Enlightenmenta z ma³ymi teksturami.

%package fast_pc
Summary:	Default Enlightenment theme with large textures
Summary(pl):	Domy¶lny motyw Enlightenmenta z du¿ymi teksturami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-theme-default = %{version}

%description fast_pc
Default Enlightenment theme with large textures.

%description fast_pc -l pl
Domy¶lny motyw Enlightenmenta z du¿ymi teksturami.

%package -n enlightenment-init-default-slow_pc
Summary:	Default Enlightenment init theme for slow computers
Summary(pl):	Domy¶lny pocz±tkowy motyw Enlightenmenta dla wolnych komputerów
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default

%description -n enlightenment-init-default-slow_pc
Default Enlightenment init theme with small textures and half number
of frames.

%description -n enlightenment-init-default-slow_pc -l pl
Domy¶lny pocz±tkowy motyw Enlightenmenta z ma³ymi teksturami i dwa
razy mniejszej liczbie ramek.

%package -n enlightenment-init-default-medium_pc
Summary:	Default Enlightenment init theme for medium speed computers
Summary(pl):	Domy¶lny pocz±tkowy motyw Enlightenmenta dla komputerów ¶redniej szybko¶ci
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default

%description -n enlightenment-init-default-medium_pc
Default Enlightenment init theme with large textures and half number
of frames.

%description -n enlightenment-init-default-medium_pc -l pl
Domy¶lny pocz±tkowy motyw Enlightenmenta z du¿ymi teksturami i dwa
razy mniejszej liczbie ramek.

%package -n enlightenment-init-default-fast_pc
Summary:	Default Enlightenment init theme with large textures and all frames
Summary(pl):	Domy¶lny pocz±tkowy motyw Enlightenmenta z du¿ymi teksturami i wszystkimi ramkami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default

%description -n enlightenment-init-default-fast_pc
Default Enlightenment init theme with large textures and all frames.

%description -n enlightenment-init-default-fast_pc -l pl
Domy¶lny pocz±tkowy motyw Enlightenmenta z du¿ymi tekstorami i
wszystkimi ramkami.

%prep
%setup -q -n %{_src_name}-%{version}
install %{SOURCE1} data/themes/images/e17_icon_background.png
for DIR in init themes; do
sed -e 's/@EDJE_DEF@/-DLOWRES_PDA=1 -DMEDIUMRES_PDA=2 -DHIRES_PDA=3 -DSLOW_PC=4 -DMEDIUM_PC=5 -DFAST_PC=6 -DE17_PROFILE=$(PROFILE)/' \
	-e 's#@edje_cc@#%{_bindir}/edje_cc#'	\
	-e 's#$(top_srcdir)/data/#../#'	\
	-e 's#$(top_builddir)/data/#../#'	\
	data/$DIR/Makefile.am > data/$DIR/Makefile
done

%build
%{__make} -C data/init init.edj PROFILE=SLOW_PC
mv data/init/{init.edj,init-slow_pc.edj}
%{__make} -C data/init init.edj PROFILE=MEDIUM_PC
mv data/init/{init.edj,init-medium_pc.edj}
%{__make} -C data/init init.edj PROFILE=FAST_PC
mv data/init/{init.edj,init-fast_pc.edj}

%{__make} -C data/themes default.edj PROFILE=SLOW_PC
mv data/themes/{default.edj,default-slow_pc.edj}
%{__make} -C data/themes default.edj PROFILE=FAST_PC
mv data/themes/{default.edj,default-fast_pc.edj}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/{init,themes}

install data/init/{init-slow_pc.edj,init-medium_pc.edj,init-fast_pc.edj} \
	$RPM_BUILD_ROOT%{_datadir}/enlightenment/data/init/
touch $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/init/init.edj

install data/themes/{default-slow_pc.edj,default-fast_pc.edj} \
	$RPM_BUILD_ROOT%{_datadir}/enlightenment/data/themes/
touch $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/themes/default.edj

%clean
rm -rf $RPM_BUILD_ROOT

%post slow_pc
[ -e %{_datadir}/enlightenment/data/themes/default.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/themes/{default-slow_pc.edj,default.edj}

%post fast_pc
[ -e %{_datadir}/enlightenment/data/themes/default.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/themes/{default-fast_pc.edj,default.edj}

%post -n enlightenment-init-default-slow_pc
[ -e %{_datadir}/enlightenment/data/init/init.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{init-slow_pc.edj,init.edj}

%post -n enlightenment-init-default-medium_pc
[ -e %{_datadir}/enlightenment/data/init/init.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{init-medium_pc.edj,init.edj}

%post -n enlightenment-init-default-fast_pc
[ -e %{_datadir}/enlightenment/data/init/init.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{init-fast_pc.edj,init.edj}

%files slow_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/themes/default-slow_pc.edj
%ghost %{_datadir}/enlightenment/data/themes/default.edj

%files fast_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/themes/default-fast_pc.edj
%ghost %{_datadir}/enlightenment/data/themes/default.edj

%files -n enlightenment-init-default-slow_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/init/init-slow_pc.edj
%ghost %{_datadir}/enlightenment/data/init/init.edj

%files -n enlightenment-init-default-medium_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/init/init-medium_pc.edj
%ghost %{_datadir}/enlightenment/data/init/init.edj

%files -n enlightenment-init-default-fast_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/init/init-fast_pc.edj
%ghost %{_datadir}/enlightenment/data/init/init.edj
