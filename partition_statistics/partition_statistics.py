import os
import sys
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt

def analyze_partition(path, type="pie", max_extension = 10):
    number_of_dirs = 0
    number_of_files = 0
    file_types_to_count = defaultdict(int)  #{".txt": 3,"no_extension": 1 , ".jpg": 2}
    file_types_to_bytes = defaultdict(int)  #{".txt": 30000,"no_extension": 20000 , ".jpg": 1000}

    for root, dirs, files in os.walk(path):
        number_of_dirs += len(dirs)
        for file in files:
            full_file_path = os.path.join(root, file)
            number_of_files += 1
            try:
                file_size = os.path.getsize(full_file_path)
                extension = os.path.splitext(file)[1]
                if not extension:
                 extension = "no_extension"
                file_types_to_count[extension] += 1
                file_types_to_bytes[extension] += file_size
            except (OSError, FileNotFoundError) as e :
                print(f"Error at {full_file_path}: {e}")
                continue

    sorted_file_types_to_count = OrderedDict(
        sorted(file_types_to_count.items(), key=lambda x: x[1], reverse=True)
    )
    sorted_file_types_to_bytes = OrderedDict(
        sorted(file_types_to_bytes.items(), key=lambda x: x[1], reverse=True)
    )
    generate_charts(number_of_files, number_of_dirs, sorted_file_types_to_count, sorted_file_types_to_bytes, type, max_extension)

def limit_extensions(file_types_to_count, file_types_to_bytes, max_extensions):
    top_extensions_count = list(file_types_to_count.items())[:max_extensions]
    top_extensions_bytes = list(file_types_to_bytes.items())[:max_extensions]

    other_count = sum(count for _, count in list(file_types_to_count.items())[max_extensions:])
    other_bytes = sum(size for _, size in list(file_types_to_bytes.items())[max_extensions:])

    top_extensions_count.append(('Other extensions', other_count))
    top_extensions_bytes.append(('Other extensions', other_bytes))

    limited_file_types_to_count = OrderedDict(top_extensions_count)
    limited_file_types_to_bytes = OrderedDict(top_extensions_bytes)

    #other extensions
    print("The other extensions: ")
    print(list(file_types_to_count.items())[max_extensions:])

    return limited_file_types_to_count, limited_file_types_to_bytes


def generate_charts(total_files, total_dirs, file_types_count, file_types_size, type, max_extension =10):
      # create a limit
    if len(file_types_count) > max_extension:
        limited_file_types_to_count, limited_file_types_to_bytes = limit_extensions(file_types_count, file_types_size, max_extension)
        extensions = list(limited_file_types_to_count.keys())
        counts = list(limited_file_types_to_count.values())
        sizes = list(limited_file_types_to_bytes.values())
    else:
        extensions = list(file_types_size.keys())
        counts = list(file_types_count.values())
        sizes = list(file_types_size.values())


    if type == "pie":
        # 2 subplots for pie chars
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.subplots_adjust(left=0.3, right=0.9)  # legend fix
        fig.suptitle(f'Total dirs: {total_dirs}  Total files : {total_files}', fontsize=10)
        # theme
        theme = plt.get_cmap('tab20')
        colors = [theme(1.0 * i / len(counts)) for i in range(len(counts))]

        # Pie for counts
        ax1.set_prop_cycle("color", colors)
        ax1.pie(counts, startangle=90)
        ax1.axis('equal')
        ax1.set_title("File types by Count")

        # Pie for sizes
        ax2.set_prop_cycle("color", colors)
        ax2.pie(sizes, startangle=90)
        ax2.axis('equal')
        ax2.set_title("File types by Size")

        # legend
        total_count = sum(counts)
        total_size = sum(sizes)
        count_legend_labels = [
            f'{l}: {count / total_count:.1%}'
            for l, count in zip(extensions, counts)
        ]
        size_legend_labels = [
            f'{l}: {size / total_size:.1%}'
            for l, size in zip(extensions, sizes)
        ]

        fig.legend(
            labels=count_legend_labels,
            loc='center left',
            bbox_to_anchor=(0.0, 0.75),  # position
            prop={'size': 10},
            title="Ordered by descending counts"
        )
        fig.legend(
            labels=size_legend_labels,
            loc='center left',
            bbox_to_anchor=(0.0, 0.25),
            prop={'size': 10},
            title="Ordered by descending sizes in bytes"
        )

        plt.show()

    elif type == "bar":
        fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 7))
        fig.suptitle(f'Total dirs: {total_dirs}  Total files : {total_files}', fontsize=10)
        ax3.bar(extensions, counts, color='red')
        ax3.set_xlabel("Extensions")
        ax3.set_ylabel("Count")
        ax3.set_title("Number of files by extensions")
        ax3.tick_params(axis='x', rotation=45)

        ax4.bar(extensions, sizes, color='green')
        ax4.set_xlabel("Extensions")
        ax4.set_ylabel("Bytes")
        ax4.set_title("Total Size by File Type")
        ax4.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

    elif type == "line":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

        ax1.plot(extensions, counts, marker='o', color='blue')
        ax1.set_xlabel("Extensions")
        ax1.set_ylabel("Count")
        ax1.set_title("Number of Files by extension")
        ax1.tick_params(axis='x', rotation=45)

        ax2.plot(extensions, sizes, marker='o', color='green')
        ax2.set_xlabel("File Types")
        ax2.set_ylabel("Size in bytes")
        ax2.set_title("Total Size by File Type")
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

    elif type:
        print("Not a supported type of chart. Available: pie, bar")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        analyze_partition(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) == 3:
        analyze_partition(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        analyze_partition(sys.argv[1])
    else:
        print("Incorrect usage, try: python Main1.py <partition_path> [chart_type] [Limit of extensions]")

