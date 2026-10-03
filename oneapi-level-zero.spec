%define srcname level-zero

%define major		1
%define libloadername	%mklibname oneapi-level-zero
%define devname		%mklibname %{srcname} -d

Name:		oneapi-level-zero
Version:	1.32.0
Release:	1
Summary:	OneAPI Level Zero Specification Headers and Loader
Group:		System/Libraries
License:	MIT
URL:		https://github.com/oneapi-src/level-zero
Source0:	https://github.com/oneapi-src/level-zero/archive/refs/tags/v%{version}/level-zero-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	make
BuildRequires:	chrpath

%description
The objective of the oneAPI Level-Zero Application Programming Interface
(API) is to provide direct-to-metal interfaces to offload accelerator
devices. Its programming interface can be tailored to any device needs
and can be adapted to support broader set of languages features such as
function pointers, virtual functions, unified memory,
and I/O capabilities.

%package -n %{libloadername}
Summary:	OneAPI Level Zero loader
Group:		System/Libraries
# Useful for a quick oneAPI Level-Zero testing
Recommends:	%{name}-zello_world
Provides:	oneapi-level-zero = %{EVRD}

%description -n %{libloadername}
The objective of the oneAPI Level-Zero Application Programming Interface
(API) is to provide direct-to-metal interfaces to offload accelerator
devices. Its programming interface can be tailored to any device needs
and can be adapted to support broader set of languages features such as
function pointers, virtual functions, unified memory,
and I/O capabilities.

%package -n %{devname}
Summary:	The oneAPI Level Zero headers and loader development files
Group:		Development/C++
Requires:	%{libloadername}%{?_isa} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{srcname}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains library and header files for
developing applications that use %{name}.

%package	zello_world
Summary:	The oneAPI Level Zero quick test program
Group:		Development/Tools
Requires:	%{libloadername}%{?_isa} = %{EVRD}

%description	zello_world
The %{name}-zello_world package contains a zello_world binary which
is capable of a quick test of the oneAPI Level-Zero driver and dumping
out the basic device and driver characteristics.

%prep
%autosetup -p1 -n level-zero-%{version}
# Top-level builds force -Werror. Keep the package buildable with the
# distro warning flags.
sed -i \
	-e 's/set(CMAKE_COMPILE_WARNING_AS_ERROR ON)/set(CMAKE_COMPILE_WARNING_AS_ERROR OFF)/' \
	-e 's/\${CMAKE_CXX_FLAGS} -Werror/\${CMAKE_CXX_FLAGS}/' \
	CMakeLists.txt

%build
%cmake -DCMAKE_COMPILE_WARNING_AS_ERROR:BOOL=OFF
%make_build

%install
%make_install -C build

mkdir -p %{buildroot}%{_bindir}
# Unix Makefiles put the sample next to its sources, not in bin/.
# %{_vpath_builddir} is a meson macro; this package does not build-require
# meson, and %cmake always configures in ./build.
_zello=$(find build -type f -name zello_world -print -quit)
test -n "$_zello"
install -pm 755 "$_zello" %{buildroot}%{_bindir}/zello_world
if chrpath -l %{buildroot}%{_bindir}/zello_world 2>/dev/null | grep -q 'RPATH\|RUNPATH'; then
	chrpath --delete %{buildroot}%{_bindir}/zello_world
fi

%files -n %{libloadername}
%license LICENSE
%doc README.md SECURITY.md
%{_libdir}/libze_loader.so.%{major}{,.*}
%{_libdir}/libze_validation_layer.so.%{major}{,.*}
%{_libdir}/libze_tracing_layer.so.%{major}{,.*}

%files zello_world
%doc README.md SECURITY.md
%{_bindir}/zello_world

%files -n %{devname}
%{_includedir}/level_zero/
%{_libdir}/libze_loader.so
%{_libdir}/libze_validation_layer.so
%{_libdir}/libze_tracing_layer.so
%{_libdir}/pkgconfig/libze_loader.pc
%{_libdir}/pkgconfig/%{srcname}.pc
