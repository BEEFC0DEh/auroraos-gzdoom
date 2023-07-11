Name   : gzdoom
Version: 4.10.0
Release: 1
Summary: Doom sourceport with advanced features
License: GPLv3
URL    : https://zdoom.org
Source0 : %{name}-%{version}.tar.bz2
Source1 : %{name}.desktop
Source2 : %{name}.png
Patch1 : 0001-Turn-on-32-bit-builds-for-armhfp.patch
Patch2 : 0002-Fix-file-paths.patch
Patch3 : 0003-Fixing-GLES-mode-to-work-on-real-GLES-hardware-and-O.patch

BuildRequires: bzip2-devel
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(zlib)
BuildRequires: cmake
BuildRequires: desktop-file-utils
Requires:      bzip2
Requires:      OpenAL
Requires:      SDL2

%description
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

# "-march=armv8-a+crc" is to fix 7Zip build
# https://stackoverflow.com/questions/37066261/why-is-arm-feature-crc32-not-being-defined-by-the-compiler
%ifarch %{arm}
%global optflags %(echo %{optflags} | sed "s|-march=armv7-a|-march=armv8-a+crc|g")
%endif

%build
mkdir -pv ../zmusic/build
cd ../zmusic/build
%cmake -DCMAKE_BUILD_TYPE=Release ..
%make_build

cd ../..
mkdir -pv upstream/build
cd upstream/build

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_FMOD=ON \
    -DNO_GTK=ON \
    -DNO_STRIP=ON \
    -DHAVE_VULKAN=OFF \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS} -DSHARE_DIR=\\\"%{_datadir}/%{name}\\\"" \
    -DZMUSIC_INCLUDE_DIR="../../zmusic/include" \
    -DZMUSIC_LIBRARIES="../../zmusic/build/source/libzmusic.so" ..

%make_build

%install
cd ../rpm
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{name}.desktop

mkdir -m 0755 -pv %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m 0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

cd ../zmusic/build
mkdir -m 0755 -pv %{buildroot}%{_libdir}
install -m 0755 source/libzmusic.so.1.1.10 %{buildroot}%{_libdir}/
ln -sfrv %{buildroot}%{_libdir}/libzmusic.so.1.1.10 %{buildroot}%{_libdir}/libzmusic.so.1
ln -sfrv %{buildroot}%{_libdir}/libzmusic.so.1 %{buildroot}%{_libdir}/libzmusic.so

cd ../../upstream/build
mkdir -m 0755 -pv %{buildroot}%{_datadir}/%{name}
cp -arv *.pk3 %{buildroot}%{_datadir}/%{name}/
mkdir -m 0755 -pv %{buildroot}%{_datadir}/doom
cp -arv soundfonts fm_banks %{buildroot}%{_datadir}/doom/
mkdir -m 0755 -pv %{buildroot}%{_bindir}
install -m 0755 %{name} %{buildroot}%{_bindir}/
install -m 0755 libraries/discordrpc/src/libdiscord-rpc.so %{buildroot}%{_libdir}/

%post
/usr/bin/update-desktop-database -q

%postun
/usr/bin/update-desktop-database -q

%files
%{_datadir}/%{name}
%{_datadir}/doom
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor
%{_bindir}/%{name}
%{_libdir}/libzmusic.so*
%{_libdir}/libdiscord-rpc.so
