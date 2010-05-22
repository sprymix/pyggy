
class Error(Exception) : 
	"Superclass of all of our Errors"
	pass

class InternalError(Error) : 
	"Internal error in our code."
	pass

class ApiError(Error) : 
	"The caller misused the API"
	pass

class SpecError(ApiError) :
	"There's an error in processing the specfile"
	pass

# XXX currently not used.. lexer returns an error token
class LexError(Error) :
	"Failure during lexing the input."
	pass

class ParseError(Error) :
	"Failure during parsing the input."
	def __init__(self, str, tok) :
		self.str = str
		self.tok = tok
	def __str__(self) :
		return "ParseError %s" % str

class AmbigParseError(ApiError) :
	"""
	This exception is used to indicate an ambiguous parse when 
	the user specified that ambiguous parses arent allowed.
	"""
	pass

