Name:		retis
Version:	1.4.0
Release:	0%{?dist}
Summary:	Tracing packets in the Linux networking stack, using eBPF and interfacing with control and data paths such as OvS or Netfilter.
License:	GPLv2

URL:		https://github.com/retis-org/retis
Source:		https://github.com/retis-org/retis/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         0000-use_pnet_packet.patch

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
Tracing packets in the Linux networking stack, using eBPF and interfacing with control and data paths such as OpenVSwitch.

%prep
%autosetup -p1 -n %{name}-%{version}
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
make release %{?_smp_mflags}

%install
env CARGO_INSTALL_OPTS=--no-track %make_install
install -m 0755 -d %{buildroot}%{_sysconfdir}/retis/profiles
install -m 0644 profiles/* %{buildroot}%{_sysconfdir}/retis/profiles

%files
%license LICENSE
%doc README.md
%{_bindir}/retis
%{_sysconfdir}/retis/profiles

%changelog
* Mon Apr 29 2024 Antoine Tenart <atenart@redhat.com> - 1.4.0-0
- Initial release.
