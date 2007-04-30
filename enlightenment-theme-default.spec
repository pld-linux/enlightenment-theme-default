#
# TODO:
#	- some smart way to create symlink when one theme is uninstalled
#	  but other still exists

%define		_src_name	enlightenment

Summary:	Default Enlightenment themes
Summary(pl.UTF-8):	Domyślne motywy Enlightenmenta
Name:		enlightenment-theme-default
Version:	0.16.999.037
Release:	1
License:	BSD
Group:		Themes
Source0:	http://enlightenment.freedesktop.org/files/%{_src_name}-%{version}.tar.gz
# Source0-md5:	7ca0359905aecc81bca85208148d9264
URL:		http://enlightenment.org/
BuildRequires:	edje
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Enlightenment default theme.

%description -l pl.UTF-8
Domyślne motywy Enlightenmenta.

%package slow_pc
Summary:	Default Enlightenment theme with small textures
Summary(pl.UTF-8):	Domyślny motyw Enlightenmenta z małymi teksturami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-theme-default = %{version}

%description slow_pc
Default Enlightenment theme with small textures.

%description slow_pc -l pl.UTF-8
Domyślny motyw Enlightenmenta z małymi teksturami.

%package fast_pc
Summary:	Default Enlightenment theme with large textures
Summary(pl.UTF-8):	Domyślny motyw Enlightenmenta z dużymi teksturami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-theme-default = %{version}

%description fast_pc
Default Enlightenment theme with large textures.

%description fast_pc -l pl.UTF-8
Domyślny motyw Enlightenmenta z dużymi teksturami.

%package -n enlightenment-init-default-slow_pc
Summary:	Default Enlightenment init theme for slow computers
Summary(pl.UTF-8):	Domyślny początkowy motyw Enlightenmenta dla wolnych komputerów
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default = %{version}

%description -n enlightenment-init-default-slow_pc
Default Enlightenment init theme with small textures and half number
of frames.

%description -n enlightenment-init-default-slow_pc -l pl.UTF-8
Domyślny początkowy motyw Enlightenmenta z małymi teksturami i dwa
razy mniejszej liczbie ramek.

%package -n enlightenment-init-default-medium_pc
Summary:	Default Enlightenment init theme for medium speed computers
Summary(pl.UTF-8):	Domyślny początkowy motyw Enlightenmenta dla komputerów średniej szybkości
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default = %{version}

%description -n enlightenment-init-default-medium_pc
Default Enlightenment init theme with large textures and half number
of frames.

%description -n enlightenment-init-default-medium_pc -l pl.UTF-8
Domyślny początkowy motyw Enlightenmenta z dużymi teksturami i dwa
razy mniejszej liczbie ramek.

%package -n enlightenment-init-default-fast_pc
Summary:	Default Enlightenment init theme with large textures and all frames
Summary(pl.UTF-8):	Domyślny początkowy motyw Enlightenmenta z dużymi teksturami i wszystkimi ramkami
Group:		Themes
Requires:	enlightenment >= 0.16.999
Provides:	enlightenment-init-default = %{version}

%description -n enlightenment-init-default-fast_pc
Default Enlightenment init theme with large textures and all frames.

%description -n enlightenment-init-default-fast_pc -l pl.UTF-8
Domyślny początkowy motyw Enlightenmenta z dużymi tekstorami i
wszystkimi ramkami.

%prep
%setup -q -n %{_src_name}-%{version}
for DIR in init themes; do
sed -e 's/@EDJE_DEF@/-DLOWRES_PDA=1 -DMEDIUMRES_PDA=2 -DHIRES_PDA=3 -DSLOW_PC=4 -DMEDIUM_PC=5 -DFAST_PC=6 -DE17_PROFILE=$(PROFILE)/' \
	-e 's#@edje_cc@#%{_bindir}/edje_cc#'	\
	-e 's#$(top_srcdir)/data/#../#'	\
	-e 's#$(top_builddir)/data/#../#'	\
	data/$DIR/Makefile.am > data/$DIR/Makefile
done

%build
%{__make} -C data/init default.edj PROFILE=SLOW_PC
mv data/init/{default.edj,default-slow_pc.edj}
%{__make} -C data/init default.edj PROFILE=MEDIUM_PC
mv data/init/{default.edj,default-medium_pc.edj}
%{__make} -C data/init default.edj PROFILE=FAST_PC
mv data/init/{default.edj,default-fast_pc.edj}

%{__make} -C data/themes default.edj PROFILE=SLOW_PC
mv data/themes/{default.edj,default-slow_pc.edj}
%{__make} -C data/themes default.edj PROFILE=FAST_PC
mv data/themes/{default.edj,default-fast_pc.edj}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/{init,themes}

install data/init/default-{slow,medium,fast}_pc.edj \
	$RPM_BUILD_ROOT%{_datadir}/enlightenment/data/init/
touch $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/init/default.edj

install data/themes/default-{slow,fast}_pc.edj \
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
[ -e %{_datadir}/enlightenment/data/init/default.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{default-slow_pc.edj,default.edj}

%post -n enlightenment-init-default-medium_pc
[ -e %{_datadir}/enlightenment/data/init/default.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{default-medium_pc.edj,default.edj}

%post -n enlightenment-init-default-fast_pc
[ -e %{_datadir}/enlightenment/data/init/default.edj ] || \
	ln -sf %{_datadir}/enlightenment/data/init/{default-fast_pc.edj,default.edj}

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
%{_datadir}/enlightenment/data/init/default-slow_pc.edj
%ghost %{_datadir}/enlightenment/data/init/default.edj

%files -n enlightenment-init-default-medium_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/init/default-medium_pc.edj
%ghost %{_datadir}/enlightenment/data/init/default.edj

%files -n enlightenment-init-default-fast_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/init/default-fast_pc.edj
%ghost %{_datadir}/enlightenment/data/init/default.edj
