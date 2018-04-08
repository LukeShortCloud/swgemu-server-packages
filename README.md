* [SWGEmu Server Packages](#sgwemu-server-packages)
	* [RPM](#rpm)
	* [Server Configuration](#server-configuration)
	* [FAQ](#faq)


# SWGEmu Server Packages

This repository aims to provide easily available and unofficial Linux packages for creating and installing a Star Wars Galaxies Emulator (SWGEmu) server. By building system packages, end user's can quickly create, update, and/or delete a server. These system packages build the latest source code from GitHub for the [PublicEngine](https://github.com/TheAnswer/PublicEngine) and [Core3](https://github.com/TheAnswer/Core3) projects to make a fully functioning SWGEmu server.


## RPM

The RPM is only offiically supported on Fedora >= 25 (64-bit).

How to create the RPM:
~~~
$ sudo dnf install 'dnf-command(builddep)' rpm-build
$ mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
$ cp -f -r rpm/SOURCES/* ~/rpmbuild/SOURCES/
$ cp -f -r rpm/SPECS/* ~/rpmbuild/SPECS/
$ sudo dnf builddep ~/rpmbuild/SPECS/swgemu-server.spec
$ rpmbuild -bb ~/rpmbuild/SPECS/swgemu-server.spec
~~~

The compiled RPM will be available at `~/rpmbuild/RPMS/x86_64/swgemu-server-<ISO_TIMESTAMP>-<RPM_SPEC_RELEASE>.<OS_VERSION>.x86_64.rpm`.


## Server Configuration

A SWGEmu server adminsitrator's guide is provided in this repository at `rpm/SOURCES/readme.md`. This is compiled into the RPM to be available at `/opt/swgemu-server/doc/readme.html` after it is installed.


## FAQ

* There is `XYZ` problem with SWGEmu. What should I do?
	* The source code is compiled from the latest unstable code that is in constant development. It is very likely that it is a bug in the source code. Visit [https://www.swgemu.com/bugs/](https://www.swgemu.com/bugs/) to view or open bug reports. Upstream patches can be submitted to [http://review.swgemu.com](http://review.swgemu.com). If the problem is directly related to the package creation then open an issue in this GitHub project.
* Why is Red Hat Enterprise Linux (RHEL) not supported?
	* SWGEmu requires at least Lua version 5.2 for support for newer functions such as `lua_version` and `luaL_traceback`. The development team recommends Lua 5.3. RHEL 7 provides Lua 5.1 by default and [will not rebase due to compatibility and stability reasons](https://bugzilla.redhat.com/show_bug.cgi?id=1437243). Replacing the system Lua library is not supported.
* Why is Debian not supported?
	* There is already an official SWGEmu development virtual machine called [ZonamaDev](https://github.com/Scurby/ZonamaDev). This uses Debian 9 (Stretch) as the operating system. There is also support for deploying SWGEmu to [Debian docker containers on Kubernetes](https://github.com/TheAnswer/Core3/commit/5815f8f975f899f626bf39e8283ae1040f087db7).


# License

This software is licensed under the GPLv3. More information about this can be found in the included "LICENSE" file or online at: http://www.gnu.org/licenses/gpl-3.0.en.html
