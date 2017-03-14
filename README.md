* [SWGEmu Server Packages](#sgwemu-server-packages)
	* [RPM](#rpm)
	* [Server Configuration](#server-configuration)
	* [FAQ](#faq)


# SWGEmu Server Packages

This repository aims to provide easily available (unofficial) Linux packages for creating and installing a SWGEmu server. By building system packages, end user's can quickly create or delete SWGEmu servers.

These packages are required to be compiled first. The latest code from GitHub for the [PublicEngine](https://github.com/TheAnswer/PublicEngine) and [Core3](https://github.com/TheAnswer/Core3) projects are automatically downloaded and used.


## RPM

The RPM is only offiically supported on Fedora >= 25.

How to create the RPM:
~~~
$ mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
$ cp -r rpm/SOURCES/* ~/rpmbuild/SOURCES/
$ cp -r rpm/SPECS/* ~/rpmbuild/SPECS/
$ sudo dnf builddep ~/rpmbuild/SPECS/swgemu-server.spec
$ rpmbuild -bb ~/rpmbuild/SPECS/swgemu-server.spec
~~~

The compiled RPM will be available at `~/rpmbuild/RPMS/x86_64/swgemu-server-<ISO_TIMESTAMP>-<RPM_SPEC_RELEASE>.<OS_VERSION>.x86_64.rpm`.


## Server Configuration

This is a post-installation configuration guide. The server files are located in `/opt/swgemu-server/`.

* Create the `swgemu` MySQL database and import all of the required tables.

```
mysql> CREATE DATABASE IF NOT EXISTS swgemu;
mysql> USE swgemu;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/datatables.sql;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/mantis.sql;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/swgemu.sql;
```

* Assign a MySQL user to the database.

```
mysql> GRANT ALL ON swgemu.* TO `swgemu`@`localhost` IDENTIFIED BY “<PASSWORD>”;
```

* For accounting purposes, it is recommended to also add additional tables to record login IP addresses and deleted accounts.
	* /opt/swgemu-server/MMOCoreORB/sql/updates/account_ips.sql
	* /opt/swgemu-server/MMOCoreORB/sql/updates/deletedcharacters_add_dbdeleted.sql

* Set the server's main IP address in the `swgemu.galaxy` table.

```
mysql> UPDATE swgemu.galaxy SET address="<SERVER_IP>";
```

* Configure the MySQL connection details to the "swgemu" database. The Mantis configuration should mirror the original MySQL connection settings.

```
# vim /opt/swgemu-server/MMOCoreORB/bin/conf/config.lua
DBHost = 127.0.0.1
DBPort = 3306
DBName = swgemu
DBUser = swgemu
DBPass = <PASSWORD>
DBSecret = <RANDOM_SECRET_STRING>
MantisHost = 127.0.0.1
MantisPort = 3306
MantisName = swgemu
MantisUser = swgemu
MantisPass = <PASSWORD>
MantisPrfx = "mantis_"
```

* Start the server.

```
# systemctl start swgemu-server
OR
# cd /opt/swgemu-server/MMOCoreORB/bin/
# core3
```

* Create an administrator user account. This can be used to log in and test the server.

```
$ echo -n "<ADMIN_PASSWORD>" | sha1sum
$ mysql -u swgemu -p
Enter password: <PASSWORD>
mysql> INSERT INTO swgemu.accounts (username, password, admin_level) VALUES ("swgemu", "<SHA1_HASHED_ADMIN_PASSWORD>", 15);
```

* Normall player accounts should have their `admin_level` set to `0`.


## FAQ

* There is `XYZ` problem with building the RPM. What should I do?
	* The source code is compiled from the latest unstable code that is in constant development. It is very likely that it is a bug in the source code. Visit [http://gerrit.swgemu.com](http://gerrit.swgemu.com) to view or open a bug report. If the problem is directly related to the RPM spec file then open an issue in this GitHub project.
* Why is Red Hat Enterprise Linux (RHEL) not supported?
	* SWGEmu requires at least Lua version 5.2 for support for newer functions such as `lua_version` and `luaL_traceback`. The development team recommends Lua 5.3. Since RHEL 7.2, only Lua 5.1 is provided as a dependency of the RPM utility. Replacing the system Lua library is not supported or endorsed by this repository. SWGEmu also does not currently provide a way to use a custom library location for Lua.
* Why is Debian not supported?
	* A Debian package is planned. For now, the official SWGEmu development environment, [ZonamaDev](https://github.com/Scurby/ZonamaDev), can be used for running a Debian 8 (Jessie) server.


# License

This software is licensed under the GPLv3. More information about this can be found in the included "LICENSE" file or online at: http://www.gnu.org/licenses/gpl-3.0.en.html
