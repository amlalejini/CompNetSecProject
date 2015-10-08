import pxssh, getpass, time

if __name__ == "__main__":
    # Some settings for ssh connection
    remote_hostname = "192.168.0.12"
    remote_uname = "amlalejini"
    remote_pass = "pass"

    my_hostname = "192.168.0.10"
    my_uname = "amlalejini"
    my_pass = "pass"
    # Prompt for password to connect
    print("Connecting to %s as %s" % (remote_hostname, remote_uname))



    # Make pxssh object
    ssh = pxssh.pxssh()
    ssh.force_password = True
    # Login
    ssh.login(remote_hostname, remote_uname, remote_pass, login_timeout = 60)
    print("Connection successful!")
    ssh.sendline("cd Garbage")
    # Do some jank shit to get FTP back to myself.
    print("Attempt to establish ftp connection back to self?")
    ssh.sendline("ftp %s" % my_hostname)
    ssh.expect("Name")
    ssh.sendline(my_uname)
    ssh.expect("Password:", timeout=120)
    ssh.sendline(my_pass)
    print("Woah.  That worked?")
    ssh.prompt()


    ssh.sendline("cd Garbage")
    ssh.prompt()


    for i in xrange(0, 5):
        # Get file (sequel gets file from original)
        ssh.sendline("get original.msg")
        time.sleep(3)

    # Say goodbye to ftp
    ssh.sendline("bye")
    # Ready to log out of ssh
    ssh.logout()
