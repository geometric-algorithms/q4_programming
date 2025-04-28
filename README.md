# KD-Tree for Range Queries and Dynamic Updates

## Problem Description

Given a set of points in 2D space (ℝ²), the goal is to:

- (a) Build a **static KD-Tree** to support efficient **orthogonal range queries**.
- (b) Extend the KD-Tree to support **dynamic updates** (insertions and deletions) along with range queries.

### Requirements:

- **Preprocessing time**: **O(n log n)**
- **Query time**: **O(√n + k)**, where `k` is the number of reported points.

---

## Implementation Details

### Part A: Static KD-Tree
- The tree is built recursively by sorting points along the x and y axes.
- **Median points** are used for splitting and are stored in the right subtree and points are stored in leaf nodes.
- Range queries efficiently prune subtrees based on region containment and overlap.
  
### Part B: Dynamic KD-Tree
- Supports **insertion**, **deletion**, and **range queries**.
- **Median points are used for splitting** and **stored at internal nodes** to maintain the tree structure.
- **Insertion and deletion operations** are implemented to update the tree dynamically while maintaining its balance based on the splitting axis.

---

## Files

| File     | Description |
| -------- | ----------- |
| `kd.py`  | Static KD-Tree for orthogonal range queries. |
| `kd2.py` | Dynamic KD-Tree with insertion, deletion, and range queries. |

---

## Running Instructions

### Part A - Static KD-Tree

1. **Give execute permission to the `test.sh` script**:

    ```bash
    chmod +x test.sh
    ```

2. **Run the `test.sh` script** to interact with the static KD-Tree:

    ```bash
    ./test.sh
    ```

    The script will:

    - Prompt you to input the number of points and their coordinates (in the format: `x y`).
    - Allow you to enter rectangle queries in the format: `xmin xmax ymin ymax`.
    - Type `stop` to exit the program.

### Part B - Dynamic KD-Tree

1. **Give execute permission to the `test.sh` script**:

    ```bash
    chmod +x test.sh
    ```

2. **Run the `test.sh` script** to interact with the dynamic KD-Tree:

    ```bash
    ./test.sh
    ```
    The script will:

    - Prompt you to input the number of points and their coordinates (in the format: `x y`).
    
    - **Choose an operation**: After building the KD-Tree, you can choose from the following operations:
      - **Insert**: Add a new point to the tree.
      - **Delete**: Remove a point from the tree.
      - **Search**: Search for points within a rectangular region.
      - **Stop**: Exit the program.

