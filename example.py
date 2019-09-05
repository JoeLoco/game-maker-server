###########################
# Init                    #
###########################

from gmserver import GameMakerServer
server = GameMakerServer(5000)

###########################
# Event handlers          #
###########################

def on_connect(event, conn):
    print(event)
    server.send(event, conn)

def on_move(event, conn):
    print(event)


###########################
# Bind event handlers     #
###########################

server.on_event("connect",on_connect)
server.on_event("move",on_move)


server.run()