from langchain import FAISS
from langchain.document_loaders import PyPDFium2Loader
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import pypdfium2 as pdfium
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from config_app.config import get_config

config_app = get_config()
# embeddings = HuggingFaceEmbeddings(model_name=config_app["parameter"]["embeddings_name"],
#                                        model_kwargs={'device': 'cpu'})
embeddings = OpenAIEmbeddings(openai_api_key="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")

def download_and_index_pdf(urls: list[str]) -> FAISS:
    """
    Download and index a list of PDFs based on the URLs
    """

    def __update_metadata(pages, url):
        """
        Add to the document metadata the title and original URL
        """
        for page in pages:
            pdf = pdfium.PdfDocument(page.metadata['source'])
            title = pdf.get_metadata_dict().get('Title', url)
            page.metadata['source'] = url
            page.metadata['title'] = title
        return pages

    all_pages = []
    for url in urls:
        loader = PyPDFium2Loader(url)
        splitter = CharacterTextSplitter(chunk_size=config_app["parameter"]["chunk_size"], chunk_overlap=config_app["parameter"]["chunk_overlap"])
        pages = loader.load_and_split(splitter)
        pages = __update_metadata(pages, url)
        all_pages += pages

    return all_pages

def download_and_index_QA(urls: list[str]) -> FAISS:
    loader = DirectoryLoader(urls, glob="**/*txt")
    print(loader)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=config_app["parameter"]["chunk_size"], chunk_overlap=config_app["parameter"]["chunk_overlap"])
    texts_QA = text_splitter.split_documents(documents)
    return texts_QA

def download_and_index_pdf_1(urls: list[str]) -> FAISS:
    """
    Download and index a list of PDFs based on the URLs
    """

    loader = DirectoryLoader("./data/pdf/",
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=config_app["parameter"]["chunk_size"], chunk_overlap=config_app["parameter"]["chunk_overlap"])
    all_pages = text_splitter.split_documents(documents)

    return all_pages


session_urls = ["./data/pdf/Quy trinh.pdf"]
all_pages = download_and_index_pdf_1(session_urls)

urls = "./data/QA/"
texts_QA = download_and_index_QA(urls)

texts = all_pages + texts_QA

faiss_index = FAISS.from_documents(all_pages, embeddings)
faiss_index.save_local(config_app["parameter"]["DB_FAISS_PATH"])