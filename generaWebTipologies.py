#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ok lpod 1.0
# Import from lpod
import  csv, unidecode, re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] inputfile')
    sys.exit(1)

infilepath = sys.argv[1]

tipus_actual = ''
dia_actual = ''
hora_actual = ''

DIAS = {
    '2': 'Martes, 2 de julio',
    '3': 'Miércoles, 3 de julio',
    '4': 'Jueves, 4 de julio',
    '5': 'Viernes, 5 de julio',
    '1': 'Del 2 al 5 de julio'
}

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

def print_accordion(seccions):
    print "\n<script type='text/javascript'>\njQuery(document).ready(function(){"
    for seccio in seccions:
        print "jQuery('#llista-%s').accordion({ autoHeight: false, active: false, collapsible: true, icons: { 'header': 'ui-icon-plus', 'headerSelected': 'ui-icon-minus' } });" % seccio
    print "\n});</script>"



seccions = []

with open(infilepath, 'rb') as infile:
    aportacions = csv.DictReader(infile, delimiter=',')
    for aportacio in aportacions:
        tipologia = aportacio['Tipologia'].decode('utf-8')
        if tipologia != tipus_actual:
            if len(hora_actual) > 0:
                print '\n</div>\n'
                hora_actual = ''
                dia_actual = ''
            if len(tipus_actual) > 0:
                print_accordion(seccions)
            print '\n\n\n<!-- INICI %s -->' % tipologia
            seccions = []
            tipus_actual = tipologia

        if aportacio['Dia'] != dia_actual:
            if len(hora_actual) > 0:
                print '\n</div>\n'
            dia_actual = aportacio['Dia']
            hora_actual = ''
            print "\n\n<a name='%s'></a>" % slugify(DIAS[dia_actual].decode('utf-8'))
            print "<h2 class='data'>%s</h2>" % DIAS[dia_actual]

        if aportacio['Hora'] != hora_actual:
            if len(hora_actual) > 0:
                print '\n</div>\n'
            hora_actual = aportacio['Hora']
            print "\n<h3 class='hora'>%s</h3>" % hora_actual.decode('utf-8')
            id_seccio = slugify((dia_actual + '-' + hora_actual).decode('utf-8'))
            print '\n<div id="llista-%s">' % id_seccio
            seccions.append(id_seccio)

        lloc = aportacio['Edifici'].decode('utf-8') + '. ' + aportacio['Aula'].decode('utf-8')
        print "\n  <h3 class='aportacio'><span class='lloc'>%s</span><span class='titol'>%s</span><span class='autors'>%s<br/>%s</span></h3>" % (lloc, aportacio['Títol'].decode('utf-8'),aportacio['Autors'].decode('utf-8'),aportacio['Afiliació'].decode('utf-8'))
        print "\n  <div>"

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
            if len(nuclis) == 1:
                print "\n    <div class='nuclis'>Nucleo temático: %s</div>" % ', '.join(nuclis)
            else:
                print "\n    <div class='nuclis'>Nucleos temáticos: %s</div>" % ', '.join(nuclis)
        if len(aportacio['Foto']) > 0:
            print "\n    <img%s|right|largeur=200>" % aportacio['Foto'].decode('utf-8')

        if len(aportacio['Observacions']) > 0:
            print "\n    <div class='observacions'>%s</div>" % aportacio['Observacions'].decode('utf-8')
            print "\n    <div class='clear'></div>"
        print "\n    <div class='resum'>%s</div>" % aportacio['Resum'].decode('utf-8')


        print "\n  </div>"



if len(hora_actual) > 0: print '\n</div>\n'
if len(tipus_actual) > 0: print_accordion(seccions)



