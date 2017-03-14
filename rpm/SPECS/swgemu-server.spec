%define timestamp_iso %(date +"%Y%m%d")

Name: swgemu-server
Version: %{timestamp_iso}
Release: 2%{?dist}
Summary: Run a Star Wars Galaxies server with SWGEmu.	

License: GPLv3
URL: https://github.com/ekultails/swgemu-server-packages	

BuildRequires: automake git gcc gcc-c++ java-1.8.0-openjdk-headless libdb-devel lua-devel mariadb-devel
Requires: lua libdb java-1.8.0-openjdk-headless shadow-utils

%description

%build

if [[ -d "PublicEngine" ]]; then
    cd PublicEngine
    git checkout master
	# undo any local changes
    git reset --hard
	# delete any other non-repository files such as existing compiled code
    git clean -f -d
    # pull the latest code
    git pull origin master
    cd ..
else
    git clone https://github.com/TheAnswer/PublicEngine.git
fi

if [[ -d "Core3" ]]; then
    cd Core3
    git checkout unstable
    git reset --hard
    git clean -f -d
    git pull origin unstable
    cd ..
else
    git clone https://github.com/TheAnswer/Core3.git
fi

cd PublicEngine/MMOEngine
make
chmod 755 bin/idlc

# the Makefile for Core3 is hardcoded to use this path for idlc
if [[ ! -f "/usr/local/bin/idlc" && ! -h "/usr/local/bin/idlc" ]]; then
    su root -c 'ln -s "$(pwd)/bin/idlc" /usr/local/bin/idlc'
fi

if [ -z ${CLASSPATH+x} ]; then
    export CLASSPATH="$(pwd)/bin/idlc.jar"
else
    # append to the CLASSPATH variable if it exists
    export CLASSPATH="${CLASSPATH}:$(pwd)/bin/idlc.jar"
fi

cd -

if [[ ! -h "Core3/MMOEngine" ]]; then
    ln -s ../PublicEngine/MMOEngine Core3/MMOEngine
fi

cd Core3/MMOCoreORB
make config
make rebuild

%pre
getent group swgemu >/dev/null || groupadd -r swgemu
getent passwd swgemu >/dev/null || \
    useradd -r -g swgemu -s /sbin/nologin \
    -c "Non-privileged user for running the SWGEmu server." swgemu
exit 0

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin/ %{buildroot}/opt/swgemu-server/ %{buildroot}/usr/lib/systemd/system/
cp -r Core3/MMOCoreORB %{buildroot}/opt/swgemu-server/
cp -r PublicEngine/MMOEngine %{buildroot}/opt/swgemu-server/
cp %{_sourcedir}/swgemu-server.service %{buildroot}/usr/lib/systemd/system/

%files
%doc
%attr(-, swgemu, swgemu) /opt/swgemu-server
%attr(755, swgemu, swgemu) /opt/swgemu-server/MMOCoreORB/bin/core3
%attr(644, root, root) /usr/lib/systemd/system/swgemu-server.service

%postun
/usr/bin/systemctl daemon-reload
exit 0

%changelog
* Mon Mar 13 2017 Luke Short <ekultails@gmail.com> 2
- Remove the "configure.ac" patch for RHEL, I got this patched upstream
    - https://github.com/TheAnswer/Core3/commit/085e2dbb21e7e97a09f2a37437a392d5143680d2
- Rebuild source code with 'make rebuild' instead of 'make build' to clean up any precompiled code
- The systemd unit file now correctly changes the 'WorkingDirectory' to start the 'core3' daemon

* Sun Feb 26 2017 Luke Short <ekultails@gmail.com> 1
- Initial RPM spec release
