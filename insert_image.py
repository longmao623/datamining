"""在报告文档中插入分析结果截图"""
from docx import Document
from docx.shared import Inches
import os

doc = Document(r'C:\Users\dbw\.openclaw\workspace\大作业\BXXXXXXXXX-XXX-数据挖掘大作业.docx')

# 在段落115（图1标题）后插入图片
para = doc.paragraphs[115]
# 在段落后添加图片
new_para = para._element.addnext(doc.add_paragraph()._element)
# 找到新段落对象
for p in doc.paragraphs:
    if p._element == new_para:
        new_para = p
        break
else:
    new_para = doc.paragraphs[-1]

img_path = r'C:\Users\dbw\.openclaw\workspace\大作业\analysis_results.png'
if os.path.exists(img_path):
    run = new_para.add_run()
    run.add_picture(img_path, width=Inches(6.0))
    new_para.alignment = 1  # CENTER

# 保存
output_path = r'C:\Users\dbw\.openclaw\workspace\大作业\BXXXXXXXXX-XXX-数据挖掘大作业.docx'
doc.save(output_path)
print(f"截图已插入: {output_path}")
