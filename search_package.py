from globel import *
import urllib.request


class PackageBlock:      # 这个结构体是用来实例化Packages文件，每个独立的数据块
    def __init__(self, block):
        self.__block = block
        # print(self.__block)

    @property
    def dictinfo(self):
        v = dict()
        for line in self.__block:
            v.update(zip(line.split(': ')[0::2], line.split(': ')[1::2]))
            # v[line.split(': ')[0]] = line.split(': ')[1]
            # print(v)
        return v

    @property
    def name(self):
        return self.dictinfo['Package']

    @property
    def depends(self):
        if 'Depends' in self.dictinfo.keys():
            return self.dictinfo['Depends'].split(', ')
        else:
            return ''

    @property
    def filename(self):
        info = self.dictinfo['Filename']
        return info


class PackageFile:    # 实例化一个packages文件
    def __init__(self, filename):
        self.filename = filename

    @property
    def infolist(self):
        fd = open(self.filename, 'r')
        infolist = fd.read().split('\n')
        fd.close()
        return infolist

    @property
    def packageline(self):      # 文件中所有package开头的行号，列表最后一个数字，为文件总行数
        linelist = list()
        with open(self.filename, 'r') as f:
            fileinfo = f.read().split(sep='\n')
            length = len(fileinfo)
            for j in range(0, length):
                if fileinfo[j].startswith('Package:'):
                    linelist.append(j)
            linelist.append(length)
        return linelist         # 返回的是把数据文件，拆分成一个个数据块的列表

    @property
    def number(self):   # 文件中一共含有的包的数量
        return len(self.packageline)-1


class Pack:       # 用来实例化一个包。
    def __init__(self, packname, searchscope):
        self.packname = packname
        self.searchscope = searchscope          # /Users/kylin/PycharmProjects/catchdeb/PBMcatchdeb/catchdeb/dists/v10+0710/arm64/

    @property
    def exist(self):      # 寻找这个包的数据块
        for root, dirs, filename in os.walk(self.searchscope):
            for i in filename:
                packagefile = PackageFile(self.searchscope + i)
                info = packagefile.infolist
                line = packagefile.packageline
                for mumber in range(0, len(line)-1):
                    # print(info[line[mumber]][9:])
                    if self.packname == info[line[mumber]][9:]: # info[line[mumber]][9:] = winmage-sane-backend  前面9个字符是Package:
                        return 1
        return 0

    @property
    def downloadurl(self):     # 下载这个包
        packblock = list()
        url = str()
        for root, dirs, filename in os.walk(self.searchscope):
            for i in filename:
                packagefile = PackageFile(self.searchscope + i)
                packinfolist = packagefile.infolist
                packlinelist = packagefile.packageline
                for mumber in range(0, len(packlinelist)-1):
                    # print(packinfolist[packlinelist[mumber]][9:])
                    if self.packname == packinfolist[packlinelist[mumber]][9:]:
                        for linenumber in range(packlinelist[mumber], packlinelist[mumber+1]):
                            if packinfolist[linenumber]:
                                packblock.append(packinfolist[linenumber])
                        block = PackageBlock(packblock)
                        url_tail = block.filename
                        url_head = i.split('_')[0].replace('++', '://').replace('+', '/')
                        url = url_head + '/' + url_tail
                        # print(url)  # http://archive.kylinos.cn/kylin/partner/pool/wechat_2.0.0_arm64.deb
                        return url
            return url

    @property
    def dependsdownload(self):  # 下载这个包的依赖
        packblock = list()
        for root, dirs, filename in os.walk(self.searchscope):
            for i in filename:
                packagefile = PackageFile(self.searchscope + i)
                packinfolist = packagefile.infolist
                packlinelist = packagefile.packageline
                for mumber in range(0, len(packlinelist)-1):        # 文件里一行行循环
                    if self.packname == packinfolist[packlinelist[mumber]][9:]:
                        for linenumber in range(packlinelist[mumber], packlinelist[mumber+1]):
                            if packinfolist[linenumber]:
                                packblock.append(packinfolist[linenumber])
                        block = PackageBlock(packblock)
                        return block.depends


def choose_search_src():
    distsnamelists = []
    userchoose = list()
    for root, dirs, filename in os.walk(SourceLists):
        distsnamelists = filename
        distsnamelists .sort()
    num = len(distsnamelists)

    while True:
        print('    请选择从哪里搜包')
        for i in range(1, num+1):
            if num == 0 or i == 1:
                print('{:10}: '.format(distsnamelists[i-1].split(sep='+')[0]), end='')
                print('# 选项{:2}: {:28}'.format(i, distsnamelists[i-1],), end='')
            elif i >= 2 and distsnamelists[i-1].split(sep='+')[0] != distsnamelists[i-2].split(sep='+')[0]:
                print()
                print('{:10}: '.format(distsnamelists[i-1].split(sep='+')[0]), end='')
                print('# 选项{:2}: {:28}'.format(i, distsnamelists[i - 1]), end='')
            else:
                print('# 选项{:2}: {:28}'.format(i, distsnamelists[i - 1]), end='')
            # print("已经存在的sources.list文件有=",FileList)
        choose = input("\n    请输入选项序号:  ")
        if not choose.isdigit():
            print('    选择错误，请输入正确选项')
        else:
            choose = int(choose)
            if not choose >= 0 and choose <= num:
                print('    选择错误，选择的数字不存在')
            else:
                userchoose = distsnamelists[choose - 1]  # 如果只用file_list[]，返回值为字符串类型，使用split函数，可以把字符串变成列表
                break

    # print(result)
    cpuinfo = userchoose.split(sep='_')[-1]
    osinfo = userchoose.split(sep='_')[0]
    path = SearchDists + osinfo + '/' + cpuinfo + '/'
    if not os.path.exists(path):
        print('Warning！！！:  您选择的文件尚未更新，请进行更新')
        sys.exit(0)
    return userchoose

