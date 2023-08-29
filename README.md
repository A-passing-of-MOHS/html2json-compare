

#功能介绍
  本项目可以根据对照规则快速对比两个html文件中的tbody标签中的数据提取为json并比较两者的的差异，
  半自动测试脚本，仅对比可见数据，手动导入数据，脚本不侵入系统不操作网页不发起请求接口，
  针对页面数据进行对照处理，实现可视化json数据对比，
  快速对比用户可见数据，对于数据库表结构依赖性低，对接口返回依赖低，无需做字典或者业务数据格式化，
#效果展示
  新旧系统对照
![image](https://github.com/A-passing-of-MOHS/html2json-compare/assets/48318560/1fbe9fdf-4d13-4b6f-8a16-cef809449d38)
![image](https://github.com/A-passing-of-MOHS/html2json-compare/assets/48318560/5d10951e-630a-43c4-ab70-b2c71a1fcba9)
![image](https://github.com/A-passing-of-MOHS/html2json-compare/assets/48318560/277979ce-4c30-42ce-bec9-47573ea4ce48)


#快速开始
   (1).复制项目中的example文件夹并改名为自己测试的模块名，
   (2).复制系统中的tbody标签到对应文件html
   (3).确定新老数据对照规则保存在dataRule.json
   (4).运行test.py生成新老数据的json以及一个可视化对比的html文件
示例：
 选中example文件夹复制 将名称名改为你业务的名称visaApplication，


#导入数据
   确定好对应的搜索条件点击查询，分页选择1000条/页

   打开控制台 ->选择元素->找到页面中的<tbody>标签->选中tbody ->右键复制->复制元素

老系统的粘贴到oldData.html
新系统的粘贴到newData.html

确定对应规则
在dataRule.json用于存储数据对照规则，规则如下 
"字段名": [老系统中列索引,新系统列索引] ，索引从0开始
{
  "批件文号/项目编号": [2,1],
  "出国任务/任务名称": [3,3],
  "创建时间/申请时间": [10,4]
}
以批件文号/项目编号为例 ，在旧系统tr中的2号索引，在新系统tr中的1号索引，
因此   "批件文号/项目编号": [2,1]
旧系统中有很多冗余td因此不能直接在页面上确定td的索引
旧系统： 

老系统有些空的td计算索引的时候要算上，例如时间页面上看是第七个

但页面里面有三个隐藏元素因此他的索引应该是10，因此规则为：
"创建时间/申请时间": [10,x]
x为新系统中申请时间的索引

新系统：

获取对比结果
运行visaApplication下的test.py

运行完成后的文件夹多了newData.json和oldData.json,以及result.html
result.html中储存这对比结果


浏览器中打开result.html可以看到数据对比左侧为老数据，右侧为新数据，
我们可以清楚的观察到’批件文号/项目编号"为 "202003446‘的数据在新数据中缺失


