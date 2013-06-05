#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ok lpod 1.0
# Import from lpod
import  csv, unidecode, re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tipus_actual = ''
dia_actual = ''
hora_actual = ''

DIAS = {
    '2': 'Martes, 2 de julio',
    '3': 'Miércoles, 3 de julio',
    '4': 'Jueves, 4 de julio',
    '5': 'Viernes, 5 de julio'
}

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

seccions = []

with open('aportacions_1juny.csv', 'rb') as infile:
    aportacions = csv.DictReader(infile, delimiter=',')
    for aportacio in aportacions:
        tipologia = aportacio['Tipologia'].decode('utf-8')
        if tipologia != tipus_actual:
            if len(tipus_actual) > 0: print '\n</div>\n'
            print '{{{ %s }}}' % tipologia
            print '\n<div id="llista-%s">' % slugify(tipologia)
            seccions.append(slugify(tipologia))
            tipus_actual = tipologia



        print "\n  <h3 class='aportacio'><span class='titol'>%s</span><span class='autors'>%s</span></h3>" % (aportacio['Títol'].decode('utf-8'),aportacio['Autors'].decode('utf-8'))
        print "\n  <div>"
        print "\n    <div class='resum'>%s</div>" % aportacio['Resum'].decode('utf-8')

        nuclis = []
        for nucli in [aportacio['Nucli temàtic 1'],aportacio['Nucli temàtic 2']]:
            if nucli.strip() != '':
                if nucli == 'I. Infantil i Primària: aquí comença tot':
                    nucli = 'I. Infantil y Primaria: ahí empieza todo'
                if nucli =='II. Didàctica i formació del professorat':
                    nucli ='II. Didáctica y formación del profesorado'
                if nucli =='III. Modelització i formalització':
                    nucli ='III. Modelización y formalización'
                if nucli =='IV. Resolució de problemes':
                    nucli ='IV. Resolución de problemas'
                if nucli =='V. Materials i recursos a l’aula de matemàtiques':
                    nucli ='V. Materiales y recursos en el aula de matemáticas'
                if nucli =='VI. Connexions i contextos':
                    nucli ='VI. Conexiones y contextos'
                if nucli =='VII. Comunicació i divulgació':
                    nucli = 'VII. Comunicación y divulgación'

                nuclis.append(nucli)
        if len(nuclis) > 0:
            print "\n    <div class='nuclis'>Nucleos temáticos: %s</div>" % ', '.join(nuclis)
        print "\n  </div>"



if len(tipus_actual) > 0: print '\n</div>\n'

print "\n<script type='text/javascript'>\njQuery(document).ready(function(){"
for seccio in seccions:
    print "jQuery('#llista-%s').accordion({ autoHeight: false, active: false, collapsible: true, icons: { 'header': 'ui-icon-plus', 'headerSelected': 'ui-icon-minus' } });" % seccio
print "\n});</script>"



