## 配置lxd
### 要求
- 将LXD配置为虚拟主机
- 将LXD配置为虚拟路由器
- 用三台虚拟路由器连接成三角形，配置OSPF路由，与虚拟路由器相连的三台虚拟主机相互可以ping通
### 步骤
- 在宿主主机安装LXD
    - 先安装snapd:
      ```bash
      sudo apt-get install snapd
      ```
    - 安装LXD:
      ```bash
      sudo snap install lxd
      ```
    - 存储方式
      ```bash
      sudo apt install zfsutils-linux
      ```
- 配置第一台路由器
    - 初始化:
      ```bash
      sudo lxd init
      ```
    - 下载镜像
      ```bash
      sudo lxc image import lxd.tar.xz rootfs.squashfs --alias HostImage
      ```
    - 查看镜像
      ```bash
      sudo lxc image list local:
      ```
      查看指定镜像的详细信息
      ```bash
      sudo lxc image show local:HostImage
      ```
      删除镜像
      ```bash
      sudo lxc image delete local:HostImage
      ```
    - 启动本地镜像
      ```bash
      sudo lxc launch local:HostImage R1`
      ```
    - 查看信息
      ```bash
      lxc list
      lxc start R1
      lxc stop R1
      lxc delete R1
      ```
- quagga配置
    - 登录容器
      ```bash
      lxc exec R1 -- /bin/bash
      ```
    - 传入quagga安装包
      ```bash
      lxc file push quagga-1.2.4.tar.gz R1/root/
      tar -xzvf quagga-1.2.4.tar.gz
      cd quagga-1.2.4/
      ```
    - 配置安装`gawk`,`libreadline7`,`libreadline-dev`,`pkg-config`
    - 启动quagga
      ```bash
      #复制库
      cp /usr/local/lib/libzebra.* /lib
      配置用户
      groupadd quagga
      useradd quagga -g quagga
      #启动
      zebra -d
      #查看守护进程
      ps -aux | grep zebra
     ```
- 打包模板
  ```bash
  lxc publish R1 --alias Router_Ubuntu1804 --public
  lxc image export Router_Ubuntu1804 .
  ```
  导入使用
  ```bash
  lxc image import <tarball_name> --alias <alias_name>
  ```
- 配置客户机
  ```bash
  sudo lxc launch local:HostImage C1
  ```
  修改软件源，并安装net-tools,然后导出镜像
  ```
  lxc publish C1 --alias Client_Ubuntu1804 --public
  ```

   
