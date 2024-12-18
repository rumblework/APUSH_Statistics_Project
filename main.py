# import pandas as pan
# import matplotlib as m
import urllib.request as req
import PyPDF2 as p
import io

linkData = []
linkDataHTML = []

def testfunc1():
    fileData = open("urls").readlines() #array for all apush pdfs
    pdfLinkData = [] #array for link data
    print(fileData[0])
    with open("output", "tw") as outputFile:
        print(fileData[0], file=outputFile)
    for url in fileData:
        pdfLinkData.append(p.PdfReader(io.BytesIO(req.urlopen(req.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read())))
        # linkData.append(req.urlopen(req.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read())
    #linkDataHTML.append(linkData[1].decode("utf-8"))
    with open("output", "ta") as outputFile:
        print(pdfLinkData[0], file=outputFile)
    print(pdfLinkData[0])
    #print(linkDataHTML[0])#cant decode some of the bytes


def testfunc3():
    fileData = open("urls").readlines()  # array for all PDF URLs
    pdfLinkData = []  # array for loaded PDF data
    print(fileData[0])  # Print the first URL (for debugging)

    with open("output", "w") as outputFile:  # Write output to file
        print(fileData[0], file=outputFile)

    for url in fileData:
        try:
            # Request the PDF file from the URL and read it into a PDF reader
            pdf_response = req.urlopen(
                req.Request(url.strip(), headers={"User-Agent": "Mozilla/5.0"})
            ).read()
            pdf_reader = p.PdfReader(io.BytesIO(pdf_response))
            pdfLinkData.append(pdf_reader)

            # Optional: Extract text from the first page for demonstration
            if pdf_reader.pages:
                first_page_text = pdf_reader.pages[0].extract_text().encode("utf-8")
                with open("output", "a") as outputFile:
                    print(f"First page text from {url.strip()}:", file=outputFile)
                    print(first_page_text, file=outputFile)

                print(
                    f"Successfully retrieved PDF from {url.strip()} with content:",
                    first_page_text,
                )

        except Exception as e:
            print(f"Error processing URL {url.strip()}: {e}")

    # No need for additional linkDataHTML usage here



def testfunc2():
    fileData = open("urls").readlines() #array for all apush pdfs

    print(fileData[0])
    with open("output", "tw") as outputFile:

        for url in fileData:
            linkDataHTML.append(q.PDFQuery(url))


    # Use CSS-like selectors to locate the elements
    # text_elements = pdf.pq('LTTextLineHorizontal')

    # Extract the text from the elements
    # text = [t.text for t in text_elements]

    # print(text)

def main():
    # testfunc1()
    # testfunc2()
    testfunc3()


main()
