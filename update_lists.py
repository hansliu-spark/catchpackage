from globel import *
import urllib.request


def get_all_sourcelists(): # 搜索./catchdeb/sourcelists 文件夹下存在的sources.list文件，作为选项   返回值——为这个路径下的文件名
    sourcenamelist = []
    for root, dirs, filename in os.walk(SourceLists):
        sourcenamelist = filename
        sourcenamelist.sort()
    if not sourcenamelist:
        print('!!未找到sources.list文件。')
        print('请将 {} 中的模板文件放入 {} 目录中'.format(Template, SourceLists))
        sys.exit(0)
    else:
        return sourcenamelist


def choose_update_sourceslist(_list):
    # 打印选项信息
    num= len(_list)
    print('# 选项0: 以下所有全部更新')
    for i in range(1, num+1):
        if num == 0 or i == 1:
            print('{:10}: '.format(_list[i-1].split(sep='+')[0]), end='')
            print('# 选项{:2}: {:28}'.format(i, _list[i-1]), end='')
        elif i >= 2 and _list[i-1].split(sep='+')[0] != _list[i-2].split(sep='+')[0]:
            print()
            print('{:10}: '.format(_list[i-1].split(sep='+')[0]),end='')
            print('# 选项{:2}: {:28}'.format(i, _list[i - 1]), end='')
        else:
            print('# 选项{:2}: {:28}'.format(i, _list[i - 1]), end='')
    print("\n# 选项n/N： 不进行更新    # 选项h/H：  查看README帮助文档")

    result = []
    while True:
        choose = input("    请输入需要更新的选项:  ")
        if not choose.isdigit():
            if choose == "n" or choose == "N":
                break
            elif choose == 'h' or choose == 'H':
                print_help()
            else:
                print('    选择错误，请输入正确选项')
        else:
            choose = int(choose)
            if not choose >= 0 and choose <= len(_list):
                print('    选择错误，选择的选项不存在')
            else:
                if int(choose) == 0:  # 全部更新
                    result = _list
                    break
                else:
                    result = _list[choose - 1].split(sep=None) # 如果只用file_list[]，返回值为字符串类型，使用split函数，可以把字符串变成列表
                    break
    if result:
        print('您选择要更新的是： ', result)
    return result


def download_packages(_list):
    if _list:
        for info in _list:
            file = SourceLists + info
            cpu = info.split(sep='_')[-1]
            osinfo = info.split(sep='_')[0]
            # print('系统版本： {}   CPU架构:  {}'.format(osinfo,cpu))
            # 获取sources.list文件中的，所有deb开头的行的信息
            # 举例获取info = deb  http://archive2.kylinos.cn/deb/kylin/production/PART-V10-SP1/custom/partner/V10-SP1 default all
            with open(file, 'r') as f:
                result = f.read().split(sep='\n')
                for i in result:
                    if i.startswith('#') or i == '':
                        result.remove(i)
                # print('需要解析路径为： ',result) # 输出结果为 'deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1 main universe multiverse restricted' <list>
        # 以上过程目的是为了分析出来，lists目录下文件中的待解析网址。
        # 以下过程，是讲待解析网址，组合成为下载地址
                dir = SearchDists + osinfo + '/' + cpu  # 下载的目标地址
                if not os.path.exists(dir):
                    os.makedirs(dir)
                    print('创建文件夹: ', dir)
                url_list = []
                va1 = va2 = va3 = ''
                for i in result:
                    print('开始解析：', i)
                    info = i.lstrip().rstrip().split(sep=' ')
                    for j in range(0, len(info) - 1):
                        if str(info[j]).startswith('http'):
                            va1 = info[j]
                            va2 = info[j + 1]
                            va3 = info[j + 2:]
                            print(va3)
                            break
                    for k in va3:
                        url = va1 + '/dists/' + va2 + '/' + k + '/binary-' + cpu + '/Packages'
                        print('下载中...', url)
                        dest = dir + '/' + va1.split(':')[0] + va1.split(':')[1].replace('/', '+') + '_' + k
                        # print('下载到...', dest)
                        urllib.request.urlretrieve(url, dest)
        print('####更新完成')

def main():
    namelist = get_all_sourcelists()    # 读取文件夹内所有sourcelist文件，作为生成选项的基础
    updatechoose = choose_update_sourceslist(namelist)  # 获取用户想要更新哪个
    download_packages(updatechoose)     # 更新用户想要更新的