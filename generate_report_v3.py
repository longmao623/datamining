"""
生成格式完全对齐模板的实验报告 v3
直接基于空模板修改内容，保留原有格式
"""
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

# 打开空模板
doc = Document(r'C:\Users\dbw\Desktop\新建文件夹 (12)\信息工程学院—实验报告(2).docx')

def clear_and_fill(para, text):
    """清空段落并填入新文本，保留原有格式"""
    # 清除所有runs
    for run in para.runs:
        run.text = ''
    # 如果段落没有runs，需要添加一个
    if not para.runs:
        para.add_run()
    # 设置第一个run的文本
    para.runs[0].text = text
    # 确保字体正确
    for run in para.runs:
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    return para

# ===== 封面信息填写 =====
# 段落9: 课程名称
p = doc.paragraphs[9]
p.runs[0].text = '课程名称'
p.runs[1].text = '  数据挖掘'

# 段落10: 实验名称
p = doc.paragraphs[10]
p.runs[0].text = '实验名称'
p.runs[1].text = '  Web日志分析与异常检测'

# 段落11: 姓名
p = doc.paragraphs[11]
p.runs[0].text = '姓    名'
p.runs[1].text = ' XXX'

# 段落12: 成绩（保持空白）

# 段落15: 专业
clear_and_fill(doc.paragraphs[15], '专业     数据科学与大数据技术')

# 段落16: 学号
clear_and_fill(doc.paragraphs[16], '学号  BXXXXXXXXX')

# 段落17: 日期
clear_and_fill(doc.paragraphs[17], '日期   2026年7月')

# ===== 实验目的（段落19-22） =====
clear_and_fill(doc.paragraphs[19], '1. 掌握Web服务器日志数据的解析与预处理方法；')
clear_and_fill(doc.paragraphs[20], '2. 学习从非结构化日志数据中提取有意义的特征；')
clear_and_fill(doc.paragraphs[21], '3. 运用KNN分类算法和K-Means聚类算法对日志数据进行异常检测；')
clear_and_fill(doc.paragraphs[22], '4. 理解监督学习与无监督学习在异常检测中的适用场景与差异；')
clear_and_fill(doc.paragraphs[23], '5. 培养完整的数据分析流程能力：从数据理解、预处理、建模到结果分析。')

# ===== 实验仪器设备（段落35-38） =====
clear_and_fill(doc.paragraphs[35], '1. 操作系统：Windows 11')
clear_and_fill(doc.paragraphs[36], '2. 编程语言：Python 3.11')
clear_and_fill(doc.paragraphs[37], '3. 主要库：pandas, numpy, scikit-learn, matplotlib')
clear_and_fill(doc.paragraphs[38], '4. 数据来源：Apache服务器access.log访问日志（11558条记录）')

# ===== 实验原理（段落56-62） =====
clear_and_fill(doc.paragraphs[56], 
    '1. KNN（K近邻）分类算法：KNN是一种基于实例的监督学习算法，对于一个待分类样本，在特征空间中找到与其最接近的K个训练样本，通过邻居投票决定类别。')
clear_and_fill(doc.paragraphs[57], 
    '2. K-Means聚类算法：K-Means是无监督学习算法，通过迭代将样本划分为K个簇，使簇内相似度最大、簇间相似度最小。')
clear_and_fill(doc.paragraphs[58], 
    '3. 异常检测原理：正常HTTP请求通常返回200状态码、使用标准方法（GET/POST）、不含攻击关键词；异常请求表现为大量404/403响应、包含敏感路径、使用非标准UA等。')

