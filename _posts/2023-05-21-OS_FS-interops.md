# 系统共容与文件系统互操作

系统共容: 多系统同时启动 主要就是利用虚拟化技术开多个系统 目的是解决一般的软件使用问题
- Windows 上跑 Linux 没啥好说的 VMWare/VirualBox/WSL 选吧
- Linux 上跑 Windows VMWare/VirualBox 是基础方法
- 特殊需要的软件: 微信 Office
- Proxmox: 一个可以基于Debian的虚拟化方案 不过一眼没看懂是不是跟EXSI一样的C/S架构 同时C/S是分离的 需要两个设备才能玩
- Wine: 除了一点心理上的恶心外 应该还算挺好的吧
- QEMU/KVM: 可以用来尝试一下微信和Office


文件系统互操作:
- Linux上访问NTFS(Windows目前主要使用的文件系统 这个一般的文件管理器都可以)
- Windows WSL2访问ext4
  - `wmic diskdrive list brief` 找磁盘
  - `wsl --mount <disk> --partition <index>` 挂载分区
  - 可以在WSL2上看见和使用了
