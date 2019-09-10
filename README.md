# Rancher Tool
运维脚本集合，可以用来下载helm chart或者docker镜像之类的，未来应该还能推送到gitlab上或者别的什么方法将这些应用推送到rancher上。

目前已有的功能：
- 下载并合并helm chart包
- 从helm chart包中得到全部需要的docker镜像，并存储在out/images.txt中
- 从本地文件中拉取镜像，并且推送到harbor中
- 迁移harbor中镜像所属的项目，类似`mv`操作
- 清空全部带有harbor地址标记的镜像。
- 将harbor中带有多层包名的项目迁移到正确的位置
- 将合并后的chart包上传到rancher的应用商店中
  
## 环境
该脚本需要以下条件才可使用，请确认都具备后

- git
- docker
- helm
- python3+
- pip
- 系统为linux并且使用最高权限运行该脚本。
- 有办法访问google api

## 安装
通过`git clone`命令克隆该项目到路径中。然后再使用pip安装python依赖，例如：
```
git clone https://github.com/Okabe-Kurisu/rancherTool.git
cd rancherTool
pip install -r requirements.txt
```
如果没有报错，那么应该就安装成功了，可以使用`python3 main.py`来得到使用方法

## 配置脚本
根据实际情况，编辑`config.py`来更好的使用脚本。
其参数如下：

|参数|类型|描述|
|:--|:---:|:------|
|proxies|dict|如果不需要代理，则设置为None。如果需要，按照`{'http': 'http://localhost:9527', 'https': 'http://localhost:9527'}`的格式设置|
|docker_retry_times|int|docker拉取时的重试次数|
|download_retry_times|int|下载图片或者chart包时的重试次数|
|path|str|下载的chart包所在的路径，默认存储在当前文件夹的`pkg`目录下|
|git_path|str|要生成的git repo所在的路径，如果这个文件夹不存在会自动创建|
|git_url|str|远程仓库的地址|
|git_username|str|远程仓库的账号|
|git_password|str|远程仓库的密码|
|harbor_url|str|harbor的域名，不要加协议|
|harbor_tls|boolean|harbor是否开启了tls|
|harbor_username|str|harbor的管理员账号|
|harbor_password|str|harbor的管理员密码|



## 使用方法
通过使用`python`运行`main.py`文件来使用该工具。
如：
``` shell
python main.py [--flag] # flag可以写多个
```
flag列表如下：

|参数|描述|
|:----|:----|
|help|获取使用方法|
|gat|从谷歌上得到held chart列表。并保存out/tar.txt。然后会将列表中的全部chart的压缩包下载下来，如果遇到已经下载过的，则会跳过|
|fut|将已经下载下来的包解压并且按照项目名称对于多个版本进行合并|
|gai|从已经下载下来的包中得到全部需要的docker镜像，并存储在out/images.txt中|
|gaicon|得到全部应用的图标|
|ppa|从out/image.txt中逐个拉取镜像，并且推送到harbor中|
|config|输出全部配置信息|
|init|顺序执行从获取chart列表到推送镜像到harbor之间的全部动作，耗时及其长，不建议使用|
|clear|会清空全部带有harbor地址标记的镜像。同id的全删，谨慎使用。|
|skin [project]|会将[project]中多层项目名包裹的image剥离出来|
|git|将chart文件上传到git|

部分flag拥有阻止其他flag生效的作用，其优先级如下所示：
```help > init > skin > config > clear```

