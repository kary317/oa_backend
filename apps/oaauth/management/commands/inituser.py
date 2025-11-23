from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser, OADepartment


class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')

        # 董事会的员工，都是superuser用户
        # 1. 东东：属于董事会的leader
        dongdong = OAUser.objects.create_superuser('东东', 'dongdong@qq.com', '111111', department=boarder)
        # 2. 多多：董事会成员
        duoduo = OAUser.objects.create_superuser('多多', 'duoduo@qq.com', '111111', department=boarder)
        # 3. 张三：产品开发部的leader
        zhangsan = OAUser.objects.create_user('张三', 'zhangsan@qq.com', '111111', department=developer)
        # 4. 李四：运营部leader
        lisi = OAUser.objects.create_user('李四', 'lisi@qq.com', '111111', department=operator)
        # 5. 王五：人事部的leader
        wangwu = OAUser.objects.create_user('王五', 'wangwu@qq.com', '111111', department=hr)
        # 6. 赵六：财务部的leader
        zhaoliu = OAUser.objects.create_user('赵六', 'zhaoliu@qq.com', '111111', department=finance)
        # 7. 孙七：销售部的leader
        sunqi = OAUser.objects.create_user('孙七', 'sunqi@qq.com', '111111', department=saler)

        # 给部门指定leader和manager
        # 分管的部门
        # 东东：产品开发部、运营部、销售部
        # 多多：人事部、财务部
        # 1. 董事会
        boarder.leader = dongdong
        boarder.manager = None
        # 2. 产品开发部
        developer.leader = zhangsan
        developer.manager = dongdong
        # 3. 运营部
        operator.leader = lisi
        operator.manager = dongdong
        # 4. 销售部
        saler.leader = sunqi
        saler.manager = dongdong
        # 5. 人事部
        hr.leader = wangwu
        hr.manager = duoduo
        # 6. 财务部
        finance.leader = zhaoliu
        finance.manager = duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write('初始用户创建成功')
