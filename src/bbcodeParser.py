import bbcode


class bbcodeParser:
	def __init__(self):
		self.init_bbcode2markdown()

	def init_bbcode2markdown(self):
		def render_quote(tag_name, value, options, parent, context):
			author = u''
			if 'quote' in options:
				author = options['quote']
			return f'> {value} — {author}\n\n'

		self.bbcode2markdown = bbcode.Parser(
			url_template="{text}(<{href}>)", install_defaults=False)
		self.bbcode2markdown.add_simple_formatter(
			'ispoiler', '|| %(value)s ||')
		self.bbcode2markdown.add_simple_formatter('color', '%(value)s')
		self.bbcode2markdown.add_simple_formatter('b', '**%(value)s**')
		self.bbcode2markdown.add_simple_formatter('u', '__%(value)s__')
		self.bbcode2markdown.add_simple_formatter('i', '__%(value)s__')
		self.bbcode2markdown.add_formatter(
			'quote', render_quote, strip=True, swallow_trailing_newline=True)

	def parse_bbcode2markdown(self, content):
		return self.bbcode2markdown.format(content)
