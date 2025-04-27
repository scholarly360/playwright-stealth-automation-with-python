
import os
from helper_utils import *
from dotenv import load_dotenv
load_dotenv()


urls = read_urls_from_file("custom_urls.txt")
browse_and_print(urls)