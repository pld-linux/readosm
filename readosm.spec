#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Simple library for extracting the contents from OpenStreetMap files
Summary(pl.UTF-8):	Prosta biblioteka do wyciągania danych z plików OpenStreetMap
Name:		readosm
Version:	1.0.0d
Release:	1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://www.gaia-gis.it/gaia-sins/readosm-sources/%{name}-%{version}.tar.gz
# Source0-md5:	ba74b5141f115de5d240cf4a40478336
URL:		https://www.gaia-gis.it/fossil/readosm
%{?with_apidocs:BuildRequires:	doxygen >= 1.7.3}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ReadOSM is a simple library intended for extracting the contents from
OpenStreetMap files: both input formats (.osm XML based and .osm.pbf
based on Google's Protocol Buffer serialization) are indifferenctly
supported.

%description -l pl.UTF-8
ReadOSM to prosta biblioteka do wydobywania danych z plików
OpenStreetMap. Oba formaty wejściowy (.osm oparty na XML oraz .osm.pbf
oparty na serializacji Google Protocol Buffer) są obsługiwane w sposób
przezroczysty.

%package devel
Summary:	Header files for ReadOSM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ReadOSM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel >= 1.95
Requires:	zlib-devel

%description devel
Header files for ReadOSM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ReadOSM.

%package static
Summary:	Static ReadOSM library
Summary(pl.UTF-8):	Statyczna biblioteka ReadOSM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ReadOSM library.

%description static -l pl.UTF-8
Statyczna biblioteka ReadOSM.

%package apidocs
Summary:	ReadOSM API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki ReadOSM
Group:		Documentation

%description apidocs
API and internal documentation for ReadOSM library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ReadOSM.

%prep
%setup -q

%build
%configure

%{__make}
#	libreadosm_la_LIBADD="-lm"

%{?with_apidocs:doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libreadosm.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libreadosm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libreadosm.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libreadosm.so
%{_includedir}/readosm.h
%{_pkgconfigdir}/readosm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libreadosm.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