def input_search_deb(searchchoose):
    cpuinfo = searchchoose.split(sep='_')[-1]     # 输出样式 v10+0710
    osinfo = searchchoose.split(sep='_')[0]       # 输出样式 arm64
    searchdir = SearchDists + osinfo + '/' + cpuinfo + '/'   # 从这个索引目录的Package文件里搜索
    search_queue = []   # 搜索队列： 输入所有的包中存在的包的列表
    while True:
        userinput = (input("    请输入需要搜索的包名  (注：包名之间用空格分开):  "))
        print('搜索中...')
        for userinputmumber in userinput.split():
            searchpack = Pack(userinputmumber, searchdir)
            if searchpack.exist:
                search_queue.append(userinputmumber)   # 将找到的包放入search_queue队列
                print("####找到 ", userinputmumber)
            else:
                print("未找到 ", userinputmumber)
        choose = input('    是否还要搜索其他包    [Y/N] \n')
        if choose == 'y' or choose == 'Y':
            continue
        elif choose == 'n' or choose == 'N':
            break
        else:
            print('    选择错误,请重新输入：')
    print('查找到的包有： ', search_queue)
    return search_queue

def downloaddeb(search_queue, searchchoose):
    cpuinfo = searchchoose.split(sep='_')[-1]  # 输出样式 v10+0710
    osinfo = searchchoose.split(sep='_')[0]  # 输出样式 arm64
    searchdir = SearchDists + osinfo + '/' + cpuinfo + '/'
    while True:
        result = input('    是否需要下载所有包    [Y/N] \n')
        if result == 'y' or result == 'Y':
            dest = ProjectDir + 'download/'
            print('开始下载......')
            for name in search_queue:
                pack = Pack(name, searchdir)
                srcurl = pack.downloadurl
                print('{}: {}'.format(name, srcurl))
                urllib.request.urlretrieve(srcurl, dest + str(srcurl).split(sep='/')[-1])
            print('下载完成! 请在{}下查看'.format(dest))
            break
        elif result == 'n' or result == 'N':
            break
        else:
            print('    选择错误,请重新输入：')


def downlaoaddepends(search_queue, searchchoose):
    cpuinfo = searchchoose.split(sep='_')[-1]  # 输出样式 v10+0710
    osinfo = searchchoose.split(sep='_')[0]  # 输出样式 arm64
    searchdir = SearchDists + osinfo + '/' + cpuinfo + '/'
    for mumber in search_queue:
        abc = []
        pack = Pack(mumber, searchdir)
        dependslist = pack.dependsdownload
        print(dependslist)          # ['libgtk2.0-0', 'libnotify4', 'libnss3', 'libxss1', 'libxtst6', 'xdg-utils', 'libgconf-2-4 | libgconf2-4', 'kde-cli-tools | kde-runtime | trash-cli | libglib2.0-bin | gvfs-bin']
        if dependslist:
            print('======== {} 的依赖包如下'.format(mumber))
            for k in dependslist:  # 得到一个存储所有依赖包的下载地址的列表 abc
                # print(k,type(k))
                if k.split('|')[0] == k.split('|')[-1]:     # 依赖不存在'|' 或关系
                    pname = k.split('(')[0].rstrip().lstrip()
                    b1 = Pack(pname, searchdir)
                    if b1.exist == 1:
                        print('####找到 ', pname)
                        abc.append(b1.downloadurl)
                        continue
                    else:
                        print('!!未找到 ', pname)
                        continue
                else:       # 依赖存在 '|' 或关系
                    tmplist = k.split('|')
                    for l in tmplist:
                        pname = l.split('(')[0].rstrip().lstrip()
                        b1 = Pack(pname, searchdir)
                        if b1.exist == 1:
                            print('####找到 ', pname, end='    ')
                            abc.append(b1.downloadurl)
                            continue
                        else:
                            print('!!未找到 ', pname, end='    ')
                            continue
                    print('')
        if abc:
            while True:
                result = input('    是否下载 {} 的依赖包    [Y/N]\n'.format(mumber))
                if result == 'y' or result == 'Y':
                    print('开始下载...')
                    dest = ProjectDir + 'download/' + mumber + '_need/'
                    if not os.path.exists(dest):
                        os.makedirs(dest)
                    for item in abc:
                        print('{}: {}'.format(item.split('/')[-1].split('_')[0], item))
                        urllib.request.urlretrieve(item, dest + str(item).split(sep='/')[-1])
                    print('{} 依赖下载完成! 请在{}下查看'.format(mumber, dest))
                    break
                elif result == 'n' or result == 'N':
                    break
                else:
                    print('    选择错误,请重新输入：')
        else:
            print(mumber, '不存在依赖')

def main():
    searchchoose = choose_search_src()
    # print(searchchoose)         # 输出样式 v10+0710_arm64
    searchqueue = input_search_deb(searchchoose)
    downloaddeb(searchqueue, searchchoose)
    downlaoaddepends(searchqueue, searchchoose)
    print('感谢您使用本工具，本项目代码完全开源，https://gitee.com/dockerwho/catchpackage')