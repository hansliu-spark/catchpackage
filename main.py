import subprocess

import search_package
from globel import *
import update_lists


def check_network():  # 返回值：网络通，返回0；网络不通，返回1
    command = 'ping archive.kylinos.cn -c 5'
    result = subprocess.call(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if result == 2:
        print('网络不通，请检查网络')
        sys.exit(0)
    elif result == 0:
        print('    网络状态：良好\n')


def project_init():  # 根据DirTreeProject创建目录
    for dirname in DirTreeProject:
        if not os.path.exists(ProjectDir + dirname):
            os.makedirs(ProjectDir + dirname)
            print('# 创建目录成功: PATH = {}'.format(ProjectDir + dirname))

def create_sourcelist_template():
    # v10sp1 0521 amd64
    name = 'v10sp1+0521_amd64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v10sp1 0521 amd64 模板\n\
        deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1 main universe multiverse restricted\n\
        deb http://archive2.kylinos.cn/deb/kylin/production/PART-V10-SP1/custom/partner/V10-SP1 default all')
        # print('模板 {} 已生成'.format(name))

    # v10sp1 0521 arm64
    name = 'v10sp1+0521_arm64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v10sp1 0521 arm64 模板\n\
        deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1 main universe multiverse restricted\n\
        deb http://archive2.kylinos.cn/deb/kylin/production/PART-V10-SP1/custom/partner/V10-SP1 default all')
        # print('模板 {} 已生成'.format(name))

    # v10 0710 amd64
    name = 'v10+0710_amd64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v10sp1 0710 amd64 模板\n\
        deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.0 main universe multiverse restricted\n\
        deb http://archive.kylinos.cn/kylin/partner juniper main')
        # print('模板 {} 已生成'.format(name))

    # v10 0710 arm64
    name = 'v10+0710_arm64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v10sp1 0710 arm64 模板\n\
        deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.0 main universe multiverse restricted\n\
        deb http://archive.kylinos.cn/kylin/partner juniper main')
        # print('模板 {} 已生成'.format(name))

    # v4 amd64
    name = 'v4+sp2_amd64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v4 sp2 amd64 模板\n\
        deb deb http://archive.kylinos.cn/kylin/KYLIN-ALL 4.0.2sp2-server main restricted universe multiverse')
        # print('模板 {} 已生成'.format(name))

    # v4 arm64
    name = 'v4+sp2_arm64'
    with open(Template + '/' + name, 'w+') as f:
        f.write('\
        # v4 sp2 amd64 模板\n\
        deb deb http://archive.kylinos.cn/kylin/KYLIN-ALL 4.0.2sp2-server main restricted universe multiverse')
        # print('模板 {} 已生成'.format(name))
    ########
    # 添加模板位
    ########









if __name__ == '__main__':
    print_flagname()        # 打印"龙抓手"三个字的字符图片
    print_info()        # 打印使用须知
    check_network()     # 检查网络情况
    project_init()
    create_sourcelist_template()    # 创建sourcelist模板
    update_lists.main()
    search_package.main()




















