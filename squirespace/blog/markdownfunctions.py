from django.utils import html
import CommonMark
from HTMLParser import HTMLParser

def markdown_unescape(markdown):
	#pus proper markdown <code> tags instead of &gt, allowing 
	#markdown to be applied, which translates and returns markdown
	#text
	temp_markdown=markdown
	#parse to decode markdown
	parse_markdown=HTMLParser()
	#split commonmark tags
	temp_markdown=temp_markdown.split('<')
	#set up begining and ending so that you can tell where to
	#append the code tags for "unescaping"
	begin=0
	end=0
	unescape_content=[]
	for text in temp_markdown:
		#deal with the begining and ending code tags, and its decoding
		if text.replace(' ','').startswith('code>'):
			begin+=1
		if text.replace(' ','').startswith('/code>'):
			end+=1
		#this below code will take into account whether you are in a code
		#tag or not
		if begin>end:
			unescape_content.append(parser.unescape(text))
		else:
			unescape_content.append(text)
	#return all the stuff joined together
	return '<'.join(unescape_content)



def markdown_stuff(text, markdown):
	#checks for block content then escapes content to another 
	#function before applying and returning markdowned content.
	#If not just replace the new line comment with a linebreak 
	#to make it markdown

	clean=html.conditional_escape(text)
	if markdown:
		#markdown block quotes
		new_markdown=clean.replace('&gt;', '>')
		new_markdown=CommonMark.commonmark(new_markdown)
		markdown_text=markdown_unescape(new_markdown)
		return markdown_text.replace('\n', '<br/>')
	return clean.replace('\n','<br/>')