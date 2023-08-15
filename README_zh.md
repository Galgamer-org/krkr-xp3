#KiriKiri .XP3文件 解包打包工具 命令行版 linux可用，GitHub Actions可用

使用方法

制作patch 
```
python xp3.py -m repack -e 加密方式 -flatten 要打包的文件夾 patch.xp3

#无加密则加密方式设置为none
```

打包data.xp3
```
python xp3.py -m repack -e 加密方式 要打包的文件夾 patch.xp3
```

解包

```
python xp3.py -m e -e 加密方式 data.xp3 输出文件夹
```
