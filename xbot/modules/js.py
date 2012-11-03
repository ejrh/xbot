import spidermonkey as lulzsec
import subprocess
import re

def execute(bot, args):
	if len(args) > 1:
		if 'jsrt' not in bot.inv:
			bot.inv['jsrt'] = lulzsec.Runtime()
		if 'js' not in bot.inv:
			bot.inv['js'] = bot.inv['jsrt'].new_context()
		try:
			command = ' '.join(args[1:])
			#cx.execute('window = {}; e = {}; e.e = "prop"')
			#cx.execute(open('/usr/local/bin/irc/xbot/modules/jquery-1.8.2.min.js', 'r').read())
			bot.inv['js'].add_global('hashlib', __import__('hashlib'))
			bot.inv['js'].max_time(10)
			bot.inv['js'].max_memory(1000)
			result = bot.inv['js'].execute(command)
			if result is not None:
				result = unicode(result).encode('utf8')
				if len(result.split('\n')) > 4 or len(result) > 445:
					service = ['curl', '-F', 'sprunge=<-', 'http://sprunge.us']
					for n in range(2):
						p = subprocess.Popen(service, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
						paste = p.communicate(input=">>> %s\n\n%s" % (command, result))[0]
						try:
							return "%s?js" % re.findall('(http://.*)', paste, re.S)[0].strip()
						except IndexError:
							pass
					return "!%s: error pasting output." % args[0]
				else:	
					return result
			else:
				return None
		except lulzsec.JSError as e:
			return str(e)
		except MemoryError:
			return "Too much RAM, nigga."
		except SystemError:
			return "Took too long, nigga."
	return "Usage: !%s <js_expr>" % args[0]