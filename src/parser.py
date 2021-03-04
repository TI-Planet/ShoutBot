import re
import html
import bbcode
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from random import choice

class Parser:
	def __init__(self, config):
		self.config = config
		self.init_bbcode2markdown()
		self.markdown = MarkdownIt(
			{
				'options': {
					'maxNesting': 20,
					'html': False,
					'linkify': False,
					'typographer': False,
					'quotes': '“”‘’',
					'xhtmlOut': False,
					'breaks': False,
					'langPrefix': 'language-',
					'highlight': None
				},
				'components': {
					'core': { 'rules': ['normalize', 'block', 'inline', 'linkify', 'replacements', 'smartquotes'] },
					'block': { 'rules':  ['code', 'fence', 'blockquote', 'paragraph'] },
					'inline': { 'rules': ['text', 'newline', 'escape', 'backticks', 'strikethrough', 'emphasis', 'entity'] }
				}
			}, renderer_cls=RendererBBCODE)

	def init_bbcode2markdown(self):
		def render_quote(tag_name, value, options, parent, context):
			author = u''
			if 'quote' in options:
				author = options['quote']

			# for some reason \n are replaced with \r when landing here
			value = value.replace('\r', '\n')

			nl = '\n' # can't be used in fstrings
			return f"\n{nl.join([f'> {line}' for line in value.split(nl)])}\n— {author}\n"

		def render_url(tag_name, value, options, parent, context):
			url = u''
			if 'url' in options:
				url = options['url']
			if 'memberlist' in url and 'viewprofile' in url:
				url = f'<{url}>'
			if 'album.php' in url:
				url = f'<{url}>'
			return f'[{value}]({url})'

		self.bbcode2markdown = bbcode.Parser(install_defaults=False, escape_html=False)
		self.bbcode2markdown.add_simple_formatter('ispoiler', '|| %(value)s ||')
		self.bbcode2markdown.add_simple_formatter('color', '%(value)s')
		self.bbcode2markdown.add_simple_formatter('code', '```%(value)s```')
		self.bbcode2markdown.add_simple_formatter('img', '%(value)s')
		self.bbcode2markdown.add_simple_formatter('b', '**%(value)s**')
		self.bbcode2markdown.add_simple_formatter('u', '__%(value)s__')
		self.bbcode2markdown.add_simple_formatter('s', '~~%(value)s~~')
		self.bbcode2markdown.add_simple_formatter('i', '*%(value)s*')
		self.bbcode2markdown.add_formatter('quote', render_quote, strip=True, swallow_trailing_newline=True)
		self.bbcode2markdown.add_formatter('url', render_url, strip=True, swallow_trailing_newline=True)

	def parse_bbcode2markdown(self, msg, id):
		# shortcut completions and other quick changes
		msg = msg.replace('[url=/', '[url=https://tiplanet.org/')
		msg = msg.replace('[img]/', '[img]https://tiplanet.org/')

		imginurl = r'\[url=(.*)]\[img](.*)\[\/img]\[\/url]'
		for match in re.finditer(imginurl, msg):
			matching_substring = match.group(0)
			url = match.group(1)
			img = match.group(2)

			if "cdn.discordapp.com" in url and "media.discordapp.net" in img:
				# it's an image sent from discord, either quoted from tiplanet or sent from a selfbot then coming here from tiplanet (or similar cases)
				replacement = url
			elif id == self.config.TiBotId and 'gallery' in img:
				# it's TI-Bot for the gallery
				replacement = '' # there is already an embed with link and thumbnail
			elif id == self.config.TiBotId:
				# it's TI-Bot for a new archive with the archive's image
				replacement = img # keep image only becase the link is already given in the message
			else:
				replacement = f'[img]{img}[/img] - [url=<{url}>]url[/url]' # can't do better

			msg = msg.replace(matching_substring, replacement)

		# bbcode and html escaping
		msg = html.unescape(html.unescape(self.bbcode2markdown.format(msg)))
		msg = re.sub(r'< *br *\/? *>', r'\n', msg)

		# simple urls are transformed to a weird bugged <a>
		def repl_func(s):
			s = s.group(1)
			s = s[0:int(len(s)/2)]
			s = s[0:s.rfind('%')]
			return s
		msg = re.sub(r'<a rel="nofollow" href="(.*)<\/a>', repl_func, msg)

		# emojis
		for tp_name, ds_name in self.config.emojis.items():
			msg = msg.replace(f'{tp_name}', f'{ds_name}')

		# censorship
		for uncensored, censored in self.config.censorship.items():
			msg = re.compile(re.escape(uncensored), re.IGNORECASE).sub([censored, choice(censored)][isinstance(censored, list)], msg)

		if msg.startswith("/login "):
			username = msg.split(" ")[1]
			msg=f"*{username} se connecte au Chat.*"
		if msg.startswith("/logout "):
			username = msg.split(" ")[1]
			if len(msg.split(" "))>2:
				msg=f"*{username} a été déconnecté (Temps écoulé).*"
			else:
				msg=f"*{username} a été déconnecté.*"

		return msg.strip()

	def parse_markdown2bbcode(self, msg):
		# fix emojis
		msg = re.sub(r'<(:\S+:)\S+>', r'\g<1>', msg)
		return self.markdown.render(msg)

	def remove_quotes(self, msg):
		return '\n'.join([
			line for line in msg.split('\n') if not line.startswith('> ') and not line.startswith('— ')
		])


class RendererBBCODE(RendererHTML):
	def paragraph_open(self, tokens, idx, options, env):
		return ''

	def paragraph_close(self, tokens, idx, options, env):
		return ''

	def em_open(self, tokens, idx, options, env):
		return '[i]'

	def em_close(self, tokens, idx, options, env):
		return '[/i]'

	def s_open(self, tokens, idx, options, env):
		return'[s]'

	def s_close(self, tokens, idx, options, env):
		return'[/s]'

	def strong_open(self, tokens, idx, options, env):
		if tokens[idx].markup == "__":
			return '[u]'
		else:
			return'[b]'

	def strong_close(self, tokens, idx, options, env):
		if tokens[idx].markup == "__":
			return '[/u]'
		else:
			return'[/b]'

	def code_inline(self, tokens, idx, options, env):
		token = tokens[idx]
		return (
			f"[code]{tokens[idx].content}[/code]"
		)

	def code_block(self, tokens, idx, options, env):
		return (
			f"[code]{tokens[idx].content}[/code]\n"
		)

	def fence(self, tokens, idx, options, env):
		return (
			f"[code]{tokens[idx].content}[/code]\n"
		)

	def blockquote_open(self, tokens, idx, options, env):
		return "[quote]"

	def blockquote_close(self, tokens, idx, options, env):
		return "[/quote]"
