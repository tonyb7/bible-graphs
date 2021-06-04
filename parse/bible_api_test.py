import free_bible_api

def bible_api_test():
    free_bible_api.set_bible("rsv.xml")
    print("Gen.5.4:", free_bible_api.text_from_osisID("Gen.5.4"))

    filename = '../cross_references.txt'
    with open(filename) as file:
        versesRead = 0
        for i, line in enumerate(file):
            if i % 50 != 1:
                continue 
            osisVerse = line.split()[0]
            print(f"{osisVerse}: {free_bible_api.text_from_osisID(osisVerse)}")

            versesRead += 1
            if versesRead > 20:
                break

if __name__ == '__main__':
    bible_api_test()

