---
layout: post
title:  "How to quickly setup an Archlinux VM"
date:   2021-07-02
tags:
  - Arch
categories: notes
---

測試東西的時候常需要一個很簡單的 Linux VM，剛好 Arch 的檔案小，安裝速度也快，為了以後不要再採坑，寫了這篇筆記來簡單紀錄一下怎麼用 Live iso 安裝 Archlinux.
<!--description-->

本篇文章從[官網教學](https://wiki.archlinux.org/title/Installation_guide)節錄而來，使用 **BIOS** 系統（大部分VM軟體預設是這個）的安裝過程。打開你喜歡的 VM 軟體，用抓下來的 Live iso 開機之後，進行以下步驟。

# 步驟

## Disk Partition

先用`lsblk`看一下你的磁碟叫什麼名字，然後進行分割的動作:
```bash
fdisk /dev/sda   # Or whatever the disk is called
```

我們需要至少三個Partition:

1. 1MB for `BIOS Boot` (No need to choose type)
2. 256MB Swap, choose `swap` type in fdisk
3. Use rest of the space as one partition

### Formatting
再來我們需要把這些 Partition 格式化。
```bash
mkswap /dev/sda2  # 處理swap
swapon /dev/sda2
mkfs.ext4 /dev/sda3 # 建立檔案系統
```
然後掛載到`/mnt`。
* `mount /dev/sda3 /mnt`

## Install using pacstrap

`pacstrap /mnt ...` 可以幫我們裝好很多東西。

* **TL;DR**: `pacstrap /mnt base linux linux-firmware networkmanager grub sudo vim`

解釋一下：

* 基本的 Linux 要用的東西: `base linux linux-firmware`
* 網路自動設定，不然會連不到: `networkmanager`
* 既然都要裝東西了那就順便: `grub sudo vim`

## fstab, arch-chroot, systemd

設定開機自動mount，並設定網路。接下來的步驟要在新的檔案系統裡做，所以要`arch-chroot`：

```bash
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
systemctl enable NetworkManager
```

## User and password

設定root的密碼，建立新的使用者。

```bash
passwd  # change root pw

# 如果你要建立使用者的話才做，不用的話可以跳過
useradd ckb # 當然你要把ckb換成自己的使用者名稱
mkdir -p /home/ckb
chown ckb:ckb /home/ckb
visudo # if you want to give it sudo, add line: ckb ALL=(ALL) ALL
```

## GRUB

裝Grub，要不然開不了機。

```bash
# use lsblk to check where the bios partition is at (the 1MB one)
grub-install --target=i386-pc /dev/sda1
grub-mkconfig -o /boot/grub/grub.cfg
```

## Finishing up

退出arch-chroot，然後重新開機。

```bash
exit # from chroot
umount -R /mnt
reboot
```

這樣子就裝好了，如果開機起來看到的是live iso的畫面的話，選擇 "Boot from existing OS" 開機，然後把你的live iso拔掉。

# References
- 官網教學: https://wiki.archlinux.org/title/Installation_guide
