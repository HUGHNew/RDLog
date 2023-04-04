import os, shutil

def get_date_str(filename:str) -> str:
    """assume filename: year-month-day-xxxxxx.md
    e.g. 2022-11-11-first.md
    22-1-1-first.md
    """
    filename = os.path.basename(filename)
    parts = filename.split('-', 3)[:-1]
    return f"date: {'-'.join(parts)}T00:00:00+08:00\n"

def convert_old_tags_and_cates(line:str) -> str:
    parts = line.strip().split(' ')
    name = parts[0]
    tag_list = ", ".join([
        f'"{tag}"'
        for tag in parts[1:]
    ])
    return f"{name} [{tag_list}]\n"

def process_front_matter(lines: list[str], f:str,
                         reverse_tag_and_category:bool=True, add_headless:bool=True) -> list[str]:
    """
    drop old layout
    add date
    convert old tags and categories
    """
    date = get_date_str(f)
    result = ["---\n"]
    tag, cate = "", ""
    for line in lines:
        if "tag" in line:
            tag = convert_old_tags_and_cates(line)
        elif "categories" in line:
            cate = convert_old_tags_and_cates(line)
        elif "layout:" in line:
            result.append("layout: search\n")
        else:
            result.append(line)
    if reverse_tag_and_category:
        tag = tag.replace("tags", "categories")
        cate = cate.replace("categories", "tags")
    result.append(tag)
    result.append(cate)
    result.append(date)
    if add_headless:
        result.append("headless: true\n")
    result.append("---\n")
    return result

def replace_image(line:str) -> str:
    return line.replace("]({{site.baseurl}}/assets/", "](")

def process_body(lines: list[str]) -> list[str]:
    pipelines = [
        replace_image
    ]
    def call_pipes(s:str) -> str:
        rel = s
        for pipe in pipelines:
            rel = pipe(rel)
        return rel
    result = [
        call_pipes(line)
        for line in lines
    ]
    return result

def tranverse(dir:str, cut_files:bool=True):
    for file in os.listdir(dir):
        if file.endswith(".md"):
            file = os.path.join(dir, file)
            with open(file) as fd:
                content = fd.readlines()
            front_matter_end = 0
            for i in range(1, len(content)):
                if content[i] == "---\n": # formatter ends
                    front_matter_end = i
                    break
            others = content[front_matter_end+1:]
            front_matter = content[1:front_matter_end]

            front_matter = process_front_matter(front_matter, file)
            body = process_body(others)
            with open(file, "w") as fd:
                fd.writelines(front_matter)
                fd.writelines(body)
        if cut_files:
            split = file.split('-', 3)
            mkd = "-".join(split[:-1])
            os.makedirs(mkd, exist_ok=True)
            nf = os.path.join(mkd, split[-1])
            shutil.move(file, nf)

if __name__ == "__main__":
    tranverse("content/post")
