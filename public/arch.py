import os
import subprocess
from time import sleep

subprocess.run(["rm", "-f", "/etc/pacman.d/mirrorlist"], check=True)
mirror_url = "https://mirror.osbeck.com/archlinux/$repo/os/$arch"

with subprocess.Popen(["tee", "/etc/pacman.d/mirrorlist"], stdin=subprocess.PIPE, text=True) as process:
    process.communicate(f"Server = {mirror_url}\n")

subprocess.run(["sed", "-i", "/^\\s*#\\(ParallelDownloads\\|Color\\)/ s/#//", "/etc/pacman.conf"], check=True)

subprocess.run(["pacman", "-Sy", "--noconfirm", "networkmanager","reflector"], check=True)
subprocess.run(["systemctl", "start", "NetworkManager.service"], check=True)

print("sleeping for 15 seconds")
sleep(15)

print("++++++++++++++Connecting to WiFi...++++++++++++++++++++")
wifi_password = input("Enter WiFi password: ")
subprocess.run(["nmcli", "device", "wifi", "connect", "Shaquib", "password", wifi_password], check=True)

root_partition = "/dev/nvme0n1p9"
boot_partition = "/dev/nvme0n1p8"

subprocess.run(["timedatectl", "set-ntp", "true"], check=True)
subprocess.run(["mkfs.ext4", root_partition], check=True)
subprocess.run(["mount", root_partition, "/mnt"], check=True)
subprocess.run(["mkdir", "/mnt/boot"], check=True)
subprocess.run(["mount", boot_partition, "/mnt/boot"], check=True)
subprocess.run(["pacstrap", "/mnt", "base", "base-devel", "linux", "linux-firmware"], check=True)
subprocess.run(["genfstab", "-U", "/mnt"], check=True)

subprocess.run(["mkdir", "-p", "/mnt/etc/NetworkManager/system-connections"], check=True)
subprocess.run(["cp", "-fr", "/etc/NetworkManager/system-connections/", "/mnt/etc/NetworkManager/"], check=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
chroot_setup_script = os.path.join(script_dir, "chroot-setup.sh")

chroot_cmd = f'cp -r {chroot_setup_script} /mnt && arch-chroot /mnt /bin/bash -c "cd / && chmod +x chroot-setup.sh && ./chroot-setup.sh"'
subprocess.run(chroot_cmd,shell=True, check=True)

print("Done! You can now reboot.")