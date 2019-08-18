from config import CONFIG

required_configs = [
	{
		'NAME' : 'HOST',
		'TYPE' : str
	},
	{
		'NAME' : 'PORT',
		'TYPE' : int
	},
	{
		'NAME' : 'ENCODING',
		'TYPE' : str
	},
	{
		'NAME' : 'NUMBER_THREADS',
		'TYPE' : int
	},
	{
		'NAME' : 'MIME_TYPES',
		'TYPE' : dict
	}
]

def validate():
	
	for required_config in required_configs:
		required_name = required_config['NAME'] in CONFIG 
		assert required_name, required_config['NAME']+' is not in the configuration; this is required.'
		required_type = required_config['TYPE'] == type(CONFIG[required_config['NAME']])
		assert required_type, required_config['NAME']+' has incorrect type, should be '+str(required_config['TYPE'])
