%define		mod_name	extract_forwarded
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Extract X-Forwarded-For header
Name:		apache-mod_%{mod_name}
Version:	2.0.2
Release:	1
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	http://www.openinfo.co.uk/apache/%{mod_name}-%{version}.tar.gz
# Source0-md5:	d7aeb59fa81cbe74c485c33873ea1c65
Source1:	%{name}.conf
URL:		http://www.openinfo.co.uk/apache/index.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_extract_forwarded is designed to transparently (to other Apache modules)
modify the information about the connection over which an HTTP request is
received when that connection is not directly from a requesting client to
the Apache server but is instead via one or more intervening proxy servers.

Operation relies on the X-Forwarded-For header, inserted by proxy servers.
This is a non-RFC-standard request header which was introduced by the Squid
caching proxy server's developers and which is now also supported, for
reverse proxy server operation, by Apache 2. If the intervening proxy
servers doesn't add such headers, we can't do anything about it. It is
worth noting that a normally configured Squid proxy server will add to the
X-Forwarded-For. However, when used as a proxy server, Apache prior to
version 2 does not add X-Forwarded-For headers unless the third party
mod_proxy_add_forward module has been added to it. This can leave
potentially important gaps in the information recorded in X-Forwarded-For
header. 

%prep
%setup -q -n %{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf
install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README INSTALL
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
