Name:           ulogd
Version:        2.0.7
Release:        1%{?dist}
Summary:        ulogd is a userspace logging daemon for netfilter/iptables related logging.

License:        GPLv2+
URL:            https://netfilter.org/projects/ulogd/
Source0:        https://netfilter.org/projects/ulogd/files/%{name}-%{version}.tar.bz2
Source1:        https://netfilter.org/projects/ulogd/files/%{name}-%{version}.tar.bz2.sig

%systemd_requires
BuildRequires:  libnfnetlink-devel
BuildRequires:  libnetfilter_log-devel
BuildRequires:  libnetfilter_conntrack-devel
BuildRequires:  libmnl-devel
Requires:       libnfnetlink
Requires:       libnetfilter_log
Requires:       libnetfilter_conntrack
Requires:       libmnl

%description


%prep
%setup -q


%build
%configure

%make_build


%install
[[ -f "%{buildroot}" ]] && rm -rf %{buildroot}
%make_install


%files
%doc



%changelog
* Thu Dec 27 2018 Ryoh Kawai <kawairyoh@gmail.com> 2.0.7-1%{?dist}
- Initial RPM release
