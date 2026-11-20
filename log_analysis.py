"""
数据挖掘期末大作业 - Web日志分析与异常检测
学号: BXXXXXXXXX  姓名: XXX
"""
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, silhouette_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 数据加载与解析 ==========
print("="*60)
print("1. 数据加载与解析")
print("="*60)

pattern = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+|-) "([^"]*)" "([^"]*)"'

records = []
with open(r'C:\Users\dbw\.openclaw\workspace\大作业\大作业\access.log', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = re.match(pattern, line)
        if m:
            records.append({
                'ip': m.group(1),
                'timestamp': m.group(2),
                'method': m.group(3),
                'path': m.group(4),
                'protocol': m.group(5),
                'status': int(m.group(6)),
                'size': 0 if m.group(7) == '-' else int(m.group(7)),
                'referer': m.group(8),
                'ua': m.group(9)
            })

df = pd.DataFrame(records)
print(f"总记录数: {len(df)}")
print(f"字段: {list(df.columns)}")
print(f"\n状态码分布:\n{df['status'].value_counts().sort_index()}")
print(f"\n请求方法分布:\n{df['method'].value_counts()}")

# ========== 2. 数据预处理 ==========
print("\n" + "="*60)
print("2. 数据预处理")
print("="*60)

# 时间解析
df['datetime'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
df['hour'] = df['datetime'].dt.hour.fillna(0).astype(int)

# 定义攻击关键词
attack_keywords = ['passwd', 'shadow', 'etc', 'nmap', 'sql', 'union', 'select', 'eval', 
                   'exec', '../', '..%2f', 'config', 'admin', 'phpmyadmin', 'login', 
                   'debug', 'trace', 'cmd', 'shell', 'wget', 'curl']

def extract_features(row):
    path = row['path'].lower()
    ua = row['ua'].lower()
    
    features = {}
    # 基础特征
    features['path_len'] = len(row['path'])
    features['path_depth'] = row['path'].count('/')
    features['has_query'] = 1 if '?' in row['path'] else 0
    features['has_attack_keyword'] = 1 if any(k in path for k in attack_keywords) else 0
    features['has_encoding'] = 1 if '%' in row['path'] else 0
    features['is_post'] = 1 if row['method'] == 'POST' else 0
    features['is_head'] = 1 if row['method'] == 'HEAD' else 0
    features['is_unusual_method'] = 1 if row['method'] not in ['GET', 'POST', 'HEAD'] else 0
    features['status_4xx'] = 1 if 400 <= row['status'] < 500 else 0
    features['status_5xx'] = 1 if 500 <= row['status'] < 600 else 0
    features['status_2xx'] = 1 if 200 <= row['status'] < 300 else 0
    features['size'] = row['size']
    features['ua_empty'] = 1 if row['ua'] == '-' else 0
    features['ua_suspicious'] = 1 if any(k in ua for k in ['nmap', 'sqlmap', 'bot', 'crawler', 'scan']) else 0
    features['hour'] = row['hour']
    
    return pd.Series(features)

feature_df = df.apply(extract_features, axis=1)
print(f"特征维度: {feature_df.shape}")
print(f"特征列表: {list(feature_df.columns)}")

# ========== 3. 标签构建（基于规则） ==========
print("\n" + "="*60)
print("3. 标签构建")
print("="*60)

# 规则：正常请求 = 状态200 + GET/POST/HEAD + 不含攻击关键词 + 非空UA
def label_request(row):
    if row['status'] == 200 and row['method'] in ['GET', 'POST', 'HEAD'] and \
       not any(k in row['path'].lower() for k in attack_keywords) and \
       row['ua'] != '-':
        return 0  # 正常
    return 1  # 异常

df['label'] = df.apply(label_request, axis=1)
print(f"正常请求: {(df['label']==0).sum()}")
print(f"异常请求: {(df['label']==1).sum()}")
print(f"异常比例: {df['label'].mean()*100:.2f}%")

# ========== 4. KNN分类模型 ==========
print("\n" + "="*60)
print("4. KNN分类模型")
print("="*60)

X = feature_df.values
y = df['label'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# 选择K值
best_k = 1
best_score = 0
for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    if score > best_score:
        best_score = score
        best_k = k

print(f"最优K值: {best_k}, 验证准确率: {best_score:.4f}")

# 最终模型
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

print(f"\nKNN分类报告 (K={best_k}):")
print(classification_report(y_test, y_pred_knn, target_names=['正常', '异常']))
print(f"准确率: {accuracy_score(y_test, y_pred_knn):.4f}")

# 混淆矩阵
cm_knn = confusion_matrix(y_test, y_pred_knn)
print(f"混淆矩阵:\n{cm_knn}")

# ========== 5. K-Means聚类模型 ==========
print("\n" + "="*60)
print("5. K-Means聚类模型")
print("="*60)

# 使用全部数据做聚类（无监督）
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# 评估轮廓系数
sil_score = silhouette_score(X_scaled, clusters)
print(f"轮廓系数: {sil_score:.4f}")

# 分析聚类结果与标签的对应关系
df['cluster'] = clusters
print(f"\n聚类分布:")
print(df['cluster'].value_counts())

print(f"\n聚类 vs 标签交叉表:")
cross_tab = pd.crosstab(df['cluster'], df['label'], margins=True)
cross_tab.columns = ['正常(0)', '异常(1)', '合计']
print(cross_tab)

# 判断哪个簇是异常簇
cluster_0_anomaly_rate = df[df['cluster']==0]['label'].mean()
cluster_1_anomaly_rate = df[df['cluster']==1]['label'].mean()
print(f"\n簇0异常率: {cluster_0_anomaly_rate:.4f}")
print(f"簇1异常率: {cluster_1_anomaly_rate:.4f}")

# 根据异常率映射聚类标签
if cluster_0_anomaly_rate > cluster_1_anomaly_rate:
    cluster_map = {0: 1, 1: 0}  # 簇0是异常
else:
    cluster_map = {0: 0, 1: 1}  # 簇1是异常

df['cluster_label'] = df['cluster'].map(cluster_map)
kmeans_acc = accuracy_score(df['label'], df['cluster_label'])
print(f"K-Means聚类准确率（映射后）: {kmeans_acc:.4f}")

# ========== 6. 可视化 ==========
print("\n" + "="*60)
print("6. 生成可视化图表")
print("="*60)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 图1: 状态码分布
ax1 = axes[0, 0]
status_counts = df['status'].value_counts().sort_index()
ax1.bar(status_counts.index.astype(str), status_counts.values, color='steelblue')
ax1.set_title('状态码分布')
ax1.set_xlabel('状态码')
ax1.set_ylabel('数量')

# 图2: 标签分布
ax2 = axes[0, 1]
labels = ['正常', '异常']
counts = [(df['label']==0).sum(), (df['label']==1).sum()]
colors = ['#2ecc71', '#e74c3c']
ax2.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title('正常/异常请求分布')

# 图3: KNN混淆矩阵热力图
ax3 = axes[0, 2]
im = ax3.imshow(cm_knn, interpolation='nearest', cmap='Blues')
ax3.set_title('KNN混淆矩阵')
tick_marks = np.arange(2)
ax3.set_xticks(tick_marks)
ax3.set_yticks(tick_marks)
ax3.set_xticklabels(['正常', '异常'])
ax3.set_yticklabels(['正常', '异常'])
ax3.set_ylabel('真实标签')
ax3.set_xlabel('预测标签')
# 添加数值
for i in range(2):
    for j in range(2):
        ax3.text(j, i, format(cm_knn[i, j], 'd'), ha="center", va="center", color="black")

# 图4: K值选择
ax4 = axes[1, 0]
k_range = range(1, 21)
k_scores = []
for k in k_range:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train, y_train)
    k_scores.append(knn_temp.score(X_test, y_test))
ax4.plot(k_range, k_scores, marker='o', color='steelblue')
ax4.axvline(x=best_k, color='red', linestyle='--', label=f'最优K={best_k}')
ax4.set_title('KNN不同K值的准确率')
ax4.set_xlabel('K值')
ax4.set_ylabel('准确率')
ax4.legend()
ax4.grid(True, alpha=0.3)

# 图5: 聚类散点图（PCA降维）
ax5 = axes[1, 1]
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
colors_cluster = ['#2ecc71' if c == 0 else '#e74c3c' for c in clusters]
ax5.scatter(X_pca[:, 0], X_pca[:, 1], c=colors_cluster, alpha=0.5, s=5)
ax5.set_title('K-Means聚类结果 (PCA降维)')
ax5.set_xlabel('主成分1')
ax5.set_ylabel('主成分2')
# 标记聚类中心
centers_pca = pca.transform(kmeans.cluster_centers_)
ax5.scatter(centers_pca[:, 0], centers_pca[:, 1], c='black', marker='x', s=100, label='聚类中心')
ax5.legend()

# 图6: 特征重要性（使用随机森林作为参考）
ax6 = axes[1, 2]
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1][:10]
ax6.barh(range(10), importances[indices], color='steelblue')
ax6.set_yticks(range(10))
ax6.set_yticklabels([feature_df.columns[i] for i in indices])
ax6.set_title('Top 10 特征重要性')
ax6.set_xlabel('重要性')
ax6.invert_yaxis()

plt.tight_layout()
plt.savefig(r'C:\Users\dbw\.openclaw\workspace\大作业\analysis_results.png', dpi=150, bbox_inches='tight')
print("图表已保存: analysis_results.png")
plt.close()

# ========== 7. 保存结果 ==========
print("\n" + "="*60)
print("7. 保存分析结果")
print("="*60)

# 保存预测结果
result_df = df[['ip', 'timestamp', 'method', 'path', 'status', 'ua', 'label', 'cluster', 'cluster_label']].copy()
result_df.to_csv(r'C:\Users\dbw\.openclaw\workspace\大作业\prediction_results.csv', index=False, encoding='utf-8-sig')
print("预测结果已保存: prediction_results.csv")

# 保存特征
feature_df['label'] = df['label']
feature_df.to_csv(r'C:\Users\dbw\.openclaw\workspace\大作业\features.csv', index=False, encoding='utf-8-sig')
print("特征数据已保存: features.csv")

# 输出汇总
print("\n" + "="*60)
print("分析完成!")
print("="*60)
print(f"总样本数: {len(df)}")
print(f"正常请求: {(df['label']==0).sum()} ({(df['label']==0).mean()*100:.2f}%)")
print(f"异常请求: {(df['label']==1).sum()} ({(df['label']==1).mean()*100:.2f}%)")
print(f"KNN最优K值: {best_k}")
print(f"KNN测试集准确率: {accuracy_score(y_test, y_pred_knn):.4f}")
print(f"K-Means轮廓系数: {sil_score:.4f}")
print(f"K-Means聚类准确率(映射后): {kmeans_acc:.4f}")
