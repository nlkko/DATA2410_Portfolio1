
commands = ["/help", "/quit", "/name"]

def help():
    client.connection.send("""
    /help - Lists all commands
    /quit - Closes session with server
    /name <name> - Change display name to <name>
    """.encode())