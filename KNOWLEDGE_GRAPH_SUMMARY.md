# 知识图谱三元组文件构建完成总结 / Knowledge Graph Triple File Build Summary

## 概述 / Overview

已成功创建完整的知识图谱三元组文件构建工具和示例，满足用户需求"帮我用这个仓库里介绍的方法构建一个知识图谱三元组文件"。

**Task completed successfully**: "Help me use the methods introduced in this repository to build a knowledge graph triple file"

---

## 创建的文件清单 / Files Created

### 📝 核心工具脚本 / Core Tool Scripts

1. **`build_kg_example.py`** (16KB)
   - 功能 / Function: 知识图谱文件构建器 / Knowledge graph file builder
   - 特性 / Features:
     - 支持三元组列表和字典两种构建方式
     - 自动生成 .kg 和 .link 文件
     - 包含完整的电影和商品推荐示例
     - 双语注释（中英文）

2. **`test_kg_files.py`** (7KB)
   - 功能 / Function: 文件格式验证工具 / File format validation tool
   - 特性 / Features:
     - 验证文件格式正确性
     - 检查数据一致性
     - 双语输出

3. **`run_kg_example.py`** (3KB)
   - 功能 / Function: 示例运行工具 / Example runner
   - 特性 / Features:
     - 简化的命令行接口
     - 支持所有知识感知推荐模型
     - 错误提示友好

### 📚 文档文件 / Documentation Files

1. **`知识图谱构建指南.md`** (14KB) - 中文完整指南
   - 包含详细的格式说明
   - 三种构建方法教程
   - 常见问题解答
   - 进阶用法示例

2. **`KG_BUILD_GUIDE.md`** (15KB) - 英文完整指南
   - Complete format specifications
   - Three construction methods
   - FAQ section
   - Advanced usage examples

3. **`README_KG_EXAMPLE.md`** (8KB) - 快速开始指南（双语）
   - 快速上手步骤
   - 文件说明
   - 常见问题

### ⚙️ 配置文件 / Configuration File

**`kg_example_config.yaml`** (1KB)
- RecBole 配置示例
- 包含所有必要的字段映射
- 可直接使用

### 📊 示例数据集 / Example Datasets

#### 1. **movie_example/** - 电影推荐知识图谱
   - `movie_example.kg` - 16个知识图谱三元组
   - `movie_example.link` - 3个物品-实体链接
   - `movie_example.inter` - 12个用户-物品交互

#### 2. **product_example/** - 商品推荐知识图谱
   - `product_example.kg` - 14个知识图谱三元组
   - `product_example.link` - 3个物品-实体链接
   - `product_example.inter` - 10个用户-物品交互

---

## 快速使用指南 / Quick Usage Guide

### 1️⃣ 生成知识图谱文件 / Generate Knowledge Graph Files

```bash
# 运行示例（推荐首次使用）
python build_kg_example.py

# 仅生成电影示例
python build_kg_example.py --example movie

# 仅生成商品示例
python build_kg_example.py --example product

# 仅查看格式指南
python build_kg_example.py --example guide
```

### 2️⃣ 验证文件格式 / Validate File Format

```bash
python test_kg_files.py
```

### 3️⃣ 在RecBole中使用 / Use in RecBole

```bash
# 安装RecBole（如果尚未安装）
pip install recbole

# 运行知识感知推荐模型
python run_kg_example.py --model CKE --dataset movie_example

# 尝试其他模型
python run_kg_example.py --model KGAT --dataset product_example
```

---

## 支持的知识感知推荐模型 / Supported Knowledge-aware Models

| 模型 / Model | 说明 / Description |
|-------------|-------------------|
| CKE | 协同知识库嵌入 / Collaborative Knowledge base Embedding |
| KGAT | 知识图谱注意力网络 / Knowledge Graph Attention Network |
| KGCN | 知识图谱卷积网络 / Knowledge Graph Convolutional Network |
| KGNNLS | 知识图谱神经网络标签平滑 / KG Neural Network with Label Smoothness |
| RippleNet | 基于传播的知识图谱网络 / Propagation-based KG Network |
| MKR | 多任务知识图谱推荐 / Multi-task KG Recommendation |
| KTUP | 知识感知元组学习 / Knowledge-aware Tuple-wise Learning |
| KGIN | 知识图谱集成网络 / Knowledge Graph Integrated Network |
| MCCLK | 元上下文对比学习 / Meta-Context Contrastive Learning |
| CFKG | 协同过滤知识图谱 / Collaborative Filtering with KG |

