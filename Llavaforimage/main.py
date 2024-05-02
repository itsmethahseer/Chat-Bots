from llava import ImageAssistant

def main():
    assistant = ImageAssistant()
    url = "https://d2slcw3kip6qmk.cloudfront.net/marketing/blog/2019Q2/workflow/content-approval-workflow-example.png"
    response = assistant.process_image_and_generate_response(url)
    print(response)

if __name__ == "__main__":
    main()
