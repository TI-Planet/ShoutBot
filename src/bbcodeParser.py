import bbcode
import html

class bbcodeParser:
	def __init__(self):
		self.init_bbcode2markdown()

	def init_bbcode2markdown(self):
		def render_quote(tag_name, value, options, parent, context):
			author = u''
			if 'quote' in options:
				author = options['quote']
			return f'> {value} — {author}\n\n'

		def render_url(tag_name, value, options, parent, context):
			url = u''
			if 'url' in options:
				url = options['url']
			return f'{value} (<{url}>)'

		self.bbcode2markdown = bbcode.Parser(install_defaults=False, escape_html=False)
		self.bbcode2markdown.add_simple_formatter('ispoiler', '|| %(value)s ||')
		self.bbcode2markdown.add_simple_formatter('color', '%(value)s')
		self.bbcode2markdown.add_simple_formatter('b', '**%(value)s**')
		self.bbcode2markdown.add_simple_formatter('u', '__%(value)s__')
		self.bbcode2markdown.add_simple_formatter('i', '*%(value)s*')
		self.bbcode2markdown.add_formatter('quote', render_quote, strip=True, swallow_trailing_newline=True)
		self.bbcode2markdown.add_formatter('url', render_url, strip=True, swallow_trailing_newline=True)

	def parse_bbcode2markdown(self, content):
		return html.unescape(html.unescape(self.bbcode2markdown.format(content.replace('[url=/forum', '[url=https://www.tiplanet.org/forum'))))
