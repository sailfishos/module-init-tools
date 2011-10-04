Summary: Kernel module management utilities
Name: module-init-tools
Version: 3.11.1
#define PreRelease
Release: 2
License: GPLv2+
Group: System/Kernel
#Source: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%{version}%{PreRelease}.tar.bz2
#Source1: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%{version}%{PreRelease}.tar.bz2.sign
Source: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%{version}.tar.bz2
Source1: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%{version}.tar.bz2.sign
Source2: modprobe-dist.conf
Source3: weak-modules
Source4: depmod-dist.conf
Exclusiveos: Linux
Obsoletes: modutils-devel modutils
Provides: modutils = %{version}
BuildRequires: zlib-devel
BuildRequires: zlib-static glibc-static

%description
The module-init-tools package includes various programs needed for automatic
loading and unloading of modules under 2.6 and later kernels, as well
as other module management programs. Device drivers and filesystems
are two examples of loaded and unloaded modules.

%prep
#setup -q -n module-init-tools-%{version}%{PreRelease}
%setup -q -n module-init-tools-%{version}

%build
export CC=gcc
export CFLAGS="$RPM_OPT_FLAGS -DCONFIG_NO_BACKWARDS_COMPAT=1"
%configure --enable-zlib
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall sbindir=$RPM_BUILD_ROOT/sbin

install -m 644 modprobe.conf.5 \
 $RPM_BUILD_ROOT/%{_mandir}/man5/modprobe.d.5

install -m 644 depmod.conf.5 \
 $RPM_BUILD_ROOT/%{_mandir}/man5/depmod.d.5

mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/modprobe.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/modprobe.d/dist.conf
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/sbin/weak-modules

mkdir -p $RPM_BUILD_ROOT/etc/depmod.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/depmod.d/dist.conf

mv $RPM_BUILD_ROOT/%{_bindir}/lsmod $RPM_BUILD_ROOT/sbin

touch $RPM_BUILD_ROOT/etc/modprobe.d/local.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# We renamed all the config files upstream so they now need to end in .conf
# and live under /etc/modprobe.d. Anaconda now uses an anaconda.conf file,
# all of which means /etc/modprobe.conf is very legacy. Rename it to
# /etc/modprobe.d/local.conf and allow local hacks to go in there.
if [ -e /etc/modprobe.conf ] && [ ! -e /etc/modprobe.d/local.conf ]
then
        mv /etc/modprobe.conf /etc/modprobe.d/local.conf
fi


%files
%defattr(-,root,root)
/etc/modprobe.d
/etc/depmod.d
/sbin/*
%{_mandir}/*/*
%ghost %config(noreplace) %verify(not md5 size mtime) /etc/modprobe.d/local.conf

