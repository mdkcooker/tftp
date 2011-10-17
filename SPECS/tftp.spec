%define		subrel 1
Summary: 	The client and server for the Trivial File Transfer Protocol (TFTP)
Name: 		tftp
Version: 	5.0
Release: 	%mkrel 7
License: 	BSD
Group: 		System/Servers
URL:		http://www.kernel.org/pub/software/network/tftp/
Source0: 	http://www.kernel.org/pub/software/network/tftp/tftp-hpa-%{version}.tar.gz
Source1: 	tftp-xinetd
Patch0:		tftp-mips.patch
Patch5: 	tftp-hpa-0.49-fortify-strcpy-crash.patch

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations. The tftp package provides the user interface for TFTP,
which allows users to transfer files to and from a remote machine. This
program, and TFTP, provide very little security, and should not be enabled
unless it is expressly needed.

%package	server
Summary:	The server for the Trivial File Transfer Protocol (TFTP)
Group:		System/Servers
Requires:	xinetd
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description	server
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations.  The tftp-server package provides the server for TFTP,
which allows users to transfer files to and from a remote machine. TFTP
provides very little security, and should not be enabled unless it is
expressly needed. The TFTP server is run from %{_sysconfdir}/xinetd.d/tftp,
and is disabled by default on a %{_vendor} systems.

%prep

%setup -q  -n tftp-hpa-%{version}
%patch0 -p1
%patch5 -p1 -b .fortify-strcpy-crash

%build

%serverbuild

sh configure --prefix=%{_prefix}
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install
install -m755 -d %{buildroot}%{_localstatedir}/lib/tftpboot/
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/xinetd.d/tftp

%post server
%_post_service %{name}

%preun server
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/tftp
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%dir %{_localstatedir}/lib/tftpboot
%config(noreplace) %{_sysconfdir}/xinetd.d/tftp
%{_sbindir}/in.tftpd
%{_mandir}/man8/*

