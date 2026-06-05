# Vector Database Operations

## Collection Lifecycle

| Phase | Activities |
|-------|-----------|
| Design | Schema definition, dimension selection, distance metric (cosine, euclidean, dot), index type selection |
| Create | Collection provisioning, index creation, partition configuration, alias setup |
| Ingest | Batch loading, streaming ingestion, data validation, consistency verification |
| Maintain | Index rebuilding, compaction, collection health monitoring, performance tuning |
| Migrate | Dimension changes, index type changes, cluster migration, data reindexing |
| Decommission | Data archival, collection backup, alias reassignment, collection drop |

## Index Type Selection

| Index Type | Best for | Tradeoffs |
|-----------|----------|-----------|
| IVF_FLAT | Balanced accuracy/speed | Higher memory, good recall |
| HNSW | High-recall, large datasets | Higher memory, slower build |
| IVF_SQ8 | Memory-efficient | Lower recall than IVF_FLAT |
| FLAT | Exact search, small datasets | O(n) search, exact recall |

## Migration Patterns

| Scenario | Approach |
|----------|----------|
| Dimension change | Create new collection with target dimension, dual-write during migration, batch reindex old data, swap alias |
| Index type change | Online index rebuild if supported, otherwise parallel collection with dual-write |
| Cluster migration | Backup → restore on target, validate row counts and sample queries, cut over via alias |
| Embedding model change | Full reindex: read source → generate new embeddings → write to new collection → verify → swap |
