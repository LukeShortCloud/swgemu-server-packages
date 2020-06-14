%define core3_commit 200e10be5055ac596c3fe4866f0a69e846314631

Name: swgemu-server
Version: 20200521
Release: 1%{?dist}
Summary: Run a Star Wars Galaxies server with SWGEmu.
License: GPLv3
URL: https://github.com/ekultails/swgemu-server-packages
%undefine _disable_source_fetch
SOURCE0: swgemu-server.service
SOURCE1: readme.md
BuildRequires: automake coreutils ccache cmake findutils git gcc gcc-c++ java-1.8.0-openjdk-headless libasan libatomic libdb-devel lua-devel make mariadb-devel openssl-devel
Requires: binutils java-1.8.0-openjdk-headless lua libdb shadow-utils
Suggests: mariadb-server


%description
Star Wars Galaxies Emulator (SWGEmu) server. Documentation for setting up a new server is provided at /opt/swgemu/doc/readme.md.


%build
if [ ! -d "Core3" ]; then
    git clone https://github.com/swgemu/Core3.git
    pushd .
    cd Core3
    # Required to pull in the engine3 dependency.
    git submodule update --init --recursive
    popd
fi

cd Core3
git reset --hard
git clean -fdx
git fetch --all
git checkout %{core3_commit}
git submodule update --recursive --remote
cd MMOCoreORB
# Disable the usage of the compilation argument "-march=native" for generic builds.
# Do not force GCC to error out on warnings.
# Enable ccache for faster compilation time when recreating the RPM.
sed -i 's/CMAKE_ARGS\ =/CMAKE_ARGS=-DENABLE_NATIVE=OFF\ -DENABLE_ERROR_ON_WARNINGS=OFF\ -DCMAKE_CXX_COMPILER_LAUNCHER=ccache/g' Makefile
make -j $(nproc)
cd %{_builddir}
# This will find and delete all files that contain a word and
# end with the file extension ".cpp", ".h", or ".py" (source files).
find . -regextype posix-egrep -regex '(.+\/\w+\.cpp|.+\/\w+\.h|.+\/\w+\.py)' -delete
# Remove all git related files.
find . -name ".git*" -exec rm -rf {} \; 2> /dev/null || true

%pre
getent group swgemu >/dev/null || groupadd -r swgemu
getent passwd swgemu >/dev/null || \
    useradd -r -g swgemu -s /sbin/nologin \
    -c "Non-privileged user for running the SWGEmu server." swgemu
exit 0


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/swgemu-server/doc/ %{buildroot}/usr/lib/systemd/system/ %{buildroot}/etc/
cp -r Core3/MMOCoreORB/bin %{buildroot}/opt/swgemu-server/
cp -r Core3/MMOCoreORB/sql %{buildroot}/opt/swgemu-server/
ln -s /opt/swgemu-server/bin/conf %{buildroot}/etc/swgemu-server
cp %{SOURCE0} %{buildroot}/usr/lib/systemd/system/
cp %{SOURCE1} %{buildroot}/opt/swgemu-server/doc/


%files
%doc
%attr(-, swgemu, swgemu) /opt/swgemu-server
%attr(644, root, root) /usr/lib/systemd/system/swgemu-server.service
%config(noreplace) /opt/swgemu-server/bin/conf/config.lua
%config(noreplace) /opt/swgemu-server/bin/databases
/etc/swgemu-server


%preun
/usr/bin/systemctl stop swgemu-server


%postun
/usr/bin/systemctl daemon-reload
rm -f /etc/swgemu-server
exit 0


%changelog
* Sun May 24 2020 Luke Short <ekultails@gmail.com> 20200521-1
- Update to the latest release of SWGEmu
- Use the recently open sourced engine3 project instead of the proprietary binary PublicEngine project
- Add build dependency on coreutils to have nproc

* Wed Nov 6 2019 Luke Short <ekultails@gmail.com> 20191028-1
- Update to the latest release of SWGEmu and use the new GitHub repositories

* Sat Nov 2 2019 Luke Short <ekultails@gmail.com> 20190705-9
- Keep the databases directory during package updates
- Re-enable ccache build depedency (it is available in EPEL for EL8 now)
- Stop the swgemu-server service during a package removable/update
- Symlink /opt/swgemu-server/bin/conf to /etc/swgemu-server
- Remove all git files

* Wed Aug 14 2019 Luke Short <ekultails@gmail.com> 20190705-8
- Only include the binaries in the RPM
- Suggest maraidb-server instead of mariadb as a dependency
- Ignore all GCC warnings
- Do not quote CMake arguments

* Fri Aug 9 2019 Luke Short <ekultails@gmail.com> 20190705-7
- Ignore GCC deprecated-copy and pessimizing-move warnings

* Thu Aug 8 2019 Luke Short <ekultails@gmail.com> 20190705-6
- Use the full path for the core3 executable in the systemd unit file

* Wed Aug 7 2019 Luke Short <ekultails@gmail.com> 20190705-5
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
