#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ok lpod 1.0
# Import from lpod
from lpod.document import odf_get_document
from lpod.document import odf_new_document
from lpod.heading import odf_create_heading
from lpod.paragraph import odf_create_paragraph
from lpod.style import odf_master_page
from lpod.list import odf_create_list

import  csv
import sys
if len(sys.argv) < 3:
    sys.stderr.write('Usage: sys.argv[0] inputfile')
    sys.exit(1)

infilepath = sys.argv[1]
outfilepath = sys.argv[2]


my_document = odf_new_document('text')
body = my_document.get_body()

# style_filename = "lpod_styles.odt"
style_filename = "estils/estils_programa.odt"
style_document = odf_get_document(style_filename)
my_document.delete_styles()
my_document.merge_styles_from(style_document)

tipus_actual = ''
dia_actual = ''
hora_actual = ''

DIAS = {
    '2': 'Martes, 2 de julio',
    '3': 'Miércoles, 3 de julio',
    '4': 'Jueves, 4 de julio',
    '5': 'Viernes, 5 de julio'
}


with open(infilepath, 'rb') as infile:
    aportacions = csv.DictReader(infile, delimiter=',')
    for aportacio in aportacions:
        tipologia = aportacio['Tipologia']
        if tipologia == 'Comunicació':
            tipologia = 'Comunicación'
        elif tipologia == 'Clip d\'aula':
            tipologia = 'Clip de aula'

        if tipologia != tipus_actual:
            tipus = odf_create_heading(1, tipologia.decode('utf-8'))
            body.append(tipus)
            body.append(odf_create_paragraph(''))
            tipus_actual = tipologia

        if aportacio['Dia'] != dia_actual:
            dia_actual = aportacio['Dia']
            hora_actual = ''

        if aportacio['Hora'] != hora_actual:
            hora_actual = aportacio['Hora']
            paragraph = odf_create_paragraph(DIAS[dia_actual].decode('utf-8'), style= 'data')
            body.append(paragraph)
            paragraph = odf_create_paragraph(hora_actual.decode('utf-8'), style= 'hora')
            body.append(paragraph)




        lloc = "%s. %s" % (aportacio['Edifici'].decode('utf-8'), aportacio['Aula'].decode('utf-8') )
        paragraph = odf_create_paragraph( lloc, style = 'lloc')
        body.append(paragraph)

        title = odf_create_heading(2, aportacio['Títol'].decode('utf-8'))
        body.append(title)

        paragraph = odf_create_paragraph(aportacio['Autors'].decode('utf-8'), style = 'autors')
        body.append(paragraph)
        if aportacio['Afiliació'] != '':
            paragraph = odf_create_paragraph(aportacio['Afiliació'].decode('utf-8'), style = 'centretreball')
            body.append(paragraph)

        body.append(odf_create_paragraph(''))

        paragraph = odf_create_paragraph(aportacio['Resum'].decode('utf-8'), style= 'resum')
        body.append(paragraph)
        # paragraph = odf_create_paragraph('Palabras clave: ' + aportacio['Paraules clau'].decode('utf-8'), style= 'keywords')
        # body.append(paragraph)

        paragraph = odf_create_paragraph(u'Nucleos temáticos:', style='titolnuclis')
        body.append(paragraph)


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

                nuclis.append(nucli.decode('utf-8'))


        if len(nuclis) > 0:
            for nucli in nuclis:
                body.append(odf_create_paragraph(nucli, style='nuclis'))
        else:
            print 'Comunicacio %s - %s no te cap nucli tematic' % (aportacio['Codi'], aportacio['Títol'])

        body.append(odf_create_paragraph(''))
        body.append(odf_create_paragraph(''))



# 3 - Saving Document
my_document.save(target=outfilepath, pretty=True)


