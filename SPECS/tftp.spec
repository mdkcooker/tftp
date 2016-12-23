Summary: 	The client and server for the Trivial File Transfer Protocol (TFTP)
Name: 		tftp
Version: 	5.2
Release: 	%mkrel 8
License: 	BSD
Group: 		System/Servers
URL:		http://www.kernel.org/pub/software/network/tftp/
Source0: 	http://www.kernel.org/pub/software/network/tftp/tftp-hpa/tftp-hpa-%{version}.tar.bz2
Source1: 	tftp-xinetd
Source2:	tftp.socket
Source3:	tftp.service
Patch0: 	tftp-mips.patch
Patch1: 	tftp-0.40-remap.patch
Patch2: 	tftp-hpa-0.39-tzfix.patch
Patch3: 	tftp-0.42-tftpboot.patch
Patch4: 	tftp-0.49-chk_retcodes.patch
Patch5: 	tftp-hpa-0.49-fortify-strcpy-crash.patch
Patch6: 	tftp-0.49-cmd_arg.patch
Patch7: 	tftp-hpa-0.49-stats.patch
Patch8:		tftp-hpa-5.2-pktinfo.patch
Patch9:		tftp-doc.patch
Patch10:	tftp-enhanced-logging.patch

BuildRequires:	tcp_wrappers-devel readline-devel

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations. The tftp package provides the user interface for TFTP,
which allows users to transfer filesn  to and from a remote machine. This
program, and TFTP, provide very little security, and should not be enabled
unless it is expressly needed.

%package	server
Summary:	The server for the Trivial File Transfer Protocol (TFTP)
Group:		System/Servers

%description	server
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp-server package provides the
server for TFTP, which allows users to transfer files to and from a
remote machine. TFTP provides very little security, and should not be
enabled unless it is expressly needed.  The TFTP server is run by using
systemd socket activation, and is disabled by default.

%prep
%autosetup -p1 -n tftp-hpa-%{version}
autoreconf -fsv -I.

%build
%serverbuild
%configure
%make MCONFIG all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install
install -m755 -d %{buildroot}%{_sharedstatedir}/tftpboot/
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/xinetd.d/tftp
install -p -m644 %{SOURCE2} -D ${RPM_BUILD_ROOT}%{_unitdir}/tftp.socket
install -p -m644 %{SOURCE3} -D ${RPM_BUILD_ROOT}%{_unitdir}/tftp.service

%files
%{_bindir}/tftp
%{_mandir}/man1/*

%files server
%doc README README.security CHANGES
%dir %{_sharedstatedir}/tftpboot
%config(noreplace) %{_sysconfdir}/xinetd.d/tftp
%{_sbindir}/in.tftpd
%{_mandir}/man8/*
%{_unitdir}/*
