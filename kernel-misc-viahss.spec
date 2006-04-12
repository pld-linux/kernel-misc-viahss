#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%define		_rel	0.1
Summary:	VIA High Speed Serial
Summary(pl):	VIA High Speed Serial
Name:		kernel-misc-viahss
Version:	0.92
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.kati.fi/viahss/viahss-%{version}.tar.gz
# Source0-md5:	a63cdb34bf50676f232192b570dd7c37
URL:		http://www.kati.fi/viahss/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VIA High Speed Serial is a little kernel module (1 KB) which enables
high speed serial port modes of VIA VT82C686A or VT82C686B
southbridge-equipped motherboards. With this module, you can use the
serial port at 230400 bit/s so that you can get the full 128000 bit/s
from ISDN-TA. The module has been tested with both 686A and 686B
chipsets.

%description -l pl
VIA High Speed Serial to ma³y modu³ j±dra (1kB) w³±czaj±cy szybkie
tryby pracy portu szeregowego wbudowanego w p³yty g³ówne z mostkiem
po³udniowym VIA VT82C686A lub VT82C686B. Przy pomocy tego modu³u mo¿na
u¿ywaæ portu szeregowego z prêdko¶ci± 230400 bit/s, co pozwala na
uzyskanie pe³nego transferu 128000 bit/s w komunikacji z ISDN-TA. Ten
modu³ by³ testowany z uk³adami zarówno 686A jak i 686B.

%package -n kernel-smp-misc-viahss
Summary:	Linux SMP driver for VIA High Speed Serial
Summary(pl):	Sterownik dla Linuksa SMP do VIA High Speed Serial
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-misc-viahss
VIA High Speed Serial SMP is a little SMP kernel module (1 KB) which
enables high speed serial port modes of VIA VT82C686A or VT82C686B
southbridge-equipped motherboards. With this module, you can use the
serial port at 230400 bit/s so that you can get the full 128000 bit/s
from ISDN-TA. The module has been tested with both 686A and 686B
chipsets.

%description -n kernel-smp-misc-viahss -l pl
VIA High Speed Serial SMP to ma³y modu³ j±dra SMP (1kB) w³±czaj±cy
szybkie tryby pracy portu szeregowego wbudowanego w p³yty g³ówne z
mostkiem po³udniowym VIA VT82C686A lub VT82C686B. Przy pomocy tego
modu³u mo¿na u¿ywaæ portu szeregowego z prêdko¶ci± 230400 bit/s, co
pozwala na uzyskanie pe³nego transferu 128000 bit/s w komunikacji z
ISDN-TA. Ten modu³ by³ testowany z uk³adami zarówno 686A jak i 686B.

%prep
%setup -q -n viahss-%{version}
mv -f Makefile{-2.6,}

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	mv viahss{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install viahss-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/viahss.ko
%if %{with smp} && %{with dist_kernel}
install viahss-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/viahss.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-viahss
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-viahss
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-viahss
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
