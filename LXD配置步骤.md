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
      #配置用户
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
  ```bash
  lxc publish C1 --alias Client_Ubuntu1804 --public
  ```
- 配置网络C1R1
    - 客户机C1连接路由器R1,创建网络并绑定网卡
      ```bash
      lxc network create C1R1 ipv6.address=none ipv4.address=192.168.174.1/24
      lxc network attach C1R1 C1 eth0
      lxc network attach C1R1 R1 eth1
      ```
    - 进入R1,分配地址
      ```bash
      ip addr add 192.168.174.2/24 dev eth1
      ip link set eht1 up # 启动网卡
      ```
    - 进入C1，分配地址
      ```bash
      ip addr add 192.168.174.1/24 dev eth0
      ip link set eth0 up
      # 替换默认网关为R1
      route delete default
      route add default gw 192.168.174.2
      ```
- 配置网络R1R2
    - 创建网络R1R1并绑定网卡
      ```bash
      lxc network create R1R2 ipv6.address=none ipv4.address=192.168.177.1/24
      lxc network attach R1R2 R1 eth2
      lxc network attach R1R2 R2 eth2
      ```
    - 进入R1,分配地址
      ```bash
      ip addr add 192.168.177.1/24 dev eth2
      ip link set eht2 up # 启动网卡
      ```
    - 进入R2,分配地址
      ```bash
      ip addr add 192.168.177.2/24 dev eth2
      ip link set eht2 up # 启动网卡
      ```
    - 查看网络配置情况
      ```bash
      lxc network list
      ```
- 配置固定地址
    修改文件
    ```bash
    vim /etc/netplan/x-lxc.yaml
    ```
    修改后应用更改
    ```bash
    netplan apply
    ```
    - C1
      ```yaml
      network:
          version: 2
          ethernets:
                  eth0:
                      dhcp4: false
                      addresses: [192.168.174.1/24]
                      gateway4: 192.168.174.2
      ```
    - R1
      ```yaml
      network:
          version: 2
          ethernets:
                  eth0:
                          dhcp4: true
                          dhcp-identifier: mac
                  eth1:
                          dhcp4: false
                          addresses: [192.168.174.2/24]
                  eth2:
                          dhcp4: false
                          addresses: [192.168.177.1/24]
                  eth3:
                          dhcp4: false
                          addresses: [192.168.179.2/24]
      ```
    其余路由器及客户机文件内容类似
- 配置OSPF
    - 修改路由器的ospf配置文件
      ```ospf
      ! -*- ospf of R1 -*-
      !
      ! OSPFd sample configuration file
      !
      !
      hostname Router01
      password zebra
      !
      router ospf
          network 192.168.174.0/24 area 1
          network 192.168.177.0/24 area 0
          network 192.168.179.0/24 area 0
      !
      log stdout
      ```
    - 在三台路由器中启动zebra和ospfd
      ```bash
      zebra -d
      ospfd -d
      ```
    - 查看邻居数据
      ```bash
      vtysh
      show ip ospf neighbor
      show ip ospf database
      ```


