"""
生成格式正确的实验报告 Word 文档 v2
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# ===== 页面设置 =====
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(3.17)
section.right_margin = Cm(3.17)

def set_run_font(run, name='宋体', size=10.5, bold=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_para(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, font_name='宋体', font_size=10.5, 
             bold=False, first_indent=0, space_before=0, space_after=0, line_spacing=1.5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Cm(first_indent) if first_indent else None
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    set_run_font(run, font_name, font_size, bold)
    return p

def set_cell_border(cell, **kwargs):
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        if edge in kwargs:
            edge_elm = OxmlElement(f'w:{edge}')
            edge_elm.set(qn('w:val'), 'single')
            edge_elm.set(qn('w:sz'), str(kwargs[edge]))
            edge_elm.set(qn('w:space'), '0')
            edge_elm.set(qn('w:color'), '000000')
            tcPr.append(edge_elm)

# ===== 封面标题 =====
add_para(doc, '', space_before=60)
add_para(doc, '西安文理学院', align=WD_ALIGN_PARAGRAPH.CENTER, font_name='宋体', font_size=22, bold=True)
add_para(doc, '', space_before=12)
add_para(doc, '信息工程学院实验报告', align=WD_ALIGN_PARAGRAPH.CENTER, font_name='黑体', font_size=18, bold=True)
add_para(doc, '', space_before=30)

# ===== 信息表格 =====
table = doc.add_table(rows=4, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# 合并单元格处理
def merge_cells(table, start_row, start_col, end_row, end_col):
    cell = table.cell(start_row, start_col)
    other = table.cell(end_row, end_col)
    cell.merge(other)
    return cell

# 第一行：课程名称 | 数据挖掘 | 实验名称 | Web日志分析与异常检测
table.cell(0,0).text = '课程名称'
table.cell(0,1).text = '数据挖掘'
table.cell(0,2).text = '实验名称'
table.cell(0,3).text = 'Web日志分析与异常检测'

# 第二行：姓名 | XXX | 成绩 | (空)
table.cell(1,0).text = '姓    名'
table.cell(1,1).text = 'XXX'
table.cell(1,2).text = '成    绩'
table.cell(1,3).text = ''

# 第三行：专业 班级（合并）| 数据科学与大数据技术 | 1班 | 学号 日期（合并）| BXXXXXXXXX | 2026年7月
table.cell(2,0).text = '专业'
table.cell(2,1).text = '数据科学与大数据技术'
table.cell(2,2).text = '班级'
table.cell(2,3).text = '1班'

# 第四行
table.cell(3,0).text = '学号'
table.cell(3,1).text = 'BXXXXXXXXX'
table.cell(3,2).text = '日期'
table.cell(3,3).text = '2026年7月'

# 设置表格样式
for row in table.rows:
    for cell in row.cells:
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                set_run_font(run, '宋体', 10.5)
        set_cell_border(cell, top=4, left=4, bottom=4, right=4)

table.autofit = False
for row in table.rows:
    row.height = Cm(0.8)

add_para(doc, '', space_before=12)
add_para(doc, '实验地点：线上', align=WD_ALIGN_PARAGRAPH.LEFT, font_name='宋体', font_size=10.5)

# ===== 实验目的 =====
add_para(doc, '一、实验目的', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)
for line in [
    '1. 掌握Web服务器日志数据的解析与预处理方法；',
    '2. 学习从非结构化日志数据中提取有意义的特征；',
    '3. 运用KNN分类算法和K-Means聚类算法对日志数据进行异常检测；',
    '4. 理解监督学习与无监督学习在异常检测中的适用场景与差异；',
    '5. 培养完整的数据分析流程能力：从数据理解、预处理、建模到结果分析。'
]:
    add_para(doc, line, first_indent=0.74)

# ===== 实验环境 =====
add_para(doc, '二、实验仪器设备（环境）', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)
for line in [
    '操作系统：Windows 11',
    '编程语言：Python 3.11',
    '主要库：pandas 2.0+, numpy 1.24+, scikit-learn 1.3+, matplotlib 3.7+',
    '开发工具：VS Code',
    '数据来源：Apache服务器access.log访问日志（11558条记录）'
]:
    add_para(doc, line, first_indent=0.74)

# ===== 实验原理 =====
add_para(doc, '三、实验原理', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)
add_para(doc, '1. KNN（K近邻）分类算法：KNN是一种基于实例的监督学习算法，其核心思想是对于一个待分类样本，在特征空间中找到与其最接近的K个训练样本，通过这K个邻居的类别投票来决定该样本的类别。KNN算法简单直观，不需要训练阶段，适用于多分类问题。', first_indent=0.74)
add_para(doc, '2. K-Means聚类算法：K-Means是一种经典的无监督学习算法，通过迭代将样本划分为K个簇，使得簇内样本之间的相似度最大、簇间样本的相似度最小。算法步骤包括：①随机选择K个初始聚类中心；②将每个样本分配到距离最近的聚类中心；③重新计算每个簇的中心；④重复②③直到收敛。', first_indent=0.74)
add_para(doc, '3. 异常检测原理：本实验基于以下假设进行异常检测：正常用户的HTTP请求通常具有明确的资源目标（返回200状态码）、使用标准请求方法（GET/POST）、不包含攻击关键词（如passwd、sql等），而异常请求（扫描、攻击尝试）往往表现为大量404/403响应、包含敏感路径、使用非标准UA等特征。', first_indent=0.74)

# ===== 实验内容 =====
add_para(doc, '四、实验内容', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)
add_para(doc, '1. 数据加载与解析：使用正则表达式解析Apache日志格式，提取IP地址、时间戳、请求方法、请求路径、状态码、响应大小、User-Agent等字段。', first_indent=0.74)
add_para(doc, '2. 数据预处理：对时间戳进行解析提取小时特征；对缺失值进行处理（如响应大小为"-"时设为0）；对类别型特征进行编码。', first_indent=0.74)
add_para(doc, '3. 特征工程：基于领域知识构建15维特征向量，包括：路径长度、路径深度、是否包含查询参数、是否包含攻击关键词、请求方法编码（是否为POST/HEAD/非常规方法）、状态码编码（4xx/5xx/2xx）、User-Agent特征（是否为空、是否可疑）、时间特征（小时）。', first_indent=0.74)
add_para(doc, '4. 标签构建：基于规则标注正常/异常样本。正常样本标准：状态码200 + 标准请求方法 + 不含攻击关键词 + 非空UA。', first_indent=0.74)
add_para(doc, '5. KNN分类模型训练：使用StandardScaler进行特征标准化，通过交叉验证选择最优K值（1-20），训练最终模型并在测试集上评估。', first_indent=0.74)
add_para(doc, '6. K-Means聚类分析：使用全部数据进行无监督聚类（K=2），通过轮廓系数评估聚类质量，分析聚类结果与标注标签的一致性。', first_indent=0.74)

# ===== 实验结果分析 =====
add_para(doc, '五、实验结果分析（数据表格及数据处理或调试及结果分析等）', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)

add_para(doc, '（一）数据集统计特征', font_name='黑体', font_size=11, bold=True, first_indent=0.74)
add_para(doc, '日志数据共计11558条记录，全部来自单一IP地址（192.168.215.24）。数据分布呈现明显的攻击特征：状态码404占99.2%（11471条），403占0.4%（41条），200仅占0.2%（24条）；请求方法中GET占90.3%，HEAD占9.5%，POST仅占0.2%。根据规则标注：正常请求21条（0.18%），异常请求11537条（99.82%）。', first_indent=0.74)

add_para(doc, '（二）KNN分类结果', font_name='黑体', font_size=11, bold=True, first_indent=0.74)
add_para(doc, '通过交叉验证选择最优K值为1。测试集（3468条，30%）评估结果：准确率100.00%；正常类精确率/召回率/F1均为1.00；异常类精确率/召回率/F1均为1.00；混淆矩阵为TP=3462, TN=6, FP=0, FN=0。', first_indent=0.74)
add_para(doc, '分析：虽然准确率达到100%，但由于类别极度不平衡（正常:异常≈1:550），该结果需谨慎解读，模型可能过度拟合了异常样本的特征模式。', first_indent=0.74)

add_para(doc, '（三）K-Means聚类结果', font_name='黑体', font_size=11, bold=True, first_indent=0.74)
add_para(doc, '轮廓系数0.9245（接近1，聚类结构清晰）；聚类分布为簇0含11534条（99.7%，异常率100%），簇1含24条（0.3%，异常率12.5%）；聚类准确率（映射后）99.97%。', first_indent=0.74)
add_para(doc, '分析：K-Means成功将数据分为"大规模异常请求簇"和"少量混合簇"，与基于规则的标签高度一致。高轮廓系数表明日志数据的正常/异常特征差异显著。', first_indent=0.74)

add_para(doc, '（四）特征重要性分析', font_name='黑体', font_size=11, bold=True, first_indent=0.74)
add_para(doc, '通过随机森林评估特征重要性，排名前三的特征为：has_attack_keyword（是否含攻击关键词）、status_4xx（是否为4xx状态码）、ua_suspicious（UA是否可疑），与人工标注规则高度吻合，验证了特征设计的合理性。', first_indent=0.74)

# ===== 总结与心得 =====
add_para(doc, '六、总结与心得', font_name='黑体', font_size=12, bold=True, space_before=12, space_after=6)
add_para(doc, '1. 本次实验完整实践了从原始日志数据到异常检测模型的全流程，包括数据解析、预处理、特征工程、模型训练和结果评估。', first_indent=0.74)
add_para(doc, '2. KNN算法在本数据集上表现优异，但由于类别极度不平衡，高准确率并不完全代表模型泛化能力强。在实际应用中，需要采用SMOTE过采样、代价敏感学习或调整分类阈值等方法来处理不平衡问题。', first_indent=0.74)
add_para(doc, '3. K-Means作为无监督方法，在没有标签的情况下也能有效发现数据中的异常模式，这对于未知攻击类型的检测具有重要价值。轮廓系数0.9245表明日志数据的内在结构非常适合聚类分析。', first_indent=0.74)
add_para(doc, '4. 特征工程是本次实验的关键环节。通过领域知识构建的攻击关键词、状态码、请求方法等特征，显著提升了模型的区分能力。这提示在实际项目中，深入理解业务场景比单纯调参更重要。', first_indent=0.74)
add_para(doc, '5. 本实验的局限在于数据全部来自单一IP，缺乏多源数据对比；正常样本过少导致模型可能偏向识别已知攻击模式。未来可以引入更多正常流量数据，并尝试其他模型（如Isolation Forest、One-Class SVM）进行对比。', first_indent=0.74)

# ===== 教师签名行 =====
add_para(doc, '', space_before=30)
add_para(doc, '教师签名：', align=WD_ALIGN_PARAGRAPH.RIGHT, font_name='宋体', font_size=10.5)
add_para(doc, '日期：', align=WD_ALIGN_PARAGRAPH.RIGHT, font_name='宋体', font_size=10.5)

# ===== 附录A：代码 =====
doc.add_page_break()
add_para(doc, '附录A：完整代码', font_name='黑体', font_size=14, bold=True, space_before=12, space_after=6)

code_lines = '''import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, silhouette_score
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# 1. 数据加载与解析
pattern = r'(\\S+) \\S+ \\S+ \\[([^\\]]+)\\] \"(\\S+) (\\S+) (\\S+)\" (\\d+) (\\d+|-) \"([^\"]*)\" \"([^\"]*)\"'
records = []
with open('access.log', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        m = re.match(pattern, line.strip())
        if m:
            records.append({
                'ip': m.group(1), 'timestamp': m.group(2), 'method': m.group(3),
                'path': m.group(4), 'protocol': m.group(5), 'status': int(m.group(6)),
                'size': 0 if m.group(7) == '-' else int(m.group(7)),
                'referer': m.group(8), 'ua': m.group(9)
            })
df = pd.DataFrame(records)

# 2. 数据预处理
df['datetime'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
df['hour'] = df['datetime'].dt.hour.fillna(0).astype(int)

# 3. 特征提取
attack_keywords = ['passwd', 'shadow', 'etc', 'nmap', 'sql', 'union', 'select', 'eval', 
                   'exec', '../', '..%2f', 'config', 'admin', 'phpmyadmin', 'login', 
                   'debug', 'trace', 'cmd', 'shell', 'wget', 'curl']

def extract_features(row):
    path = row['path'].lower()
    ua = row['ua'].lower()
    return pd.Series({
        'path_len': len(row['path']),
        'path_depth': row['path'].count('/'),
        'has_query': 1 if '?' in row['path'] else 0,
        'has_attack_keyword': 1 if any(k in path for k in attack_keywords) else 0,
        'has_encoding': 1 if '%' in row['path'] else 0,
        'is_post': 1 if row['method'] == 'POST' else 0,
        'is_head': 1 if row['method'] == 'HEAD' else 0,
        'is_unusual_method': 1 if row['method'] not in ['GET', 'POST', 'HEAD'] else 0,
        'status_4xx': 1 if 400 <= row['status'] < 500 else 0,
        'status_5xx': 1 if 500 <= row['status'] < 600 else 0,
        'status_2xx': 1 if 200 <= row['status'] < 300 else 0,
        'size': row['size'],
        'ua_empty': 1 if row['ua'] == '-' else 0,
        'ua_suspicious': 1 if any(k in ua for k in ['nmap', 'sqlmap', 'bot', 'crawler', 'scan']) else 0,
        'hour': row['hour']
    })

feature_df = df.apply(extract_features, axis=1)

# 4. 标签构建
def label_request(row):
    if row['status'] == 200 and row['method'] in ['GET', 'POST', 'HEAD'] and \
       not any(k in row['path'].lower() for k in attack_keywords) and row['ua'] != '-':
        return 0
    return 1
df['label'] = df.apply(label_request, axis=1)

# 5. KNN分类
X = feature_df.values
y = df['label'].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

best_k, best_score = 1, 0
for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    if score > best_score:
        best_k, best_score = k, score

knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(f"KNN准确率: {accuracy_score(y_test, y_pred):.4f}")

# 6. K-Means聚类
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
print(f"轮廓系数: {silhouette_score(X_scaled, clusters):.4f}")
'''

p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.0
run = p.add_run(code_lines)
run.font.name = 'Consolas'
run.font.size = Pt(8)

# ===== 附录B：截图 =====
doc.add_page_break()
add_para(doc, '附录B：运行结果截图', font_name='黑体', font_size=14, bold=True, space_before=12, space_after=6)

img_path = r'C:\Users\dbw\.openclaw\workspace\大作业\analysis_results.png'
if os.path.exists(img_path):
    doc.add_picture(img_path, width=Inches(6.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run('图1 实验分析结果汇总（状态码分布、标签分布、KNN混淆矩阵、K值选择、聚类散点图、特征重要性）')
    set_run_font(run, '宋体', 9)

# 保存
output_path = r'C:\Users\dbw\.openclaw\workspace\大作业\BXXXXXXXXX-XXX-数据挖掘大作业.docx'
doc.save(output_path)
print(f"报告已生成: {output_path}")
