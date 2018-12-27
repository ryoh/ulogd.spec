%global _hardened_build 1

Name:           ulogd
Version:        2.0.7
Release:        1%{?dist}
Summary:        ulogd is a userspace logging daemon for netfilter/iptables related logging.
Group:          System Environment/Daemons

License:        GPLv2+
URL:            https://netfilter.org/projects/ulogd/
Source0:        https://netfilter.org/projects/ulogd/files/%{name}-%{version}.tar.bz2
Source1:        https://netfilter.org/projects/ulogd/files/%{name}-%{version}.tar.bz2.sig
Source100:      ulogd.conf

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
ulogd is a userspace logging daemon for netfilter/iptables related logging.
This includes per-packet logging of security violations, per-packet logging
 for accounting, per-flow logging and flexible user-defined accounting.


%prep
%setup -q


%build
%configure \
  --disable-nfacct

%make_build


%install
[[ -f "%{buildroot}" ]] && rm -rf %{buildroot}
%make_install

%__rm -f %{buildroot}%{_libdir}/ulogd/*.la

# Set service files
%__mkdir_p %{buildroot}/%{_sysconfdir}
install -p -m 0644 %{SOURCE100} %{buildroot}%{_sysconfdir}/ulogd.conf

%files
%defattr(0644,root,root,0755)
%doc COPYING AUTHORS README
%doc doc/mysql-ulogd2.sql doc/mysql-ulogd2-flat.sql
%doc doc/pgsql-ulogd2.sql doc/pgsql-ulogd2-flat.sql
%doc doc/sqlite3.table
%config(noreplace) %{_sysconfdir}/ulogd.conf
%{_sbindir}/ulogd
%{_mandir}/man8/ulogd.8.gz
%{_libdir}/ulogd/ulogd_filter_HWHDR.so
%{_libdir}/ulogd/ulogd_filter_IFINDEX.so
%{_libdir}/ulogd/ulogd_filter_IP2BIN.so
%{_libdir}/ulogd/ulogd_filter_IP2HBIN.so
%{_libdir}/ulogd/ulogd_filter_IP2STR.so
%{_libdir}/ulogd/ulogd_filter_MARK.so
%{_libdir}/ulogd/ulogd_filter_PRINTFLOW.so
%{_libdir}/ulogd/ulogd_filter_PRINTPKT.so
%{_libdir}/ulogd/ulogd_filter_PWSNIFF.so
%{_libdir}/ulogd/ulogd_inpflow_NFCT.so
%{_libdir}/ulogd/ulogd_inppkt_NFLOG.so
%{_libdir}/ulogd/ulogd_inppkt_ULOG.so
%{_libdir}/ulogd/ulogd_inppkt_UNIXSOCK.so
%{_libdir}/ulogd/ulogd_output_GPRINT.so
%{_libdir}/ulogd/ulogd_output_GRAPHITE.so
%{_libdir}/ulogd/ulogd_output_LOGEMU.so
%{_libdir}/ulogd/ulogd_output_NACCT.so
%{_libdir}/ulogd/ulogd_output_OPRINT.so
%{_libdir}/ulogd/ulogd_output_SYSLOG.so
%{_libdir}/ulogd/ulogd_output_XML.so
%{_libdir}/ulogd/ulogd_raw2packet_BASE.so


%changelog
* Thu Dec 27 2018 Ryoh Kawai <kawairyoh@gmail.com> 2.0.7-1%{?dist}
- Initial RPM release
