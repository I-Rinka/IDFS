# IDFS:the Individual Distributed File System

It is the implementation of the paper named *IDFS:the Individual Distributed File System*.

## PyIDFS

First, you need to install `pyrqlite` to enable rqlite database can be accessed by python.

```shell
cd pyrqlite
python ./setup.py install
```

and you should go to `client/config.py` to config your client.

`my_ip` is the intranet address of the personal device, and the `rqlited_path` is the path of rqlite daemon binary file.

```python
my_ip="192.168.91.8"
rqlited_path = "/home/rinka/rqlite-v6.6.0-linux-amd64/rqlited"
IDFS_root="files"
```

Worth mention, server and client configs are located in different directories.

---

As the paper described, we implement three roles of IDFS in this repository.

* In `client/` directroy, there is `active_client.py`  as the active client object.
* There is also `lonely_client.py` which is the lonely client.
* In `server/` directory, you can see the `server.py`. And this is the server that runs in server.

By institiating them and connect to a certain network, you can create your own IDFS topology.

Here are examples that show how it works:

`run_client_fst.py` is the first active client instance that runs rqlite and it initialize rqlite with its IP ``192.168.91.9`` and will connect to the server `192.168.91.8` for remote access. Then, it will upload and then download several files in `bigfile/` directory (which is not in our current repository and it holds randomly generated files).

`run_client_ac.py` creates other active clients and join the rqlite instance of the first active client. In fact, you can join rqlite instance of the second or third active client.

`run_client_ll.py` creates a lonely client that will connect to server.

`run_server.py` will create a server.

The sequence of creating topology is `run_server.py` -> `run_client_ll.py`

`run_client_fst.py` -> `run_client_ac.py`

## IDFS emulator

In `IDFS_EMU` directory, there are components to emulate the behavior of IDFS.

To simplify the work, the emulator does not create roles in IDFS. Instead, you have to use `cluster.add_active_device()` and `cluster.add_lonely_device()` to create device in different situation. The clients' role will change dynamicly. `IDFS_EMU\run.py` shows how to create IDFS cluster.

`IDFS_EMU\config.py` is configuration of time interval or other aspects.

## Known issues

rqlite some times may not response to SQL or connection.
