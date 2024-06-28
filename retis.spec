Name:		retis
Version:	1.5.0
Release:	0%{?dist}
Summary:	Tracing packets in the Linux networking stack
License:	GPLv2

URL:		https://github.com/retis-org/retis
%if 0
Source:		https://github.com/retis-org/retis/archive/v%{version}/%{name}-%{version}.tar.gz
%else
%global commit 7777b074a5c7785484460250044fcc6f385b91b5
Source:		https://github.com/retis-org/retis/archive/%{commit}/%{name}-%{commit}.tar.gz
%endif

Patch0:		retis-drop-rbpf.diff
Patch1:		retis-drop-dev-deps.diff
ExclusiveArch:	x86_64

BuildRequires:	rust-packaging
BuildRequires:	clang
BuildRequires:	curl
BuildRequires:	elfutils-libelf-devel
BuildRequires:	jq
BuildRequires:	libpcap-devel
BuildRequires:	llvm
BuildRequires:	make
BuildRequires:	zlib-devel

%description
Tracing packets in the Linux networking stack, using eBPF and interfacing with
control and data paths such as OpenVSwitch.

%prep
%if 0
%autosetup -n %{name}-%{version} -p1
%else
%autosetup -n %{name}-%{commit} -p1
%endif
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
* Mon Apr 29 2024 Antoine Tenart <atenart@redhat.com> - 1.4.0-0
- Initial release.