# ===== 实验内容（段落70-81） =====
clear_and_fill(doc.paragraphs[70], '【任务1：数据加载与解析】')
clear_and_fill(doc.paragraphs[71], '使用正则表达式解析Apache日志格式，提取IP地址、时间戳、请求方法、请求路径、状态码、响应大小、User-Agent等字段。共解析11558条记录。')
clear_and_fill(doc.paragraphs[72], '')
clear_and_fill(doc.paragraphs[73], '【任务2：数据预处理与特征工程】')
clear_and_fill(doc.paragraphs[74], '对时间戳解析提取小时特征；对缺失值处理（响应大小为"-"时设为0）；构建15维特征向量：路径长度、深度、是否含攻击关键词、请求方法编码、状态码编码、UA特征等。')
clear_and_fill(doc.paragraphs[75], '')
clear_and_fill(doc.paragraphs[76], '【任务3：标签构建】')
clear_and_fill(doc.paragraphs[77], '基于规则标注正常/异常样本。正常标准：状态码200 + 标准请求方法 + 不含攻击关键词 + 非空UA。标注结果：正常21条（0.18%），异常11537条（99.82%）。')
clear_and_fill(doc.paragraphs[78], '')
clear_and_fill(doc.paragraphs[79], '【任务4：KNN分类模型训练】')
clear_and_fill(doc.paragraphs[80], '使用StandardScaler标准化，通过交叉验证选择最优K值（1-20）。最终K=1，测试集准确率100.00%。')
clear_and_fill(doc.paragraphs[81], '')

# ===== 实验结果分析（段落93-116） =====
clear_and_fill(doc.paragraphs[93], '（一）数据集统计特征')
clear_and_fill(doc.paragraphs[94], '日志数据共计11558条记录，全部来自单一IP地址（192.168.215.24）。状态码404占99.2%（11471条），403占0.4%（41条），200仅占0.2%（24条）；请求方法GET占90.3%，HEAD占9.5%，POST仅占0.2%。')
clear_and_fill(doc.paragraphs[95], '')
clear_and_fill(doc.paragraphs[96], '（二）KNN分类结果')
clear_and_fill(doc.paragraphs[97], '最优K值为1，测试集准确率100.00%。正常类/异常类精确率、召回率、F1均为1.00。混淆矩阵：TP=3462, TN=6, FP=0, FN=0。')
clear_and_fill(doc.paragraphs[98], '分析：由于类别极度不平衡（正常:异常≈1:550），高准确率需谨慎解读，模型可能过度拟合异常样本模式。')
clear_and_fill(doc.paragraphs[99], '')
clear_and_fill(doc.paragraphs[100], '（三）K-Means聚类结果')
clear_and_fill(doc.paragraphs[101], '轮廓系数0.9245（聚类结构清晰）；簇0含11534条（异常率100%），簇1含24条（异常率12.5%）；聚类准确率（映射后）99.97%。')
clear_and_fill(doc.paragraphs[102], '分析：K-Means成功将数据分为"大规模异常请求簇"和"少量混合簇"，与标签高度一致，表明正常/异常特征差异显著。')
clear_and_fill(doc.paragraphs[103], '')
clear_and_fill(doc.paragraphs[104], '（四）特征重要性分析')
clear_and_fill(doc.paragraphs[105], '随机森林评估排名前三特征：has_attack_keyword、status_4xx、ua_suspicious，与人工标注规则高度吻合，验证了特征设计合理性。')
clear_and_fill(doc.paragraphs[106], '')
clear_and_fill(doc.paragraphs[107], '（五）总结与心得')
clear_and_fill(doc.paragraphs[108], '1. 本次实验完整实践了从原始日志到异常检测模型的全流程。')
clear_and_fill(doc.paragraphs[109], '2. KNN在极度不平衡数据上表现优异但需谨慎解读；K-Means作为无监督方法能有效发现未知异常模式。')
clear_and_fill(doc.paragraphs[110], '3. 特征工程是关键：领域知识构建的特征显著提升了模型区分能力。')
clear_and_fill(doc.paragraphs[111], '4. 本实验局限在于数据来自单一IP、正常样本过少；未来可引入更多正常流量并尝试Isolation Forest等模型。')
clear_and_fill(doc.paragraphs[112], '')
clear_and_fill(doc.paragraphs[113], '实验运行截图如下：')
clear_and_fill(doc.paragraphs[114], '')
clear_and_fill(doc.paragraphs[115], '图1 实验分析结果汇总（状态码分布、标签分布、KNN混淆矩阵、K值选择、聚类散点图、特征重要性）')

# ===== 保存 =====
output_path = r'C:\Users\dbw\.openclaw\workspace\大作业\BXXXXXXXXX-XXX-数据挖掘大作业.docx'
doc.save(output_path)
print(f"报告已生成: {output_path}")
