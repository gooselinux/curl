Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.19.7
Release: 26%{?dist}
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/%{name}-%{version}.tar.lzma
Source2: curlbuild.h
Patch1: curl-7.19.7-modelfree.patch
Patch2: curl-7.19.7-ssl-retry.patch
Patch3: curl-7.19.7-nss-warning.patch
Patch4: curl-7.19.7-ssl-timeout.patch
Patch5: curl-7.19.7-socks-man.patch
Patch6: curl-7.19.7-dns-timeout.patch
Patch7: curl-7.20.0-read.patch
Patch8: curl-7.20.0-cc-err.patch
Patch9: curl-7.20.0-bz579732.patch
Patch10: curl-7.20.1-crl.patch
Patch11: curl-7.19.7-bz586355.patch
Patch12: curl-7.19.7-bz589132.patch
Patch13: curl-7.21.0-ntlm.patch
Patch101: curl-7.15.3-multilib.patch
Patch102: curl-7.16.0-privlibs.patch
Patch103: curl-7.19.4-debug.patch
Patch104: curl-7.19.7-s390-sleep.patch
Patch105: curl-7.19.7-localhost6.patch
Patch201: curl-7.19.7-bz563220.patch
Patch202: curl-7.19.7-bz623663.patch
Patch203: curl-7.19.7-bz655134.patch
Patch204: curl-7.19.7-bz625685.patch
Patch205: curl-7.19.7-bz651592.patch
Patch206: curl-7.19.7-bz669702.patch
Patch207: curl-7.19.7-bz670802.patch
Patch208: curl-7.19.7-bz678594.patch
Patch209: curl-7.19.7-bz678580.patch
Patch210: curl-7.19.7-bz684892.patch
Patch211: curl-7.19.7-bz694294.patch
Provides: webclient
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn-devel
BuildRequires: libssh2-devel >= 1.2
BuildRequires: nss-devel
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: pkgconfig
BuildRequires: stunnel

# valgrind is not available on some architectures, however it's going to be
# used only by the test-suite anyway
%ifnarch s390 s390x
BuildRequires: valgrind
%endif

BuildRequires: zlib-devel
Requires: libcurl = %{version}-%{release}

%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy support,
user authentication, FTP upload, HTTP post, and file transfer resume.

%package -n libcurl
Summary: A library for getting files from web servers
Group: Development/Libraries

# libssh2 ABI has been changed since libssh2-1.0
# this forces update of libssh2 before update of libcurl
Requires: libssh2 >= 1.2

%description -n libcurl
This package provides a way for applications to use FTP, HTTP, Gopher and
other servers for getting files.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries
Requires: automake
Requires: libcurl = %{version}-%{release}
Requires: libidn-devel
Requires: pkgconfig

Provides: curl-devel = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The libcurl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.

%prep
%setup -q

# upstream patches (already applied)
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# other patches
%patch4 -p1

# bz #565972
%patch8 -p1

# bz #579732
%patch9 -p1

# Fedora patches
%patch101 -p1
%patch102 -p1
%patch103 -p1

# http://curl.haxx.se/mail/lib-2009-12/0031.html
%patch104 -p1

# we have localhost6 instead of ip6-localhost as name for ::1
%patch105 -p1

# bz #563236
%patch201 -p1

# bz #581485
%patch10 -p1

# bz #586355
%patch11 -p1

# bz #589132
%patch12 -p1

# bz #606819
%patch13 -p1

# bz #623663
%patch202 -p1

# bz #655134
%patch203 -p1

# bz #625685
%patch204 -p1

# bz #651592
%patch205 -p1

# bz #669702
%patch206 -p1

# bz #670802
%patch207 -p1

# bz #678594
%patch208 -p1

# bz #678580
%patch209 -p1

# bz #684892
%patch210 -p1

# bz #694294
%patch211 -p1

# run aclocal since we are going to run automake
aclocal -I m4

# libnih.m4 is badly broken (#669059), we need to work around it (#669048)
sed -e 's|^m4_rename(\[AC_COPYRIGHT\], \[_NIH_AC_COPYRIGHT\])$||' \
    -e 's|^AC_DEFUN(\[AC_COPYRIGHT\],$|AC_DEFUN([NIH_COPYRIGHT],|' \
    -e 's|^\[_NIH_AC_COPYRIGHT(\[\$1\])$|[AC_COPYRIGHT([$1])|' \
    -i aclocal.m4

