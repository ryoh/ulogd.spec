%global _hardened_build 1

%global daemon_user      ulog
%global daemon_group     ulog
%global daemon_home      %{_datadir}/ulogd

%bcond_without json
%bcond_without pcap
%bcond_without sqlite

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
Source101:      ulogd.service
Source102:      ulogd.logrotate

%{?systemd_requires}
BuildRequires:  systemd
Requires(pre):  shadow-utils

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


%if %{with json}
%package json
Release:        1%{?dist}
Summary:        ulogd's JSON output module
BuildRequires:  jansson-devel
Requires:       jansson

%description json
%{summary}

%files json
%{_libdir}/ulogd/ulogd_output_JSON.so
%endif


%if %{with pcap}
%package pcap
Release:        1%{?dist}
Summary:        ulogd's PCAP output module
BuildRequires:  libpcap-devel
Requires:       libpcap

%description pcap
%{summary}

%files pcap
%{_libdir}/ulogd/ulogd_output_PCAP.so
%endif


%if %{with sqlite}
%package sqlite
Release:        1%{?dist}
Summary:        ulogd's SQLite output module
BuildRequires:  sqlite-devel
Requires:       sqlite

%description sqlite
%{summary}

%files sqlite
%{_libdir}/ulogd/ulogd_output_SQLITE3.so
%endif


%prep
%setup -q


%build
%configure \
  --disable-nfacct \
  --with-pgsql=%{_prefix} \
  --with-mysql=%{_prefix} \
  --with-dbi=%{_prefix} \
  %{?with_json:--with-jansson} \
  %{?with_pcap:--with-pcap} \
  %{?with_sqlite:--with-sqlite} \

%{make_build}


%install
[[ -f "%{buildroot}" ]] && rm -rf %{buildroot}
%{make_install}

%{__rm} -f %{buildroot}%{_libdir}/ulogd/*.la

# Set service files
%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/ulogd
%{__install} -D -p -m 0644 %{SOURCE100} %{buildroot}%{_sysconfdir}/
%{__install} -D -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}/
%{__install} -D -p -m 0644 %{SOURCE102} %{buildroot}%{_sysconfdir}/logrotate.d/ulogd


%pre
getent group  %{daemon_group} >/dev/null || groupadd -r %{daemon_group}
getent passwd %{daemon_user}  >/dev/null || \
  useradd -r -g %{daemon_group} -d %{daemon_home} -s /sbin/nologin \
  -c "Netfilter userspace logging daemon user" %{daemon_user}
exit 0


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.service


%files
%defattr(0644,root,root,0755)
%doc COPYING AUTHORS README
%doc doc/mysql-ulogd2.sql doc/mysql-ulogd2-flat.sql
%doc doc/pgsql-ulogd2.sql doc/pgsql-ulogd2-flat.sql
%doc doc/sqlite3.table
%{_mandir}/man8/ulogd.8.gz

%config(noreplace) %{_sysconfdir}/ulogd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ulogd
%config(noreplace) %{_unitdir}/ulogd.service

%attr(0755,ulog,ulog) %dir %{_localstatedir}/log/ulogd

%attr(0755,root,root) %{_sbindir}/ulogd

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
