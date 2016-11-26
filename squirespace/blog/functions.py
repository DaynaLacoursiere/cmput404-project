from django.utils import html
import CommonMark


def markdown_stuff(contentType, markdown):
	clean=html.conditional_escape(contentType)
	if markdown:
		new_markdown=clean.replace('&gt;', '>')
		new_markdown=CommonMark.commonmark(new_markdown)