from django.db import models
from django.contrib.auth.models import User


class category(models.Model):
	name = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True) 
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		ordering = ['name']

class territorial(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', models.DO_NOTHING,related_name='dad', blank=False, null=False)
	territorial_list = (('country', 'pais',),('city', 'ciudad',))
	territorial_type = models.CharField(max_length=12, choices=territorial_list, default='city')
	created_at = models.DateTimeField(auto_now_add=True) 
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return '{} {} {}'.format(self.id, self.name, self.territorial_type)

class cliente(models.Model):
	name = models.CharField(max_length=50)
	country = models.ForeignKey(territorial, models.DO_NOTHING,related_name='pais', blank=False, null=False)
	city = models.ForeignKey(territorial,models.DO_NOTHING,related_name='ciudad', blank=False, null=False)
	category = models.ForeignKey(category, models.DO_NOTHING, blank=False, null=False) 
	user_created = models.ForeignKey(User, models.DO_NOTHING) 
	active = (('1', 'activo',),('0', 'inactivo',))
	is_active = models.CharField(max_length=1, choices=active, default='1')
	created_at = models.DateTimeField(auto_now_add=True) 
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']
	