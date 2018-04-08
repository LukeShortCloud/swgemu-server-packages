%define timestamp_iso %(date +"%Y%m%d")

Name: swgemu-server
Version: %{timestamp_iso}
Release: 5%{?dist}
Summary: Run a Star Wars Galaxies server with SWGEmu.
License: GPLv3
URL: https://github.com/ekultails/swgemu-server-packages
BuildRequires: automake findutils git gcc gcc-c++ java-1.8.0-openjdk-headless libdb-devel lua-devel make mariadb-devel pandoc
Requires: java-1.8.0-openjdk-headless lua libdb shadow-utils


%description


%build

if [[ -d "PublicEngine" ]]; then
	cd PublicEngine
	git checkout master
	# Undo any local changes.
	git reset --hard
	# Delete any other non-repository files such as existing compiled code.
	git clean -f -d
	# Pull the latest code.
	git pull origin master
	cd ..
else
	git clone --depth 1 https://github.com/TheAnswer/PublicEngine.git
fi

if [[ -d "Core3" ]]; then
	cd Core3
	git checkout unstable
	git reset --hard
	git clean -f -d
	git pull origin unstable
	cd ..
else
	git clone --depth 1 https://github.com/TheAnswer/Core3.git
fi

pushd .
cd PublicEngine/MMOEngine
make
chmod 755 bin/idlc

# The Makefile for Core3 is hardcoded to use this path for idlc.
if [[ ! -f "/usr/local/bin/idlc" && ! -h "/usr/local/bin/idlc" ]]; then
	su root -c 'ln -s "$(pwd)/bin/idlc" /usr/local/bin/idlc'
fi

if [ -z ${CLASSPATH+x} ]; then
	export CLASSPATH="$(pwd)/bin/idlc.jar"
else
	# Append to the CLASSPATH variable if it exists.
	export CLASSPATH="${CLASSPATH}:$(pwd)/bin/idlc.jar"
fi

popd

# If the symbolic link to "MMOEngine" does not exist,
# then create it.
if [[ ! -h "Core3/MMOEngine" ]]; then
	ln -s ../PublicEngine/MMOEngine Core3/MMOEngine
fi

cd Core3/MMOCoreORB
make config
patch -p2 < %{_sourcedir}/Makefile_generic_x86-64_build.patch
make rebuild
cd %{_builddir}
# This will find and delete all files that contain a word and
# end with the file extension ".cpp" or ".h" (source files).
find . -regextype posix-egrep -regex '(.+\/\w+\.cpp|.+\/\w+\.h)' -delete


%pre
getent group swgemu >/dev/null || groupadd -r swgemu
getent passwd swgemu >/dev/null || \
	useradd -r -g swgemu -s /sbin/nologin \
	-c "Non-privileged user for running the SWGEmu server." swgemu
exit 0


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin/ %{buildroot}/opt/swgemu-server/doc/\
 %{buildroot}/usr/lib/systemd/system/
cp -r Core3/MMOCoreORB %{buildroot}/opt/swgemu-server/
cp -r PublicEngine/MMOEngine %{buildroot}/opt/swgemu-server/
cp %{_sourcedir}/swgemu-server.service %{buildroot}/usr/lib/systemd/system/
find %{buildroot} -name ".git*" -delete
pandoc %{_sourcedir}/readme.md > %{buildroot}/opt/swgemu-server/doc/readme.html


%files
%doc
%attr(-, swgemu, swgemu) /opt/swgemu-server
%attr(644, root, root) /usr/lib/systemd/system/swgemu-server.service
%config(noreplace) /opt/swgemu-server/MMOCoreORB/bin/conf/config.lua


%postun
/usr/bin/systemctl daemon-reload
exit 0


%changelog
* Sat Apr 7 2018 Luke Short <ekultails@gmail.com> 5
- Removed unnecessary dependencies
- Rebased the Makefile's generic processor compilation patch

* Mon May 29 2017 Luke Short <ekultails@gmail.com> 4
- Features added:
	- Updated RPM changelog format.
	- Server administration documentation is now included as a read me HTML file.
	- Do not override the main configuration file "config.lua" on package upgrades.
	- Remove all Git related files from the built RPM.
- Bugs fixed:
	- Patched the Core3 Makefile to allow cross-platform compilation for all x86-64 processors.
	- The systemd unit file will now correctly stop the server.

* Sat Mar 25 2017 Luke Short <ekultails@gmail.com> 3
- Feature added: Decreased the build time of the package and saved space in the RPM.

* Mon Mar 13 2017 Luke Short <ekultails@gmail.com> 2
- Features added:
	- Remove the "configure.ac" patch for RHEL, I got this patched upstream.
		- https://github.com/TheAnswer/Core3/commit/085e2dbb21e7e97a09f2a37437a392d5143680d2
	- Rebuild source code with 'make rebuild' instead of 'make build' to clean up any precompiled code.
- Bug fixed: The systemd unit file now correctly changes the 'WorkingDirectory' to start the 'core3' daemon.

* Sun Feb 26 2017 Luke Short <ekultails@gmail.com> 1
- Initial RPM spec release.
