%global optflags %{optflags} -O2 -fpie
%global build_ldflags %{build_ldflags} -pie -Wl,-z,relro,-z,now

Summary:	Network monitoring tools including ping
Name:		iputils
Version:	20250605
Release:	1
License:	BSD
Group:		System/Base
URL:		https://github.com/iputils/iputils
Source0:	https://github.com/iputils/iputils/releases/download/%{version}/iputils-%{version}.tar.xz
# ifenslave.c seems to come from linux-2.6.25/Documentation/networking/ifenslave.c
# (tpg) grab it from Fedora
Source1:	ifenslave.tar.gz
Patch0:		iputils-use-libc-gettext.patch
Patch3:		https://src.fedoraproject.org/rpms/iputils/raw/rawhide/f/iputils-ifenslave.patch
Patch4:		https://src.fedoraproject.org/rpms/iputils/raw/rawhide/f/iputils-ifenslave-CWE-170.patch
%ifarch riscv64
BuildRequires:	atomic-devel
%endif
# The "ip" tool must be on PATH
BuildRequires:	iproute >= 5.18.0-2
BuildRequires:	intltool
BuildRequires:	docbook-style-xsl-ns
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	perl-SGMLSpm >= 1.1-2
BuildRequires:	cap-devel
BuildRequires:	libcap-utils
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:  make
BuildRequires:	systemd-rpm-macros
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	meson
BuildRequires:	cmake
Requires(post):	filesystem >= 2.1.9-18
%{?systemd_ordering}
%rename ninfod

%description
The iputils package contains ping, a basic networking tool. The ping command
sends a series of ICMP protocol ECHO_REQUEST packets to a specified network
host and can tell you if that machine is alive and receiving network traffic.

%prep
%setup -q -a 1 -n %{name}-%{version}
%autopatch -p1

%build
%meson
%meson_build

%make_build ifenslave CFLAGS="%{optflags} -fPIC"

%install
%meson_install
mkdir -p %{buildroot}%{_mandir}/man8

install -cp ifenslave %{buildroot}%{_bindir}/
install -cp ifenslave.8 %{buildroot}%{_mandir}/man8/

%find_lang %{name}

%files -f %{name}.lang
%doc README.md README.bonding
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %{_bindir}/ping
%{_bindir}/tracepath
%{_bindir}/ifenslave
# Contains HTML documentation
%doc %{_datadir}/iputils
%doc %attr(644,root,root) %{_mandir}/man8/clockdiff.8*
%doc %attr(644,root,root) %{_mandir}/man8/arping.8*
%doc %attr(644,root,root) %{_mandir}/man8/ping.8*
%doc %attr(644,root,root) %{_mandir}/man8/tracepath.8*
%doc %attr(644,root,root) %{_mandir}/man8/ifenslave.8*
