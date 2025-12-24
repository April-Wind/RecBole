# RecBole Knowledge Graph Triple File Builder Guide

[中文指南](./知识图谱构建指南.md) | **English Guide**

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [File Format Specification](#file-format-specification)
3. [Quick Start](#quick-start)
4. [Detailed Tutorial](#detailed-tutorial)
5. [Examples](#examples)
6. [FAQ](#faq)

---

## Introduction

This guide explains how to build knowledge graph triple files for RecBole recommendation system library. Knowledge graphs can provide rich entity relationship information to improve recommendation performance.

RecBole supports knowledge-aware recommendation models such as:
- **CKE** (Collaborative Knowledge base Embedding)
- **KGAT** (Knowledge Graph Attention Network)
- **KGCN** (Knowledge Graph Convolutional Network)
- **RippleNet**
- **KGIN** (Knowledge Graph Integrated Network)
- And more...

---

## File Format Specification

RecBole's knowledge graph data consists of two core files:

### 1. Knowledge Graph Triples File (`.kg`)

**Format Requirements:**
```
head_id:token	relation_id:token	tail_id:token
entity_1	relation_type	entity_2
entity_1	relation_type	entity_3
...
```

**Description:**
- First line must be field definition (with `:token` type annotation)
- Use **tab character** (`\t`) to separate fields
- `head_id`: Head entity ID
- `relation_id`: Relation type
- `tail_id`: Tail entity ID

**Example:**
```
head_id:token	relation_id:token	tail_id:token
movie_1	directed_by	director_nolan
movie_1	has_actor	actor_dicaprio
movie_1	has_genre	genre_scifi
movie_2	directed_by	director_tarantino
```

### 2. Item-Entity Link File (`.link`)

**Format Requirements:**
```
item_id:token	entity_id:token
item_id_1	entity_id_1
item_id_2	entity_id_2
...
```

**Description:**
- First line must be field definition (with `:token` type annotation)
- Use **tab character** (`\t`) to separate fields
- `item_id`: Item ID in the recommendation system (corresponding to item_id in `.inter` file)
- `entity_id`: Entity ID in the knowledge graph (corresponding to entities in `.kg` file)

**Example:**
```
item_id:token	entity_id:token
1	movie_1
2	movie_2
3	movie_3
```

---

## Quick Start

### Step 1: Run Example Script

We provide a complete example script `build_kg_example.py` to quickly generate knowledge graph files:

```bash
# Run all examples (recommended for first use)
python build_kg_example.py

# Run only movie recommendation example
python build_kg_example.py --example movie

# Run only product recommendation example
python build_kg_example.py --example product

# Show only format guide
python build_kg_example.py --example guide
```

### Step 2: Check Generated Files

After running, example files will be generated in `./dataset/` directory:

```
dataset/
├── movie_example/
│   ├── movie_example.kg      # Movie knowledge graph triples
│   └── movie_example.link    # Movie-entity links
└── product_example/
    ├── product_example.kg    # Product knowledge graph triples
    └── product_example.link  # Product-entity links
```

### Step 3: Use in RecBole

Create a configuration file `config.yaml`:

```yaml
# Dataset configuration
USER_ID_FIELD: user_id
ITEM_ID_FIELD: item_id
HEAD_ENTITY_ID_FIELD: head_id
TAIL_ENTITY_ID_FIELD: tail_id
RELATION_ID_FIELD: relation_id
ENTITY_ID_FIELD: entity_id

# Load data columns
load_col:
    inter: [user_id, item_id]       # Interaction data
    kg: [head_id, relation_id, tail_id]  # Knowledge graph triples
    link: [item_id, entity_id]      # Item-entity links

# Model configuration
embedding_size: 64
kg_embedding_size: 64
```

Then run the model:

```bash
python run_recbole.py --model=CKE --dataset=movie_example --config_files=config.yaml
```

---

## Detailed Tutorial

### Method 1: Build Using Triple List

Suitable for small datasets or scenarios requiring precise control of each triple.

```python
from build_kg_example import KnowledgeGraphBuilder

# Create builder
builder = KnowledgeGraphBuilder(
    dataset_name='my_dataset',
    output_dir='./dataset'
)

# Define knowledge graph triples
kg_triples = [
    ('movie_1', 'directed_by', 'director_nolan'),
    ('movie_1', 'has_actor', 'actor_dicaprio'),
    ('movie_2', 'has_genre', 'genre_action'),
]

# Define item-entity links
item_links = [
    ('1', 'movie_1'),
    ('2', 'movie_2'),
]

# Generate files
builder.build_kg_triples(kg_triples)
builder.build_item_entity_links(item_links)
```

### Method 2: Build Using Dictionary

Suitable for hierarchical structures or batch processing scenarios.

```python
from build_kg_example import KnowledgeGraphBuilder

# Create builder
builder = KnowledgeGraphBuilder(
    dataset_name='my_dataset',
    output_dir='./dataset'
)

# Define knowledge graph data (dictionary format)
kg_data = {
    'movie_1': [
        ('directed_by', 'director_nolan'),
        ('has_actor', 'actor_dicaprio'),
        ('has_genre', 'genre_scifi'),
    ],
    'movie_2': [
        ('has_genre', 'genre_action'),
    ],
}

# Define item-entity mapping
item_entity_map = {
    '1': 'movie_1',
    '2': 'movie_2',
}

# Generate files
builder.build_from_dict(kg_data, item_entity_map)
```

### Method 3: Build from External Data Sources

If you have external knowledge bases (such as DBpedia, Freebase, etc.):

```python
import pandas as pd
from build_kg_example import KnowledgeGraphBuilder

# Assume data is fetched from external API or database
# Example: Read from CSV file
external_kg = pd.read_csv('external_knowledge.csv')

# Convert to triple format
triples = []
for _, row in external_kg.iterrows():
    triples.append((row['subject'], row['predicate'], row['object']))

# Create builder and generate files
builder = KnowledgeGraphBuilder('external_dataset', './dataset')
builder.build_kg_triples(triples)

# Establish item to entity mapping
# This needs to be based on your actual situation
item_links = [
    (str(i), f"entity_{i}") for i in range(1, 101)
]
builder.build_item_entity_links(item_links)
```

---

## Examples

### Movie Recommendation Example

**Scenario Description:**
Build a knowledge graph for a movie recommendation system, including entities such as movies, directors, actors, genres and their relationships.

**Knowledge Graph Structure:**
```
Movie ---directed_by---> Director
Movie ---has_actor---> Actor
Movie ---has_genre---> Genre
Director ---won_award---> Award
Actor ---collaborated_with---> Actor
```

**Generated File Content Example:**

`movie_example.kg`:
```
head_id:token	relation_id:token	tail_id:token
movie_1	directed_by	director_nolan
movie_1	has_actor	actor_dicaprio
movie_1	has_genre	genre_scifi
movie_2	directed_by	director_tarantino
movie_2	has_actor	actor_travolta
```

`movie_example.link`:
```
item_id:token	entity_id:token
1	movie_1
2	movie_2
3	movie_3
```

### Product Recommendation Example

**Scenario Description:**
Build a knowledge graph for an e-commerce recommendation system, including entities such as products, brands, categories, features and their relationships.

**Knowledge Graph Structure:**
```
Product ---brand---> Brand
Product ---category---> Category
Product ---has_feature---> Feature
Brand ---headquartered_in---> Location
```

**Generated File Content Example:**

`product_example.kg`:
```
head_id:token	relation_id:token	tail_id:token
product_laptop_1	brand	brand_dell
product_laptop_1	category	category_electronics
product_laptop_1	has_feature	feature_16gb_ram
product_laptop_2	brand	brand_apple
```

`product_example.link`:
```
item_id:token	entity_id:token
101	product_laptop_1
102	product_laptop_2
103	product_phone_1
```

---

## FAQ

### Q1: Why do we need the `.link` file?

**A:** The `.link` file establishes a mapping between item IDs (item_id) in the recommendation system and entity IDs (entity_id) in the knowledge graph. This is necessary because:
- The `.inter` file in the recommendation system uses simple item_ids (e.g., 1, 2, 3...)
- The knowledge graph uses meaningful entity IDs (e.g., movie_1, product_laptop_1...)
- The `.link` file is needed to connect the two

### Q2: Where can I get knowledge graph data?

**A:** Common knowledge graph data sources include:
- **Public knowledge bases**: DBpedia, Freebase, Wikidata, YAGO, etc.
- **Domain knowledge bases**: IMDB (movies), MusicBrainz (music), etc.
- **Self-built knowledge bases**: Built from business data
- **Third-party APIs**: Such as Google Knowledge Graph API

### Q3: How to determine entities and relationships?

**A:** When designing a knowledge graph, consider:
1. **Entity selection**: Select entities helpful for recommendation tasks (e.g., movies, directors, actors, genres)
2. **Relationship definition**: Define meaningful relationships (e.g., directed_by, has_actor, has_genre)
3. **Granularity control**: Balance the scale and quality of the knowledge graph
4. **Data quality**: Ensure accuracy of triples

### Q4: How to handle large-scale knowledge graphs?

**A:** For large-scale knowledge graphs:
1. **Batch processing**: Use pandas' `chunksize` parameter for batch reading and writing
2. **Filtering**: Keep only entities and relationships relevant to recommendation tasks
3. **Entity alignment**: Use entity alignment techniques to reduce redundancy
4. **Parallel processing**: Use multiprocessing for large-scale data

Example code:
```python
import pandas as pd

# Batch processing of large files
chunk_size = 10000
triples = []

for chunk in pd.read_csv('large_kg.csv', chunksize=chunk_size):
    for _, row in chunk.iterrows():
        # Perform necessary filtering and transformation
        if is_relevant(row):
            triples.append((row['head'], row['relation'], row['tail']))

builder.build_kg_triples(triples)
```

### Q5: Can the generated files be used directly?

**A:** After generating `.kg` and `.link` files, you still need to:
1. **Prepare interaction file** (`.inter`): Contains user-item interaction records
2. **Prepare configuration file**: Set field mapping and model parameters
3. **Validate data**: Ensure item IDs are consistent in `.inter` and `.link` files

A complete dataset should include:
```
dataset/
└── my_dataset/
    ├── my_dataset.inter    # User-item interactions
    ├── my_dataset.kg       # Knowledge graph triples
    └── my_dataset.link     # Item-entity links
```

### Q6: Which knowledge-aware recommendation models are supported?

**A:** RecBole supports multiple knowledge-aware recommendation models:

| Model | Description |
|-------|-------------|
| CKE | Collaborative Knowledge base Embedding |
| KGAT | Knowledge Graph Attention Network |
| KGCN | Knowledge Graph Convolutional Network |
| KGNNLS | Knowledge Graph Neural Network with Label Smoothness |
| RippleNet | Propagation-based Knowledge Graph Network |
| MKR | Multi-task Knowledge Graph Recommendation |
| KTUP | Knowledge-aware Tuple-wise Learning |
| KGIN | Knowledge Graph Integrated Network |
| MCCLK | Meta-Context Contrastive Learning |
| CFKG | Collaborative Filtering with Knowledge Graph |

Usage examples:
```bash
# Use CKE model
python run_recbole.py --model=CKE --dataset=my_dataset

# Use KGAT model
python run_recbole.py --model=KGAT --dataset=my_dataset

# Use RippleNet model
python run_recbole.py --model=RippleNet --dataset=my_dataset
```

### Q7: How to verify if the knowledge graph files are correct?

**A:** You can verify using the following methods:

```python
from recbole.config import Config
from recbole.data import create_dataset

# Load configuration
config = Config(model='CKE', dataset='my_dataset')

# Create dataset
dataset = create_dataset(config)

# View knowledge graph statistics
print(f"Number of entities: {dataset.entity_num}")
print(f"Number of relations: {dataset.relation_num}")
print(f"Number of triples: {len(dataset.kg_feat)}")
print(f"Number of linked items: {len(dataset.item2entity)}")

# View partial data
print("\nKnowledge graph triple examples:")
print(dataset.kg_feat.head(10))

print("\nItem-entity mapping examples:")
for item_id, entity_id in list(dataset.item2entity.items())[:5]:
    print(f"Item {item_id} -> Entity {entity_id}")
```

---

## Advanced Usage

### Adding Entity Attributes

In addition to basic triples, you can add attributes to entities:

```python
# Extended knowledge graph with attributes
extended_kg = [
    # Basic relationships
    ('movie_1', 'directed_by', 'director_nolan'),
    ('movie_1', 'has_actor', 'actor_dicaprio'),
    
    # Attribute information
    ('movie_1', 'has_rating', 'rating_8.8'),
    ('movie_1', 'release_year', 'year_2010'),
    ('director_nolan', 'nationality', 'country_uk'),
    ('actor_dicaprio', 'birth_year', 'year_1974'),
]
```

### Enhancing Graph with Reverse Relations

```python
def add_reverse_relations(triples, reverse_suffix='_reverse'):
    """Add reverse relation for each triple"""
    extended_triples = list(triples)
    for head, relation, tail in triples:
        # Add reverse relation
        reverse_relation = relation + reverse_suffix
        extended_triples.append((tail, reverse_relation, head))
    return extended_triples

# Usage
kg_triples = [
    ('movie_1', 'directed_by', 'director_nolan'),
    ('movie_1', 'has_actor', 'actor_dicaprio'),
]

extended_triples = add_reverse_relations(kg_triples)
# Result will include:
# ('director_nolan', 'directed_by_reverse', 'movie_1')
# ('actor_dicaprio', 'has_actor_reverse', 'movie_1')
```

### Building Knowledge Graph from Relational Database

```python
import sqlite3
from build_kg_example import KnowledgeGraphBuilder

# Connect to database
conn = sqlite3.connect('movie_database.db')

# Extract movie-director relationships
query_director = """
SELECT m.movie_id, d.director_id 
FROM movies m 
JOIN directors d ON m.director_id = d.id
"""
df_director = pd.read_sql_query(query_director, conn)

# Extract movie-actor relationships
query_actor = """
SELECT m.movie_id, a.actor_id 
FROM movies m 
JOIN movie_actors ma ON m.id = ma.movie_id
JOIN actors a ON ma.actor_id = a.id
"""
df_actor = pd.read_sql_query(query_actor, conn)

# Build triples
triples = []
for _, row in df_director.iterrows():
    triples.append((f"movie_{row['movie_id']}", 'directed_by', f"director_{row['director_id']}"))

for _, row in df_actor.iterrows():
    triples.append((f"movie_{row['movie_id']}", 'has_actor', f"actor_{row['actor_id']}"))

# Generate knowledge graph files
builder = KnowledgeGraphBuilder('movie_db', './dataset')
builder.build_kg_triples(triples)
```

---

## Reference Resources

1. **RecBole Official Documentation**: https://recbole.io/docs/
2. **Knowledge-aware Recommendation Quick Start**: https://recbole.io/docs/user_guide/usage/running_new_dataset.html
3. **Data Format Specification**: https://recbole.io/docs/user_guide/data_intro.html
4. **GitHub Repository**: https://github.com/RUCAIBox/RecBole
5. **Paper**: RecBole: Towards a Unified, Comprehensive and Efficient Framework for Recommendation Algorithms

---

## Contributing

If you find issues or have suggestions during use, please:
- Submit Issue: https://github.com/RUCAIBox/RecBole/issues
- Submit Pull Request
- Participate in discussions

---

## License

This project is open source under the MIT License.

---

**Last Updated**: December 2024
**Maintainer**: RecBole Team
