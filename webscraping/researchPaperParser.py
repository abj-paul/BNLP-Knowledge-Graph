import scipdf
MINIMUM_TITLE_LENGTH = 20
article_dict = scipdf.parse_pdf_to_dict('example_data/futoma2017improved.pdf') # return dictionary
 
article_dict = scipdf.parse_pdf_to_dict('./data/Anaphora Resolution And Bangla/Paper_1.pdf', as_list=False)
for index, reference in enumerate(article_dict["references"]):
    if len(reference["title"])>MINIMUM_TITLE_LENGTH:
        print(f"{index}) {reference['title']}")
