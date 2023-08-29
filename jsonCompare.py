#coding=utf-8
import datetime
import json
import os
import time

from bs4 import BeautifulSoup
import difflib

class compareJSON_Utils():
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
    def tbody_to_json_list(self,tbody,rules,TagIndex):
        # 获取tbody标签下的所有tr标签
        trs = tbody.find_all('tr')
        if TagIndex==0:
           #老系统数据删除第一个tr
           trs.pop(0)
        # 初始化jsonList
        json_list = []
        # 遍历tr标签，将其转换为json对象并添加到jsonList中
        for tr in trs:
            # 获取tr标签下的所有td标签
            tds = tr.find_all('td')
            # 初始化json对象
            tdslen=len(tds)
            json_obj = {}
            # 遍历td标签，将其转换为json字符串并添加到json对象中

            for index,td in enumerate(tds):
                # 获取td标签中的文本内容
                text = td.text.strip()
                # 将文本内容转换为json字符串并添加到json对象中
                formatText = text.split()
                # 新系统标题中包含了其他字段例如
                #赴哈萨克斯坦执行市场开发任务 赵铁申请护照

                if len(formatText) > 1:
                    text = formatText[0]
                json_obj[index] = text

            # 将json对象添加到jsonList中
            format = {}
            ruleslist = rules.keys()

            for rule in ruleslist:
                ruleIndex = rules[rule][TagIndex]
                if ruleIndex+1 > tdslen:
                    raise Exception(f"数组越界第{ruleIndex}列不存在，总共就{tdslen}列")
                format[rule] = json_obj[ruleIndex]
            json_list.append(format)
        print(f'TagIndex:{TagIndex}总共{tdslen}列')
        return json_list
    def html_to_format_json_list(self,dataRule,fileName,TagIndex):

        # 打开HTML文件
        with open(f'{fileName}.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('tbody') is None:
                raise Exception(f'没有tbody标签,请检查{fileName}.html文件')
        json_list = self.tbody_to_json_list(soup, dataRule, TagIndex)
        # print(json_list)

        with open(f'{fileName}.json', 'w', encoding='utf-8') as file:
            json.dump(json_list, file, ensure_ascii=False, indent=2)
        return json_list






    def compare_json(self,json1, json2,cwd):
        text1 =json.dumps(json1, ensure_ascii=False,indent=4).splitlines()
        text2 =json.dumps(json2, ensure_ascii=False,indent=4).splitlines()
        m = difflib.HtmlDiff()
        result = m.make_file(text1, text2)
        with open( f'{cwd}/result.html', 'w', encoding='utf-8') as f:
            f.writelines(result)
        # 判断是否有变化，有变化则生产报告，没有则不生成报告
        if result.count('<span class="diff_sub">') > 0 or result.count('<span class="diff_chg">') > 0 or result.count(
                '<span class="diff_add">') > 0:
            print("\033[31m找到不同数据 \033[0m")
            format_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result=result.replace('<table ',f'<div style="display: flex;width: 100%;position: fixed;margin-top: -24px;background-color: #409EFF; color: aliceblue;" ><div style="flex: 1;background-color: #F56C6C">旧系统数据 {len(json1) }条</div><div style="flex: 1">新系统数据 {len(json2)}条</div> </div>  <table style="width: 100%;margin-top: 24px"',1 )
            result=result.replace('</body>',f'<h2>生成时间：{format_time}</h2></body>')
            with open(f'{cwd}/result.html', 'w', encoding='utf-8') as f:

                f.writelines(result)
                print("生成对比列表完成")

        else:

            print("没有找到不同数据")

    def runThisFolder(self,cwd):

        start_time = time.time()
        # 读取规则
        with open(f'{cwd}/dataRule.json', 'r', encoding='utf-8') as dataRuleF:
            dataRule = json.load(dataRuleF)
        oldData = self.html_to_format_json_list(dataRule, f'{cwd}/oldData', 0)
        newData = self.html_to_format_json_list(dataRule, f'{cwd}/newData', 1)

        if len(oldData) != len(newData):
            print(f"文件的行数不一致老数据有{len(oldData)}行，新数据有{len(newData)}行")
            if len(oldData) > len(newData):
                print(f"老数据多了{len(oldData) - len(newData)}行")

            if len(oldData) < len(newData):
                print(f"新数据多了{len(newData) - len(oldData)}行")
        # 比较并生成HTML展示结果
        self.compare_json(oldData, newData,cwd)

        end_time = time.time()

        print(f'对比完成了旧系统数据 \033[33m{len(oldData)}\033[0m行，新系统数据 \033[33m{len(newData)}\033[0m 行')
        print(f'共计\033[31m{len(oldData)+len(newData)} \033[0m行')
        print("耗时:\033[32m{:.2f}秒\033[0m".format(end_time - start_time))


if __name__ == '__main__':

    compareJSON_Utils().runThisFolder()
