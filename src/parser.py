import re
import html
from reTagParser.reTagParser import Parser as reParser
from random import choice

class Parser:
	def __init__(self, config):
		self.config = config
		self.bbcode2md = reParser()
		self.md2bbcode = reParser()

		# just a shortcut
		sp = reParser.SubParser

		# init bbcode2md
		def render_quote(value, om, cm):
			nl = '\n' # can't use it in f-strings
			return f"{nl.join([f'> {l}' for l in value.split(nl)])}{nl}— {om.group('author')}{nl}"
		def render_url(value, om, cm):
			url = om.group('url')
			if 'memberlist' in url and 'viewprofile' in url:
				url = f'<{url}>'
			if 'album.php' in url:
				url = f'<{url}>'
			return f'[{value}]({url})'
		self.simpleBbcodeParser('ispoiler', '||')
		self.simpleBbcodeParser('img', '')
		self.simpleBbcodeParser('b', '**')
		self.simpleBbcodeParser('u', '__')
		self.simpleBbcodeParser('s', '~~')
		self.simpleBbcodeParser('i', '*')
		self.simpleBbcodeParser('code', '`')
		self.bbcode2md.declare(sp('[code]\n', '[/code]', lambda value, om, cm: f'```\n{value}```', parse_value=False))
		self.bbcode2md.declare(sp('$$', '$$', lambda value, om, cm: f'$${value}$$', parse_value=False))
		self.bbcode2md.declare(sp(r'\[url=(?P<url>.*?)]', r'\[\/url]', render_url, escape_in_regex=False))
		self.bbcode2md.declare(sp(r'\[quote=(?P<author>.*?)]', r'\[\/quote]', render_quote, escape_in_regex=False))
		self.bbcode2md.declare(sp(r'\[color=(.*?)]', r'\[\/color]', lambda value, om, cm: value, escape_in_regex=False))

		# init md2bbcode
		self.md2bbcode.declare(sp('||', '||', self.bbcodeLambda('ispoiler')))
		self.md2bbcode.declare(sp('___', '___', self.bbcodeLambda(['i', 'u'])))
		self.md2bbcode.declare(sp('__', '__', self.bbcodeLambda('u')))
		self.md2bbcode.declare(sp('_', '_', self.bbcodeLambda('i'), requires_boundary=True))
		self.md2bbcode.declare(sp('*', '*', self.bbcodeLambda('i'), allows_space=False))
		self.md2bbcode.declare(sp('**', '**', self.bbcodeLambda('b')))
		self.md2bbcode.declare(sp('***', '***', self.bbcodeLambda(['i', 'b'])))
		self.md2bbcode.declare(sp('`', '`', self.bbcodeLambda('code'), parse_value=False))
		self.md2bbcode.declare(sp('```', '```', self.bbcodeLambda('code'), parse_value=False))
		self.md2bbcode.declare(sp('~~', '~~', self.bbcodeLambda('s')))

	def simpleBbcodeParser(self, bbctag, mdtag):
		self.bbcode2md.declare(reParser.SubParser(f'[{bbctag}]', f'[/{bbctag}]', lambda value, om, cm: f'{mdtag}{value}{mdtag}'))
	def bbcodeLambda(self, tags):
		if isinstance(tags, str):
			tags = [tags]
		return lambda value, om, cm: f"{''.join([f'[{tag}]' for tag in tags])}{value}{''.join([f'[/{tag}]' for tag in tags[::-1]])}"

	def parse_bbcode2markdown(self, msg, id):
		msg = html.unescape(msg)

		if id == self.config.TiBotId and msg.startswith('/roll '):
			split = msg.split()
			if len(split) == 4:
				return f'{split[1]} lance {split[2]} et obtient {split[3]}.'

		# shortcut completions and other quick changes
		msg = msg.replace('[url=/', '[url=https://tiplanet.org/')
		msg = msg.replace('[img]/', '[img]https://tiplanet.org/')

		imginurl = r'\[url=([^\]]*)]\[img]([^\]]*)\[\/img]\[\/url]'
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

		# bbcode
		msg = self.bbcode2md.parse(msg)

		# emojis
		for tp_name, ds_name in self.config.emojis.items():
			msg = msg.replace(f'{tp_name}', f'{ds_name}')

		# censorship
		for uncensored, censored in self.config.censorship.items():
			msg = re.compile(fr'\b{uncensored}\b', re.IGNORECASE).sub([censored, choice(censored)][isinstance(censored, list)], msg)

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

		# quotes
		msg = self.mdquotes2bbcode(msg)

		# md tags
		msg = self.md2bbcode.parse(msg)

		return msg.strip()

	def mdquotes2bbcode(self, msg):
		nl = '\n' # can't use in f-strings
		lines = msg.split(nl)
		res = []
		for line in lines:
			if line.startswith('> '):
				line = line[2:]
				if len(res)!=0 and isinstance(res[-1], list):
					res[-1].append(line)
				else:
					res.append([line])
			elif line.startswith('— '):
				if len(res)!=0 and isinstance(res[-1], list):
					line = line[2:]
					res[-1] = f'[quote={line}]{nl.join(res[-1])}[/quote]'
				else:
					res.append(line)
			else:
				if len(res)!=0 and isinstance(res[-1], list):
					res[-1] = f'[quote]{nl.join(res[-1])}[/quote]'
				res.append(line)
		if len(res)!=0 and isinstance(res[-1], list):
			res[-1] = f'[quote]{nl.join(res[-1])}[/quote]'
		return '\n'.join(res)

	def remove_quotes(self, msg):
		return '\n'.join([
			line for line in msg.split('\n') if not line.startswith('> ') and not line.startswith('— ')
		])
