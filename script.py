"""
NextUp Server Setup - GUI Version
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import paramiko
import threading
from typing import List

class ServerSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NextUp Server Setup")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="NextUp Server Setup",
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input fields
        fields = [
            ("Server IP Address:", "host"),
            ("Server Username:", "username"),
            ("Server Password:", "password"),
            ("Admin Password:", "admin_password")
        ]
        
        self.entries = {}
        for idx, (label_text, field_name) in enumerate(fields, start=1):
            label = ttk.Label(main_frame, text=label_text, font=("Helvetica", 10))
            label.grid(row=idx, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(main_frame, width=40)
            if "password" in field_name.lower():
                entry.config(show="*")
            entry.grid(row=idx, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            self.entries[field_name] = entry
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.deploy_btn = ttk.Button(
            button_frame,
            text="Deploy Server",
            command=self.start_deployment
        )
        self.deploy_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to deploy",
            font=("Helvetica", 9),
            foreground="gray"
        )
        self.status_label.grid(row=7, column=0, columnspan=2)
        
        # Output console
        console_label = ttk.Label(
            main_frame,
            text="Console Output:",
            font=("Helvetica", 10, "bold")
        )
        console_label.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.console = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=70,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.console.grid(row=9, column=0, columnspan=2, pady=(0, 10))
        self.console.config(state=tk.DISABLED)
        
    def log(self, message, color=None):
        """Add message to console"""
        self.console.config(state=tk.NORMAL)
        if color:
            self.console.tag_config(color, foreground=color)
            self.console.insert(tk.END, message + "\n", color)
        else:
            self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_fields(self):
        """Clear all input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        self.status_label.config(text="Ready to deploy", foreground="gray")
    
    def validate_inputs(self):
        """Check if all fields are filled"""
        for field_name, entry in self.entries.items():
            if not entry.get().strip():
                messagebox.showerror(
                    "Validation Error",
                    f"Please fill in the {field_name.replace('_', ' ').title()}"
                )
                return False
        return True
    
    def start_deployment(self):
        """Start deployment in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Disable deploy button
        self.deploy_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        
        # Start progress bar
        self.progress.start(10)
        self.status_label.config(text="Deploying...", foreground="orange")
        
        # Clear console
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        
        # Run deployment in thread
        thread = threading.Thread(target=self.run_deployment, daemon=True)
        thread.start()
    
    def run_deployment(self):
        """Execute deployment commands"""
        host = self.entries["host"].get().strip()
        user = self.entries["username"].get().strip()
        password = self.entries["password"].get().strip()
        admin_password = self.entries["admin_password"].get().strip()
        
        commands = [
            f"rm -rf NextUp-Database && git clone https://github.com/SparklySparky/NextUp-Database.git",
            f"cd NextUp-Database && sed -i 's|pathoftheserver|/home/{user}/NextUp-Database|g' nextupHttpServer.py",
            f"cd NextUp-Database && rm -rf script.py",
            f"cd NextUp-Database && sed -i 's|pathoftheserver|/home/{user}/NextUp-Database|g' nextupdb.py",
            f"cd NextUp-Database && echo '{admin_password}' > password.txt",
            f"cat > /tmp/nextup.service << 'EOF'\n"
            f"[Unit]\n"
            f"Description=NextUp Server\n"
            f"After=network.target\n\n"
            f"[Service]\n"
            f"Type=simple\n"
            f"Restart=always\n"
            f"RestartSec=1\n"
            f"User={user}\n"
            f"ExecStart=/usr/bin/python3 /home/{user}/NextUp-Database/main.py\n\n"
            f"[Install]\n"
            f"WantedBy=multi-user.target\n"
            f"EOF",
            f"echo '{password}' | sudo -S mv /tmp/nextup.service /etc/systemd/system/nextup.service",
            f"echo '{password}' | sudo -S chmod 644 /etc/systemd/system/nextup.service",
            f"echo '{password}' | sudo -S systemctl daemon-reload",
            f"echo '{password}' | sudo -S systemctl enable nextup.service",
            f"echo '{password}' | sudo -S systemctl start nextup.service",
            f"echo '{password}' | sudo -S systemctl is-active nextup.service"
        ]
        
        success = self.execute_commands(host, user, password, commands)
        
        # Stop progress bar
        self.progress.stop()
        
        # Update UI
        if success:
            self.status_label.config(text="Deployment successful!", foreground="green")
            self.log(f"\nServer is running at http://{host}:4444", "cyan")
            self.log(f"Test with: curl http://{host}:4444/ping", "cyan")
            messagebox.showinfo("Success", f"Server deployed successfully!\n\nURL: http://{host}:4444")
        else:
            self.status_label.config(text="❌ Deployment failed", foreground="red")
            messagebox.showerror("Error", "Deployment failed. Check console for details.")
        
        # Re-enable buttons
        self.deploy_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)
    
    def execute_commands(self, host: str, user: str, password: str, commands: List[str], timeout: int = 30):
        """Execute SSH commands"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.log(f"Connecting to {user}@{host}...", "yellow")
            client.connect(hostname=host, username=user, password=password, timeout=timeout)
            self.log("Connected successfully!", "green")
        except Exception as e:
            self.log(f"Connection failed: {e}", "red")
            return False
        
        success = True
        try:
            for idx, cmd in enumerate(commands, 1):
                # Hide passwords in logs
                safe_cmd = cmd.replace(password, "***")
                if "echo" in safe_cmd and ">" in safe_cmd:
                    safe_cmd = safe_cmd.split(">")[0] + "> password.txt"
                
                self.log(f"\n[{idx}/{len(commands)}] Running: {safe_cmd[:80]}...", "cyan")
                
                stdin, stdout, stderr = client.exec_command(cmd, get_pty=True, timeout=timeout)
                
                out = stdout.read().decode(errors="replace")
                err = stderr.read().decode(errors="replace")
                rc = stdout.channel.recv_exit_status()
                
                if out and len(out.strip()) > 0:
                    for line in out.strip().split('\n')[:10]:  # Limit output lines
                        self.log(f"  {line}", "white")
                
                if rc != 0:
                    self.log(f"  Exit code: {rc}", "orange")
                    if err:
                        self.log(f"  Error: {err[:200]}", "red")
                    success = False
                else:
                    self.log(f"  Success", "green")
        
        except Exception as e:
            self.log(f"Error during execution: {e}", "red")
            success = False
        finally:
            client.close()
            self.log("\nConnection closed", "yellow")
        
        return success

def main():
    root = tk.Tk()
    app = ServerSetupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()