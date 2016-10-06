Name:           ceph-iscsi-config
Version:        0.8
Release:        1%{?dist}
Summary:        Python package providing modules for ceph iscsi gateway configuration management

License:        GPLv3
URL:            https://github.com/pcuzner/ceph-iscsi-config
Source0:        https://github.com/pcuzner/ceph-iscsi-config/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:  noarch

Requires:  python-rados
Requires:  python-rbd
Requires:  python-netaddr
Requires:  python-netifaces
Requires:  python-rtslib

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Python package providing the modules used to handle the configuration of an iSCSI
gateway, backed by ceph/kRBD. The modules are consumed by custom Ansible modules
and may also be used independently to manage the configuration once the environment
is installed.

%prep
%setup -q

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}/usr/bin
install -m 0644 lib/systemd/system/rbd-target-gw.service %{buildroot}/lib/systemd/system
install -m 0755 usr/bin/rbd-target-gw %{buildroot}/usr/bin

%post
/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable rbd-target-gw &> /dev/null || :

%files
%doc LICENSE
%doc README
%{python2_sitelib}/*
%{_bindir}/rbd-target-gw
/lib/systemd/system/rbd-target-gw.service

%changelog
* Thu Oct 06 2016 Paul Cuzner <pcuzner@redhat.com> - 0.8.1
- fixed tpg creation on existing gateways when a new gateway(s) is added to the configuration
- removed rpm packages from the source archive

* Wed Oct 05 2016 Paul Cuzner <pcuzner@redhat.com> - 0.7.1
- added rbd-target-gw daemon (started at boot)

* Tue Oct 04 2016 Paul Cuzner <pcuzner@redhat.com> - 0.6.2
- more meta data added to the gateway dict

* Mon Oct 03 2016 Paul Cuzner <pcuzner@redhat.com> - 0.6.1
- update LUN module to use a pool/image key, and include more meta data on the disk object
- moved generic rados query functions to the common.utils module
- updated the client module to handle rbd names in pool/image format

* Tue Sep 27 2016 Paul Cuzner <pcuzner@redhat.com> - 0.5-1
- initial rpm build
