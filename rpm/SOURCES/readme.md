# SWGEmu Server

* [Getting Started](#getting-started)
    * [Database](#getting-started---database)
    * [TRE Files](#getting-started---tre-files)
    * [Planets](#getting-started---planets)
* [Configurations](#configurations)
    * [Ports](#configurations---ports)
    * [Users](#configurations---users)


# Getting Started

After installing the "swgemu-server" package for the first time, initial setup is required. A MySQL or MariaDB database needs to be setup and configured. The client TRE files also need to be copied over from a official Star Wars Galaxies game installation.


## Getting Started - Database

All of the databases and tables are stored in the "/opt/swgemu-server/MMOCoreORB/sql/" directory.

Install a MySQL compatiblle database server.

```
# dnf install mariadb
# systemctl start mariadb
# systemctl enable mariadb
```

As the root MySQL user, create the `swgemu` MySQL database and import all of the required tables.

```
# mysql
mysql> CREATE DATABASE IF NOT EXISTS swgemu;
mysql> USE swgemu;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/datatables.sql;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/mantis.sql;
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/swgemu.sql;
```

Assign a MySQL user to the database. In this example, "swgemu" is used as the MySL user.

```
mysql> GRANT ALL ON swgemu.* TO `swgemu`@`localhost` IDENTIFIED BY “<PASSWORD>”;
```

For accounting purposes, it is recommended to also add additional tables to record login IP addresses and deleted accounts.

```
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/updates/account_ips.sql
mysql> SOURCE /opt/swgemu-server/MMOCoreORB/sql/updates/deletedcharacters_add_dbdeleted.sql
```

Set the server's main IP address in the `swgemu.galaxy` table.

```
mysql> UPDATE swgemu.galaxy SET address="<SERVER_IP>";
```

Configure the MySQL connection details to the "swgemu" database. The Mantis configuration should mirror the original MySQL connection settings. Mantis is used for helping to track issues in the game.

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

Create an administrator user account. This can be used to log in and test the server. Normal player character accounts should have their "admin_level" set to "0."

```
$ echo -n "<ADMIN_PASSWORD>" | sha1sum
$ mysql -u swgemu -p
Enter password: <PASSWORD>
mysql> INSERT INTO swgemu.accounts (username, password, admin_level) VALUES ("swgemu", "<SHA1_HASHED_ADMIN_PASSWORD>", 15);
```

Start the server using systemd or manually.

```
# systemctl start swgemu-server
```
```
# cd /opt/swgemu-server/MMOCoreORB/bin/
# core3
```


# Getting Started - TRE Files

TRE files contain all of the models and client-side data for rendering. These must be obtained by an installation of a fully updated original Star Wars Galaxies game. Some TRE files may need to be copied from a SWGEmu launcher installation. The TRE files to load can be modified in the  "/opt/swgemu-server/MMOCoreORB/bin/conf/config.lua" file.

* TrePath = The full path to the directory that contains the TRE files and the "live.cfg" configuration file. By default, SWGEmu will look for TRE files in the "/home/swgemu/Desktop/SWGEmu/" directory.
* TreFiles = All of the TRE files to load for the server.


# Getting Started - Planets

By default, only the Tutorial and Tatooine zones are enabled to lower the resource usage of a new server. Enabling and disabling zones/planets is handled in the "/opt/swgemu-server/MMOCoreORB/bin/conf/config.lua" file with the "ZonesEnabled" variable. Remove any "--" Lua comment characters from planets that should be enabled. Below is an example of enabling all zones.

```
ZonesEnabled = {
        "09",
        "10",
        "11",
        "character_farm",
        "cinco_city_test_m5",
        "corellia",
        "creature_test",
        "dantooine",
        "dathomir",
        "dungeon1",
        "endor",
        "endor_asommers",
        "floratest",
        "godclient_test",
        "lok",
        "naboo",
        "otoh_gunga",
        "rivertest",
        "rori",
        "runtimerules",
        "simple",
        "space_09",
        "space_corellia",
        "space_corellia_2",
        "space_dantooine",
        "space_dathomir",
        "space_endor",
        "space_env",
        "space_halos",
        "space_heavy1",
        "space_light1",
        "space_lok",
        "space_naboo",
        "space_naboo_2",
        "space_tatooine",
        "space_tatooine_2",
        "space_yavin4",
        "taanab",
        "talus",
        "tatooine",
        "test_wearables",
        "tutorial",
        "umbra",
        "watertabletest",
        "yavin4"
}
```


# Configurations

All of the server files are located in "/opt/swgemu-server/" directory. The main configuration file is "/opt/swgemu-server/MMOCoreORB/bin/conf/config.lua."

Lua scripts from "/opt/swgemu-server/MMOCoreORB/bin/scripts/" are used to handle many in-game mechanics.

* ai = Determine artificial intelligence (A.I.) logic for non-player characters (NPCs).
* commands = Commands that player characters (PCs) can run in-game.
* loot = These handle which objects can be found in continers or dropped from a dead NPC.
* managers = These handle passive events such as weather, player creation, crafting, etc.
* mobile = Determine when, where, and for how long objects will spawn.
* object = All objects in the game such as armor, weapons, and space ships.
* screenplays = These handle reactions to events that players can trigger such as conversations.
* skills = User privileges are defined here for use with the "staff" groups.
* staff = Staff groups are assigned to a player character (via the database) as a access control list (ACL) for what commands they can run.
* utils = Miscellaneous global functions that can be used for other scripts.


## Configurations - Ports

Many ports are used for the SWGEmu server.

| Name | Port | Description |
| --- | --- | --- |
| ORBPort | 44419 | The port to listen on for the MMOCoreORB game engine. |
| DBPort | 3306 | The MySQL database client port to connect to the "swgemu" database.. |
| Login Port | 44453 | The port to listen on for user account authentication. |
| MantisPort | 3306 | The MySQL databse client port to use to connect to the "mantis" database. |
| PingPort | 44462 | The port to listen on for simple server status connections from clients. |
| StatusPort | 44455 | The port to listen on to report the health of a server. |
| WebPorts | 44460 | |


## Configurations - Users

SWGEmu user accounts are all handled by the "swgemu" database. User passwords are stored after being encrypted in SHA1. Adding users can be done via the command.

```
$ echo -n "<PASSWORD>" | sha1sum
$ mysql -u swgemu -p
Enter password: <PASSWORD>
mysql> INSERT INTO swgemu.accounts (username, password, admin_level) VALUES ("swgemu", "<SHA1_HASHED_ADMIN_PASSWORD>", <ADMIN_LEVEL>);
```

Different admin levels exist to give users more or less control of the server. These access control lists (ACLs) are all defined as Lua scripts in "/opt/swgemu-server/MMOCoreORB/bin/scripts/staff/levels." The default levels include:

* 15 = Administrator
* 14 = Developer
* 13 = Quality assurance (QA)
* 12 = Community Support Representative (CSR)
* 11 = Event Coordinator (EC)
* 10 = Event Coordinator Intern (ECI)
* 9 = Community Support Intern (CSI)
* 8 = CT
* 7 = CC
* 6 = Tester
* 1 = Intern
* 0 = Non-privileged player