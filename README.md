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
	* SWGEmu requires at least Lua version 5.2 for support for newer functions such as `lua_version` and `luaL_traceback`. The development team recommends Lua 5.3. Since RHEL 7.2, only Lua 5.1 is provided as a dependency of the RPM utility. Replacing the system Lua library is not supported or endorsed by this repository. SWGEmu also does not currently provide a way to use a custom library location for Lua.
* Why is Debian not supported?
	* A Debian package is planned. For now, the official SWGEmu development environment, [ZonamaDev](https://github.com/Scurby/ZonamaDev), can be used for running a Debian 8 (Jessie) server.


# License

This software is licensed under the GPLv3. More information about this can be found in the included "LICENSE" file or online at: http://www.gnu.org/licenses/gpl-3.0.en.html