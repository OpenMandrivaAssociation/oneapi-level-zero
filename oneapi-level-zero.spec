%define srcname level-zero

%define major             1
%define libloadername     %mklibname oneapi-level-zero
%define devname           %mklibname %{srcname} -d

Name:           oneapi-level-zero
Version:        1.22.2
Release:        1
Summary:        OneAPI Level Zero Specification Headers and Loader
Group:          System/Libraries
License:        MIT
URL:            https://github.com/oneapi-src/level-zero
Source0:         https://github.com/oneapi-src/level-zero/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  chrpath
BuildRequires:  pkgconfig(spdlog)

%description
The objective of the oneAPI Level-Zero Application Programming Interface
(API) is to provide direct-to-metal interfaces to offload accelerator
devices. Its programming interface can be tailored to any device needs
and can be adapted to support broader set of languages features such as
function pointers, virtual functions, unified memory,
and I/O capabilities.

%package -n %{libloadername}
Summary:        OneAPI Level Zero Specification Headers and Loader
Group:          System/Libraries
# Useful for a quick oneAPI Level-Zero testing
Recommends:     %{name}-zello_world
Provides:       oneapi-level-zero = %{version}-%{release}

%description -n %{libloadername}
The objective of the oneAPI Level-Zero Application Programming Interface
(API) is to provide direct-to-metal interfaces to offload accelerator
devices. Its programming interface can be tailored to any device needs
and can be adapted to support broader set of languages features such as
function pointers, virtual functions, unified memory,
and I/O capabilities.

%package -n %{devname}
Summary:        The oneAPI Level Zero Specification Headers and Loader development package
Group:          Development/C++
Requires:       %{libloadername}%{?_isa} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{srcname}-devel = %{version}-%{release}

%description -n %{devname}
The %{name}-devel package contains library and header files for
developing applications that use %{name}.

%package        zello_world
Summary:        The oneAPI Level Zero quick test package with zello_world binary

%description    zello_world
The %{name}-zello_world package contains a zello_world binary which
is capable of a quick test.
of the oneAPI Level-Zero driver and dumping out the basic device
and driver characteristics.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
# spdlog uses fmt, but since this doesn't setup linking, use it in header only mode
export CXXFLAGS="%{build_cxxflags} -DFMT_HEADER_ONLY=1"
%cmake -DSYSTEM_SDPLOG=ON
%make_build

%install
%make_install -C build

# Install also the zello_world binary to ease up testing of the l0
mkdir -p %{buildroot}%{_bindir}
install -pm 755 %{_vpath_builddir}/bin/zello_world %{buildroot}%{_bindir}/zello_world
chrpath --delete %{buildroot}%{_bindir}/zello_world

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
