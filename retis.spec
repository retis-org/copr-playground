Name:		retis
Version:	1.5.0
Release:	0%{?dist}
Summary:	Tracing packets in the Linux networking stack
License:	GPLv2

URL:		https://github.com/retis-org/retis
Source:		https://github.com/retis-org/retis/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:		retis-drop-dev-debug-deps.diff
Patch1:		retis-fix-deps.diff
ExclusiveArch:	x86_64 aarch64

BuildRequires:	rust-packaging
BuildRequires:	clang
BuildRequires:	elfutils-libelf-devel
BuildRequires:	git
BuildRequires:	jq
BuildRequires:	libpcap-devel
BuildRequires:	llvm
BuildRequires:	make
BuildRequires:	python3-devel
BuildRequires:	zlib-devel

%description
Tracing packets in the Linux networking stack, using eBPF and interfacing with
control and data paths such as OpenVSwitch.

%prep
%autosetup -n %{name}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
make release %{?_smp_mflags}

%install
env CARGO_INSTALL_OPTS=--no-track %make_install
install -m 0755 -d %{buildroot}%{_sysconfdir}/retis/profiles
install -m 0644 retis/profiles/* %{buildroot}%{_sysconfdir}/retis/profiles
rm -rf %{buildroot}/include
rm -rf %{buildroot}/pkgconfig
rm -f %{buildroot}/libbpf.a

%files
%license retis/LICENSE
%doc README.md
%{_bindir}/retis
%{_sysconfdir}/retis/profiles

%changelog
%autochangelog
