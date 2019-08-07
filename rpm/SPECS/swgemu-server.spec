%define core3_commit cd5b463d60f34de138861bff5b00d8554655103a
%define publicengine_commit 1bbdb8a182a9e44bc23f1d972ac254c1ca98db03

Name: swgemu-server
Version: 20190705
Release: 5%{?dist}
Summary: Run a Star Wars Galaxies server with SWGEmu.
License: GPLv3
URL: https://github.com/ekultails/swgemu-server-packages
%undefine _disable_source_fetch
SOURCE0: https://github.com/TheAnswer/PublicEngine/archive/%{publicengine_commit}.tar.gz
SOURCE1: swgemu-server.service
SOURCE2: readme.md
BuildRequires: automake cmake findutils git gcc gcc-c++ java-1.8.0-openjdk-headless libatomic libdb-devel lua-devel make mariadb-devel openssl-devel
%if 0%{?fedora}
BuildRequires: ccache
%endif
Requires: java-1.8.0-openjdk-headless lua libdb shadow-utils
Suggests: mariadb


%description
Star Wars Galaxies Emulator (SWGEmu) server. Documentation for setting up a new server is provided at /opt/swgemu/doc/readme.md.


%prep
tar -x -v -f %{SOURCE0}


%build
pushd .
cd PublicEngine-%{publicengine_commit}/MMOEngine
make
chmod 755 bin/idlc

if [ -z ${CLASSPATH+x} ]; then
    export CLASSPATH="$(pwd)/bin/idlc.jar"
else
    # Append to the CLASSPATH variable if it exists.
    export CLASSPATH="${CLASSPATH}:$(pwd)/bin/idlc.jar"
fi

popd

if [ ! -d "Core3" ]; then
    git clone https://github.com/TheAnswer/Core3.git
fi

cd Core3
git reset --hard
git clean -fdx
git fetch --all
git checkout %{core3_commit}

# If the symbolic link to "MMOEngine" does not exist,
# then create it.
if [[ ! -h "MMOEngine" ]]; then
    ln -s ../PublicEngine-%{publicengine_commit}/MMOEngine MMOEngine
fi

cd MMOCoreORB
make config
make config
make cleanidl
# Disable the usage of the compilation argument "-march=native" for generic builds.
# Enable ccache for faster compilation time when recreating the RPM.
%if 0%{?fedora}
sed -i 's/CMAKE_ARG\S =/CMAKE_ARGS="-DENABLE_NATIVE=OFF -DCMAKE_CXX_COMPILER_LAUNCHER=ccache"/g' Makefile
%else
sed -i 's/CMAKE_ARG\S =/CMAKE_ARGS="-DENABLE_NATIVE=OFF"/g' Makefile
%endif
make -j 4 build-cmake
cd %{_builddir}
# This will find and delete all files that contain a word and
# end with the file extension ".cpp", ".h", or ".py" (source files).
find . -regextype posix-egrep -regex '(.+\/\w+\.cpp|.+\/\w+\.h|.+\/\w+\.py)' -delete


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
cp -r PublicEngine-%{publicengine_commit}/MMOEngine %{buildroot}/opt/swgemu-server/
cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
find %{buildroot} -name ".git*" -delete
cp %{SOURCE2} %{buildroot}/opt/swgemu-server/doc/


%files
%doc
%attr(-, swgemu, swgemu) /opt/swgemu-server
%attr(644, root, root) /usr/lib/systemd/system/swgemu-server.service
%config(noreplace) /opt/swgemu-server/MMOCoreORB/bin/conf/config.lua


%postun
/usr/bin/systemctl daemon-reload
exit 0


%changelog
* Wed Aug 7 2019 Luke Short <ekultails@gmail.com> 20190707-5
- Only have a build dependency for ccache on Fedora where it is available

* Sun Aug 4 2019 Luke Short <ekultails@gmail.com> 20190705-4
- Delete Python files from the source code
- Use ccache for faster compilation
- Suggest mariadb as a dependency

* Wed Jul 31 2019 Luke Short <ekultails@gmail.com> 20190705-3
- Remove pandoc as a build dependency

* Sun Jul 28 2019 Luke Short <ekultails@gmail.com> 20190705-2
- Include source files in the RPM spec file
- Do not delete the local Core3 git repository when rebuilding the RPM
- Remove workaround for the idlc symlink (the build now uses a relative path)
- Turn off native CPU compilation for generic x86_64 builds

* Fri Jul 5 2019 Luke Short <ekultails@gmail.com> 20190705-1
- Update Core3 to the latest commit (cd5b463d) to address build issues with GCC 8
- Use a git repository for Core3
- Add build dependency: openssl-devel

* Mon Jun 24 2019 Luke Short <ekultails@gmail.com> 20190623-1
- Use specific git commits for the build
- Use the date of the latest commit for the swgemu-server version

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