---

## 文件格式规范 / File Format Specifications

### .kg 文件格式 / .kg File Format

```
head_id:tokenrelation_id:tokentail_id:token
movie_1directed_bydirector_nolan
movie_1has_actoractor_dicaprio
movie_2has_genregenre_action
```

- 使用制表符 `\t` 分隔 / Tab-separated
- 第一行为头部定义 / First line is header
- 三个字段：头实体、关系、尾实体 / Three fields: head, relation, tail

### .link 文件格式 / .link File Format

```
item_id:tokenentity_id:token
1movie_1
2movie_2
3movie_3
```

- 使用制表符 `\t` 分隔 / Tab-separated
- 第一行为头部定义 / First line is header
- 两个字段：物品ID、实体ID / Two fields: item ID, entity ID

---

## 自定义使用示例 / Custom Usage Examples

### 方法1: 使用三元组列表 / Method 1: Triple List

```python
from build_kg_example import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder('my_dataset', './dataset')

# 定义知识图谱三元组
kg_triples = [
    ('entity_1', 'relation_type', 'entity_2'),
    ('entity_2', 'another_relation', 'entity_3'),
]

# 定义物品-实体链接
item_links = [
    ('1', 'entity_1'),
    ('2', 'entity_2'),
]

# 生成文件
builder.build_kg_triples(kg_triples)
builder.build_item_entity_links(item_links)
```

### 方法2: 使用字典 / Method 2: Dictionary

```python
# 知识图谱数据
kg_data = {
    'entity_1': [('relation_1', 'entity_2'), ('relation_2', 'entity_3')],
    'entity_2': [('relation_3', 'entity_4')],
}

# 物品-实体映射
item_entity_map = {
    '1': 'entity_1',
    '2': 'entity_2',
}

builder.build_from_dict(kg_data, item_entity_map)
```

---

## 验证结果 / Validation Results

✅ 所有文件格式验证通过 / All file format validations passed  
✅ 数据一致性检查通过 / Data consistency checks passed  
✅ 可直接在RecBole中使用 / Ready to use in RecBole  

---

## 扩展资源 / Additional Resources

1. **RecBole官方文档** / RecBole Documentation: https://recbole.io/docs/
2. **知识感知推荐快速开始** / Knowledge-aware Quick Start: https://recbole.io/docs/get_started/started/knowledge-based.html
3. **数据格式说明** / Data Format Guide: https://recbole.io/docs/user_guide/data_intro.html
4. **GitHub仓库** / GitHub Repo: https://github.com/RUCAIBox/RecBole

---

## 下一步建议 / Next Steps

1. 📖 **阅读详细文档** / Read detailed documentation
   - 中文：`知识图谱构建指南.md`
   - English: `KG_BUILD_GUIDE.md`

2. 🔧 **尝试自定义数据** / Try custom data
   - 使用自己的知识图谱数据
   - 调整构建脚本适配需求

3. 🚀 **运行推荐模型** / Run recommendation models
   - 尝试不同的知识感知模型
   - 调整超参数优化性能

4. 📊 **扩展知识图谱** / Extend knowledge graph
   - 添加更多实体和关系
   - 集成外部知识库（如DBpedia, Freebase）

---

## 技术支持 / Support

如有问题或建议 / For questions or suggestions:
- 提交Issue / Submit Issue: https://github.com/RUCAIBox/RecBole/issues
- 查看文档 / Check Docs: https://recbole.io/docs/
- 参与讨论 / Join Discussion: https://github.com/RUCAIBox/RecBole/discussions

---

**创建时间 / Created**: 2024年12月  
**状态 / Status**: ✅ 完成 / Completed  
**许可证 / License**: MIT License
