from django.utils import html
import CommonMark
from HTMLParser import HTMLParser

def markdown_escape(markdown):
	#pus proper markdown <code> tags instead of &gt, allowing 
	#markdown to be applied, which translates and returns markdown
	#text
	temp_markdown=markdown

	#parse to decode markdown
	parse_markdown=HTMLParser()
	#split commonmark tags
	temp_markdown=temp_markdown.split('<')



def markdown_stuff(contentType, markdown):
	#checks for block content then escapes content to another 
	#function before applying and returning markdowned content.
	#If not just replace the new line comment with a linebreak 
	#to make it markdown

	clean=html.conditional_escape(contentType)
	if markdown:
		#markdown block quotes
		new_markdown=clean.replace('&gt;', '>')
		new_markdown=CommonMark.commonmark(new_markdown)
		markdown_text=markdown_escape(new_markdown)
		return markdown_text.replace('\n', '<br/>')
	return clean.replace('\n','<br/>')