import net.listener as server
server.db.create_table()
server.LOCAL_SERVER.serve_forever()