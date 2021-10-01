# How to use

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

Then, you can cun the client process:

```shell
python ./run_client.py
```

Once you enter the command line interface, you can choose the option between `server` | `client` | `none`

If `server` is selected, you will want to connect an IDFS server.

If `client` is selected, you will want to connect another IDFS client. If that client is connected to devices, this device you use will also join that cluster.

If `none` is selected, this device you use will become a single device.
