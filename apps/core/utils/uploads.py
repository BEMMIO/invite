import os

def upload_cover_dir(obj,file_obj):
	file_ext = file_obj.split('.')[-1].lower
	_file = '{0}.{1}'.format(obj.id,file_ext)
	return os.path.join('book_cover',_file)


def upload_pdf_dir(obj,file_obj):
	file_ext = file_obj.split('.')[-1].lower
	_file = '{0}.{1}'.format(obj.id,file_ext)
	return os.path.join('pdf',_file)