# run automake because of added lib/md4.c (#606819)
automake

# required by curl-7.19.4-debug.patch and curl-7.21.0-ntlm.patch
autoconf

# replace hard wired port numbers in the test suite
sed -i s/899\\\([0-9]\\\)/%{?__isa_bits}9\\1/ tests/data/test*

# Convert docs to UTF-8
for f in CHANGES README; do
	iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
	mv -f ${f}.utf8 ${f}
done

%build
%configure --without-ssl --with-nss --enable-ipv6 \
	--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
	--with-gssapi --with-libidn \
	--enable-ldaps --disable-static --with-libssh2 --enable-manual
sed -i -e 's,-L/usr/lib ,,g;s,-L/usr/lib64 ,,g;s,-L/usr/lib$,,g;s,-L/usr/lib64$,,g' \
	Makefile libcurl.pc
# Remove bogus rpath
sed -i \
	-e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
cd tests
make %{?_smp_mflags}
# use different port range for 32bit and 64bit build, thus make it possible
# to run both in parallel on the same machine
./runtests.pl -a -b%{?__isa_bits}90 -p -v

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p" install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

install -d $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Make libcurl-devel multilib-ready (bug #488922)
%if 0%{?__isa_bits} == 64
%define _curlbuild_h curlbuild-64.h
%else
%define _curlbuild_h curlbuild-32.h
%endif
mv $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h \
   $RPM_BUILD_ROOT%{_includedir}/curl/%{_curlbuild_h}

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h

# don't need curl's copy of the certs; use openssl's
find ${RPM_BUILD_ROOT} -name ca-bundle.crt -exec rm -f '{}' \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libcurl -p /sbin/ldconfig

%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/MANUAL docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n libcurl
%defattr(-,root,root,-)
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS
%doc docs/CONTRIBUTE docs/libcurl/ABI
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%changelog
* Thu Apr 07 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-26
- force NSS to ask for a new client certificate when connecting second time
  to the same host (#694294)

* Wed Apr 06 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-25
- fix SIGSEGV in CERT_VerifyCert (#690273)

* Thu Mar 17 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-24
- make GSS authentication work when a curl handle is reused (#684892)

* Wed Mar 16 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-23
- do not ignore value of CURLOPT_SSL_VERIFYPEER in certain cases (#678580)

* Tue Feb 22 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-22
- do not ignore failure of SSL handshake (#669702)

* Fri Feb 18 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-21
- avoid memory leaks on SSL connection failure (#678594)

* Wed Jan 19 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-20
- avoid memory leaks and failure of NSS shutdown (#670802)

* Tue Jan 18 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-19
- fix handling of CURLOPT_CAPATH in libcurl (#669702)

* Thu Jan 13 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-18
- avoid build failure caused by a bug in libnih-devel (#669048)

* Mon Jan 10 2011 Kamil Dudka <kdudka@redhat.com> 7.19.7-17
- avoid CURLE_OUT_OF_MEMORY given a file name without any slash (#623663)
- proxy tunnel support for LDAP requests (#655134)
- proxy with kerberos authentication for https (#625685)
- improve handling of FTP server session timeout (#651592)

* Wed Jun 30 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-16
- add support for NTLM authentication (#606819)

* Thu Jun 17 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-15
- improve handling of proxy related environment variables (#589132)

* Tue Apr 27 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-14
- do not ignore given timeout during SSL connection (#586355)

* Wed Apr 14 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-13
- kerberos installation prefix has been changed

* Wed Apr 14 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-12
- support for CRL loading from a PEM file (#581485)

* Tue Apr 06 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-11
- eliminated a race condition in handling of SIGALRM (#579732)

* Fri Mar 26 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-10
- throw CURLE_SSL_CERTPROBLEM in case peer rejects a certificate (#565972)
- add change-log entries for patches applied upstream

* Tue Mar 23 2010 Kamil Dudka <kdudka@redhat.com> - 7.19.7-9
- remove signal handler in case of DNS timeout (#575977)

* Mon Feb 22 2010 Kamil Dudka <kdudka@redhat.com> - 7.19.7-8
- http://curl.haxx.se/docs/adv_20100209.html (#563236)

* Tue Feb 02 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-7
- mention lack of IPv6, FTPS and LDAP support while using a socks proxy
  (#559578)

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-6
- fix incorrect SSL recv/send timeout handling, patch contributed
  by Kevin Baughman
- http://permalink.gmane.org/gmane.comp.web.curl.library/26302

* Tue Dec 15 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-5
- use different port numbers for 32bit and 64bit builds
- replace hard wired port numbers in the test suite

* Tue Dec 08 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-4
- avoid use of uninitialized value in lib/nss.c
- make it possible to run test241
- suppress failure of test513 on s390
- re-enable SCP/SFTP tests (#539444)

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-3
- do not require valgrind on s390 and s390x
- temporarily disabled SCP/SFTP test-suite (#539444)

* Thu Nov 26 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-2
- workaround for broken TLS servers (#525496, #527771)

* Thu Nov 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-1
- new upstream release, dropped applied patches
- fix crash on doubly closed NSPR descriptor, patch contributed
  by Kevin Baughman (#534176)

* Sun Sep 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-10
- require libssh2>=1.2 properly (#525002)

* Sat Sep 26 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-9
- let curl test-suite use valgrind
- require libssh2>=1.2 (#525002)

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 7.19.6-8
- rebuild for libssh2 1.2

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-7
- make curl test-suite more verbose

* Wed Sep 16 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-6
- update polling patch to the latest upstream version

* Thu Sep 03 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-5
- cover ssh and stunnel support by the test-suite

* Wed Sep 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-4
- use pkg-config to find nss and libssh2 if possible
- better patch (not only) for SCP/SFTP polling
- improve error message for not matching common name (#516056)

* Fri Aug 21 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-3
- avoid tight loop during a sftp upload
- http://permalink.gmane.org/gmane.comp.web.curl.library/24744

* Tue Aug 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-2
- let curl package depend on the same version of libcurl

* Fri Aug 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-1
- new upstream release, dropped applied patches
- changed NSS code to not ignore the value of ssl.verifyhost and produce more
  verbose error messages (#516056)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.19.5-10
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-8
- do not pre-login to all PKCS11 slots, it causes problems with HW tokens
- try to select client certificate automatically when not specified, thanks
  to Claes Jakobsson

* Fri Jul 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-7
- fix SIGSEGV when using NSS client certificates, thanks to Claes Jakobsson

* Sun Jul 05 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-6
- force test suite to use the just built libcurl, thanks to Paul Howarth

* Thu Jul 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-5
- run test suite after build
- enable built-in manual

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-4
- fix bug introduced by the last build (#504857)

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-3
- exclude curlbuild.h content from spec (#504857)

* Wed Jun 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-2
- avoid unguarded comparison in the spec file, thanks to R P Herrold (#504857)

* Tue May 19 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-1
- update to 7.19.5, dropped applied patches

* Mon May 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-11
- fix infinite loop while loading a private key, thanks to Michael Cronenworth
  (#453612)

* Mon Apr 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-10
- fix curl/nss memory leaks while using client certificate (#453612, accepted
  by upstream)

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-9
- add missing BuildRequire for autoconf

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-8
- fix configure.ac to not discard -g in CFLAGS (#496778)

* Tue Apr 21 2009 Debarshi Ray <rishi@fedoraproject.org> 7.19.4-7
- Fixed configure to respect the environment's CFLAGS and CPPFLAGS settings.

* Tue Apr 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-6
- upstream patch fixing memory leak in lib/nss.c (#453612)
- remove redundant dependency of libcurl-devel on libssh2-devel

* Wed Mar 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-5
- enable 6 additional crypto algorithms by default (#436781,
  accepted by upstream)

* Thu Mar 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-4
- fix memory leak in src/main.c (accepted by upstream)
- avoid using %%ifarch

* Wed Mar 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-3
- make libcurl-devel multilib-ready (bug #488922)

* Fri Mar 06 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-2
- drop .easy-leak patch, causes problems in pycurl (#488791)
- fix libcurl-devel dependencies (#488895)

* Tue Mar 03 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-1
- update to 7.19.4 (fixes CVE-2009-0037)
- fix leak in curl_easy* functions, thanks to Kamil Dudka
- drop nss-fix patch, applied upstream

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.3-1
- update to 7.19.3, dropped applied nss patches
- add patch fixing 7.19.3 curl/nss bugs

* Mon Dec 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-9
- rebuild for f10/rawhide cvs tag clashes

* Sat Dec 06 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-8
- use improved NSS patch, thanks to Rob Crittenden (#472489)

* Tue Sep 09 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-7
- update the thread safety patch, thanks to Rob Crittenden (#462217)

* Wed Sep 03 2008 Warren Togami <wtogami@redhat.com> 7.18.2-6
- add thread safety to libcurl NSS cleanup() functions (#459297)

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-5
- undo mini libcurl.so.3

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-4
- make miniature library for libcurl.so.3

* Wed Jul  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-3
- enable support for libssh2 (#453958)

* Wed Jun 18 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-2
- fix curl_multi_perform() over a proxy (#450140), thanks to
  Rob Crittenden

* Wed Jun  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-1
- update to 7.18.2

* Wed May  7 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-2
- spec cleanup, thanks to Paul Howarth (#225671)
  - drop BR: libtool
  - convert CHANGES and README to UTF-8
  - _GNU_SOURCE in CFLAGS is no more needed
  - remove bogus rpath

* Mon Mar 31 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-1
- update to curl 7.18.1 (fixes #397911)
- add ABI docs for libcurl
- remove --static-libs from curl-config
- drop curl-config patch, obsoleted by @SSL_ENABLED@ autoconf
  substitution (#432667)

* Fri Feb 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-2
- define _GNU_SOURCE so that NI_MAXHOST gets defined from glibc

* Mon Jan 28 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-1
- update to curl-7.18.0
- drop sslgen patch -> applied upstream
- fix typo in description

* Tue Jan 22 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-6
- fix curl-devel obsoletes so that we don't break F8->F9 upgrade
  path (#429612)

* Tue Jan  8 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-5
- do not attempt to close a bad socket (#427966),
  thanks to Caolan McNamara

* Tue Dec  4 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-4
- rebuild because of the openldap soname bump
- remove old nsspem patch

* Fri Nov 30 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-3
- drop useless ldap library detection since curl doesn't
  dlopen()s it but links to it -> BR: openldap-devel
- enable LDAPS support (#225671), thanks to Paul Howarth
- BR: krb5-devel to reenable GSSAPI support
- simplify build process
- update description

* Wed Nov 21 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-2
- update description to contain complete supported servers list (#393861)

* Sat Nov 17 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-1
- update to curl 7.17.1
- include patch to enable SSL usage in NSS when a socket is opened
  nonblocking, thanks to Rob Crittenden (rcritten@redhat.com)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-10
- correctly provide/obsolete curl-devel (#130251)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-9
- create libcurl and libcurl-devel subpackages (#130251)

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-8
- list features correctly when curl is compiled against NSS (#316191)

* Mon Sep 17 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-7
- add zlib-devel BR to enable gzip compressed transfers in curl (#292211)

* Mon Sep 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-6
- provide webclient (#225671)

* Thu Sep  6 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-5
- add support for the NSS PKCS#11 pem reader so the command-line is the
  same for both OpenSSL and NSS by Rob Crittenden (rcritten@redhat.com)
- switch to NSS again

* Mon Sep  3 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-4
- revert back to use OpenSSL (#266021)

* Mon Aug 27 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-3
- don't use openssl, use nss instead

* Fri Aug 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-2
- fix anonymous ftp login (#251570), thanks to David Cantrell

* Wed Jul 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-1
- update to 7.16.4

* Mon Jun 25 2007 Jindrich Novy <jnovy@redhat.com> 7.16.3-1
- update to 7.16.3
- drop .print patch, applied upstream
- next series of merge review fixes by Paul Howarth
- remove aclocal stuff, no more needed
- simplify makefile arguments
- don't reference standard library paths in libcurl.pc
- include docs/CONTRIBUTE

* Mon Jun 18 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-5
- don't print like crazy (#236981), backported from upstream CVS

* Fri Jun 15 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-4
- another series of review fixes (#225671),
  thanks to Paul Howarth
- check version of ldap library automatically
- don't use %%makeinstall and preserve timestamps
- drop useless patches

* Fri May 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-3
- add automake BR to curl-devel to fix aclocal dir. ownership,
  thanks to Patrice Dumas

* Thu May 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-2
- package libcurl.m4 in curl-devel (#239664), thanks to Quy Tonthat

* Wed Apr 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-1
- update to 7.16.2

* Mon Feb 19 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-3
- don't create/ship static libraries (#225671)

* Mon Feb  5 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-2
- merge review related spec fixes (#225671)

* Mon Jan 29 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-1
- update to 7.16.1

* Tue Jan 16 2007 Jindrich Novy <jnovy@redhat.com> 7.16.0-5
- don't package generated makefiles for docs/examples to avoid
  multilib conflicts

* Mon Dec 18 2006 Jindrich Novy <jnovy@redhat.com> 7.16.0-4
- convert spec to UTF-8
- don't delete BuildRoot in %%prep phase
- rpmlint fixes

* Thu Nov 16 2006 Jindrich Novy <jnovy@redhat.com> -7.16.0-3
- prevent curl from dlopen()ing missing ldap libraries so that
  ldap:// requests work (#215928)

* Tue Oct 31 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-2
- fix BuildRoot
- add Requires: pkgconfig for curl-devel
- move LDFLAGS and LIBS to Libs.private in libcurl.pc.in (#213278)

* Mon Oct 30 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-1
- update to curl-7.16.0

* Thu Aug 24 2006 Jindrich Novy <jnovy@redhat.com> - 7.15.5-1.fc6
- update to curl-7.15.5
- use %%{?dist}

* Fri Jun 30 2006 Ivana Varekova <varekova@redhat.com> - 7.15.4-1
- update to 7.15.4

* Mon Mar 20 2006 Ivana Varekova <varekova@redhat.com> - 7.15.3-1
- fix multilib problem using pkg-config
- update to 7.15.3

* Thu Feb 23 2006 Ivana Varekova <varekova@redhat.com> - 7.15.1-2
- fix multilib problem - #181290 - 
  curl-devel.i386 not installable together with curl-devel.x86-64

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 7.15.1-1
- update to 7.15.1 (bug 175191)

* Wed Nov 30 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-3
- fix curl-config bug 174556 - missing vernum value

* Wed Nov  9 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-2
- rebuilt

* Tue Oct 18 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-1
- update to 7.15.0

* Thu Oct 13 2005 Ivana Varekova <varekova@redhat.com> 7.14.1-1
- update to 7.14.1

* Thu Jun 16 2005 Ivana Varekova <varekova@redhat.com> 7.14.0-1
- rebuild new version 

* Tue May 03 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-3
- fix bug 150768 - curl-7.12.3-2 breaks basic authentication
  used Daniel Stenberg patch 

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 7.13.1-2
- update to use ca-bundle in /etc/pki
- mark License as MIT not MPL

* Mon Mar  9 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-1
- rebuilt (7.13.1)

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 7.13.0-2
- rebuild with openssl-0.9.7e

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com>
- 7.13.0

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 7.12.3-3
- don't pass /usr to --with-libidn to remove "-L/usr/lib" from
  'curl-config --libs' output on x86_64.

* Fri Jan 28 2005 Adrian Havill <havill@redhat.com> 7.12.3-1
- Upgrade to 7.12.3, which uses poll() for FDSETSIZE limit (#134794)
- require libidn-devel for devel subpkg (#141341)
- remove proftpd kludge; included upstream

* Wed Oct 06 2004 Adrian Havill <havill@redhat.com> 7.12.1-1
- upgrade to 7.12.1
- enable GSSAPI auth (#129353)
- enable I18N domain names (#134595)
- workaround for broken ProFTPD SSL auth (#134133). Thanks to
  Aleksandar Milivojevic

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 7.12.0-4
- move new docs position so defattr gets applied

* Mon Sep 27 2004 Warren Togami <wtogami@redhat.com> 7.12.0-3
- remove INSTALL, move libcurl docs to -devel

* Fri Jul 26 2004 Jindrich Novy <jnovy@redhat.com>
- updated to 7.12.0
- updated nousr patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 07 2004 Adrian Havill <havill@redhat.com> 7.11.1-1
- upgraded; updated nousr patch
- added COPYING (#115956)
- 

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 31 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.8
- remove patch2, already upstream

* Wed Oct 15 2003 Adrian Havill <havill@redhat.com> 7.10.6-7
- aclocal before libtoolize
- move OpenLDAP license so it's present as a doc file, present in
  both the source and binary as per conditions

* Mon Oct 13 2003 Adrian Havill <havill@redhat.com> 7.10.6-6
- add OpenLDAP copyright notice for usage of code, add OpenLDAP
  license for this code

* Tue Oct 07 2003 Adrian Havill <havill@redhat.com> 7.10.6-5
- match serverAltName certs with SSL (#106168)

* Mon Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4.1
- bump n-v-r for RHEL

* Mon Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4
- restore ca cert bundle (#104400)
- require openssl, we want to use its ca-cert bundle

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 7.10.6-3
- rebuild

* Fri Sep  5 2003 Joe Orton <jorton@redhat.com> 7.10.6-2.2
- fix to include libcurl.so

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2.1
- bump n-v-r for RHEL

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2
- devel subpkg needs openssl-devel as a Require (#102963)

* Tue Jul 28 2003 Adrian Havill <havill@redhat.com> 7.10.6-1
- bumped version

* Tue Jul 01 2003 Adrian Havill <havill@redhat.com> 7.10.5-1
- bumped version

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.4
- adapt nousr patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Joe Orton <jorton@redhat.com> 7.9.8-4
- don't add -L/usr/lib to 'curl-config --libs' output

* Mon Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 7.9.8-3
- rebuild

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 7.9.8-2
- fix `curl-config --libs` output for libdir!=/usr/lib
- remove docs/LIBCURL from docs list; remove unpackaged libcurl.la
- libtoolize and reconf

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.8-1
- 7.9.8 (# 69473)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.7-1
- 7.9.7

* Wed Apr 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.6-1
- 7.9.6

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-2
- Stop the curl-config script from printing -I/usr/include 
  and -L/usr/lib (#59497)

* Fri Mar  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-1
- 7.9.5

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.3-2
- Rebuild

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 7.9.3-1
- update to 7.9.3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 7.9.2-2
- automated rebuild

* Wed Jan  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.2-1
- 7.9.2

* Fri Aug 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- include curl-config in curl-devel
- update to 7.8 to fix memory leak and strlcat() symbol pollution from libcurl

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added openssl-devel build req

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the distro

* Tue Apr 24 2001 Jeff Johnson <jbj@redhat.com>
- upgrade to curl-7.7.2.
- enable IPv6.

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Thu Jan  4 2001 Tim Powers <timp@redhat.com>
- fixed mising ldconfigs
- updated to 7.5.2, bug fixes

* Mon Dec 11 2000 Tim Powers <timp@redhat.com>
- updated to 7.5.1

* Mon Nov  6 2000 Tim Powers <timp@redhat.com>
- update to 7.4.1 to fix bug #20337, problems with curl -c
- not using patch anymore, it's included in the new source. Keeping
  for reference

* Fri Oct 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bogus req in -devel package

* Fri Oct 20 2000 Tim Powers <timp@redhat.com> 
- devel package needed defattr so that root owns the files

* Mon Oct 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 7.3
- apply vsprintf/vsnprintf patch from Colin Phipps via Debian

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable SSL support
- fix packager tag
- move buildroot to %%{_tmppath}

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- fixed vendor tag for bug #15028

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Tue Jul 11 2000 Tim Powers <timp@redhat.com>
- workaround alpha build problems with optimizations

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- put man pages in correct place
- use %%makeinstall

* Mon Apr 24 2000 Tim Powers <timp@redhat.com>
- updated to 6.5.2

* Wed Nov 3 1999 Tim Powers <timp@redhat.com>
- updated sources to 6.2
- gzip man page

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Thu Aug 26 1999 Tim Powers <timp@redhat.com>
- changelog started
- general cleanups, changed prefix to /usr, added manpage to files section
- including in Powertools
