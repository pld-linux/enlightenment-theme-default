#
# TODO:
#	- some smart way to create symlink when one theme is uninstalled
#	  but other still exists

%define		src_name	enlightenment

# /usr/share/enlightenment/data/themes/default.edj must be in both packages
%define		_duplicate_files_terminate_build	0

Summary:	Default Enlightenment themes
Summary(pl.UTF-8):	Domyślne motywy Enlightenmenta
Name:		enlightenment-theme-default
Version:	0.17.2.1
Release:	1
License:	BSD
Group:		Themes
Source0:	http://download.enlightenment.org/releases/%{src_name}-%{version}.tar.bz2
# Source0-md5:	a0da142a9a44540506149936bfc6e28c
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
Requires:	enlightenment >= %{version}
Provides:	enlightenment-theme-default = %{version}

%description slow_pc
Default Enlightenment theme with small textures.

%description slow_pc -l pl.UTF-8
Domyślny motyw Enlightenmenta z małymi teksturami.

%package fast_pc
Summary:	Default Enlightenment theme with large textures
Summary(pl.UTF-8):	Domyślny motyw Enlightenmenta z dużymi teksturami
Group:		Themes
Requires:	enlightenment >= %{version}
Provides:	enlightenment-theme-default = %{version}

%description fast_pc
Default Enlightenment theme with large textures.

%description fast_pc -l pl.UTF-8
Domyślny motyw Enlightenmenta z dużymi teksturami.

%prep
%setup -q -n %{src_name}-%{version}
for DIR in themes; do
sed -e 's/@EDJE_DEF@/-DLOWRES_PDA=1 -DMEDIUMRES_PDA=2 -DHIRES_PDA=3 -DSLOW_PC=4 -DMEDIUM_PC=5 -DFAST_PC=6 -DE17_PROFILE=$(PROFILE)/' \
	-e 's#@edje_cc@#%{_bindir}/edje_cc#'	\
	-e 's#$(top_srcdir)/data/#../#'	\
	-e 's#$(top_builddir)/data/#../#'	\
	data/$DIR/Makefile.am > data/$DIR/Makefile
done

%build
%{__make} -C data/themes default.edj PROFILE=SLOW_PC
mv data/themes/{default.edj,default-slow_pc.edj}
%{__make} -C data/themes default.edj PROFILE=FAST_PC
mv data/themes/{default.edj,default-fast_pc.edj}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/enlightenment/data/themes

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

%files slow_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/themes/default-slow_pc.edj
%ghost %{_datadir}/enlightenment/data/themes/default.edj

%files fast_pc
%defattr(644,root,root,755)
%{_datadir}/enlightenment/data/themes/default-fast_pc.edj
%ghost %{_datadir}/enlightenment/data/themes/default.edj
