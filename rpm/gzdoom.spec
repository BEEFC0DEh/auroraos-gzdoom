Name   : gzdoom
Version: 4.8.0
Release: 1
Summary: Doom sourceport with advanced features
License: GPLv3
URL    : https://zdoom.org
Source : %{name}-%{version}.tar.bz2

BuildRequires: bzip2-devel
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(zlib)
BuildRequires: cmake
Requires:      bzip2
Requires:      OpenAL
Requires:      SDL2

%description
%{summary}.

%prep
%autosetup

%build
export CFLAGS="${CFLAGS} -march=armv8-a+crc"
export CXXFLAGS="${CXXFLAGS} -march=armv8-a+crc"
mkdir -pv zmusic/build
cd zmusic/build
%cmake -DCMAKE_BUILD_TYPE=Release ..
%make_build

cd ../..
mkdir -pv upstream/build
cd upstream/build

# -DCMAKE_CXX_FLAGS="-march=armv8-a+crc" is to fix 7Zip build
# https://stackoverflow.com/questions/37066261/why-is-arm-feature-crc32-not-being-defined-by-the-compiler
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_FMOD=ON \
    -DNO_GTK=ON \
    -DNO_STRIP=ON \
    -DHAVE_VULKAN=OFF \
    -DZMUSIC_INCLUDE_DIR="../../zmusic/include" \
    -DZMUSIC_LIBRARIES="../../zmusic/build/source/libzmusic.so" ..

%make_build

%install
cd zmusic/build
mkdir -m 0755 -pv %{buildroot}%{_libdir}
install -m 0755 source/libzmusic.so.1.1.10 %{buildroot}%{_libdir}/
ln -sfrv %{buildroot}%{_libdir}/libzmusic.so.1.1.10 %{buildroot}%{_libdir}/libzmusic.so.1
ln -sfrv %{buildroot}%{_libdir}/libzmusic.so.1 %{buildroot}%{_libdir}/libzmusic.so

cd ../../upstream/build
mkdir -m 0755 -pv %{buildroot}%{_datadir}/doom
cp -arv *.pk3 soundfonts fm_banks %{buildroot}%{_datadir}/doom/
mkdir -m 0755 -pv %{buildroot}%{_bindir}
install -m 0755 gzdoom %{buildroot}%{_bindir}/
install -m 0755 libraries/discordrpc/src/libdiscord-rpc.so %{buildroot}%{_libdir}/


%files
%dir %{_datadir}/doom
%{_datadir}/doom/*
%{_bindir}/gzdoom
%{_libdir}/libzmusic.so*
%{_libdir}/libdiscord-rpc.so
