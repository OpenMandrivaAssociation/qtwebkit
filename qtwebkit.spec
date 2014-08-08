%define major 4
%define libname %mklibname qtwebkit %{major}
%define devname %mklibname qtwebkit -d

Summary:	Qt WebKit
Name:		qtwebkit
# Make sure rpm prefers us over the old QtWebKit built into Qt 4.8.x
Epoch:		5
Version:	2.3.3
Release:	8
License:	GPLv2
Group:		System/Libraries
Url:		http://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23
# Sources from git://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23.git
Source0:	qtwebkit-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		qtwebkit-2.3.1-qstyleoptions.patch
Patch1:		qtwebkit-2.3.3-aarch64.patch
BuildRequires:	bison
BuildRequires:	gperf
BuildRequires:	flex
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtNetwork)
BuildRequires:	pkgconfig(QtXml)
BuildRequires:	pkgconfig(QtOpenGL)

%track
prog %{name} = {
	url = http://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23/trees/qtwebkit-2.3
	regex = "qtwebkit-(__VER__)"
	version = %{version}
}

%description
Qt WebKit

%package -n %{libname}
Summary:	Qt WebKit
Group:		System/Libraries

%description -n %{libname}
Qt WebKit

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package qml
Summary:	QML module for QtWebKit integration in Qt Quick
Group:		Development/KDE and Qt
Requires:	%{libname} = %{EVRD}

%description qml
QML module for QtWebKit integration in Qt Quick

%prep
%setup -q
%apply_patches
Tools/Scripts/build-webkit \
	--qt \
	--release \
	--no-webkit2 \
	--no-force-sse2 \
	--qmakearg="CONFIG+=production_build" \
	--qmakearg="DEFINES+=HAVE_LIBWEBP=1" \
%ifarch aarch64
	--qmakearg="DEFINES+=ENABLE_JIT=0" \
	--qmakearg="DEFINES+=ENABLE_YARR_JIT=0" \
	--qmakearg="DEFINES+=ENABLE_ASSEMBLER=0"
%endif

%build
cd WebKitBuild/Release
%make

%install
cd WebKitBuild/Release
make install INSTALL_ROOT=%{buildroot}
# For compatibility with QtWebKit 2.2.x included in Qt 4.8.5 source
ln -s qt_webkit.pri %{buildroot}%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit_version.pri

%files -n %{libname}
%{_libdir}/libQtWebKit.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_prefix}/lib/qt4/include/QtWebKit
%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit.pri
%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit_version.pri
%{_libdir}/libQtWebKit.prl

%files qml
%{_prefix}/lib/qt4/imports/QtWebKit

