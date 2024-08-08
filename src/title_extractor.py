
def extract_title(markdown):
    split_list = markdown.split("\n")
    extracted_title = []
    for line in split_list:
        if line[:2] == "# ":
            extracted_title.append(line)
    if len(extracted_title) == 0:
        raise Exception("No header in markdown file")

    remove_hash = list(map(lambda a: a[2:].strip(), extracted_title))

    return "\n".join(remove_hash)
