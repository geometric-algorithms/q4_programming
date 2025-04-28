import sys

# Node class for KD-tree
class KDNode:
    def __init__(self, axis=None, split=None, left=None, right=None, point=None, region=None):
        self.axis = axis          # Splitting axis: 0 for x, 1 for y
        self.split = split        # Split value on the axis
        self.left = left          # Left child
        self.right = right        # Right child
        self.point = point        # Leaf node stores a point
        self.region = region      # Bounding region of the node

# Recursively build KD-tree
def build_kd_tree(px, py, depth=0, region=(float('-inf'), float('inf'), float('-inf'), float('inf'))):
    if not px:
        return None
    if len(px) == 1:
        return KDNode(point=px[0], region=region)

    axis = depth % 2  # Alternate between x and y
    
    # Partition points based on axis
    if axis == 0:
        median_idx = len(px) // 2
        median_point = px[median_idx]
        split = median_point[axis]
        left_px = [p for p in px if p[0] < split]
        right_px = [p for p in px if p[0] >= split]
        left_py = [p for p in py if p[0] < split]
        right_py = [p for p in py if p[0] >= split]
        left_region = (region[0], split, region[2], region[3])
        right_region = (split, region[1], region[2], region[3])
    else:
        median_idx = len(py) // 2
        median_point = py[median_idx]
        split = median_point[axis]
        left_px = [p for p in px if p[1] < split]
        right_px = [p for p in px if p[1] >= split]
        left_py = [p for p in py if p[1]<split]
        right_py = [p for p in py if p[1]>=split]
        left_region = (region[0], region[1], region[2], split)
        right_region = (region[0], region[1], split, region[3])

    # Recursively build children
    left = build_kd_tree(left_px, left_py, depth + 1, left_region)
    right = build_kd_tree(right_px, right_py, depth + 1, right_region)

    return KDNode(axis=axis, split=split, left=left, right=right, region=region)

# Check if point is inside rectangle
def in_rectangle(point, rect):
    x, y = point
    xmin, xmax, ymin, ymax = rect
    return xmin <= x <= xmax and ymin <= y <= ymax

# Check if a region is fully inside a rectangle
def region_inside(region, rect):
    rxmin, rxmax, rymin, rymax = region
    xmin, xmax, ymin, ymax = rect
    return (xmin <= rxmin and rxmax <= xmax and ymin <= rymin and rymax <= ymax)

# Check if region overlaps with rectangle
def region_overlap(region, rect):
    rxmin, rxmax, rymin, rymax = region
    xmin, xmax, ymin, ymax = rect
    return not (rxmax < xmin or rxmin > xmax or rymax < ymin or rymin > ymax)

# Collect all points in a subtree
def report_subtree(node, result):
    if node is None:
        return
    if node.point is not None:
        result.append(node.point)
    else:
        report_subtree(node.left, result)
        report_subtree(node.right, result)

# Query KD-tree for points in rectangle
def search_kd_tree(node, rect, result):
    if node is None:
        return
    if node.point is not None:
        if in_rectangle(node.point, rect):
            result.append(node.point)
        return
    # Recurse if region is inside or overlaps with query rect
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

# print KD-tree
def print_kd_tree(node, depth=0):
    indent = "  " * depth
    if node is None:
        print(f"{indent}Empty")
        return
    if node.point is not None:
        print(f"{indent}Leaf: point={node.point}, region={node.region}")
    else:
        axis_name = 'x' if node.axis == 0 else 'y'
        print(f"{indent}Node: split {axis_name} = {node.split}, region={node.region}")
        print(f"{indent}Left:")
        print_kd_tree(node.left, depth + 1)
        print(f"{indent}Right:")
        print_kd_tree(node.right, depth + 1)

# Main driver
def main():
    try:
        n = int(input("Enter number of points: "))
        points = []
        for i in range(n):
            while True:
                try:
                    x, y = map(float, input(f"Point {i + 1} (format: x y): ").strip().split())
                    points.append((x, y))
                    break
                except:
                    print("Invalid input. Please enter two numbers separated by space.")
        # Sort points by x and y
        px = sorted(points, key=lambda p: p[0])
        py = sorted(points, key=lambda p: p[1])
        kd_tree = build_kd_tree(px, py)
        # print("\nKD-tree structure:")
        # print_kd_tree(kd_tree)

        print("\nNow enter query rectangles as: xmin xmax ymin ymax")
        print("Type 'stop' to end.")
        while True:
            query_input = input("Query rectangle: ").strip()
            if query_input.lower() == 'stop':
                print("Exiting...")
                break
            try:
                xmin, xmax, ymin, ymax = map(float, query_input.split())
                rect = (xmin, xmax, ymin, ymax)
                result = []
                search_kd_tree(kd_tree, rect, result)
                print("Query result:", sorted(result))
            except:
                print("Invalid query. Format: xmin xmax ymin ymax")

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
