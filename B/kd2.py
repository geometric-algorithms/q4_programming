# KD-Tree Node
class KDNode:
    def __init__(self, point=None, left=None, right=None, region=None, axis=0):
        self.point = point          # Coordinates of the point
        self.left = left            # Left child
        self.right = right          # Right child
        self.axis = axis            # Splitting axis: 0 for x, 1 for y
        self.region = region        # Bounding box of the region

# Build KD-Tree recursively
def build_kd_tree(px, py, depth=0, region=(float('-inf'), float('inf'), float('-inf'), float('inf'))):
    if not px:
        return None
    if len(px) == 1:
        return KDNode(point=px[0], region=region, axis=depth % 2)

    axis = depth % 2  # Alternate axis: 0 -> x, 1 -> y

    if axis == 0:
        median_idx = len(px) // 2
        median_point = px[median_idx]
        split = median_point[0]

        # Partition points based on x-axis
        left_px = [p for p in px if p[0] < split]
        right_px = [p for p in px if p[0] >= split and p != median_point]
        left_py = [p for p in py if p[0] < split]
        right_py = [p for p in py if p[0] >= split and p != median_point]

        left_region = (region[0], split, region[2], region[3])
        right_region = (split, region[1], region[2], region[3])
    else:
        median_idx = len(py) // 2
        median_point = py[median_idx]
        split = median_point[1]

        # Partition points based on y-axis
        left_py = [p for p in py if p[1] < split]
        right_py = [p for p in py if p[1] >= split and p != median_point]
        left_px = [p for p in px if p[1] < split]
        right_px = [p for p in px if p[1] >= split and p != median_point]

        left_region = (region[0], region[1], region[2], split)
        right_region = (region[0], region[1], split, region[3])

    # Recursively build subtrees
    left = build_kd_tree(left_px, left_py, depth + 1, left_region)
    right = build_kd_tree(right_px, right_py, depth + 1, right_region)

    return KDNode(point=median_point, left=left, right=right, region=region, axis=axis)

# Check if point lies inside rectangle
def in_rectangle(point, rect):
    x, y = point
    xmin, xmax, ymin, ymax = rect
    return xmin <= x <= xmax and ymin <= y <= ymax

# Check if region completely inside query rectangle
def region_inside(region, rect):
    rxmin, rxmax, rymin, rymax = region
    xmin, xmax, ymin, ymax = rect
    return (xmin <= rxmin <= rxmax <= xmax) and (ymin <= rymin <= rymax <= ymax)

# Check if region overlaps with query rectangle
def region_overlap(region, rect):
    rxmin, rxmax, rymin, rymax = region
    xmin, xmax, ymin, ymax = rect
    return not (rxmax < xmin or rxmin > xmax or rymax < ymin or rymin > ymax)

# Collect all points in subtree
def report_subtree(node, result):
    if node is None:
        return
    result.append(node.point)
    report_subtree(node.left, result)
    report_subtree(node.right, result)

# Search for points in a given rectangle
def search_kd_tree(node, rect, result):
    if node is None:
        return
    if in_rectangle(node.point, rect):
        result.append(node.point)

    # Recur on children if needed
    if node.left:
        if region_inside(node.left.region, rect):
            report_subtree(node.left, result)
        elif region_overlap(node.left.region, rect):
            search_kd_tree(node.left, rect, result)

    if node.right:
        if region_inside(node.right.region, rect):
            report_subtree(node.right, result)
        elif region_overlap(node.right.region, rect):
            search_kd_tree(node.right, rect, result)

# Insert point into KD-Tree
def insert_kd_tree(node, point, depth=0, region=(float('-inf'), float('inf'), float('-inf'), float('inf'))):
    if node is None:
        return KDNode(point=point, region=region, axis=depth % 2)

    axis = node.axis
    # Decide direction and compute sub-region
    if point[axis] < node.point[axis]:
        if axis == 0:
            left_region = (region[0], node.point[0], region[2], region[3])
        else:
            left_region = (region[0], region[1], region[2], node.point[1])
        node.left = insert_kd_tree(node.left, point, depth + 1, left_region)
    else:
        if axis == 0:
            right_region = (node.point[0], region[1], region[2], region[3])
        else:
            right_region = (region[0], region[1], node.point[1], region[3])
        node.right = insert_kd_tree(node.right, point, depth + 1, right_region)

    return node

# Delete point from KD-Tree
def delete_kd_tree(node, point, depth=0):
    if node is None:
        return None

    axis = depth % 2

    if node.point == point:
        # Replace with min from right or left
        if node.right:
            min_node = find_min(node.right, axis, depth + 1)
            node.point = min_node.point
            node.right = delete_kd_tree(node.right, min_node.point, depth + 1)
        elif node.left:
            min_node = find_min(node.left, axis, depth + 1)
            node.point = min_node.point
            node.right = delete_kd_tree(node.left, min_node.point, depth + 1)
            node.left = None
        else:
            return None
    elif point[axis] < node.point[axis]:
        node.left = delete_kd_tree(node.left, point, depth + 1)
    else:
        node.right = delete_kd_tree(node.right, point, depth + 1)

    return node

# Find node with minimum value in given axis
def find_min(node, axis, depth=0):
    if node is None:
        return None

    current_axis = depth % 2

    if current_axis == axis:
        if node.left is None:
            return node
        return find_min(node.left, axis, depth + 1)

    # Compare current, left, right
    left_min = find_min(node.left, axis, depth + 1)
    right_min = find_min(node.right, axis, depth + 1)
    candidates = [n for n in (node, left_min, right_min) if n is not None]
    return min(candidates, key=lambda n: n.point[axis])

# Print KD-Tree structure
def print_kd_tree(node, depth=0):
    if node is None:
        return
    indent = "  " * depth
    print(f"{indent}Depth {depth}, Axis {node.axis}, Point {node.point}, Region {node.region}")
    if node.left:
        print(f"{indent}L:")
        print_kd_tree(node.left, depth + 1)
    if node.right:
        print(f"{indent}R:")
        print_kd_tree(node.right, depth + 1)

# === MAIN PROGRAM ===
def main():
    n = int(input("Enter number of points: "))
    points = []
    for _ in range(n):
        x, y = map(float, input("Enter point (x y): ").split())
        points.append((x, y))

    # Sort by x and y
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    kd_tree = build_kd_tree(px, py)

    # print("\nKD-Tree built successfully.\n")
    # print_kd_tree(kd_tree)

    while True:
        op = input("\nChoose operation (insert, delete, search, stop): ").strip().lower()

        if op == "insert":
            x, y = map(float, input("Enter point to insert (x y): ").split())
            kd_tree = insert_kd_tree(kd_tree, (x, y))
            print("Point inserted.")
            # print_kd_tree(kd_tree)

        elif op == "delete":
            x, y = map(float, input("Enter point to delete (x y): ").split())
            kd_tree = delete_kd_tree(kd_tree, (x, y))
            print("Point deleted.")
            # print_kd_tree(kd_tree)

        elif op == "search":
            xmin, xmax, ymin, ymax = map(float, input("Enter rectangle (xmin xmax ymin ymax): ").split())
            result = []
            search_kd_tree(kd_tree, (xmin, xmax, ymin, ymax), result)
            print("Search results:", sorted(result))

        elif op == "stop":
            print("Exiting program.")
            break

        else:
            print("Invalid operation. Please try again.")

if __name__ == "__main__":
    main()
