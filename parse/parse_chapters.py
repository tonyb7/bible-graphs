
def main():
    filename = '../cross_references.txt'
    chapter_maxlen = 20

    chapterset = set()
    chapterlist = []
    with open(filename) as file:
        for chapter in map(lambda l: l.split('.')[0], file):
            if chapter not in chapterset and len(chapter) < chapter_maxlen:
                chapterlist.append(chapter)
                chapterset.add(chapter)

    for chapter in chapterlist:
        print(chapter)

if __name__ == '__main__':
    main()


