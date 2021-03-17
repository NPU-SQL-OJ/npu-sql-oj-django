# SQL_memOJi  
DESCRIPTIONS


## Files  
```  
.
└── tree
```  

## Environment
- `env`

## Usage  
- `To be finished.`  


## Installation  
- `To be finished.`  

## TO-DO List
- [x] 仪表板
  - [ ] 学生：通过率、最近考试、练习
  - [ ] 老师：已发布的考试、练习、统计信息
- [x] 统一各页面 `base.html` 部分
  - [x] html
  - [ ] django template
  - [ ] title

- [x] 账号认证
  - [x] 登录
  - [x] 找回密码
  - [x] 注册
    - [ ] `auth-register.html` 实现分步表单注册
    - [ ] form validation

- [x] 日历 `calendar.html`
- [x] 统计数据 `statistics.html`
  - [ ] 学生：已通过/未通过
  - [ ] 老师：练习/考试 已完成/未完成，通过率
- [x] 个人信息 `user-info.html`
- [x] 答题 `coding.html`
  - [ ] 编辑器 `coding-editor.html`
  - [ ] 取消“已完成”列，整合到考试、练习中
- [x] 练习 & 考试 `exams-manage.html`
  - [ ] 练习详情编辑 `modal`
  - [ ] 考试详情编辑 `modal`
  - [ ] 顶部卡片: 下一场练习、暂无考试
  - [ ] 删除/终止考试
- [x] 班级管理 `class-manage.html`
  - [ ] 学生信息编辑
  - [ ] 班级列表卡片式+列表
  - [ ] 负责老师默认是自己
  - [ ] 列表隐藏邮件、班级
- [x] 题库 & 试卷 `questions-manage.html`
  - [x] 题目描述省略多余信息
  - [x] 题目详情编辑
    - [ ] 正确答案
  - [ ] 试卷详情编辑
  - [ ] 创建题库（可选项）
  - [ ] 二级菜单
  - [ ] 取消垃圾箱
  - [ ] 批量管理工具栏
  - [ ] 题目类型（选择/判断/SQL）


- [x] 数据模型
- [ ] 数据字典
- [ ] ER图
- [ ] 文档
- [ ] 拓展功能:利用模式挖掘等技术，自动总结学生提交 SQL 中的错误使用模式

## 数据模型
> **粗体** 表示主键  
> *FK* 表示外键 (Foreign Key)

### 1. `auth` 模块
- [ ] 用户 `User` (**用户名**, 密码, 权限等级, 学校全称, 真实姓名, 学工号)
- [ ] 学校 `School` (**学校全称**, 校名英文缩写)
- [ ] 班级 `Classroom` (**班级ID**, 学校(*FK: 学校.学校全称*), 班级名称, 负责教师(*FK: 用户.真实姓名*), 备注信息, 学生名单)
- [ ] 班级-学生 `Class-Stud` (班级ID(*FK: 班级.班级ID*), 学工号(*FK: 用户.学工号*), 姓名(*FK: 用户.真实姓名*), 学院, 加入状态)

### 2. `coding` 模块
- [ ] 题目 `Question` (**题号**, 题目名, 所属数据库, 题目难度, 题目描述, 标准答案)
- [ ] 题库 `QuestionSet` (**题库ID**, 题库名称, 题号列表)
- [ ] 试卷 `Paper` (**试卷ID**, 试卷名称, 题号列表)
- [ ] 事件(练习/考试) `Event` (**事件ID**, 事件类型, 开始时间, 结束时间, 试卷ID(*FK: 试卷.试卷ID*))
- [ ] 事件-班级 (发起人(*FK: 用户.真实姓名*), 参与班级(*FK: 班级.班级ID*))
- [ ] 作答记录 `AnswerRec` (用户名(*FK: 用户.用户名*), 题号(*FK: 题目列表.题号*), 答案正确性, 作答次数)

### 3. `calendar` 模块
> 无数据表, 使用 `Event` 中的事件

## 数据字典

| 字段名                 | 数据类型             | 非空  | Key | 默认值               |
|-----------------------|---------------------|------|-----|---------------------|
|                       |                     |      |     |                     |



---  
**by [Steve X](https://github.com/Steve-Xyh/SQL_memOJi)**  