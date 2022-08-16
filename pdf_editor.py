import argparse
import os
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter


def get_information(path):
    pdf = PdfFileReader(path)
    information = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()

    info = f"""
        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {number_of_pages}
    """

    print(info)
    return info


def rotate(path, page, angle):
    writer = PdfFileWriter()
    reader = PdfFileReader(path)

    try: 
        angle = int(angle)
    except:
        print("Angle must be an integer")
        sys.exit(1)
    if angle not in [90, 180, 270]:
        print("Angle must be 90, 180, or 270")
        sys.exit(1)
    
    try:
        if page == 'all':
            for p in range(reader.getNumPages()):
                writer.addPage(reader.getPage(p).rotateClockwise(angle))
        else:
            try:
                page = int(page) - 1
                for p in range(reader.getNumPages()):
                    if p == int(page):
                        writer.addPage(reader.getPage(p).rotateClockwise(angle))
                    else:
                        writer.addPage(reader.getPage(p))
            except:
                raise Exception("Page must be 'all' or an integer")
    
    except Exception as e:
        print(e)
        sys.exit(1)
    
    with open(path[:-4] + '_rotated.pdf', "wb") as output:
        writer.write(output)


def merge(paths):
    
    for path in paths:
        if not os.path.isfile(path):
            print(f"{path} is not a file")
            sys.exit(1)

    writer = PdfFileWriter()
    for path in paths:
        reader = PdfFileReader(path)
        for p in range(reader.getNumPages()):
            writer.addPage(reader.getPage(p))
    
    with open(paths[0][:-4] + '_merged.pdf', "wb") as output:
        writer.write(output)


def split(path, page, output_dir):
    reader = PdfFileReader(path)

    try:
        page = int(page)
    except:
        print("Page must be an integer")
        sys.exit(1)
    writer = PdfFileWriter()
    for p in range(page):
        writer.addPage(reader.getPage(p))   
    with open(os.path.join(output_dir, f"split_1.pdf"), "wb") as output:
        writer.write(output)

    writer = PdfFileWriter()
    for p in range(page, reader.getNumPages()):
        print(p)
        writer.addPage(reader.getPage(p))
    with open(os.path.join(output_dir, f"split_2.pdf"), "wb") as output:
        writer.write(output)


def protect(path, password):
    writer = PdfFileWriter()
    reader = PdfFileReader(path)

    for p in range(reader.getNumPages()):
        writer.addPage(reader.getPage(p))
    
    writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)

    with open(path[:-4] + '_protected.pdf', "wb") as output:
        writer.write(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get information from pdf')
    parser.add_argument('path', help='Path to pdf')
    parser.add_argument('method', help='Choose which operation you want to perform', 
        choices=['info', 'rotate', 'merge', 'split', 'protect'])
    parser.add_argument('options', help='Options for the operation', nargs='*')

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f'{args.path} does not exist')
        sys.exit(1)

    if args.method == 'info':
        # ex. pdf_editor.py path info
        get_information(args.path)
    elif args.method == 'rotate':
        # ex. python pdf_editor.py path/to/pdf rotate all/int 180
        rotate(args.path, args.options[0], args.options[1])
    elif args.method == 'merge':
        # ex. python pdf_editor.py path/to/pdf merge path/to/pdf path/to/pdf
        merge([args.path] + args.options)
    elif args.method == 'split':
        # ex. python pdf_editor.py path/to/pdf split int output_dir
        split(args.path, args.options[0], args.options[1])
    elif args.method == 'protect':
        # ex. python pdf_editor.py path/to/pdf protect password
        protect(args.path, args.options[0])
    else:
        print('Invalid method')
        sys.exit(1)

