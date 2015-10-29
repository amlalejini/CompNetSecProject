import pxssh, getpass, time, json, sys, os

DEFAULT_SETTINGS_FILE = "settings.json"
MSG_FREQ = 3 # Message frequency in seconds
DEBUG = True

if __name__ == "__main__":
    # Load up some defaults
    settings_file = DEFAULT_SETTINGS_FILE
    if "-h" in sys.argv:
        # HELP!
        print("Usage:  python ssh_comms.py [settings file (JSON)]")
        exit()
    elif len(sys.argv) > 1:
        # Check arg for settings file
        if os.path.isfile(sys.argv[1]):
            # The file is for real.
            settings_file = sys.argv[1]
        else:
            # Given file is not real.
            print("Invalid settings file.")
            exit()

    # Extract settings from settings file
    with open(settings_file) as fp:
        settings = json.load(fp)

    # Try to grab all the things we need to run this script
    try:
        # Local info (FTP target -- we target ourself after ssh)
        local_ip = settings["local"]["ip"]
        local_uname = settings["local"]["username"]
        local_pass = settings["local"]["password"]
        local_machine_name = settings["local"]["machine_name"]
        # Remote info (SSH target)
        remote_ip = settings["remote"]["ip"]
        remote_uname = settings["remote"]["username"]
        remote_pass = settings["remote"]["password"]
        remote_machine_name = settings["remote"]["machine_name"]
    except:
        print("Incorrectly formatted settings in settings file.")
        exit()

    # ===========================================
    # Establish SSH connection to remote machine
    print("Establishing SSH connection to '%s' at %s with the following credentials:" % (remote_machine_name, remote_ip))
    print("  Username: %s" % remote_uname)
    print("  Password: %s" % "".join(["*" for _ in xrange(0, len(remote_pass))]))
    ssh = pxssh.pxssh()
    ssh.force_password = True
    try:
        ssh.login(remote_ip, remote_uname, remote_pass, login_timeout = 60)
    except:
        print("Failed to establish SSH connection with ''%s' at %s" % (remote_machine_name, remote_ip))
        exit()
    else:
        print("SSH Connection Established!")

    # Move to Garbage directory (where we'll do all of our file manipulating)
    ssh.sendline("cd msg_vault")

    # This is where it gets dumb.
    # ===========================================
    # Establish FTP connection back to local machine from remote machine
    print("REMOTE>> Establishing FTP connection to '%s' at %s with the following credentials:" % (local_machine_name, local_ip))
    print("REMOTE>>   Username: %s" % local_uname)
    print("REMOTE>>   Password: %s" % "".join(["*" for _ in xrange(0, len(local_pass))]))
    # Send ftp command over ssh
    ssh.sendline("ftp %s" % local_ip)
    # Wait for uname prompt
    ssh.expect("Name")
    # Enter username
    ssh.sendline(local_uname)
    # Wait for password prompt
    ssh.sendline(local_pass)
    # After some time, we should be in.

    # ===========================================
    # Transfer files!
    # Go to garbage directory
    ssh.sendline("cd msg_vault")  # FTP
    # Infinitely get the message.
    while True:
        if DEBUG: print("GRABBING MSG!")
        ssh.sendline("get secret.msg")
        time.sleep(MSG_FREQ)

    # Well, because we're doing things infinitely now, we'll just always leave a mess on the floor because who actually cares?
    # Say goodbye to ftp
    ssh.sendline("bye")
    # Ready to log out of ssh
    ssh.logout()
