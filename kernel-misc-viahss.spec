#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
%define		_orig_name	viahss
%define		_rel		0.1

Summary:	VIA High Speed Serial
Summary(pl):	VIA High Speed Serial
Name:		kernel-net-%{_orig_name}
Version:	0.92
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.kati.fi/%{_orig_name}/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	a63cdb34bf50676f232192b570dd7c37
URL:		http://www.kati.fi/%{_orig_name}/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VIA High Speed Serial is a little kernel module (1 KB) which enables high speed serial
port modes of VIA VT82C686A or VT82C686B southbridge-equipped motherboards.
With this module, you can use the serial port at 230400 bit/s so that
you can get the full 128000 bit/s from ISDN-TA. The module has been tested with both 686A and
686B chipsets.

%description -l pl
dopisz mnie

%package -n kernel-smp-net-%{_orig_name}
Summary:	VIA High Speed Serial - SMP
Summary(pl):	VIA High Speed Serial - SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-%{_orig_name}
VIA High Speed Serial is a little kernel module (1 KB) which enables high speed serial
port modes of VIA VT82C686A or VT82C686B southbridge-equipped motherboards.
With this module, you can use the serial port at 230400 bit/s so that
you can get the full 128000 bit/s from ISDN-TA. The module has been tested with both 686A and
686B chipsets.

SMP version.

%description -n kernel-smp-net-%{_orig_name} -l pl
dopisz mnie

%prep
%setup -q -n %{_orig_name}-%{version}

%build
rm -f %{_orig_name}.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ \
    -O2 -DSMP=1 -D__SMP__ \
%ifarch %{ix86}
    -DCONFIG_X86_LOCAL_APIC \
%endif
    -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c

mv -f %{_orig_name}.o %{_orig_name}-smp.o

%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean 
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
