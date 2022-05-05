import os
import sys



ProjectDir = os.path.dirname(os.path.realpath(sys.argv[0])) + '/PBMcatchdeb/'
DirTreeProject = ['catchdeb/', 'catchdeb/dists', 'catchdeb/sourcelists', 'catchdeb/template', 'download']
Template = ProjectDir + 'catchdeb/template/'     # 生成sources.list文件模板位置
SourceLists = ProjectDir + 'catchdeb/sourcelists/'
SearchDists = ProjectDir + 'catchdeb/dists/'


def print_info():
    pyinfo = "\
    #####################################################\n\
    # 工具：龙抓手\n\
    # 用途：用来从外网源抓取包\n\
    # 使用须知：该版本可抓取多个包，可同时抓取依赖，请确保机器联网\n\
    # 日期：2022.2.25             所有作者：麒麟软件天津事业部刘汉霆\n\
    #####################################################\n\
    请稍后，正在检查网络中...".format(os.getcwd() + '/catchdeb/lists')
    print(pyinfo)

def print_help():
    pyinfo = "\
# 使用前请阅读该信息\n\
## 目录结构\n\
---\n\
- main.py 为运行主函数。使用python3运行该函数即可使用本工具\n\
- catchdeb 为工作过程，索引文件等目录（无需手动配置）\n\
    - lists 为索引目录，可将需要查找系统的/etc/apt/sources.list文件复制放入即可。\n\
    命名规则为：系统大版本+系统小版本号_架构（例如：v10sp1+0521_amd64）\n\
    架构：可选择 amd64，arm64，mips64el,loongarch64,armhf,i386\n\
    注意：请按照命名规则大版本和小版本号之间用 + 进行链接，版本和架构之间用 _ 进行链接\n\
    - dists 为Packages文件下载位置，无需人工干预\n\
- download 为下载的包所在目录\n\
    - *_need为 *的依赖包\n\
- template 为sources.list文件的模板目录，存储了默认模板。如有使用可直接复制到catchdeb/lists中\n\
\
## 使用方法：\n\
    1.在终端中使用命令 python3 ./main.py 即可。\n\
    2.如有需要可将 sources.list文件放入 ./catchdeb/lists中\n\
        命名规则为：系统大版本+系统小版本号_架构（例如：v10sp1+0521_amd64）\n\
        架构：可选择 amd64，arm64，mips64el,loongarch64,armhf,i386\n\
        注意：请按照命名规则大版本和小版本号之间用 + 进行链接，版本和架构之间用 _ 进行链接\n\
    3.下载完成后，可在./download中查看， *_need文件夹中存储的*的依赖包\n"
    print(pyinfo)

def print_flagname():
    dragon = str(
"          =@^  ..@@]       =@^  ,]]].@@@@@`   @@@@@@@@@@@@@@@^      \n\
          =@^     ,@`   .]].@.]]=@..@@ =@^    ...    =@^            \n\
     @@@@@@@@@@@@@@@@@@  [[.@.[`=@^ @@ =@^    ,]]]]]].@.]]]]]`      \n\
          @@. =@^  ,.`     =@^ .=@^ @@ .@^    ,[[[[[[.@.[[[[[`      \n\
          @@  =@^ .@.     ,.@@@.@@  @@  @@           =@^            \n\
         @@`  =@.@@`    ,@@.@^  @@  @@  .@. .@@@@@@@@@@@@@@@@@@^    \n\
       .@@`  ..@@`   @.    =@^ =@^  @@  =@^          =@^            \n\
     ..@@.]@@@@@^   .@@    =@^,@@   @@   @@.         =@^            \n\
     @@`   .  ,@@@@@@@`  .@@@`@@.   @@   ,@^     =@@@@@.            ")
    print(dragon)