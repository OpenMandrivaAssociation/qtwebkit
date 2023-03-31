%define major 4
%define libname %mklibname qtwebkit %{major}
%define devname %mklibname qtwebkit -d

Summary:	Qt WebKit
Name:		qtwebkit
# Make sure rpm prefers us over the old QtWebKit built into Qt 4.8.x
Epoch:		5
Version:	2.3.4
Release:	11
License:	GPLv2
Group:		System/Libraries
Url:		http://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23
# Sources from git://gitorious.org/+qtwebkit-developers/webkit/qtwebkit-23.git
Source0:	qtwebkit-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
# patch from Linux From Scratch, fix build with bison 3.0
Patch2:		qt-5.1.0-bison_fixes-1.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3:		qtwebkit-2.3-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4:		qtwebkit-2.3-save_memory.patch

# backport from qt5-qtwebkit: URLs visited during private browsing show up in WebpageIcons.db
Patch101:	webkit-qtwebkit-23-private_browsing.patch
# backport from qt5-qtwebkit: Fix g++ 5.0 build (QTBUG-44829)
Patch102:	qtwebkit-g++-5.0-build.patch

BuildRequires:	bison
BuildRequires:	ruby
BuildRequires:	rubygems
BuildRequires:	gperf
BuildRequires:	flex
BuildRequires:	jpeg-devel
BuildRequires:	python2
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtNetwork)
BuildRequires:	pkgconfig(QtXml)
BuildRequires:	pkgconfig(QtOpenGL)
BuildRequires:	chrpath

%description
Qt WebKit.

%package -n %{libname}
Summary:	Qt WebKit
Group:		System/Libraries

%description -n %{libname}
Qt WebKit.

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
QML module for QtWebKit integration in Qt Quick.


%prep
%setup -q -c %{name}-%{release}

export CC=gcc
export CXX=g++

%autopatch -p1

mkdir pybin
ln -s %{_bindir}/python2 pybin/python
export QTDIR=/usr
export PATH=`pwd`/pybin:$PATH
Tools/Scripts/build-webkit \
	--qt \
	--release \
	--3d-rendering \
	--no-webkit2 \
	--no-force-sse2 \
	--qmakearg="CONFIG+=production_build QMAKE_CXX=g++ DEFINES+=HAVE_LIBWEBP=1 QMAKE_CFLAGS=\"%{optflags}\" QMAKE_CXXFLAGS=\"%{optflags} -Wno-expansion-to-defined\" QMAKE_LFLAGS=\"%{?ldflags}\" QMAKE_STRIP=" \
%ifarch aarch64
	--qmakearg="DEFINES+=ENABLE_JIT=0" \
	--qmakearg="DEFINES+=ENABLE_YARR_JIT=0" \
	--qmakearg="DEFINES+=ENABLE_ASSEMBLER=0" \
%endif
	--makeargs="%{_smp_mflags}"

%build
export CC=gcc
export CXX=g++
cd WebKitBuild/Release
%make

%install
cd WebKitBuild/Release
make install INSTALL_ROOT=%{buildroot}
# For compatibility with QtWebKit 2.2.x included in Qt 4.8.5 source
ln -s qt_webkit.pri %{buildroot}%{_prefix}/lib/qt4/mkspecs/modules/qt_webkit_version.pri
# # Fix wrong path in prl file
sed -i -e '/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/' %{buildroot}/%{_libdir}/libQtWebKit.prl

# Remove rpath
chrpath --list   %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.10.? ||:
chrpath --delete %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.10.? ||:

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
