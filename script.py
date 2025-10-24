"""
Script to setup the entire server by using a series of ssh commands
"""

import paramiko
import sys
from typing import List

def run_commands(host: str, user: str, password: str, commands: List[str], timeout: int = 30):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=user, password=password, timeout=timeout)
    except Exception as e:
        print(f"[ERROR] Could not connect to {user}@{host}: {e}", file=sys.stderr)
        return 1

    exit_code = 0
    try:
        for cmd in commands:
            print(f"\n--- Running: {cmd} ---")
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=True, timeout=timeout)

            out = stdout.read().decode(errors="replace")
            err = stderr.read().decode(errors="replace")
            rc = stdout.channel.recv_exit_status()

            if out:
                print("[STDOUT]")
                print(out.strip())
            if err:
                print("[STDERR]")
                print(err.strip(), file=sys.stderr)

            print(f"[EXIT CODE] {rc}")
            if rc != 0:
                exit_code = rc
                # Decide whether to continue on non-zero exit status or break:
                # break
    finally:
        client.close()

    return exit_code

def main():
    host = input("Insert Server IP Address: ")
    serverUser = input("Insert Server Username: ")
    serverPassword = input("Insert Server Password: ")
    adminPassword = input("Insert Database Admin Password: ")

    commands = [
        f"rm -rf NextUp-Database && git clone https://github.com/SparklySparky/NextUp-Database.git",
        f"cd NextUp-Database && sed -i 's|pathoftheserver|/home/{serverUser}/NextUp-Database|g' nextupHttpServer.py",
        f"cd NextUp-Database && rm -rf script.py",
        f"cd NextUp-Database && sed -i 's|pathoftheserver|/home/{serverUser}/NextUp-Database|g' nextupdb.py",
        f"cd NextUp-Database && sed -i 's|password|{adminPassword}|g' password.txt",
        # Create service file in /tmp first (no sudo needed)
        f"cat > /tmp/nextup.service << 'EOF'\n"
        f"[Unit]\n"
        f"Description=NextUp Server\n"
        f"After=network.target\n\n"
        f"[Service]\n"
        f"Type=simple\n"
        f"Restart=always\n"
        f"RestartSec=1\n"
        f"User={serverUser}\n"
        f"ExecStart=/usr/bin/python3 /home/{serverUser}/NextUp-Database/main.py\n\n"
        f"[Install]\n"
        f"WantedBy=multi-user.target\n"
        f"EOF",
        f"echo '{serverPassword}' | sudo -S mv /tmp/nextup.service /etc/systemd/system/nextup.service",
        f"echo '{serverPassword}' | sudo -S chmod 644 /etc/systemd/system/nextup.service",
        f"echo '{serverPassword}' | sudo -S systemctl daemon-reload",
        f"echo '{serverPassword}' | sudo -S systemctl enable nextup.service",
        f"echo '{serverPassword}' | sudo -S systemctl start nextup.service"
    ]

    rc = run_commands(host, serverUser, serverPassword, commands)
    if rc == 0:
        print("\nAll done — commands finished successfully (or non-fatal errors).")
    else:
        print(f"\nFinished with non-zero exit code: {rc}", file=sys.stderr)

if __name__ == "__main__":
    main()