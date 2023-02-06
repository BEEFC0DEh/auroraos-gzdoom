Name   : gzdoom
Version: 4.7.1
Release: 1
Summary: Doom sourceport with advanced features
License: GPLv3
URL    : https://zdoom.org
Source : %{name}-%{version}.tar.bz2

BuildRequires: pkgconfig(bzip2)
BuildRequires: pkgconfig(OpenAL)
BuildRequires: pkgconfgi(SDL2)
BuildRequires: cmake
Requires:      bzip2
Requires:      OpenAL
Requires:      SDL2

%description
%{summary}.

%prep
%autosetup

%build
mkdir -pv zmusic/build
cd zmusic/build
%cmake -DCMAKE_BUILD_TYPE=Release ..
%make_build

cd ../..
mkdir -pv upstream/build
cd upstream/build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_FMOD=ON \
    -DNO_OPENAL=ON \
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
mkdir -m 0755 -pv %{buildroot}/usr/games/gzdoom
cp -arv *.pk3 soundfonts fm_banks %{buildroot}/usr/games/gzdoom/
mkdir -m 0755 -pv %{buildroot}%{_bindir}
install -m 0755 gzdoom %{buildroot}%{_bindir}/


%files
%dir /usr/games/gzdoom
/usr/games/gzdoom/*
%{_bindir}/gzdoom
%{_libdir}/libzmusic.so*
