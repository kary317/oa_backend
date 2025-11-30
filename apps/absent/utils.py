def get_responder(request):
    user = request.user
    # 获取考勤审批者responder
    # 如果是部门leader,又分董事会leader和非董事会leader
    if user.department.leader.uid == user.uid:
        if user.department.name == '董事会':
            # 如果是董事会的leader,那么没有审批者
            responder = None
        else:
            # 如果不是是董事会的leader,审批者是部门的管理者
            responder = user.department.manager
    else:
        # 如果不是部门leader,审批者是部门leader
        responder = user.department.leader

    return responder
