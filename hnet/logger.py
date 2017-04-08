import datetime


def CreateLogEntry(user, message):
    """
    Creates a Log entry that is saved into a activity.log text file
    :param user:
    :param message:
    :return: null
    """
    log_file = open('activity.log','a')
    log_file.write(""+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", " + str(user) +", " + message + "\n")