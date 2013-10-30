%define major 4
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname qtwebkit %{major}
%define devname %mklibname qtwebkit -d

Name: qtwebkit
# Make sure rpm prefers us over the old QtWebKit built into Qt 4.8.x
Epoch: 5
Version: 2.3.3
# Sources from git://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23.git
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 1
Source0: qtwebkit-%{version}.tar.xz
%else
Release: 0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Source100: %name.rpmlintrc
Patch0: qtwebkit-2.3.1-qstyleoptions.patch
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtNetwork)
BuildRequires:	pkgconfig(QtXml)
BuildRequires:	pkgconfig(QtOpenGL)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	bison
BuildRequires:	gperf
BuildRequires:	flex
Summary: Qt WebKit
URL: http://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23
License: GPL
Group: System/Libraries

%track
prog %{name} = {
	url = http://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23/trees/qtwebkit-2.3
	regex = "qtwebkit-(__VER__)"
	version = %{version}
}

%description
Qt WebKit

%package -n %{libname}
Summary: Qt WebKit
Group: System/Libraries

%description -n %{libname}
Qt WebKit

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package qml
Summary: QML module for QtWebKit integration in Qt Quick
Group: Development/KDE and Qt
Requires: %{libname} = %{EVRD}

%description qml
QML module for QtWebKit integration in Qt Quick

%prep
%if "%{scmrev}" == ""
%setup -q -n qtwebkit-%{version}%{beta}
%else
%setup -q -n qtwebkit
%endif
%apply_patches
Tools/Scripts/build-webkit --qt --release --no-webkit2 --no-force-sse2 --qmakearg="CONFIG+=production_build" --qmakearg="DEFINES+=HAVE_LIBWEBP=1"

%build
cd WebKitBuild/Release
%make

%install
cd WebKitBuild/Release
make install INSTALL_ROOT=%{buildroot}
# For compatibility with QtWebKit 2.2.x included in Qt 4.8.5 source
ln -s qt_webkit.pri %{buildroot}%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit_version.pri

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_prefix}/lib/qt4/include/QtWebKit
%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit.pri
%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit_version.pri
%{_libdir}/libQtWebKit.prl

%files qml
%{_prefix}/lib/qt4/imports/QtWebKit
