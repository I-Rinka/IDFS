import net.listener as server
import util.tools as ut
ut.IS_SERVER=True
print("My name: %s\nMy id: %s\n" % (ut.GetMyDevName(), ut.GetMyDeviceID()))
server.db.create_table()
server.LOCAL_SERVER.serve_forever()