import datetime

def CreateLogEntry(user, message):
    log_file = open('activity.log','a')
    log_file.write(""+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", " + str(user) +", " + message + "\n")