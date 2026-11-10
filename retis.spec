%global wireshark_plugindir %(pkg-config --variable plugindir wireshark 2>/dev/null)/epan

Name:           retis
Version:        1.7.0
Release:        %autorelease
Summary:        Tracing packets in the Linux networking stack
SourceLicense:  GPL-2.0-only
# Additional license terms from statically-linked Rust dependencies, from the
# output of %%{cargo_license_summary}:
#
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause
# GPL-2.0-only
# LGPL-2.1-only OR BSD-2-Clause
# LGPL-2.1-or-later
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
# Unlicense OR MIT
License:        %{shrink:
    (MIT OR Apache-2.0) AND
    Unicode-3.0 AND
    Unicode-DFS-2016 AND
    (0BSD OR MIT OR Apache-2.0) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    BSD-2-Clause AND
    GPL-2.0-only AND
    (LGPL-2.1-only OR BSD-2-Clause) AND
    LGPL-2.1-or-later AND
    MIT AND
    (MIT OR Zlib OR Apache-2.0) AND
    (Unlicense OR MIT)
    }

URL:            https://github.com/retis-org/retis
Source:         https://github.com/retis-org/retis/archive/v%{version}/%{name}-%{version}.tar.gz
# Manually created to use the rpm profile when building and installing the
# release target.
Patch:          retis-release-profile.diff
# Manually created to:
# - Remove the rbpf dependency (was in the unused 'debug' feature).
# - Remove the dev-dependencies.
# - Downgrade the libbpf-rs/cargo and pcap dependencies.
Patch:          retis-fix-deps.diff

ExclusiveArch:  x86_64 aarch64

Requires:       python3

BuildRequires:  wireshark-devel
BuildRequires:  json-c-devel
BuildRequires:  rust-packaging
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  jq
BuildRequires:  llvm
BuildRequires:  make
BuildRequires:  python3-devel

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
make wireshark %{?_smp_mflags}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies

%install
env CARGO_INSTALL_OPTS="--no-track" make install
install -m 0755 -d %{buildroot}%{_datadir}/retis/profiles
install -m 0644 retis/profiles/* %{buildroot}%{_datadir}/retis/profiles
install -m 0755 -d %{buildroot}%{wireshark_plugindir}
install -m 0755 tools/wireshark/retis.so %{buildroot}%{wireshark_plugindir}/retis.so
rm -rf %{buildroot}/include
rm -rf %{buildroot}/pkgconfig
rm -f %{buildroot}/libbpf.a

%package -n retis-wireshark
Summary:        Wireshark dissector plugin for retis pcap files
Requires:       retis = %{version}-%{release}
Requires:       wireshark

%description -n retis-wireshark
A Wireshark dissector plugin that decodes retis pcap capture files,
providing human-readable display of retis events inside Wireshark.

%files
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/retis
%{_datadir}/retis/profiles

%files -n retis-wireshark
%license LICENSE
%{wireshark_plugindir}/retis.so

%changelog
%autochangelog
