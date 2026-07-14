# e-hentai插画自动下载器
第一次写这种东西……
## 1.环境配置
我使用的是python3.14.2，更老的版本应该也可以吧…… (\*T_T\*) 
克隆库：

```shell
git clone https://github.com/stukdee/ehenpicdown.git
cd ehenpicdown
```
创建虚拟环境：
```shell
python3 -m venv .venv
```
激活：
```shell
source ./.venv/bin/activate
```
fish shell可能会报错，建议使用zsh或bash。
```shell
pip3 install requests lxml beautifulsoup4
```
## 2.设置代码
用文本编辑器打开`main.py`文件，将`web_url`变量设置为插画网址。
必要的时候（比如“内容危险提示”可能会阻止网页爬取，这时候需要点击“永远不要显示”并复制cookies）设置cookies和headers。
## 3.运行代码
```shell
python3 main.py
```