from django.db import models


class ProductManager(models.Manager):
    """ Manager del Modelo Producto """
    
    def productos_por_user(self, usuario):
        """ Filtra los productos creados por usuario en particular """
        
        return (self.filter(
            user_created = usuario,
        ))
    
    def productos_por_stock(self):
        """ Devuelve todos los producto que hay en stock """
        
        return (self.filter(stock__gt=0).order_by('-num_sales'))
    
    def productos_por_genero(self, genero):
        """ Filtra productos segun Genero """
        if genero == 'm':
            mujer = True
            varon = False
        elif genero == 'v':
            mujer = False
            varon = True
        else:
            mujer = True
            varon = True
        
        return (
            self.filter(
                man = varon,
                woman = mujer
                ).order_by('created')
                )
    
    def filtrar_productos(self, **filtros):
        """ Filtra productos segun Genero """
        return (self.filter(
            man = filtros['man'],
            woman = filtros['woman'],
            name__icontains = filtros['name'],
        ))
