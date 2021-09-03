import net.listener as server
import util.tools as ut
print("My name: %s\nMy id: %s\n" % (ut.GetMyDevName(), ut.GetMyDeviceID()))
server.db.create_table()
server.LOCAL_SERVER.serve_forever()